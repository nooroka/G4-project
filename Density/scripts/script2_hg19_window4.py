import subprocess
import sys
from pathlib import Path

# ── Аргументы ──────────────────────────────────────────────────────────────
chrom       = sys.argv[2]   # Номер хромосомы (например: 1)
output_file = sys.argv[3]   # Файл для записи результатов


# ── Пути ───────────────────────────────────────────────────────────────────
BASE         = Path("/data/nooroka/grant/punkt3")
bed_file     = BASE / f"bed-37/bed_chr_{chrom}_sorted.bed"
bed_clean    = BASE / f"stage2/bed_clean/bed_chr_{chrom}_clean.bed"
genome_file  = BASE / "stage2/scripts/hg19_window.genome"
windows_bed  = BASE / f"stage2/windows_chr{chrom}_46.bed"
uniq_bed     = BASE / f"stage2/resultgene/resultgenehg19_window{chrom}_hg19_window_un.bed"

bed_clean.parent.mkdir(parents=True, exist_ok=True)
uniq_bed.parent.mkdir(parents=True, exist_ok=True)

# ── 1. Предобработка: убрать track, исправить end<=start ───────────────────
cmd_clean = f"""
grep -v "^track" {bed_file} \
  | awk 'BEGIN{{OFS="\\t"}} $3<=$2{{$3=$2+1}} {{print}}' \
  > {bed_clean}
"""
subprocess.run(cmd_clean, shell=True, executable="/bin/bash", check=True)

# ── 2. Создание окон ────────────────────────────────────────────────────────
cmd_windows = f"""
bedtools makewindows -g {genome_file} -w 46 -s 46 \
  | awk '$1=="chr{chrom}"' \
  > {windows_bed}
"""
subprocess.run(cmd_windows, shell=True, executable="/bin/bash", check=True)

# ── 3. Пересечение + дедупликация + сортировка ─────────────────────────────
cmd_intersect = f"""
bedtools intersect \
  -a {bed_clean} \
  -b {windows_bed} \
  -wa -wb \
  | awk '!seen[$4]++' \
  | sort -k4,4 -k5,5n \
  > {uniq_bed}
"""
subprocess.run(cmd_intersect, shell=True, executable="/bin/bash", check=True)

# ── 4. Суммарная длина интервалов в чистом bed-файле ─────────────────────
def count_bed_length(path: Path) -> int:
    total = 0
    with open(path) as f:
        for line in f:
            if not line.strip():
                continue
            fields = line.split("\t")
            start, end = int(fields[1]), int(fields[2])
            total += end - start
    return total


total_genome_length = count_bed_length(bed_clean)
def count_lines_fast(filepath):
    """Быстрый подсчет строк (не загружает файл в память)"""
    count = 0
    with open(filepath, 'r') as f:
        for line in f:
            count += 1
    return count

d5 = count_lines_fast(f'{uniq_bed}')
d6 = count_bed_length(f'{windows_bed}')
w = open(output_file,"w")
w.write("chr{}".format(sys.argv[2])+"\t"+"\t"+"average density"+"\t"+str(float(int(d5)/int(d6)))+"\taverage G4 motif/interval length"+"\t"+"46"+"\n")
w.close()
