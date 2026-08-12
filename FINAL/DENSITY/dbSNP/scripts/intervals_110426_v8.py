import os
import subprocess
import sys
import gzip


def sum_interval_lengths(filepath):
    """Сумма (end-start) по bed-файлу. Поддерживает .gz и обычный .bed."""
    total = 0
    try:
        opener = gzip.open if filepath.endswith('.gz') else open
        with opener(filepath, 'rt') as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 3:
                    total += int(parts[2]) - int(parts[1])
    except FileNotFoundError:
        print("WARNING: file not found: {}".format(filepath))
    return total


def count_unique_mutations(mut_file, bed_arg, chr_id):
    """
    Считает число уникальных мутаций (по col4):
    Исправляет координаты через awk и передает в bedtools intersect через stdin.
    """
    mut_cmd = "zcat {}".format(mut_file) if mut_file.endswith(".gz") else "cat {}".format(mut_file)

    cmd = (
        "{mut_cmd} "
        "| awk 'BEGIN{{OFS=\"\\t\"}} $3<=$2{{$3=$2+1}} 1' "
        "| bedtools intersect -a stdin -b {bed_arg} "
        "| sort -k4,4 -T /tmp -S 2G -u "
        "| wc -l"
    ).format(mut_cmd=mut_cmd, bed_arg=bed_arg)

    result = subprocess.run(
        cmd,
        shell=True,
        executable="/bin/bash",
        stdout=subprocess.PIPE,
        check=True
    )
    return int(result.stdout.strip())


b_pattern         = "../../../punkt1/stage2/merged/quadr7_chain180424_merged2_sorted_{}_{}.bed"
gccoords_pattern  = "../gccoords2/def/gccoords_{}2defhg19_{}_all_loop7_control2_{}_gc_corrected.bed"
mutations_pattern = "/data/nooroka/grant/punkt3/bed-37/bed_chr_{}_sorted.bed.gz"

total_gccoords = total_b = total_mut_gc = total_mut_b = 0
out_file = "results100826/results_density_control2_{}_{}_gc.tsv".format(sys.argv[1],sys.argv[2])

with open(out_file, "w") as w:
    w.write("chr\tgccoords_len\tb_len\tmut_on_gc\tmut_on_b\tdensity_control\tdensity_quadr\n")
    for i in range(1, 25):
        gc_file  = gccoords_pattern.format(i,sys.argv[1],sys.argv[2])
        b_file   = b_pattern.format(i,sys.argv[1])
        mut_file = mutations_pattern.format(i)

        gc_len = sum_interval_lengths(gc_file)
        b_len  = sum_interval_lengths(b_file)
        mut_gc = count_unique_mutations(mut_file, gc_file, i)  # ← gccoords
        mut_b  = count_unique_mutations(mut_file, b_file, i)   # ← квадруплексы

        dc = mut_gc / gc_len if gc_len else 0
        dq = mut_b  / b_len  if b_len  else 0

        print("chr{}: gccoords_len={}, b_len={}, mut_on_gc={}, mut_on_b={}, density_control={}, density_quadr={}".format(
            i, gc_len, b_len, mut_gc, mut_b, dc, dq))
        w.write("chr{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(i, gc_len, b_len, mut_gc, mut_b, dc, dq))

        total_gccoords += gc_len;  total_b    += b_len
        total_mut_gc   += mut_gc;  total_mut_b += mut_b

    tdc = total_mut_gc / total_gccoords if total_gccoords else 0
    tdq = total_mut_b  / total_b        if total_b        else 0

    print("\nРезультат:")
    print("Сумма длин gccoords:   {}".format(total_gccoords))
    print("Сумма длин b-файлов:   {}".format(total_b))
    print("Мутации на gccoords:   {}".format(total_mut_gc))
    print("Мутации на b-файлах:   {}".format(total_mut_b))
    print("Плотность контроль:    {}".format(tdc))
    print("Плотность quadr:       {}".format(tdq))

    w.write("TOTAL\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
        total_gccoords, total_b, total_mut_gc, total_mut_b, tdc, tdq))
