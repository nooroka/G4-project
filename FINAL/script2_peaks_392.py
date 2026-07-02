import subprocess
import sys

w = open(sys.argv[3], "a")

cmd = (
    "bedtools intersect "
    "-a <(awk 'BEGIN{{OFS=\"\\t\"}} {{ if ($3 <= $2) $3=$2+1; print }}' "
    "<(zcat /data/nooroka/grant/punkt3/bed-37/bed_chr_{0}_sorted.bed.gz)) "
    "-b {1} "
    "| sort -k4,4 -T /tmp -S 2G -u "
    "| wc -l"
).format(sys.argv[2], sys.argv[1])

result = subprocess.run(cmd, shell=True, executable="/bin/bash", capture_output=True, text=True)
d2 = int(result.stdout.strip())

d4 = 0
op2 = open(sys.argv[1], "r")
for line2 in op2:
    line2 = line2.strip().split()
    sum22 = int(line2[2]) - int(line2[1])
    d4 += sum22
op2.close()

d6 = sum(1 for _ in open(sys.argv[1]))

w.write(
    "chr{}\tG4 motif all\taverage density\t{}\taverage G4 motif/interval length\t{}\n".format(
        sys.argv[2],
        float(d2 / d4),
        float(d4 / d6)
    )
)
w.close()
