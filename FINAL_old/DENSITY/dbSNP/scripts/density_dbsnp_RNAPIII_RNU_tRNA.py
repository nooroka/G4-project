import os
import subprocess
import sys
import gzip


def sum_interval_lengths_stream(text):
    """Сумма (end-start) по тексту в bed-формате (уже прочитанному)."""
    total = 0
    for line in text.splitlines():
        parts = line.split()
        if len(parts) >= 3:
            total += int(parts[2]) - int(parts[1])
    return total


def extract_chr_lines(bed_file, chr_name):
    """Достаёт из общего bed-файла только строки нужной хромосомы (chr1, chr2, ...)."""
    cmd = "awk -v c=\"{c}\" '$1==c' {f}".format(c=chr_name, f=bed_file)
    result = subprocess.run(
        cmd, shell=True, executable="/bin/bash",
        stdout=subprocess.PIPE, text=True, check=True
    )
    return result.stdout


def count_unique_mutations(mut_file, bed_arg, chr_id):
    """
    bedtools intersect(-a mut_file фикс координат, -b bed_arg)
    | sort -k4,4 -u | wc -l
    mut_file может быть .gz — читается через zcat.
    bed_arg — путь к обычному bed-файлу (уже отфильтрованному по хромосоме).
    """
    a_src = "zcat {}".format(mut_file) if mut_file.endswith(".gz") else "cat {}".format(mut_file)
    cmd = (
        "bedtools intersect "
        "-a <({a_src} | awk 'BEGIN{{OFS=\"\\t\"}} $3<=$2{{$3=$2+1}} 1') "
        "-b {b} "
        "| sort -k4,4 -T /tmp -S 2G -u "
        "| wc -l"
    ).format(a_src=a_src, b=bed_arg)
    result = subprocess.run(
        cmd, shell=True, executable="/bin/bash",
        stdout=subprocess.PIPE, text=True, check=True
    )
    return int(result.stdout.strip())


control_bed       = "control_without_rnapIII_39_merged.bed"
mutations_pattern = "/data/nooroka/grant/punkt3/bed-37/bed_chr_{}_sorted.bed.gz"

total_len = total_mut = 0
out_file = "results_density_control_no_RNAPIII_39.tsv"

with open(out_file, "w") as w:
    w.write("chr\tcontrol_len\tmut_on_control\tdensity\n")
    for i in range(1, 25):
        chr_name = "chr{}".format(i)
        mut_file = mutations_pattern.format(i)

        # достаём кусок control-файла только для текущей хромосомы во временный файл
        chr_lines = extract_chr_lines(control_bed, chr_name)
        tmp_control = "/tmp/{}_control_tmp.bed".format(chr_name)
        with open(tmp_control, "w") as tf:
            tf.write(chr_lines)

        b_len  = sum_interval_lengths_stream(chr_lines)
        mut_gc = count_unique_mutations(mut_file, tmp_control, i)

        density = mut_gc / b_len if b_len else 0

        print("chr{}: control_len={}, mut_on_control={}, density={}".format(
            i, b_len, mut_gc, density))
        w.write("chr{}\t{}\t{}\t{}\n".format(i, b_len, mut_gc, density))

        total_len += b_len
        total_mut += mut_gc

        os.remove(tmp_control)

    total_density = total_mut / total_len if total_len else 0
    print("\nTOTAL: control_len={}, mut_on_control={}, density={}".format(
        total_len, total_mut, total_density))
    w.write("TOTAL\t{}\t{}\t{}\n".format(total_len, total_mut, total_density))
