import os
import subprocess
import sys

# ── аргументы ────────────────────────────────────────────────────────────────
# sys.argv[1] — bed-файл мутаций (отсортированный по chr/start)
# sys.argv[2] — bed-файл GC-координат (control)
# sys.argv[3] — номер хромосомы
# sys.argv[4] — выходной файл результатов

CHR          = sys.argv[3]
MUTATIONS    = sys.argv[1]
GC_COORDS    = sys.argv[2]
RESULT_FILE  = sys.argv[4]

BED_SORTED   = f"/data/nooroka/grant/punkt3/bed-37/bed_chr_{CHR}_sorted.bed.gz"
STAGE2       = "/data/nooroka/grant/punkt3/stage2"

RESULT_GENE_ALL = f"{STAGE2}/resultgene/resultgenehg19{CHR}_40_all_loop7_control2_no_gc_corrected_plus.bed"
RESULT_GENE_UN  = f"{STAGE2}/resultgene/resultgenehg19{CHR}_un_40_all_loop7_control2_no_gc_corrected_plus.bed"
GCCOORDS_DEF    = f"{STAGE2}/gccoords/def/gccoords_{CHR}2defhg19_40_all_loop7_control2_no_gc_corrected2_plus.bed"

CHUNK_LINES  = 500_000

# ── helpers ───────────────────────────────────────────────────────────────────

def sh(cmd: str) -> None:
    """Запустить bash-команду, бросить исключение при ошибке."""
    subprocess.run(cmd, shell=True, executable="/bin/bash", check=True)


def sh_out(cmd: str) -> bytes:
    """Запустить bash-команду, вернуть stdout."""
    return subprocess.run(
        cmd, shell=True, executable="/bin/bash",
        stdout=subprocess.PIPE, check=True
    ).stdout


def count_lines(path: str) -> int:
    n = 0
    with open(path) as f:
        for _ in f:
            n += 1
    return n


# ── 1. bedtools: мутации × гены ───────────────────────────────────────────────
sh(
    f"bedtools intersect "
    f"-a <(zcat {BED_SORTED} | awk 'BEGIN{{OFS=\"\\t\"}} {{if($3<=$2) $3=$2+1; print}}') "
    f"-b <(sort -k1,1 -k2,2n {MUTATIONS}) "
    f"-sorted -wa -wb "
    f"> {RESULT_GENE_ALL}"
)

# ── 2. Читаем GC_COORDS → пишем gccoords_def, считаем sum_control1 ───────────
sum_control1 = 0
last_a = 0

with open(GC_COORDS) as f, open(GCCOORDS_DEF, "w") as out:
    for raw in f:
        cols   = raw.strip().split()
        last_a = cols[6]
        start  = int(cols[7][1:-1])
        end    = int(cols[8][:-1])
        sum_control1 += end - start
        out.write(f"chr{CHR}\t{start}\t{end}\n")

# ── 3. Дедупликация resultgene по col4 ───────────────────────────────────────
sh(
    f"sort -k4,4 -s {RESULT_GENE_ALL} "
    f"| awk '!seen[$4]++' "
    f"> {RESULT_GENE_UN}"
)
d_gene_unique = count_lines(RESULT_GENE_UN)       # кол-во уникальных генов

# ── 4. bedtools: мутации × gccoords чанками → считаем строки без файла ───────
# sort убран: awk хранит только хэш уже виденных $4 (намного меньше RAM)
def count_intersect_dedup(bed_gz: str, bed_b: str, chunk_size: int) -> int:
    """
    Пересекает bed_gz с bed_b чанками.
    Дедуплицирует результат по col4 прямо в потоке через awk.
    Возвращает число уникальных строк. Никаких промежуточных файлов.
    """
    tmp_dir = f"{STAGE2}/intmut/tmp_{CHR}"
    os.makedirs(tmp_dir, exist_ok=True)

    # ── разбиваем bed_b на чанки ──────────────────────────────────────────
    chunk_paths = []
    idx = line_count = 0
    cur = open(f"{tmp_dir}/c{idx}.bed", "w")

    with open(bed_b) as fb:
        for line in fb:
            cur.write(line)
            line_count += 1
            if line_count >= chunk_size:
                cur.close()
                chunk_paths.append(cur.name)
                idx += 1
                cur = open(f"{tmp_dir}/c{idx}.bed", "w")
                line_count = 0
        cur.close()
        if line_count > 0:
            chunk_paths.append(cur.name)
        else:
            os.remove(cur.name)

    # ── awk-дедуп как долгоживущий процесс ───────────────────────────────
    # stdin получает построчно вывод bedtools по каждому чанку
    # stdout мы читаем построчно и просто считаем
    dedup = subprocess.Popen(
        "awk '!seen[$4]++'",
        shell=True, executable="/bin/bash",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    for cp in chunk_paths:
        data = sh_out(
            f"bedtools intersect "
            f"-a <(zcat {bed_gz} | awk 'BEGIN{{OFS=\"\\t\"}} {{if($3<=$2) $3=$2+1; print}}') "
            f"-b {cp} -wa -wb"
        )
        dedup.stdin.write(data)

    dedup.stdin.close()
    n = sum(1 for _ in dedup.stdout)
    dedup.wait()

    import shutil
    shutil.rmtree(tmp_dir, ignore_errors=True)
    return n


d_intmut = count_intersect_dedup(BED_SORTED, GCCOORDS_DEF, CHUNK_LINES)

# ── 5. Считаем длину интервалов мутаций (d4) стримингом ──────────────────────
d_mut_span = 0
with open(MUTATIONS) as f:
    for raw in f:
        cols = raw.strip().split()
        d_mut_span += int(cols[2]) - int(cols[1])

d_mut_count = count_lines(MUTATIONS)              # кол-во строк мутаций

# ── 6. Запись результата ─────────────────────────────────────────────────────
with open(RESULT_FILE, "a") as w:
    if sum_control1 == 0:
        w.write(
            f"chr{CHR}\tnon G4 motif\taverage density\t0"
            f"\taverage G4 motif/interval length\t{last_a}\n"
        )
    else:
        w.write(
            f"chr{CHR}\tnon G4 motif\taverage density\t{d_intmut / sum_control1}"
            f"\taverage G4 motif/interval length\t{last_a}\n"
        )

    w.write(
        f"chr{CHR}\tG4 motif all\taverage density\t{d_gene_unique / d_mut_span}"
        f"\taverage G4 motif/interval length\t{d_mut_span / d_mut_count}\n"
    )


