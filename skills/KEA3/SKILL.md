---
name: KEA3
description: >
    Kinase enrichment analysis tool (KEA3). Used for inferring upstream kinases with overrepresented putative substrates from input list of proteins or genes.
license: CC-BY-4.0
---

# KEA3

## Overview

Kinase Enrichment Analysis 3 (KEA3) is an enrichment analysis tool that identifies upstream kinases whose known or predicted substrates are significantly overrepresented in an input gene or protein list.

Users input list of proteins/genes or differentially phosphorylated proteins.

KEA3 compares these inputs against curated kinase-substrate gene set libraries constructed from publicly available interaction and phosphorylation datasets. Statistical significance of overlap is computed using Fisher’s Exact Test, followed by multiple testing correction.

The output is a ranked list of candidate kinases organized across multiple independent libraries.


## When to Use This Skill
- inferring upstream kinase activity from phosphoproteomics or protein/gene lists
- analyzing protein or gene lists to identify signaling regulators  
- prioritizing candidate kinases from experimental omics results  
- interpreting phosphorylation-based signaling changes across conditions  
- linking protein-level signatures to upstream regulatory mechanisms  


## Core Capabilities

Performs kinase enrichment analysis across all KEA3 libraries.

**Parameters**
- query_name (string)
- gene_set (array of strings)

**Returns:** JSON array of KEA3 library result objects

**Example code**
```python
import json
import requests

url = "https://maayanlab.cloud/kea3/api/enrich/"

payload = {
    "query_name": "myQuery",
    "gene_set": ["FOXM1", "SMAD9", "MYC", "SMAD3", "STAT1", "STAT3"]
}

response = requests.post(url, json=payload)

response.raise_for_status()

results = response.json()
print(results)
```

**Example results**
```python
[
  {
    "library_name": "KEGG",
    "kinases": [
      {
        "kinase": "MAPK1",
        "p_value": 0.00012,
        "adjusted_p_value": 0.0014,
        "overlap": 5,
        "substrates": ["SMAD3", "STAT1", "..."]
      }
    ]
  },
  {
    "library_name": "ChEA",
    "kinases": [
      {
        "kinase": "CDK1",
        "p_value": 0.0021,
        "adjusted_p_value": 0.01,
        "overlap": 4
      }
    ]
  }
]
```

## Additional Resources
- KEA3 libraries: https://maayanlab.cloud/kea3/templates/libraries.jsp
- Requests library installation documentation: https://pypi.org/project/requests/

## Citations
Maxim V Kuleshov, Zhuorui Xie, Alexandra B K London, Janice Yang, John Erol Evangelista, Alexander Lachmann, Ingrid Shu, Denis Torre, Avi Ma'ayan, KEA3: improved kinase enrichment analysis via data integration, Nucleic Acids Research, 2021; gkab359