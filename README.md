# G4-Mutation-Density

Pipelines and scripts for calculating **mutation density** in G-quadruplex regions and matched genomic controls, using variant data from **dbSNP** and **COSMIC**.

The repository is organized into two main components:

- **`DENSITY/`** — pipelines and scripts for computing mutation density across the genome, coding/non-coding regions, RNU and tRNA genes, and quadruplex/control regions, using dbSNP and COSMIC variant sets.
- **`OQs/`** — scripts for processing **Observed Quadruplexes (OQs)** data (G4-seq), including region extraction and preparation for downstream density calculations.

---

## 📖 Background

G-quadruplexes (G4s) are non-canonical secondary DNA structures formed in guanine-rich regions of the genome. This repository provides a computational framework to compare mutation density between:

- Experimentally **observed G-quadruplexes (OQs)**, detected by G4-seq
- Matched **genomic controls** (non-G4 regions)

Both quadruplexes and controls are further stratified by genomic context, including but not limited to:

| Category | Description |
|---|---|
| **Coding** | G4s / controls located within protein-coding regions |
| **Non-coding** | G4s / controls located within non-coding regions |
| **RNU genes** | Small nuclear RNA gene loci |
| **tRNA genes** | Transfer RNA gene loci |
| **Whole genome** | Genome-wide mutation density, independent of G4 status |

Mutation density is calculated separately using two variant databases:

- **dbSNP** — germline single nucleotide polymorphisms
- **COSMIC** — somatic mutations observed in cancer

## 🧬 G4-seq samples

Observed quadruplex regions are derived from two G4-seq datasets (Marsico *et al.*, 2019):

| Sample | GEO accession |
|---|---|
| Sample 1 | [GSM3003539](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM3003539) |
| Sample 2 | [GSM3003540](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM3003540) |

> Marsico, G., Chambers, V.S., Sahakyan, A.B. *et al.* Whole genome experimental maps of DNA G-quadruplexes in multiple species. *Nucleic Acids Research*, 2019. [doi:10.1093/nar/gkz179](https://doi.org/10.1093/nar/gkz179)

---

## 📂 Repository structure

```
.
├── DENSITY/     # Mutation density pipelines (dbSNP & COSMIC)
│   ├── ...      # scripts for genome-wide, coding/non-coding,
│   │            # RNU/tRNA and G4/control density calculations
│   └── ...
│
└── OQs/         # Observed Quadruplexes processing scripts
    ├── ...      # extraction, filtering and formatting of
    │            # G4-seq (GSM3003539 / GSM3003540) regions
    └── ...
```

## ⚙️ Workflow overview

1. **`OQs/`** — process raw G4-seq data for samples GSM3003539 and GSM3003540 to obtain observed quadruplex (OQ) coordinates, and generate matched non-G4 control regions.
2. **`DENSITY/`** — intersect OQ and control regions (including, among others, coding, non-coding, RNU, tRNA, and whole-genome intervals) with dbSNP and COSMIC variant sets, and compute mutation density for each category.

## 🚀 Requirements

- Python 3 / Bash
- [BEDTools](https://bedtools.readthedocs.io/)
- Standard genomic file formats: BED, VCF/GTF

*(see individual scripts for specific dependencies and input arguments)*

## 📐 Mutation density calculation

Mutation density is defined as **"interval mutation density"**:

1. Windows (control regions) or quadruplex regions are intersected with the mutation files (dbSNP / COSMIC).
2. The number of resulting lines (i.e., individual mutations falling within the intervals) is counted. Mutations are counted **per occurrence**, regardless of their length.
3. This count is divided by the **total summed length** of the corresponding windows or quadruplex regions.

```
mutation density = (number of mutations intersecting the intervals) / (total length of the intervals)
```

## 📊 Output

For each region category (genome-wide, coding, non-coding, RNU, tRNA, G4/control), the pipeline outputs interval mutation density values computed separately for dbSNP and COSMIC variants, enabling direct comparison between quadruplex and control regions.

## 📄 Citation

If you use this pipeline, please cite the G4-seq data source:

> Marsico, G. *et al.* (2019). Whole genome experimental maps of DNA G-quadruplexes in multiple species. *Nucleic Acids Research*, 47(8), 3862–3874.

---

*For questions or issues, please open an [issue](../../issues) in this repository.*
