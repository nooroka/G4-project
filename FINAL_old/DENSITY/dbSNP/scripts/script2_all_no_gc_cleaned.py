import gzip
import subprocess
import sys

output_file = open(sys.argv[4], "a")


def count_lines_fast(filepath):
    count = 0
    with open(filepath, "r") as f:
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


gccoords_path = (
    "/data/nooroka/grant/punkt3/stage2/gccoords/def/"
    "gccoords_{}2defhg19_{}_all_loop7_control2_no_gc_corrected_cleaned.bed".format(sys.argv[3], sys.argv[5])
)
gccoords_file = open(gccoords_path, "w")
avg_quadruplex_length = ""
n_control_lines = 0
sum_control_length = 0
with gzip.open(sys.argv[2], "rt") as input_file:
    for line in input_file:
        line = line.strip().split()
        avg_quadruplex_length = line[6]
        interval_start = int(line[7][1:-1])
        interval_end = line[8][:-1]
        gccoords_file.write("chr{}\t{}\t{}\n".format(sys.argv[3], interval_start, interval_end))
        n_control_lines += 1
        interval_length = int(interval_end) - interval_start
        sum_control_length += interval_length
gccoords_file.close()

bed_chr_gz = "/data/nooroka/grant/punkt3/bed-37/bed_chr_{}_sorted.bed.gz".format(sys.argv[3])
n_mutations_in_g4 = run_count(bed_chr_gz, sys.argv[1])

n_mutations_in_control = run_count(bed_chr_gz, gccoords_path)

sum_g4_length = 0
n_g4_intervals = 0
with open(sys.argv[1], "r") as g4_intervals_file:
    for line in g4_intervals_file:
        line = line.strip().split()
        sum_g4_length += int(line[2]) - int(line[1])
        n_g4_intervals += 1

if avg_quadruplex_length == "":
    avg_quadruplex_length = 0

if n_control_lines == 0:
    output_file.write(
        "chr{}\tnon G4 motif\taverage density\t0"
        "\taverage G4 motif/interval length\t{}\n".format(sys.argv[3], avg_quadruplex_length)
    )
else:
    output_file.write(
        "chr{}\tnon G4 motif\taverage density\t{}"
        "\taverage G4 motif/interval length\t{}\n".format(
            sys.argv[3], float(n_mutations_in_control) / float(sum_control_length), avg_quadruplex_length
        )
    )
output_file.write(
    "chr{}\tG4 motif all\taverage density\t{}"
    "\taverage G4 motif/interval length\t{}\n".format(
        sys.argv[3],
        float(n_mutations_in_g4) / float(sum_g4_length),
        float(sum_g4_length) / float(n_g4_intervals),
    )
)
output_file.close()
