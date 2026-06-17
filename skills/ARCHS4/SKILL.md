---
name: ARCHS4
description: >
    All RNA-seq sample and signature search (ARCHS4). Used for providing access to gene counts for human and mouse experiments and gene expression analysis.
license: Apache-2.0 (software); CC-BY-4.0 (data)
---

# ARCHS4

## Overview
All RNA-seq sample and signature search (ARCHS4) provides access to gene and transcript counts processed from all human and mouse RNA-seq experiments from the Gene Expression Omnibus (GEO) and the Sequence Read Archive (SRA). ARCHS4 database now includes 35000 samples from additional species, such as C. elegans and Drosophila melanogaster. 
Supports human and mouse gene expression and sample-level queries. Features 3 main search tools.

**Metadata Search:**
Search samples by tissue or condition metadata from GEO.

**Signature Search:**
Find matching samples using up/down gene signatures. Gene expression is z-score normalized across samples to identify relative gene expression.

**Gene Search:**
Retrieve gene-level expression profiles and functional predictions for input Entrez gene symbol. Landing page provides Pearson correlation and tissue and cell line expression atlas. High z-score means high correlation.


## When to Use This Skill & Its Capabilities
- querying and analyzing gene expression across large human and mouse RNA-seq datasets  
- searching GEO-derived samples by tissue, disease, or other metadata  
- performing gene-level analysis (correlation, differential expression, and k-NN similarity search)
- exploring tissue and cell line expression patterns across heterogeneous datasets


## API Documentation

Most data interactions are served via public APIs. For larger queries resort to ARCHS4 Python or R packages (see installation above for archs4py).

### Quick Search Metadata

**Parameters**
- query (search term)
- species (optional, defaults to "human")

**Example code**

```python
import requests

url = "https://maayanlab.cloud/sigpy/meta/quicksearch?query=%s&species=human"
term = "kidney"

response = requests.get(url % (term)
    )

response.raise_for_status()
samples = response.json()
print(samples)
```

### List Genes (Metadata)

**Parameters**
- species (option, via query or JSON body, defaults to "human")

**Returns:** list of all gene symbols available

**Example code (GET)**
```python
import requests

response = requests.get(
    "https://maayanlab.cloud/sigpy/meta/genes",
    params={"species": "human"}
)

response.raise_for_status()

genes = response.json()
print(genes)
```

**Example code (POST)**
```python
import requests

response = requests.post(
    "https://maayanlab.cloud/sigpy/meta/genes",
    json={"species": "mouse"}
)

response.raise_for_status()

genes = response.json()
print(genes)
```

### Request Sample Data

**Parameters (GET)**
- comma-separated list of sample GSM IDs
- species

**Example code (GET)**
```python
import requests

response = requests.get(
    "https://maayanlab.cloud/sigpy/data/samples",
    params={
        "gsm_ids": "GSM1335489,GSM1342284",
        "species": "human"
    }
)

response.raise_for_status()

print(response.json())
```

**Parameters (POST)**
- gsm_ids (array of GSM IDs)
- species (options: "human" (default), "mouse)

Note: maximum allowed samples is 10,000.

**Example code (POST)**
```python
import requests

data = {
    "gsm_ids": ["GSM1335489", "GSM1342284"],
    "species": "human"
}

response = requests.post(
    "https://maayanlab.cloud/sigpy/data/samples",
    json=data
)

response.raise_for_status()

print(response.json())
```

### Check Task Status for Sample Data Request
Checks download task status for previous samples request

**Example code**
```python
import requests

task_id = "your_task_id_here"
url = f"https://maayanlab.cloud/sigpy/data/samples/status/{task_id}"
response = requests.get(url)
print(response.json())
```

### Download Sample Data Zip
Once processing complete, use this endpoint to download the generated ZIP file containing the data.

**Example code**
```python
import requests

task_id = "your_task_id_here"
url = f"https://maayanlab.cloud/sigpy/data/samples/download/{task_id}"
response = requests.get(url)
with open("matrix.zip", "wb") as f:
    f.write(response.content)
print("File downloaded as matrix.zip")
```

### k-NN Signature Query

Can be performed either using gene expression profile (gene counts) or marker genes (up genes for characteristically upregulated, down genes for characteristically down regulated. Down genes can be left blank).

**Parameters**
- signatures (input signature vector)
- species ("human" or "mouse")
- signame (name identifier for signature)
- k (number of nearest neighbors to return, defaults to 10)

**Example code for up/down gene set**
```python
import requests

payload = {
  "signatures": [
    {
      "up_genes": [
        "XGY2",
        "HBA1",
        "CA3",
        ...
      ],
      "down_genes": [
        "NRBP2",
        "ASAH2B",
        "PPIL6",
        ...
      ]
    }
  ],
  "species": "human",
  "k": 500,
  "signame": "Example similarity search"
}

url = "https://maayanlab.cloud/sigpy/data/knn/signature"
response = requests.post(url, json=payload)
```

**Example code for full gene expression profile**
```python
import requests

payload = {
  "signatures": [
    {
      "genes": [
        "XGY2",
        "HBA1",
        "CA3",
        ...
      ],
      "values": [
        421215,
        965,
        12349,
        ...
      ]
    }
  ],
  "species": "human",
  "k": 500,
  "signame": "Example similarity search"
}

url = "https://maayanlab.cloud/sigpy/data/knn/signature"
response = requests.post(url, json=payload)
```

**Example output**
```python
{
    "distances": [
        -0.5242219944566326,
        -0.513229216535615,
        -0.5111980232411404,
        ...
    ],
    "indexes": [
        793578,
        531388,
        572691,
        ...
    ],
    "samples": [
        "GSM7092078",
        "GSM5211863",
        "GSM5397753",
        ...
    ],
    "series_count": 130,
    "signame": "Example similarity search",
    "species": "human"
}
```

### Gene Correlation Analysis
**Parameters**
- gene (gene symbol to examine)
- meta (metadata/filter criteria)
- species ("human" (default) or "mouse")
- k (optional, number of correlations to return)

**Example code**
```python
import requests

url = "https://maayanlab.cloud/sigpy/data/correlation"

payload = {
    "gene": "PCSK9",
    "species": "human",
    "meta": "keratinocyte"
}

response = requests.post(url, json=payload)
response.json()
```

**Example output**
```python
{
 'gene': 'PCSK9',
 'mean_log_expression': 10.248437881469727,
 'negative_correlated_genes': [
  {'correlation': -0.5214786152955715,
   'gene': 'ENSG00000287180',
   'mean_log_expression': 1.1113303899765015
  },
  {
   'correlation': -0.5077861735543857,
   'gene': 'SLA',
   'mean_log_expression': 0.9335980415344238
  },
 ...],
 'positive_correlated_genes': [
  {
   'correlation': 0.6705970458859031,
   'gene': 'ARTN',
   'mean_log_expression': 8.389211654663086
  },
  {
   'correlation': 0.6586166071822823,
   'gene': 'ITGB4',
   'mean_log_expression': 13.432361602783203
  },
 ...],
 'samples': [
    'GSM1432456',
    'GSM1432458',
    'GSM1446887',
    'GSM1716887',
    ...
  ],
 'searchterm': 'keratinocyte'
}
```

### Differential Expression
**Parameters**
- gene (gene for which to check differential expression)
- meta (metadata/filter criteria)
- species ("human" (default) or "mouse")
- fdr_cutoff (false discovery rate threshold, defaults to 0.1)

**Example code**
```python
import requests

url = "https://maayanlab.cloud/sigpy/data/diffexp"

payload = {
    "gene": "TP53",
    "meta": "keratinocyte",
    "species": "human",
    "fdr_cutoff": 0.1
}

response = requests.post(url, json=payload)
response.raise_for_status()

results = response.json()
print(results)
```

## Additional Resources
- ARCHS4 use in Python (archs4py) documentation: https://github.com/MaayanLab/archs4py
- Requests library documentation: https://pypi.org/project/requests/
- Website documentation: https://archs4.org/help


## Citations
Lachmann A, Torre D, Keenan AB, Jagodnik KM, Lee HJ, Wang L, Silverstein MC, Ma’ayan A. Massive mining of publicly available RNA-seq data from human and mouse. Nature Communications 9. Article number: 1366 (2018), doi:10.1038/s41467-018-03751-6