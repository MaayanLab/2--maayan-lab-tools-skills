---
name: ChEA3
description: >
    Transcription factors enrichment analysis (TFEA) tool. Used for predicting transcription factors responsible for changes in gene expression or identifying common regulators.
license: CC BY-NC-SA 4.0
---

# ChEA3

## Overview

ChEA3 aids in identifying the transcription factors (TFs) responsible for observed changes in gene expression when comparing control and perturbation samples. It does this by comparing input gene set to libraries of TF target gene sets, using Fisher's Exact Test to determine which TFs are most closely associated.

ChEA3 accepts HGNC-approved gene symbols as inputs.
Returns are sorted by Fisher's Exact Test p-value. Lower scores indicate more relevancy.

## When to Use This Skill

- users present an input gene set in HGNC-approved format
- users would like to identify TFs responsible for changes in gene expression (TFEA)
- users present inputs from GWAS studies or whole-genome CRISPR-KO screen hits to identify common regulators


## Installation

When running on Python, needs requests library. To install, run in terminal:

```bash
$ python -m pip install requests
```

## Core Capabilities

Queries all ChEA3 TF target library database for TFs associated with input set of genes.


**Parameters**
- query_name (string)
- gene_set (array of strings)

**Returns:** JSON file of ChEA3 library result objects

**Example code**

```python
import requests
import json

url = "https://maayanlab.cloud/chea3/api/enrich/"

genes = [
    "KIAA0907", "KDM5A", "CDC25A", "EGR1", "GADD45B", "RELB", "TERF2IP", "SMNDC1", "TICAM1", "NFKB2", "RGS2", "NCOA3", "ICAM1", "TEX10", "CNOT4", "ARID4B", "CLPX", "CHIC2", "CXCL2", "FBXO11", "MTF2", "CDK2", "DNTTIP2", "GADD45A", "GOLT1B", "POLR2K", "NFKBIE", "GABPB1", "ECD", "PHKG2", "RAD9A", "NET1", "KIAA0753", "EZH2", "NRAS", "ATP6V0B", "CDK7", "CCNH", "SENP6", "TIPARP", "FOS", "ARPP19", "TFAP2A", "KDM5B", "NPC1", "TP53BP2", "NUSAP1", "SCCPDH", "KIF20A", "FZD7", "USP22", "PIP4K2B", "CRYZ", "GNB5", "EIF4EBP1", "PHGDH", "RRAGA", "SLC25A46", "RPA1", "HADH", "DAG1", "RPIA", "P4HA2", "MACF1", "TMEM97", "MPZL1", "PSMG1", "PLK1", "SLC37A4", "GLRX", "CBR3", "PRSS23", "NUDCD3", "CDC20", "KIAA0528", "NIPSNAP1", "TRAM2", "STUB1", "DERA", "MTHFD2", "BLVRA", "IARS2", "LIPA", "PGM1", "CNDP2", "BNIP3", "CTSL1", "CDC25B", "HSPA8", "EPRS", "PAX8", "SACM1L", "HOXA5", "TLE1", "PYGL", "TUBB6", "LOXL1"
]

payload = {
    "query_name": "myQuery",
    "gene_set": genes
}

response = requests.post(
    url,
    json=payload,
    headers={"Content-Type": "application/json"}
)

if not response.ok:
    raise Exception('Error querying results')

data = response.json()
with open("results.json", "w") as f:
    json.dump(data, f, indent=2)
```

## Additional Resources
Website: https://maayanlab.cloud/chea3/#top


## Citations
Keenan AB, Torre D, Lachmann A, Leong AK, Wojciechowicz M, Utti V, Jagodnik K, Kropiwnicki E, Wang Z, Ma'ayan A (2019) ChEA3: transcription factor enrichment analysis by orthogonal omics integration. Nucleic Acids Research.
doi: 10.1093/nar/gkz446