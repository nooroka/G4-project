import subprocess
import sys

output_file = open(sys.argv[3], "a")
input_file = open(sys.argv[1], "r")
gccoords_path = "{}".format(sys.argv[4])
gccoords_file = open(gccoords_path, "w")
avg_quadruplex_length = ""
sum_control_length = 0
for line in input_file:
    line = line.strip().split()
    avg_quadruplex_length = line[6]
    interval_start = int(line[7][1:-1])
    interval_end = line[8][:-1]
    gccoords_file.write("chr{}\t{}\t{}\n".format(sys.argv[2], interval_start, interval_end))
    interval_length = int(interval_end) - interval_start
    sum_control_length += interval_length
gccoords_file.close()
input_file.close()

if avg_quadruplex_length == "":
    avg_quadruplex_length = 0

if sum_control_length == 0:
    output_file.write("chr{}\tnon G4 motif\taverage density\t0\taverage G4 motif/interval length\t{}\n".format(
        sys.argv[2], avg_quadruplex_length
    ))
else:
    cmd_mutations_vs_control = (
        "bedtools intersect "
        "-a <(awk 'BEGIN{{OFS=\"\\t\"}} {{ if ($3 <= $2) $3=$2+1; print }}' "
        "<(zcat /data/nooroka/grant/punkt3/bed-37/bed_chr_{0}_sorted.bed.gz)) "
        "-b {1} "
        "| sort -k4,4 -T /tmp -S 2G -u | wc -l"
    ).format(sys.argv[2], gccoords_path)
    result_control = subprocess.run(
        cmd_mutations_vs_control, shell=True, executable="/bin/bash", capture_output=True, text=True
    )
    n_mutations_in_control = int(result_control.stdout.strip())
    output_file.write("chr{}\tnon G4 motif\taverage density\t{}\taverage G4 motif/interval length\t{}\n".format(
        sys.argv[2],
        float(n_mutations_in_control / sum_control_length),
        avg_quadruplex_length
    ))
output_file.close()
