import sys
from Bio import SeqIO

def gc_content(seq):
    seq = seq.upper()
    gc = seq.count('G') + seq.count('C')
    return gc / len(seq) * 100 if len(seq) > 0 else 0

def parse_fasta_key(header):
    """Парсит заголовок FASTA в ключ (chr, start, end)."""
    header = header.strip()
    # Формат: chr:start-end
    if ':' in header and '-' in header:
        chrom, rest = header.split(':', 1)
        start, end = rest.split('-', 1)
    # Формат: chr_start_end
    else:
        return None
    return (chrom.strip(), int(start.strip()), int(end.strip()))
def main(bed_file, fasta_file, out_bed, out_fasta, gc_threshold=50.0):
    # Загрузка FASTA: ключ -> SeqRecord
    fasta_dict = {}
    for record in SeqIO.parse(fasta_file, "fasta"):
        key = parse_fasta_key(record.id)
        if key:
            fasta_dict[key] = record

    passed_records = []
    passed_bed_lines = []

    with open(bed_file) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            fields = line.strip().split('\t')
            chrom, start, end = fields[0], int(fields[1]), int(fields[2])
            key = (chrom, start, end)

            if key not in fasta_dict:
                print(f"Предупреждение: не найдена запись в FASTA для {key}", file=sys.stderr)
                continue

            seq = str(fasta_dict[key].seq)
            if gc_content(seq) >= gc_threshold:
                passed_bed_lines.append(line)
                passed_records.append(fasta_dict[key])

    # Запись результатов
    with open(out_bed, 'w') as f:
        f.writelines(passed_bed_lines)

    SeqIO.write(passed_records, out_fasta, "fasta")

    print(f"Прошло фильтрацию: {len(passed_bed_lines)} квадруплексов из {len(passed_bed_lines) + (len(fasta_dict) - len(passed_bed_lines))} записей FASTA")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Использование: python filter_gc.py input.bed input.fasta output.bed output.fasta [gc_threshold]")
        sys.exit(1)

    bed_in   = sys.argv[1]
    fasta_in = sys.argv[2]
    bed_out  = sys.argv[3]
    fasta_out = sys.argv[4]
    threshold = float(sys.argv[5]) if len(sys.argv) > 5 else 50.0

    main(bed_in, fasta_in, bed_out, fasta_out, threshold)
