import gzip
import os
import subprocess

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

def count_lines_fast(filepath):
    count = 0
    opener = gzip.open if filepath.endswith('.gz') else open
    with opener(filepath, 'rt') as f:
        for line in f:
            count += 1
    return count

def bash(cmd):
    subprocess.run(cmd, shell=True, executable="/bin/bash", check=True)

b_pattern         = "/data/nooroka/grant/punkt1/stage2/merged/quadr7_chain180424_merged2_sorted_{c}_39.bed"
gccoords_pattern  = "/data/nooroka/grant/punkt3/stage2/gccoords/def/gccoords_{c}2defhg19_39_all_loop7_control3_no_gc.bed.gz"
mutations_pattern = "/data/nooroka/grant/punkt3/bed-37/bed_chr_{c}_sorted.bed.gz"

tmp_dir = "/tmp/intersect_results"
os.makedirs(tmp_dir, exist_ok=True)

total_gccoords = 0
total_b        = 0
total_mut_gc   = 0
total_mut_b    = 0

for i in range(1, 25):
    gccoords_file = gccoords_pattern.format(c=i)
    b_file        = b_pattern.format(c=i)
    mut_file      = mutations_pattern.format(c=i)

    gc_len = sum_interval_lengths(gccoords_file)
    b_len  = sum_interval_lengths(b_file)

    # пересечение мутаций с gccoords
    out_gc    = "{}/intersect_gc_{}.bed".format(tmp_dir, i)
    out_gc_un = "{}/intersect_gc_{}_un.bed".format(tmp_dir, i)
    cmd_gc = """bedtools intersect -a <(awk 'BEGIN{{OFS="\\t"}} {{ if ($3 <= $2) $3=$2+1; print }}' <(zcat {mut})) -b <(zcat {gc}) -u > {out}""".format(
        mut=mut_file, gc=gccoords_file, out=out_gc
    )
    bash(cmd_gc)
    bash("sort -k4,4 -s {inp} | awk '!seen[$4]++' > {out}".format(inp=out_gc, out=out_gc_un))
    mut_gc = count_lines_fast(out_gc_un)

    # пересечение мутаций с b-интервалами
    out_b    = "{}/intersect_b_{}.bed".format(tmp_dir, i)
    out_b_un = "{}/intersect_b_{}_un.bed".format(tmp_dir, i)
    cmd_b = """bedtools intersect -a <(awk 'BEGIN{{OFS="\\t"}} {{ if ($3 <= $2) $3=$2+1; print }}' <(zcat {mut})) -b {b} -u > {out}""".format(
        mut=mut_file, b=b_file, out=out_b
    )
    bash(cmd_b)
    bash("sort -k4,4 -s {inp} | awk '!seen[$4]++' > {out}".format(inp=out_b, out=out_b_un))
    mut_b = count_lines_fast(out_b_un)

    density_control = mut_gc / gc_len if gc_len > 0 else 0
    density_quadr   = mut_b  / b_len  if b_len  > 0 else 0

    print("chr{c}: gccoords_len={gl}, b_len={bl}, mut_on_gc={mg}, mut_on_b={mb}, density_control={dc}, density_quadr={dq}".format(
        c=i, gl=gc_len, bl=b_len, mg=mut_gc, mb=mut_b, dc=density_control, dq=density_quadr
    ))

    total_gccoords += gc_len
    total_b        += b_len
    total_mut_gc   += mut_gc
    total_mut_b    += mut_b

print("\nРезультат:")
print("Сумма длин интервалов gccoords (все хромосомы):    {}".format(total_gccoords))
print("Сумма длин интервалов -b файлов (все хромосомы):   {}".format(total_b))
print("Кол-во мутаций на gccoords интервалах (все хром.): {}".format(total_mut_gc))
print("Кол-во мутаций на -b интервалах (все хром.):       {}".format(total_mut_b))
print("Плотность мутаций контроль  {}".format(total_mut_gc / total_gccoords if total_gccoords > 0 else 0))
print("Плотность мутаций quadr:    {}".format(total_mut_b  / total_b        if total_b        > 0 else 0))
