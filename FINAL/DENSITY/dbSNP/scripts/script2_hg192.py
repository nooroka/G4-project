import subprocess
import sys

output_file = open(sys.argv[3], "a")

cmd_mutations_vs_g4 = (
    "bedtools intersect "
    "-a <(awk 'BEGIN{{OFS=\"\\t\"}} {{ if ($3 <= $2) $3=$2+1; print }}' "
    "<(zcat /data/nooroka/grant/punkt3/bed-37/bed_chr_{0}_sorted.bed.gz)) "
    "-b {1} "
    "| sort -k4,4 -T /tmp -S 2G -u | wc -l"
).format(sys.argv[2], sys.argv[1])
result_g4 = subprocess.run(
    cmd_mutations_vs_g4, shell=True, executable="/bin/bash", capture_output=True, text=True
)
n_mutations_in_g4 = int(result_g4.stdout.strip())

sum_g4_length = 0
g4_intervals_file = open(sys.argv[1], "r")
for line in g4_intervals_file:
    line = line.strip().split()
    interval_length = int(line[2]) - int(line[1])
    sum_g4_length += interval_length
g4_intervals_file.close()

n_g4_intervals = sum(1 for _ in open(sys.argv[1]))

output_file.write(
    "chr{}\tG4 motif all\taverage density\t{}\taverage G4 motif/interval length\t{}\n".format(
        sys.argv[2],
        float(n_mutations_in_g4 / sum_g4_length),
        float(sum_g4_length / n_g4_intervals)
    )
)
output_file.close()
