import os
import sys
import subprocess
import shutil

CHR = sys.argv[3]
CHUNK = 500_000

BASE = "/data/nooroka/grant/punkt3/stage2"
BED_GZ = f"/data/nooroka/grant/punkt3/bed-37/bed_chr_{CHR}_sorted.bed.gz"

paths = {
    "gccoords": f"{BASE}/gccoords/def/gccoords_{CHR}2defhg19_40_all_loop7_control2_no_gc_corrected2.bed",
    "intmut":   f"{BASE}/intmut/intmuthg19{CHR}_40_all_loop7_control2_no_gc_corrected2.bed",
    "res_raw":  f"{BASE}/resultgene/resultgenehg19{CHR}_40_all_loop7_control2_no_gc_corrected2.bed",
    "res_uniq": f"{BASE}/resultgene/resultgenehg19{CHR}_un_40_all_loop7_control2_no_gc_corrected2.bed",
}

# ── utils ─────────────────────────────────────────

def run(cmd):
    subprocess.run(cmd, shell=True, executable="/bin/bash", check=True)

def count_lines(f):
    with open(f) as fh:
        return sum(1 for _ in fh)

def fix_bed():
    return f"zcat {BED_GZ} | awk 'BEGIN{{OFS=\"\\t\"}}{{if($3<=$2)$3=$2+1;print}}'"

# ── 1. mutations × genes ─────────────────────────

run(
    f"bedtools intersect "
    f"-a <({fix_bed()}) "
    f"-b <(sort -k1,1 -k2,2n {sys.argv[1]}) "
    f"-sorted -u > {paths['res_raw']}"
)

# dedup через sort (НЕ awk!)
run(f"sort -k4,4 {paths['res_raw']} | uniq > {paths['res_uniq']}")

# ── 2. GC coords ─────────────────────────────────

sum_len = 0
last_a = 0

with open(sys.argv[2]) as inp, open(paths["gccoords"], "w") as out:
    for line in inp:
        p = line.split()
        last_a = p[6]
        start, end = int(p[7][1:-1]), int(p[8][:-1])
        sum_len += end - start
        out.write(f"chr{CHR}\t{start}\t{end}\n")

# ── 3. chunked intersect ─────────────────────────

def intersect_chunked(b_file, out_file):
    tmp = f"{BASE}/intmut/tmp_{CHR}"
    os.makedirs(tmp, exist_ok=True)

    chunks = []
    i = 0
    n = 0
    chunk_path = f"{tmp}/c{i}.bed"
    cur = open(chunk_path, "w")

    # режем на чанки
    with open(b_file) as f:
        for line in f:
            cur.write(line)
            n += 1
            if n >= CHUNK:
                cur.close()
                chunks.append(chunk_path)
                i += 1
                chunk_path = f"{tmp}/c{i}.bed"
                cur = open(chunk_path, "w")
                n = 0

    cur.close()
    if n > 0:
        chunks.append(chunk_path)
    else:
        os.remove(chunk_path)

    raw = out_file + ".raw"

    # пишем сразу в файл (без PIPE!)
    with open(raw, "w") as out:
        for c in chunks:
            subprocess.run(
                f"bedtools intersect -a <({fix_bed()}) -b {c} -u",
                shell=True,
                executable="/bin/bash",
                stdout=out,
                check=True
            )

    # dedup безопасный
    run(f"sort -k4,4 {raw} | uniq > {out_file}")

    os.remove(raw)
    shutil.rmtree(tmp, ignore_errors=True)


intersect_chunked(paths["gccoords"], paths["intmut"])

# ── 4. stats ─────────────────────────────────────

d1 = count_lines(paths["intmut"])
d2 = count_lines(paths["res_uniq"])
d6 = count_lines(sys.argv[1])

d4 = 0
with open(sys.argv[1]) as f:
    for line in f:
        p = line.split()
        d4 += int(p[2]) - int(p[1])

# ── 5. output ────────────────────────────────────

with open(sys.argv[4], "a") as out:
    dens_non_g4 = 0 if sum_len == 0 else d1 / sum_len
    dens_g4 = d2 / d4

    out.write(
        f"chr{CHR}\tnon G4 motif\taverage density\t{dens_non_g4}\t"
        f"average G4 motif/interval length\t{last_a}\n"
    )

    out.write(
        f"chr{CHR}\tG4 motif all\taverage density\t{dens_g4}\t"
        f"average G4 motif/interval length\t{d4/d6}\n"
    )

with open("test_quadr.txt", "a") as f:
    f.write(f"{CHR}\t{d2}\t{d4}\n")
