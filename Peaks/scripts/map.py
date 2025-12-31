op = open("../sorted/quadr7_chain180424_merged2_sorted_39.bed","r")
list1 = []
for line in op:
    line = line.strip()
    line = line.split()
    a = int(line[2])-int(line[1])
    list1.append(a)

op.close()
print(min(list1))
print(max(list1))
