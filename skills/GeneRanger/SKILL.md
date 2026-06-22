---
name: GeneRanger
description: >
    Centralized place for gene expression. Used for retrieving gene and protein expression data from several atlases with input human gene or transcript. 
license: CC-BY-SA-3.0
---

# GeneRanger

## Overview

GeneRanger provides access to processed gene and protein expression data across human tissues, cell types, and cell lines from multiple transcriptomics and proteomics atlases. Users can query expression profiles using a human gene symbol or transcript identifier.

## When to Use This Skill

* analyzing gene and protein expression across tissues, cell types, and cell lines
* identifying tissue- and cell-type-specific expression patterns
* comparing expression across transcriptomics and proteomics atlases
* retrieving gene- and transcript-level expression profiles
* supporting target discovery and biomarker evaluation

## Core Capabilities

**1. Query for processed data by gene and resource.**

If the "databases" property is not included in the request body, information from all available resources are returned.

Parameters:
- Human gene symbol (string)
- databases (array, optional)

**Example code**

```python
import requests

payload = { 
    "gene": "TP53" 
} 

response = requests.post( 
    "https://generanger.maayanlab.cloud/api/data", 
    json=payload 
) 
    
response.raise_for_status() 

print(response.json())
```

**Example output structure**
```python
{ 
    "allData": { 
        "gene": "TP53", 
        "dbData": {
            "ARCHS4": {...}, 
            "GTEx_transcriptomics": {...}, 
            "Tabula_Sapiens": {...}, 
            "CCLE_transcriptomics": {...}, 
            "HPM": {...}, 
            "HPA": {...}, 
            "GTEx_proteomics": {...}, 
            "CCLE_proteomics": {...} 
        }, 
        "NCBI_data": "Gene description..." } 
    }
```

**2. Query for all processed data relating to gene**

**Example code**
```python
import requests 

response = requests.get( 
    "https://generanger.maayanlab.cloud/api/data" 
) 

response.raise_for_status() 

results = response.json() 

print(results)
```

**3. Retrieve expression information for a specific transcript across available transcript-level resources**

Parameters:
- Ensembl transcript identifier (string)
- database (array, optional)

**Example code**
```python
import requests 

payload = { 
    "transcript": "ENST00000495442" 
} 

response = requests.post(
    "https://generanger.maayanlab.cloud/api/data_transcript", 
    json=payload 
) 

response.raise_for_status() 

print(response.json())
```

**Example output structure**
```python
{ 
    "allData": { 
        "gene": "ENST00000495442", 
        "dbData": { 
            "ARCHS4_transcript": {...}, 
            "GTEx_transcript": {...} 
        }, 
        "NCBI_data": "Transcript annotation..." 
    } 
}
```

## Supported Data Sources

### Transcriptomics

ARCHS4
- Uniformly processed RNA-seq profiles from over one million GEO and SRA samples.

GTEx Transcriptomics
- Bulk RNA-seq expression across 54 human tissues.

Tabula Sapiens
- Single-cell RNA-seq atlas containing hundreds of human cell types.

HubMAP
- Single-cell and spatial molecular atlas of healthy human tissues.

CCLE Transcriptomics
- RNA-seq expression profiles from more than 1,000 cancer cell lines.


### Proteomics

Human Proteome Map (HPM)
- Mass spectrometry-derived protein expression across human tissues.

Human Protein Atlas (HPA)
- Antibody-based protein expression profiling across normal human tissues.

GTEx Proteomics
- Tandem mass tag (TMT)-based proteomics across normal tissues.

CCLE Proteomics
- Protein expression profiles from hundreds of cancer cell lines.

## Additional Resources
- Website Documentation: https://generanger.maayanlab.cloud/api_documentation
- Requests library: https://pypi.org/project/requests/

## Citations
Marino GB, Ngai M, Clarke DJB, Fleishman RH, Deng EZ, Xie Z, Ahmed N, Ma’ayan A. GeneRanger and TargetRanger: processed gene and protein expression levels across cells and tissues for target discovery, Nucleic Acids Research, 2023; gkad399.