import os
import subprocess
import sys
import gzip


def sum_interval_lengths_for_chr(bed_file, chr_name):
    """
    Сумма (end-start) по bed-файлу, но только для одной хромосомы.
    В отличие от исходной версии — фильтрация по хромосоме и суммирование
    длин делаются одним awk-пайпом, без записи отфильтрованного куска
    control-файла во временный файл на диске.
    """
    cmd = (
        "awk -v c=\"{c}\" '$1==c {{s += $3-$2}} END{{print s+0}}' {f}"
    ).format(c=chr_name, f=bed_file)
    result = subprocess.run(
        cmd, shell=True, executable="/bin/bash",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, check=True
    )
    return int(result.stdout.strip())


def count_unique_mutations(mut_file, control_bed, chr_name):
    """
    Считает число уникальных мутаций (по col4), пересёкшихся с control_bed,
    отфильтрованным по нужной хромосоме.
    В отличие от исходной версии — НЕ создаётся tmp_control-файл на диске:
    фильтрация control-bed по хромосоме идёт через process substitution
    (<(awk ...)), а мутации подаются в bedtools через stdin.
    """
    mut_cmd = "zcat {}".format(mut_file) if mut_file.endswith(".gz") else "cat {}".format(mut_file)
    cmd = (
        "set -o pipefail; "
        "{mut_cmd} "
        "| awk 'BEGIN{{OFS=\"\\t\"}} $3<=$2{{$3=$2+1}} 1' "
        "| bedtools intersect -a stdin -b <(awk -v c=\"{c}\" '$1==c' {bed}) "
        "| sort -k4,4 -T /tmp -S 2G -u "
        "| wc -l"
    ).format(mut_cmd=mut_cmd, c=chr_name, bed=control_bed)
    result = subprocess.run(
        cmd,
        shell=True,
        executable="/bin/bash",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )
    return int(result.stdout.strip())


control_bed       = "control_RNU_tRNA_39_merged_2.bed"
mutations_pattern = "/data/nooroka/grant/punkt3/bed-37/bed_chr_{}_sorted.bed.gz"

total_len = total_mut = 0
out_file = "results_density_control_RNU_tRNA_39_1309.tsv"

with open(out_file, "w") as w:
    w.write("chr\tcontrol_len\tmut_on_control\tdensity\n")
    for i in range(1, 25):
        chr_name = "chr{}".format(i)
        mut_file = mutations_pattern.format(i)

        b_len  = sum_interval_lengths_for_chr(control_bed, chr_name)

        # Пересечение считается напрямую через пайп, без промежуточных
        # bed-файлов на диске (ни для control, ни для мутаций).
        mut_gc = count_unique_mutations(mut_file, control_bed, chr_name)

        density = mut_gc / b_len if b_len else 0

        print("chr{}: control_len={}, mut_on_control={}, density={}".format(
            i, b_len, mut_gc, density))
        w.write("chr{}\t{}\t{}\t{}\n".format(i, b_len, mut_gc, density))

        total_len += b_len
        total_mut += mut_gc

    total_density = total_mut / total_len if total_len else 0

    print("\nРезультат:")
    print("Сумма длин control:    {}".format(total_len))
    print("Мутации на control:    {}".format(total_mut))
    print("Плотность общая:       {}".format(total_density))

    w.write("TOTAL\t{}\t{}\t{}\n".format(total_len, total_mut, total_density))

print("\nГотово. Промежуточные bed-файлы не сохранялись.")
