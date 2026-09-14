import os
import subprocess
from collections import defaultdict
import sys

output_file = open(sys.argv[3], "a")


def count_lines_fast(filepath):
    count = 0
    with open(filepath, 'r') as f:
        for line in f:
            count += 1
    return count


def run_count(bed_a_gz, bed_b_path):
    cmd = (
        "bedtools intersect "
        "-a <(zcat {a} "
        "| awk 'BEGIN{{OFS=\"\\t\"}} $3<=$2{{$3=$2+1}} 1') "
        "-b {b} "
        "| sort -k4,4 -T /tmp -S 2G -u "
        "| wc -l"
    ).format(a=bed_a_gz, b=bed_b_path)
    result = subprocess.run(
        cmd, shell=True, executable="/bin/bash",
        capture_output=True, text=True, check=True
    )
    return int(result.stdout.strip())


bed_chr_gz = "/data/nooroka/grant/punkt3/bed-37/bed_chr_{}_sorted.bed.gz".format(sys.argv[2])
n_mutations_in_g4 = run_count(bed_chr_gz, sys.argv[1])

sum_g4_length = 0
g4_intervals_file = open(sys.argv[1], "r")
for line in g4_intervals_file:
    line = line.strip().split()
    interval_length = int(line[2]) - int(line[1])
    sum_g4_length += interval_length
g4_intervals_file.close()

n_g4_intervals = count_lines_fast(sys.argv[1])

output_file.write(
    "chr{}\tG4 motif all\taverage density\t{}\taverage G4 motif/interval length\t{}\n".format(
        sys.argv[2],
        float(n_mutations_in_g4 / sum_g4_length),
        float(sum_g4_length / n_g4_intervals),
    )
)
output_file.close()
