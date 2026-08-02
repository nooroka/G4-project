import os
import gzip
import subprocess
from collections import defaultdict
import sys

output_file = open(sys.argv[4], "a")


def count_lines_fast(filepath):
    if filepath.endswith(".gz"):
        cmd = "zcat {} | wc -l".format(filepath)
        result = subprocess.run(
            cmd, shell=True, executable="/bin/bash",
            capture_output=True, text=True, check=True
        )
        return int(result.stdout.strip())
    count = 0
    with open(filepath, 'r') as f:
        for line in f:
            count += 1
    return count


def run_count(bed_a, bed_b_path):
    a_src = "zcat {}".format(bed_a) if bed_a.endswith(".gz") else "cat {}".format(bed_a)
    cmd = (
        "bedtools intersect "
        "-a <({a_src} | awk 'BEGIN{{OFS=\"\\t\"}} {{ if ($3 <= $2) $3=$2+1; print }}') "
        "-b {b} "
        "| sort -k4,4 -T /tmp -S 2G -u "
        "| wc -l"
    ).format(a_src=a_src, b=bed_b_path)
    result = subprocess.run(
        cmd, shell=True, executable="/bin/bash",
        capture_output=True, text=True, check=True
    )
    return int(result.stdout.strip())


bed_chr = "/data/nooroka/grant/punkt3/bed-37/bed_chr_{}_sorted.bed.gz".format(sys.argv[3])

n_mutations_in_g4 = run_count(bed_chr, sys.argv[1])

g4_intervals_file = open(sys.argv[1], "r")
sum_g4_length = 0
control_file = open(sys.argv[2], "r")

gccoords_path = (
    "/data/nooroka/grant/punkt3/stage2/gccoords/def/"
    "gccoords_{}2defhg19_{}_all_loop7_control1_50_more_equal.bed".format(sys.argv[3], sys.argv[5])
)

gccoords_file = open(gccoords_path, "wt")
avg_quadruplex_length = ""
sum_control_length = 0
for line in control_file:
    line = line.strip().split()
    avg_quadruplex_length = line[6]
    interval_start = int(line[7][1:-1])
    interval_end = line[8][:-1]
    interval_length = int(interval_end) - interval_start
    sum_control_length += interval_length
    gccoords_file.write("chr{}\t{}\t{}\n".format(sys.argv[3], interval_start, interval_end))
gccoords_file.close()
control_file.close()

n_control_descriptor_lines = count_lines_fast(sys.argv[2])

n_mutations_in_control = run_count(bed_chr, gccoords_path)

for line in g4_intervals_file:
    line = line.strip().split()
    g4_interval_length = int(line[2]) - int(line[1])
    sum_g4_length += g4_interval_length
g4_intervals_file.close()

n_g4_intervals = count_lines_fast(sys.argv[1])

if avg_quadruplex_length == "":
    avg_quadruplex_length = 0
if n_control_descriptor_lines == 0:
    output_file.write(
        "chr{}\tnon G4 motif\taverage density\t0"
        "\taverage G4 motif/interval length\t{}\n".format(sys.argv[3], avg_quadruplex_length)
    )
else:
    output_file.write(
        "chr{}\tnon G4 motif\taverage density\t{}"
        "\taverage G4 motif/interval length\t{}\n".format(
            sys.argv[3], float(n_mutations_in_control / sum_control_length), avg_quadruplex_length
        )
    )
output_file.write(
    "chr{}\tG4 motif all\taverage density\t{}"
    "\taverage G4 motif/interval length\t{}\n".format(
        sys.argv[3],
        float(n_mutations_in_g4 / sum_g4_length),
        float(sum_g4_length / n_g4_intervals),
    )
)
output_file.close()
