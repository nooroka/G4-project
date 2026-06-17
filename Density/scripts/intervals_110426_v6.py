import gzip
import subprocess
import sys

def interval_lengths(filepath):
    total = 0
    opener = gzip.open if filepath.endswith('.gz') else open
    try:
        with opener(filepath, 'rt') as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 3:
                    total += int(parts[2]) - int(parts[1])
    except FileNotFoundError:
        print("WARNING: not found:", filepath)
    return total

def count_lines(cmd):
    r = subprocess.run(cmd, shell=True, executable="/bin/bash",
                       stdout=subprocess.PIPE, check=True)
    return int(r.stdout.strip())

B_PAT   = "/data/nooroka/grant/punkt1/stage2/merged/quadr7_chain180424_merged2_sorted_{}_{}.bed"
GC_PAT  = "/data/nooroka/grant/punkt3/stage2/gccoords/def/gccoords_{}2defhg19_{}_all_loop7_{}_no_gc.bed.gz"
MUT_PAT = "/data/nooroka/grant/punkt3/bed-37/bed_chr_{}_sorted.bed.gz"
DEDUP   = "cut -f4 | sort -u | wc -l"

print("Running: threshold={}, control={}".format(sys.argv[1], sys.argv[2]))

total_gc, total_b, total_mut_gc, total_mut_b = 0, 0, 0, 0
out_file = "results_density_{}_{}_2.tsv".format(sys.argv[1], sys.argv[2])

with open(out_file, "w") as w:
    w.write("chr\tgccoords_len\tb_len\tmut_on_gc\tmut_on_b\tdensity_control\tdensity_quadr\n")

    for i in range(1, 25):
        gc_file  = GC_PAT.format(i, sys.argv[1], sys.argv[2])
        b_file   = B_PAT.format(i, sys.argv[1])
        mut_file = MUT_PAT.format(i)

        gc_len = interval_lengths(gc_file)
        b_len  = interval_lengths(b_file)

        a_cmd = "<(zcat {mut} | awk -v OFS='\\t' '{{if ($3<=$2) $3=$2+1; print}}')".format(mut=mut_file)

        mut_gc = count_lines("bedtools intersect -a {a} -b <(zcat {gc}) -u | {dedup}".format(
            a=a_cmd, gc=gc_file, dedup=DEDUP))
        mut_b  = count_lines("bedtools intersect -a {a} -b {b} -u | {dedup}".format(
            a=a_cmd, b=b_file, dedup=DEDUP))

        dc = mut_gc / gc_len if gc_len else 0
        dq = mut_b  / b_len  if b_len  else 0

        print("chr{}: gc_len={}, b_len={}, mut_gc={}, mut_b={}, dc={:.6f}, dq={:.6f}".format(
            i, gc_len, b_len, mut_gc, mut_b, dc, dq))
        w.write("chr{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
            i, gc_len, b_len, mut_gc, mut_b, dc, dq))

        total_gc     += gc_len
        total_b      += b_len
        total_mut_gc += mut_gc
        total_mut_b  += mut_b

    tdc = total_mut_gc / total_gc if total_gc else 0
    tdq = total_mut_b  / total_b  if total_b  else 0

    print("\nИТОГО: gc={}, b={}, mut_gc={}, mut_b={}, dc={:.6f}, dq={:.6f}".format(
        total_gc, total_b, total_mut_gc, total_mut_b, tdc, tdq))
    w.write("TOTAL\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
        total_gc, total_b, total_mut_gc, total_mut_b, tdc, tdq))

print("Записано в", out_file)
