import sys
import re
import bisect
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction


def find_target_windows(seq, target, id2, writer):
    t = len(seq)
    if t == 0:
        return

    prefix = [0] * (t + 1)
    for idx, ch in enumerate(seq, start=1):
        prefix[idx] = prefix[idx - 1] + (0 if ch in "Nn" else 1)

    atgc_intervals = [(m.start(), m.end()) for m in re.finditer("[ATGCatgc]+", seq)] #list of islands
    starts = [iv[0] for iv in atgc_intervals]

    id2_offset = int(id2[0])
    k = 0
    while k < t:
        needed = prefix[k] + target
        i = bisect.bisect_left(prefix, needed, k + 1, t + 1)
        if i > t or prefix[i] < needed:
            break
        if i - k > 100000:
            break
        idx = bisect.bisect_right(starts, k) - 1 #define the position for collection of islands' coordinates
        if idx >= 0 and atgc_intervals[idx][1] > k:
            first_idx = idx
        else:
            first_idx = bisect.bisect_right(starts, k)

        int2 = []
        j = first_idx
        while j < len(atgc_intervals) and atgc_intervals[j][0] < i: #continue while island is somehow in the current window
            s, e = atgc_intervals[j]
            s_clip = max(s, k) #beginning of the island
            e_clip = min(e, i) #end of the island
            int2.append([s_clip + id2_offset, e_clip + id2_offset]) #add coordinates of islands
            j += 1

        window = seq[k:i]
        non_n = window.replace("N", "").replace("n", "")
        gc = gc_fraction(non_n, "remove")

        writer.write(
            "gc\t" + str(gc) + "\tseq\t" + non_n + "\t" +
            str(id2[0]) + "\t" + str(id2[1]) + "\t" +
            str(len(non_n)) + "\t" + str(int2) + "\n"
        )
        k = i


def main():
    fasta_path = sys.argv[1]
    target = int(sys.argv[2])
    out_path = sys.argv[3]

    with open(out_path, "w") as writer, open(fasta_path, "r") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            id1 = record.id.split(":")
            id2 = id1[1].split("-")
            find_target_windows(str(record.seq), target, id2, writer)


if __name__ == "__main__":
    main()
