import gzip
import os
import subprocess
import sys

def sum_interval_lengths(filepath):
    total = 0
    try:
        opener = gzip.open if filepath.endswith('.gz') else open
        with opener(filepath, 'rt') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                total += int(parts[2]) - int(parts[1])
    except FileNotFoundError:
        print("WARNING: file not found: {}".format(filepath))
    return total

def count_from_pipe(cmd):
    """Считает строки прямо из stdout, без записи на диск"""
    result = subprocess.run(
        cmd, shell=True, executable="/bin/bash",
        stdout=subprocess.PIPE, check=True
    )
    return result.stdout.count(b'\n')

b_pattern         = "/data/nooroka/grant/punkt1/stage2/merged/quadr7_chain180424_merged2_sorted_{}_{}.bed"
gccoords_pattern  = "/data/nooroka/grant/punkt3/stage2/gccoords/def/gccoords_{}2defhg19_{}_all_loop7_{}_no_gc.bed.gz"
mutations_pattern = "/data/nooroka/grant/punkt3/bed-37/bed_chr_{}_sorted.bed.gz"

total_gccoords = 0
total_b        = 0
total_mut_gc   = 0
total_mut_b    = 0

out_file = "results_density_{}_{}_3.tsv".format(sys.argv[1], sys.argv[2])

with open(out_file, "w") as w:
    w.write("chr\tgccoords_len\tb_len\tmut_on_gc\tmut_on_b\tdensity_control\tdensity_quadr\n")

    for i in range(1, 25):
        gccoords_file = gccoords_pattern.format(i, sys.argv[1], sys.argv[2])
        b_file        = b_pattern.format(i, sys.argv[1])
        mut_file      = mutations_pattern.format(i)

        gc_len = sum_interval_lengths(gccoords_file)
        b_len  = sum_interval_lengths(b_file)

        # пересечение с gccoords — всё в одном pipe, без файлов
        cmd_gc = """bedtools intersect \
            -a <(awk 'BEGIN{{OFS="\\t"}} {{ if ($3 <= $2) $3=$2+1; print }}' <(zcat {mut})) \
            -b <(zcat {gc}) -u \
            | sort -k4,4 -s | awk '!seen[$4]++""".format(
            mut=mut_file, gc=gccoords_file
        )
        mut_gc = count_from_pipe(cmd_gc)

        # пересечение с b-интервалами — всё в одном pipe, без файлов
        cmd_b = """bedtools intersect \
            -a <(awk 'BEGIN{{OFS="\\t"}} {{ if ($3 <= $2) $3=$2+1; print }}' <(zcat {mut})) \
            -b {b} -u \
            | sort -k4,4 -s |awk '!seen[$4]++""".format(
            mut=mut_file, b=b_file
        )
        mut_b = count_from_pipe(cmd_b)

        density_control = mut_gc / gc_len if gc_len > 0 else 0
        density_quadr   = mut_b  / b_len  if b_len  > 0 else 0

        print("chr{c}: gccoords_len={gl}, b_len={bl}, mut_on_gc={mg}, mut_on_b={mb}, density_control={dc}, density_quadr={dq}".format(
            c=i, gl=gc_len, bl=b_len, mg=mut_gc, mb=mut_b, dc=density_control, dq=density_quadr
        ))

        w.write("chr{c}\t{gl}\t{bl}\t{mg}\t{mb}\t{dc}\t{dq}\n".format(
            c=i, gl=gc_len, bl=b_len, mg=mut_gc, mb=mut_b, dc=density_control, dq=density_quadr
        ))

        total_gccoords += gc_len
        total_b        += b_len
        total_mut_gc   += mut_gc
        total_mut_b    += mut_b

    total_density_control = total_mut_gc / total_gccoords if total_gccoords > 0 else 0
    total_density_quadr   = total_mut_b  / total_b        if total_b        > 0 else 0

    print("\nРезультат:")
    print("Сумма длин интервалов gccoords (все хромосомы):    {}".format(total_gccoords))
    print("Сумма длин интервалов -b файлов (все хромосомы):   {}".format(total_b))
    print("Кол-во мутаций на gccoords интервалах (все хром.): {}".format(total_mut_gc))
    print("Кол-во мутаций на -b интервалах (все хром.):       {}".format(total_mut_b))
    print("Плотность мутаций контроль: {}".format(total_density_control))
    print("Плотность мутаций quadr:    {}".format(total_density_quadr))

    w.write("TOTAL\t{gl}\t{bl}\t{mg}\t{mb}\t{dc}\t{dq}\n".format(
        gl=total_gccoords, bl=total_b, mg=total_mut_gc, mb=total_mut_b,
        dc=total_density_control, dq=total_density_quadr
    ))

print("Результаты записаны в {}".format(out_file))
