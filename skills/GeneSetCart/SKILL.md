---
name: GeneSetCart
description: >
  Gene set assembly and analysis workspace. Used for managing gene sets from Common Fund Data Ecosystem (CFDE) resources and user-inputted gene lists. Also provides visualizations, gene set operations, and gene set augmentation.
license: GPL-3.0
---

# GeneSetCart

## Overview

GeneSetCart is an interactive platform for assembling, managing, and analyzing gene sets from Common Fund Data Ecosystem (CFDE) resources and user-provided gene lists.

Users can search and collect gene sets from multiple biomedical resources, upload custom gene sets, augment them with gene-gene co-expression or protein-protein interactions, perform set operations, generate publication-ready visualizations, and export assembled gene sets for downstream analysis.

GeneSetCart also integrates with external enrichment tools including Enrichr, ChEA3, KEA3, CFDE-GSE, Rummagene, and RummaGEO.

The primary capabilities include:

**Gene Set Search**
Search gene sets from CFDE libraries using biomedical terms.

**Gene Set Assembly**
Create collections of gene sets from public resources or uploaded gene lists.

**Gene Set Operations**
Perform union, intersection, consensus, and overlap analysis across multiple gene sets.

**Visualization**
Generate Venn diagrams, UpSet plots, SuperVenn diagrams, heatmaps, and UMAP visualizations.

**Gene Set Augmentation**
Expand gene sets using gene co-expression or protein-protein interaction networks.


## When to Use This Skill

- searching CFDE gene set libraries by biomedical concepts or disease terms
- assembling gene sets from multiple experimental and computational sources
- augmenting gene sets or performing gene set operations
- comparing gene sets with overlap and similarity visualizations
- exporting gene sets for downstream enrichment and signature analysis
- saving and sharing gene set collections for reproducible analyses


## Core Capabilities

Below are the available APIs and example codes for Gene Set Cart.

### Uploading gene sets

1. Upload single custom gene set

**Parameters:**
- term (string)
- genes (array)
- description (string)
- validate (boolean)

```python
import requests

payload = {
    "term": "Example Gene Set",
    "genes": ["TP53", "EGFR", "MYC"],
    "description": "Example upload",
    "validate": True
}

response = requests.post(
    "https://genesetcart.cfde.cloud/api/addUserGeneset",
    json=payload
)

print(response.json())
```

2. Upload multiple gene sets

**Parameters:**
- term (string)
- genes (array)
- description (string)

```python
import requests

payload = [
  {
    "term": "test set 1",
    "genes": [
      "FAM83E",
      "TJP3",
      "HEPACAM2",
      "GCNT3",
      "NXPE2",
      "LRRC31"
    ],
    "description": "First gene set"
  },
  {
    "term": "test set 2",
    "genes": [
      "ACTB",
      "ACTG1",
      "ADAR",
      "PARP1",
      "FAM83E",
      "AGXT",
      "ALDOA"
    ],
    "description": "Second gene set"
  }
]

response = requests.post(
    "https://genesetcart.cfde.cloud/api/addMultipleGenesets",
    json=payload
)

print(response.json())
```


## Additional Resources
- GeneSetCart website: https://genesetcart.cfde.cloud/about
- Requests library documentation: https://pypi.org/project/requests/

## Citations
Marino GB, Olaiya S, Evangelista JE, Clarke DJB, Ma'ayan A. GeneSetCart: assembling, augmenting, combining, visualizing, and analyzing gene sets. Gigascience. 2025 Jan 6;14:giaf025. doi: 10.1093/gigascience/giaf025.