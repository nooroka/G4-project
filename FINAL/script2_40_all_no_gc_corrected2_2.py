import subprocess
import sys

w = open(sys.argv[4], "a")

# ── 1. Читаем sys.argv[2], пишем gccoords ────────────────────────────────────
op = open(sys.argv[2], "r")
gccoords_path = (
    "/data/nooroka/grant/punkt3/stage2/gccoords/def/"
    "gccoords_{}2defhg19_40_all_loop7_control2_no_gc_corrected.bed".format(sys.argv[3])
)
w3 = open(gccoords_path, "w")

a = ""
sum_control1 = 0
for line in op:
    line = line.strip().split()
    a = line[6]
    line77 = int(line[7][1:-1])
    line88 = line[8][:-1]
    sum_control1 += int(line88) - int(line77)
    w3.write("chr{}\t{}\t{}\n".format(sys.argv[3], line77, line88))
w3.close()
op.close()

# ── 2. Первый bedtools: мутации × гены ──────────────────────────────────────
cmd1 = (
    "bedtools intersect "
    "-a <(zcat /data/nooroka/grant/punkt3/bed-37/bed_chr_{0}_sorted.bed.gz "
    "| awk 'BEGIN{{OFS=\"\\t\"}} $3<=$2{{$3=$2+1}} 1') "
    "-b {1} "
    "| sort -k4,4 -T /tmp -S 2G -u "
    "| wc -l"
).format(sys.argv[3], sys.argv[1])

result1 = subprocess.run(cmd1, shell=True, executable="/bin/bash", capture_output=True, text=True)
d2 = int(result1.stdout.strip())

# ── 3. Второй bedtools: мутации × GC-координаты ─────────────────────────────
cmd2 = (
    "bedtools intersect "
    "-a <(zcat /data/nooroka/grant/punkt3/bed-37/bed_chr_{0}_sorted.bed.gz "
    "| awk 'BEGIN{{OFS=\"\\t\"}} $3<=$2{{$3=$2+1}} 1') "
    "-b {1} "
    "| sort -k4,4 -T /tmp -S 2G -u "
    "| wc -l"
).format(sys.argv[3], gccoords_path)

result2 = subprocess.run(cmd2, shell=True, executable="/bin/bash", capture_output=True, text=True)
d11 = int(result2.stdout.strip())

# ── 4. Считаем d4 ────────────────────────────────────────────────────────────
d4 = 0
op2 = open(sys.argv[1], "r")
for line2 in op2:
    line2 = line2.strip().split()
    d4 += int(line2[2]) - int(line2[1])
op2.close()

d6 = sum(1 for _ in open(sys.argv[1]))

if a == "":
    a = 0
# ── 5. Запись результата ──────────────────────────────────────────────────────
if sum_control1 == 0:
    w.write(
        "chr{}\tnon G4 motif\taverage density\t0"
        "\taverage G4 motif/interval length\t{}\n".format(sys.argv[3], a)
    )
else:
    w.write(
        "chr{}\tnon G4 motif\taverage density\t{}"
        "\taverage G4 motif/interval length\t{}\n".format(
            sys.argv[3], float(d11 / sum_control1), a
        )
    )

w.write(
    "chr{}\tG4 motif all\taverage density\t{}"
    "\taverage G4 motif/interval length\t{}\n".format(
        sys.argv[3],
        float(d2 / d4),
        float(d4 / d6),
    )
)
w.close()
