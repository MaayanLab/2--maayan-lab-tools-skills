---
name: Geneshot
description: >
  .
license: Apache-2.0 (software)
---

# Geneshot

## Overview



## When to Use This Skill

## Core Capabilities

### 1. Retrieve PubMed IDs associated with gene

Returns PubMed metadata on input gene

**Parameters**
- gene (gene symbol)
- rif (generif or autorif)
- term (search term)

**Example code**

```python
import json
import requests

GENESHOT_URL = 'https://maayanlab.cloud/geneshot/api/genepublications'
payload = {"gene": "FOXM1", "rif": "autorif", "term": "cell cycle"}

response = requests.post(GENESHOT_URL, json=payload)

data = json.loads(response.text)
print(data)
```

**Example output**

```python
{
  "PubMed_date": {
    "11971982": "2002-04-25",
    "11971982": "2002-04-25",
    "11971982": "2002-04-25",
    ...
  },
  "filtered_pmid": {
    "11971982": "2002-04-25",
    "11971982": "2002-04-25",
    "11971982": "2002-04-25",
    ...
  }
  "search_term": "wound healing",
  "count_pmid": 7231,
  "count_filtered_pmid": 123
}
```

### 2. Retrieve genes associated with search terms

**Parameter**
- term (search term)

**Example code**

```python
import json
import requests

GENESHOT_URL = 'https://maayanlab.cloud/geneshot/api/search'
payload = {"rif": "generif", "term": "hair loss"}

response = requests.post(GENESHOT_URL, json=payload)

data = json.loads(response.text)
print(data)
```

**Example output**

```python
{
  "PubMedID_count": 34412,
  "gene_count": {
      "ABCC6P2": [
          1,
          0.25
      ],
      "ABI3": [
          2,
          0.125
      ],
      ...
    },
    "query_time": 1.121943712234497,
    "return_size": 298,
    "search_term": "hair loss"
}
```

### 3. Retrieve publications counts for matching gene

Returns PubMed publications counts in semiannual intervals for genes relevant to input search term.

**Parameters**
- gene (gene symbol)
- rif (generif or autorif)
- term (search term)
	
**Example code**

```python
import json
import requests

GENESHOT_URL = 'https://maayanlab.cloud/geneshot/api/histogram'
payload = {"rif": "autorif", "gene": "MYO7A", "term": "hair loss"}

response = requests.post(GENESHOT_URL, json=payload)

data = json.loads(response.text)
print(data)
```

**Example output**

```python
{
  "filtered_pmid": {
    "1992-12": 0,
    "1994-6": 0,
    "1995-12": 1,
    ...
  },
  "gene": "MYO7A",
  "pubmed_date": {
    "1992-12": 1,
    "1994-6": 2,
    "1995-12": 2,
    ...
  },
  "search_term": "hair loss"
}
```

### 4. Predict associated genes

Returns predictions for associated genes using gene-gene similarity. 

**Parameters:**
- similarity (gene-gene similarity matrix, options are: generif, tagger, autorif, coexpression, enrichr)
- gene symbols (comma separated)

**Example code**

```python
import json
import requests

GENESHOT_URL = 'https://maayanlab.cloud/geneshot/api/associate'
payload = {
  "gene_list": ["CRP","IL6","TNF","IL1B","TAC1","ALB","CALCA","TRPV1","INS","NGF","PTGS2","FOS","POMC","IL10","CD4","BDNF","ATP4A","ATP12A","ACE","CXCL8","GPT","OPRM1","TRPA1","GAPDH","F2","PTH","CCL2","CD34","CNR1","AKT1","F3","KLK3","OXT","SST","IL2","TLR4","CD8A","AFP","SCN9A","IL4","SCN10A","CEACAM5","NTRK1","KIT","AIF1","JUN"],
  "similarity": "coexpression" 
}
response = requests.post(GENESHOT_URL, json=payload)

data = json.loads(response.text)
print(data)
```

**Example output**

```python
{
"association": {
    "A1CF": {
        "publications": 126,
        "simScore": 0.05238375919205802,
        "topGenes": {
            "0": "ALB",
            "1": "F2",
            ...
        },
        "topScores": {
            "0": 0.8976537585258484,
            "1": 0.8907041549682617, 
            ...
        }
    },
    ... 
},
"darkgpcr": [],
"darkionchannel": [
    "SLC26A1"
],
"darkkinase": [],
"gpcr": [],
"ionchannel": [
    "SLC26A1",
    "SCN10A",
    "SCN11A",
    "KCNK18"
],
"kinase": [
    "DGKH",
    "KHK"
],
"query_time": 2.161868095397949
}
```

### 5. Predict gene function

**Parameters:**
- gene (gene symbol)
- similarity (gene-gene similarity matrix, options are: generif, tagger, autorif, coexpression, enrichr)
- library (gene-set library)
- offset
- limit

**Returns:**
- tpcount (total true positives for gene in library)
- auc (area under ROC curve)
- total (library size)
- tprank (rank of all true positives)
- tpkey (list of dark ionchannel associated to input list)
- results (library term predictions ranked by significance)

**Example code**

```python
import json
import requests

GENESHOT_URL = 'https://maayanlab.cloud/geneshot/api/predict'

payload = {
  "gene": "FOXM1",
  "library": "WikiPathways_2016",
  "similarity": "coexpression",
  "offset": 0,
  "limit": 200
}

response = requests.post(GENESHOT_URL, json=payload)

data = json.loads(response.text)
print(data)
```

**Example output**

```python
{
  "tpcount": 60,
  "auc" : 0.7204209328782708,
  "total" : 293,
  "tprank" : [
    0 : 3,
    1 : 6,
    2 : 8,
    3 : 12,
    ...
  ],
  "tpkey" : {
    0 : "Dorso-ventral axis formation_Homo sapiens_hsa04320",
    1 : "Thyroid cancer_Homo sapiens_hsa05216",
    2 : "Long-term depression_Homo sapiens_hsa04730",
    ...
  },
  "results" : {
    0 : {
      "property" : "Nicotine addiction_Homo sapiens_hsa05033",
      "score" : 4.0014677,
      "tp" : 0
    },
    1 : {
      "property" : "Butirosin and neomycin biosynthesis_Homo sapiens_hsa00524",
      "score" : 2.922457,
      "tp" : 0
    },
    3 : {
      "property" : "Dorso-ventral axis formation_Homo sapiens_hsa04320",
      "score" : 2.539165,
      "tp" : 1
    },
    ...
  }
}
```

## Additional Resources
- Geneshot website: https://maayanlab.cloud/geneshot/help.html
- Requests library: https://pypi.org/project/requests/

## Citations
Alexander Lachmann, Brian M. Schilder, Megan L. Wojciechowicz, Denis Torre, Maxim V. Kuleshov, Alexandra B. Keenan, and Avi Ma’ayan
Nucleic Acids Research, gkz393, https://doi.org/10.1093/nar/gkz393
Volume 47, Issue W1, 02 July 2019, Pages W571–W577