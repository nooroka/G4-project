import sys
import subprocess
import ast
output_file = open(sys.argv[4], "a")

input_file = open(sys.argv[2], "r")
gccoords_path =("{}".format(sys.argv[5]))
gaps_path = ("{}".format(sys.argv[6]))
gccoords_file = open(gccoords_path, "w")
gaps_file = open(gaps_path, "w")  
 
avg_quadruplex_length = ""
sum_control_length = 0
prev_end = None  
 
for line in input_file:
    fields = line.rstrip("\n").split("\t")
    avg_quadruplex_length = fields[6]
    coords_str = fields[7]
    intervals = ast.literal_eval(coords_str)
 
    for interval_start, interval_end in intervals:
        interval_start = int(interval_start)
        interval_end = int(interval_end)
 
        if prev_end is not None and interval_start > prev_end:
            gaps_file.write(
                "chr{}\t{}\t{}\n".format(sys.argv[3], prev_end, interval_start)
            )
 
        sum_control_length += interval_end - interval_start
        gccoords_file.write(
            "chr{}\t{}\t{}\n".format(sys.argv[3], interval_start, interval_end)
        )
 
        prev_end = interval_end
 
gccoords_file.close()
gaps_file.close()
input_file.close()
cmd_mutations_vs_g4 = (
    "bedtools intersect "
    "-a <(zcat /data/nooroka/grant/punkt3/bed-37/bed_chr_{0}_sorted.bed.gz "
    "| awk 'BEGIN{{OFS=\"\\t\"}} $3<=$2{{$3=$2+1}} 1') "
    "-b {1} "
    "| sort -k4,4 -T /tmp -S 2G -u "
    "| wc -l"
).format(sys.argv[3], sys.argv[1])
result_g4 = subprocess.run(
    cmd_mutations_vs_g4, shell=True, executable="/bin/bash", capture_output=True, text=True
)
n_mutations_in_g4 = int(result_g4.stdout.strip())

cmd_mutations_vs_control = (
    "bedtools intersect "
    "-a <(zcat /data/nooroka/grant/punkt3/bed-37/bed_chr_{0}_sorted.bed.gz "
    "| awk 'BEGIN{{OFS=\"\\t\"}} $3<=$2{{$3=$2+1}} 1') "
    "-b {1} "
    "| sort -k4,4 -T /tmp -S 2G -u "
    "| wc -l"
).format(sys.argv[3], gccoords_path)
result_control = subprocess.run(
    cmd_mutations_vs_control, shell=True, executable="/bin/bash", capture_output=True, text=True
)
n_mutations_in_control = int(result_control.stdout.strip())

sum_g4_length = 0
g4_intervals_file = open(sys.argv[1], "r")
for line in g4_intervals_file:
    line = line.strip().split()
    sum_g4_length += int(line[2]) - int(line[1])
g4_intervals_file.close()
n_g4_intervals = sum(1 for _ in open(sys.argv[1]))

if avg_quadruplex_length == "":
    avg_quadruplex_length = 0

if sum_control_length == 0:
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
