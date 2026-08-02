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


input_file = open(sys.argv[1], "r")
gccoords_file = open(
    "/data/nooroka/grant/punkt3/stage2/gccoords/def/gccoords_new_{}2defnongenes_less_50_control_39.bed".format(sys.argv[2]),
    "w"
)
avg_quadruplex_length = ""
sum_control_length = 0
for line in input_file:
    line = line.strip().split()
    avg_quadruplex_length = line[6]
    interval_start = int(line[7][1:-1])
    interval_end = line[8][:-1]
    interval_length = int(interval_end) - int(interval_start)
    sum_control_length += interval_length
    gccoords_file.write("chr{}\t{}\t{}\n".format(sys.argv[2], interval_start, interval_end))
gccoords_file.close()
input_file.close()

if avg_quadruplex_length == "":
    avg_quadruplex_length = 0

n_control_intervals = count_lines_fast(sys.argv[1])
bed_chr_gz = "/data/nooroka/grant/punkt3/bed-37/bed_chr_{}_sorted.bed.gz".format(sys.argv[2])
gccoords_path = "/data/nooroka/grant/punkt3/stage2/gccoords/def/gccoords_new_{}2defnongenes_less_50_control_39.bed".format(sys.argv[2])
n_mutations_in_control = run_count(bed_chr_gz, gccoords_path)

if sum_control_length == 0 or n_mutations_in_control == 0:
    output_file.write("chr{}\tnon G4 motif\taverage density\t0\taverage G4 motif/interval length\t{}\n".format(
        sys.argv[2], avg_quadruplex_length
    ))
else:
    control_density = n_mutations_in_control / sum_control_length
    output_file.write("chr{}\tnon G4 motif\taverage density\t{}\taverage G4 motif/interval length\t{}\n".format(
        sys.argv[2], control_density, avg_quadruplex_length
    ))
output_file.close()
