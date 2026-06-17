import sys
import gzip

def sum_interval_lengths(filepath):
    total = 0
    try:
        opener = gzip.open if filepath.endswith('.gz') else open
        with opener(filepath, 'rt') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                total += int(parts[2]) - int(parts[1])
    except FileNotFoundError:
        print(f"WARNING: file not found: {filepath}", file=sys.stderr)
    return total

b_pattern        = "/data/nooroka/grant/punkt1/stage2/merged/quadr7_chain180424_merged2_sorted_{}_39.bed"
gccoords_pattern = "/data/nooroka/grant/punkt3/stage2/gccoords/def/gccoords_{}2defhg19_40_all_loop7_control3_no_gc.bed.gz"

total_gccoords = 0
total_b        = 0

for i in range(1, 25):
    gccoords_file = gccoords_pattern.format(i)
    b_file        = b_pattern.format(i)

    gc_len = sum_interval_lengths(gccoords_file)
    b_len  = sum_interval_lengths(b_file)

    print(f"chr{i}: gccoords={gc_len}, b={b_len}")

    total_gccoords += gc_len
    total_b        += b_len

print(f"\nРезультат:")
print(f"Сумма длин интервалов gccoords (все хромосомы): {total_gccoords}")
print(f"Сумма длин интервалов -b файлов (все хромосомы): {total_b}")
