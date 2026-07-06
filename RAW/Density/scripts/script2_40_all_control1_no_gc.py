

import os
import subprocess
from collections import defaultdict
import sys

w = open(sys.argv[4], "a")


def count_lines_fast(filepath):
    """Быстрый подсчет строк (не загружает файл в память)"""
    count = 0
    with open(filepath, 'r') as f:
        for line in f:
            count += 1
    return count


# ── 1. Первый bedtools: мутации × гены ──────────────────────────────────────
# -sorted  → sweep-алгоритм, O(1) RAM вместо загрузки всего в память.
# Оба входных файла должны быть отсортированы по (chr, start).
# bed_chr_{N}_sorted.bed уже отсортирован по имени; sys.argv[1] сортируем на лету.
cmd1 = (
    """bedtools intersect """
    """-a <(awk 'BEGIN{{OFS="\\t"}} {{ if ($3 <= $2) $3=$2+1; print }}' """
    """/data/nooroka/grant/punkt3/bed-37/bed_chr_{c}_sorted.bed) """
    """-b <(sort -k1,1 -k2,2n {b}) """
    """-sorted -wa -wb """
    """> /data/nooroka/grant/punkt3/stage2/resultgene/"""
    """resultgenehg19{c}_40_all_loop7_control1_no_gc.bed"""
).format(c=sys.argv[3], b=sys.argv[1])

subprocess.run(cmd1, shell=True, executable="/bin/bash")

# ── 2. Читаем sys.argv[2], пишем gccoords ────────────────────────────────────
op2 = open(sys.argv[1], "r")
d4 = 0
op = open(sys.argv[2], "r")
w3 = open(
    "/data/nooroka/grant/punkt3/stage2/gccoords/def/"
    "gccoords_{}2defhg19_40_all_loop7_control1_no_gc.bed".format(sys.argv[3]),
    "w"
)
a = ""
for line in op:
    line = line.strip().split()
    a = line[6]
    line77 = int(line[7][1:-1])
    line88 = line[8][:-1]
    w3.write("chr{}\t{}\t{}\n".format(sys.argv[3], line77, line88))
w3.close()
op.close()

d5 = count_lines_fast(sys.argv[2])

os.system(
    "sort -k1,1 -k2,2n /data/nooroka/grant/punkt3/stage2/gccoords/def/"
    "gccoords_{c}2defhg19_40_all_loop7_control1_no_gc.bed "
    "| awk '!seen[$1,$2,$3]++' "
    "> /data/nooroka/grant/punkt3/stage2/gccoords/def/"
    "gccoords_{c}_undefhg19_40_all_loop7_control1_no_gc.bed".format(c=sys.argv[3])
)

os.system(
    "sort -k4,4 -s /data/nooroka/grant/punkt3/stage2/resultgene/"
    "resultgenehg19{c}_40_all_loop7_control1_no_gc.bed "
    "| awk '!seen[$4]++' "
    "> /data/nooroka/grant/punkt3/stage2/resultgene/"
    "resultgenehg19{c}_un_40_all_loop7_control1_no_gc.bed".format(c=sys.argv[3])
)

# ── 3. Второй bedtools: мутации × GC-координаты ─────────────────────────────
# gccoords_undef отсортирован по -k4,4 (принципиально).
# bedtools -sorted требует координатной сортировки → не используем его здесь.
# Вместо этого: разбиваем -b на чанки по N строк, пересекаем каждый чанк,
# результаты объединяем. Это резко снижает пиковый RSS.

gccoords_undef = (
    "/data/nooroka/grant/punkt3/stage2/gccoords/def/"
    "gccoords_{c}_undefhg19_40_all_loop7_control1_no_gc.bed".format(c=sys.argv[3])
)
intmut_out = (
    "/data/nooroka/grant/punkt3/stage2/intmut/"
    "intmuthg19{c}_40_all_loop7_control1_no_gc.bed".format(c=sys.argv[3])
)

CHUNK_LINES = 500_000   # подбери под доступный RAM; меньше → меньше памяти

def run_bedtools_chunked(bed_a_cmd, bed_b_path, output_path, chunk_size):
    """Запускает bedtools intersect чанками по bed_b, пишет результат в output_path."""
    import tempfile, shutil
    tmp_dir = "/data/nooroka/grant/punkt3/stage2/intmut/tmp_chunks_{}".format(sys.argv[3])
    os.makedirs(tmp_dir, exist_ok=True)

    chunk_idx = 0
    chunk_path = os.path.join(tmp_dir, "chunk_{}.bed".format(chunk_idx))
    fchunk = open(chunk_path, "w")
    line_count = 0

    chunk_files = []

    with open(bed_b_path, "r") as fb:
        for line in fb:
            fchunk.write(line)
            line_count += 1
            if line_count >= chunk_size:
                fchunk.close()
                chunk_files.append(chunk_path)
                chunk_idx += 1
                chunk_path = os.path.join(tmp_dir, "chunk_{}.bed".format(chunk_idx))
                fchunk = open(chunk_path, "w")
                line_count = 0
        fchunk.close()
        if line_count > 0:
            chunk_files.append(chunk_path)
        else:
            os.remove(chunk_path)

    # Запускаем bedtools на каждый чанк, результаты пишем в один выходной файл
    with open(output_path, "w") as fout:
        for cf in chunk_files:
            cmd = (
                "bedtools intersect "
                "-a <({a}) "
                "-b {b} "
                "-wa -wb"
            ).format(a=bed_a_cmd, b=cf)
            result = subprocess.run(
                cmd, shell=True, executable="/bin/bash",
                stdout=subprocess.PIPE, check=True
            )
            fout.write(result.stdout.decode())

    shutil.rmtree(tmp_dir, ignore_errors=True)

bed_a_inner = (
    "awk 'BEGIN{{OFS=\"\\t\"}} {{ if ($3 <= $2) $3=$2+1; print }}' "
    "/data/nooroka/grant/punkt3/bed-37/bed_chr_{c}_sorted.bed"
).format(c=sys.argv[3])

run_bedtools_chunked(bed_a_inner, gccoords_undef, intmut_out + ".raw", CHUNK_LINES)

# Дедупликация по 4-му столбцу после объединения чанков
os.system("sort -k4,4 -s {raw} | awk '!seen[$4]++' > {out}".format(
    raw=intmut_out + ".raw", out=intmut_out
))
os.remove(intmut_out + ".raw")

# Считаем d2 ДО второго subprocess (не держим лишние fd)
d2 = count_lines_fast(
    "/data/nooroka/grant/punkt3/stage2/resultgene/"
    "resultgenehg19{}_un_40_all_loop7_control1_no_gc.bed".format(sys.argv[3])
)

# Считаем d4 стримингом — не грузим весь файл в память
for line2 in op2:
    line2 = line2.strip().split()
    d4 += int(line2[2]) - int(line2[1])
op2.close()



# ── 4. Финальные счётчики и запись результата ────────────────────────────────
d6  = count_lines_fast(sys.argv[1])
g1  = count_lines_fast(intmut_out)   # = d11 в оригинале

d11 = g1
d22 = d2
d66 = d6

if a == "":
    a = 0

d55 = int(d5) * int(a)
print("d11-55-22-4 {}\t{}\t{}\t{}".format(d11, d55, d22, d4))

w2 = open("test_quadr.txt", "a")
w2.write("{}\t{}\t{}\n".format(sys.argv[3], d22, d4))
w2.close()

if d55 == 0:
    w.write(
        "chr{}\tnon G4 motif\taverage density\t0"
        "\taverage G4 motif/interval length\t{}\n".format(sys.argv[3], a)
    )
else:
    w.write(
        "chr{}\tnon G4 motif\taverage density\t{}"
        "\taverage G4 motif/interval length\t{}\n".format(
            sys.argv[3], float(int(d11) / int(d55)), a
        )
    )

w.write(
    "chr{}\tG4 motif all\taverage density\t{}"
    "\taverage G4 motif/interval length\t{}\n".format(
        sys.argv[3],
        float(int(d22) / int(d4)),
        float(int(d4) / int(d66)),
    )
)
w.close()
