import gzip
import subprocess
import sys

w = open(sys.argv[4], "a")


def count_lines_fast(filepath):
    """Быстрый подсчет строк (не загружает файл в память)"""
    count = 0
    with open(filepath, "r") as f:
        for line in f:
            count += 1
    return count


def run_count(bed_a_gz, bed_b_path):
    """
    bedtools intersect(-a zcat(bed_a_gz) фикс координат, -b bed_b_path)
    | sort -k4,4 -u | wc -l
    Возвращает число уникальных пересечений (по 4-й колонке).
    """
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


# ── 1. Читаем sys.argv[2] (GC-corrected control, .gz), пишем gccoords ───────
gccoords_path = (
    "/data/nooroka/grant/punkt3/stage2/gccoords/def/"
    "gccoords_{}2defhg19_{}_all_loop7_control2_no_gc_corrected_cleaned.bed".format(sys.argv[3], sys.argv[5])
)
w3 = open(gccoords_path, "w")
a = ""
d5 = 0
sum1 = 0
with gzip.open(sys.argv[2], "rt") as op:
    for line in op:
        line = line.strip().split()
        a = line[6]
        line77 = int(line[7][1:-1])
        line88 = line[8][:-1]
        w3.write("chr{}\t{}\t{}\n".format(sys.argv[3], line77, line88))
        d5 += 1
        b = int(line88) - line77
        sum1 += b
w3.close()

# ── 2. Первый bedtools: мутации (argv1) × гены ───────────────────────────────
bed_chr_gz = "/data/nooroka/grant/punkt3/bed-37/bed_chr_{}_sorted.bed.gz".format(sys.argv[3])
d2 = run_count(bed_chr_gz, sys.argv[1])

# ── 3. Второй bedtools: мутации (гены) × GC-координаты ───────────────────────
d11 = run_count(bed_chr_gz, gccoords_path)

# ── 4. Считаем d4 и d6 стримингом по argv[1] ─────────────────────────────────
d4 = 0
d6 = 0
with open(sys.argv[1], "r") as op2:
    for line2 in op2:
        line2 = line2.strip().split()
        d4 += int(line2[2]) - int(line2[1])
        d6 += 1

if a == "":
    a = 0

d22 = d2
d66 = d6

# ── 5. Запись результата ─────────────────────────────────────────────────────
if d5 == 0:
    w.write(
        "chr{}\tnon G4 motif\taverage density\t0"
        "\taverage G4 motif/interval length\t{}\n".format(sys.argv[3], a)
    )
else:
    w.write(
        "chr{}\tnon G4 motif\taverage density\t{}"
        "\taverage G4 motif/interval length\t{}\n".format(
            sys.argv[3], float(d11) / float(sum1), a
        )
    )

w.write(
    "chr{}\tG4 motif all\taverage density\t{}"
    "\taverage G4 motif/interval length\t{}\n".format(
        sys.argv[3],
        float(d22) / float(d4),
        float(d4) / float(d66),
    )
)
w.close()
