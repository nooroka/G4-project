import sys
import gzip
import subprocess
import os

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
        print(f"WARNING: file not found: {filepath}", file=sys.stderr)
    return total

def count_lines_fast(filepath):
    count = 0
    opener = gzip.open if filepath.endswith('.gz') else open
    with opener(filepath, 'rt') as f:
        for line in f:
            count += 1
    return count

b_pattern        = "/data/nooroka/grant/punkt1/stage2/merged/quadr7_chain180424_merged2_sorted_{}_39.bed"
gccoords_pattern = "/data/nooroka/grant/punkt3/stage2/gccoords/def/gccoords_{}2defhg19_3g_all_loop7_control3_no_gc.bed.gz"
mutations_pattern = "/data/nooroka/grant/punkt3/bed-37/bed_chr_{}_sorted.bed.gz"

# временная папка для результатов пересечения
tmp_dir = "/tmp/intersect_results"
os.makedirs(tmp_dir, exist_ok=True)

total_gccoords  = 0
total_b         = 0
total_mut_gc    = 0  # мутации на gccoords
total_mut_b     = 0  # мутации на b-интервалы

for i in range(1, 25):
    gccoords_file  = gccoords_pattern.format(i)
    b_file         = b_pattern.format(i)
    mut_file       = mutations_pattern.format(i)

    gc_len = sum_interval_lengths(gccoords_file)
    b_len  = sum_interval_lengths(b_file)

    # пересечение мутаций с gccoords
    out_gc = f"{tmp_dir}/intersect_gc_{i}.bed"
    cmd_gc = f"bedtools intersect -a <(zcat {mut_file}) -b <(zcat {gccoords_file}) -u > {out_gc}"
    subprocess.run(cmd_gc, shell=True, executable="/bin/bash", check=True)
    mut_gc = count_lines_fast(out_gc)

    # пересечение мутаций с b-интервалами
    out_b = f"{tmp_dir}/intersect_b_{i}.bed"
    cmd_b = f"bedtools intersect -a <(zcat {mut_file}) -b {b_file} -u > {out_b}"
    subprocess.run(cmd_b, shell=True, executable="/bin/bash", check=True)
    mut_b = count_lines_fast(out_b)
    print(f"chr{i}: gccoords_len={gc_len}, b_len={b_len}, mut_on_gc={mut_gc}, mut_on_b={mut_b}, density_control={mut_gc/gc_len}, density_quadr={mut_b/b_len}")
    total_gccoords += gc_len
    total_b        += b_len
    total_mut_gc   += mut_gc
    total_mut_b    += mut_b

print(f"\nРезультат:")
print(f"Сумма длин интервалов gccoords (все хромосомы):      {total_gccoords}")
print(f"Сумма длин интервалов -b файлов (все хромосомы):     {total_b}")
print(f"Кол-во мутаций на gccoords интервалах (все хром.):   {total_mut_gc}")
print(f"Кол-во мутаций на -b интервалах (все хром.):         {total_mut_b}")
print(f"Плотность мутаций контроль: float({total_mut_gc/total_gccoords})")
print(f"Плотность мутаций контроль: float({total_mut_b/total_b})")

