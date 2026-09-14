import subprocess
import sys
import gzip

g4_path = sys.argv[1]
chrom = sys.argv[2]
output_path = sys.argv[3]

is_gz = g4_path.endswith(".gz")

if is_gz:
    b_arg = (
        "<(zcat {} | awk 'BEGIN{{OFS=\"\\t\"}} NF>=3 {{print $1,$2,$3}}')"
    ).format(g4_path)
else:
    b_arg = (
        "<(awk 'BEGIN{{OFS=\"\\t\"}} NF>=3 {{print $1,$2,$3}}' {})"
    ).format(g4_path)

cmd_mutations_vs_g4 = (
    "bedtools intersect "
    "-a <(awk 'BEGIN{{OFS=\"\\t\"}} {{ if ($3 <= $2) $3=$2+1; print }}' "
    "<(zcat /data/nooroka/grant/punkt3/bed-37/bed_chr_{0}_sorted.bed.gz)) "
    "-b {1} "
    "| sort -k4,4 -T /tmp -S 2G -u | wc -l"
).format(chrom, b_arg)

result_g4 = subprocess.run(
    cmd_mutations_vs_g4, shell=True, executable="/bin/bash", capture_output=True, text=True
)

if result_g4.returncode != 0 or "Error" in result_g4.stderr:
    sys.stderr.write("bedtools intersect failed for chr{}:\n".format(chrom))
    sys.stderr.write("CMD: {}\n".format(cmd_mutations_vs_g4))
    sys.stderr.write("STDERR: {}\n".format(result_g4.stderr))
    sys.exit(1)

stdout = result_g4.stdout.strip()
if stdout == "":
    sys.stderr.write("Empty stdout from bedtools for chr{}, cannot proceed.\n".format(chrom))
    sys.stderr.write("STDERR: {}\n".format(result_g4.stderr))
    sys.exit(1)

n_mutations_in_g4 = int(stdout)

def open_maybe_gz(path):
    if path.endswith(".gz"):
        return gzip.open(path, "rt")
    return open(path, "r")

sum_g4_length = 0
n_g4_intervals = 0

with open_maybe_gz(g4_path) as g4_intervals_file:
    for line in g4_intervals_file:
        fields = line.strip().split()
        if len(fields) < 3:
            continue
        try:
            start = int(fields[1])
            end = int(fields[2])
        except ValueError:
            continue
        sum_g4_length += end - start
        n_g4_intervals += 1

if n_g4_intervals == 0 or sum_g4_length == 0:
    sys.stderr.write(
        "No valid G4 intervals found in {} for chr{} (n_intervals={}, sum_length={})\n".format(
            g4_path, chrom, n_g4_intervals, sum_g4_length
        )
    )
    sys.exit(1)

with open(output_path, "a") as output_file:
    output_file.write(
        "chr{}\tG4 motif all\taverage density\t{}\taverage G4 motif/interval length\t{}\n".format(
            chrom,
            float(n_mutations_in_g4 / sum_g4_length),
            float(sum_g4_length / n_g4_intervals),
        )
    )
