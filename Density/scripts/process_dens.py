from collections import defaultdict
import os
def split_by_word(text, word):
    if word in text:
        parts = text.split(word, maxsplit=1)
        return [word, parts[1].strip()]
    return [text, ""]
for file1 in os.listdir("../densities3_final"):
    dict1 = defaultdict(list)
    op = open(f'../densities3_final/{file1}',"r")
    file_split = split_by_word(file1,"densities")
    #op = open("../densities_final/densities2GSM39_percent-1208_all_control1_minus.txt")
    for line in op:
        line = line.strip()
        line = line.split("\t")
        dict1[str(line[0])].append((line[3]))
    op.close()
    file2 = "../compare3/compare"+str(file_split[1])
    w = open(file2,"w")
    #w = open("../compare2/compareGSM39_percent-1208_all_control1_minus.txt","w")
    for key in dict1:
        w.write(str(dict1[key][1])+"\t"+str(dict1[key][0])+"\n")
    w.close()
