#!/usr/bin/env python3
import sys
import pandas as pd

if len(sys.argv) < 2:
    print("Usage: python per_chrom_density.py input.bed [out.csv]")
    sys.exit(1)

inp = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else "per_chrom_density.csv"

# читаем без заголовка, любой разделитель пробел/табы
df = pd.read_csv(inp, sep=r"\s+", header=None, engine="python")

# count = 3rd from last, length = 2nd from last
count_col = df.columns[-3]
length_col = df.columns[-2]
chrom_col = df.columns[0]

df[count_col] = pd.to_numeric(df[count_col], errors='coerce').fillna(0)
df[length_col] = pd.to_numeric(df[length_col], errors='coerce').fillna(0)

grouped = df.groupby(chrom_col).agg(total_count=(count_col,'sum'), total_length_bp=(length_col,'sum')).reset_index()
grouped['density_per_kb'] = grouped.apply(
    lambda r: (r['total_count']*1000.0/r['total_length_bp']) if r['total_length_bp']>0 else 0.0, axis=1)

# сортируем естественно по хрому (chr1..chr22,chrX,chrY) если нужно:
def chrom_key(ch):
    ch = str(ch).lstrip('chr')
    if ch.isdigit(): return int(ch)
    if ch == 'X': return 1000
    if ch == 'Y': return 1001
    return 2000 + hash(ch)%1000

grouped['ck'] = grouped[chrom_col].map(chrom_key)
grouped = grouped.sort_values('ck').drop(columns=['ck'])

grouped.to_csv(out, index=False, float_format='%.10f',sep = "\t")
print("Wrote:", out)
print(grouped.to_string(index=False))
