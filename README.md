The project is dedicated to calculating the density in G-quadruplex and interquadruplex regions.
In the "Peaks" folder, there are peak-extraction and quadruplex-making scripts (Python scripts and Snakemake); in the "Density" folder, we calculate control regions and then compare mutational density.
Mutations are from COSMIC and dbSNP; they are calculated for plus and minus strands.
The data were taken from GSE110582 (samples GSM3003539 and GSM3003540, e.g., the human HEK-293T cell line with or without PDS).
"39" or "40" in the script means this file is for GSM3003539 or for GSM3003540.
Snakefiles use scripts in the "scripts" folder.
There are some controls indicated in the script or Snakemake file names in the "Density" folder. <br>
FINAL are the scripts prepared for the paper.

