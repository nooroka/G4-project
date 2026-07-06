
#!/bin/bash
bedtools subtract -a $1 -b  $2 > ../comp/temp.bed
bedtools getfasta  -fi  ../../hg19_new_rc.fna -bed ../comp/temp.bed  -fo $3

