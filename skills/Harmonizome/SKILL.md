---
name: Harmonizome
description: >
  Multi-omics data integration platform. Used for retrieving gene metadata, functional associations, gene sets, and datasets from a harmonized collection of datasets and literature. Provides knowledge graph visualization of biological relationships.
license: CC-BY-NC-SA-4.0
metadata:
  version: 3.0
---

# Harmonizome

## Overview

Harmonizome is a multi-omics data integration platform that aggregates and harmonizes 138 datasets from platforms across the web relating to information from genomics, proteomics, transcriptomics, metabolomics, and texts from biomedical literature. In doing so, Harmonizome provides users access to gene metadata, functional associations, gene sets, and datasets.

Knowledge graph relationships can be accesed through Harmonizome-KG API.

## When to Use This Skill

- retrieving integrated gene and protein knowledge from diverse biomedical resources
- exploring gene associations with pathways, phenotypes, diseases, and ontologies
- searching genes, gene sets, datasets, and resources
- analyzing functional relationships between genes and biological concepts
- exploring biological networks through a knowledge graph framework

## Core Capabilities

Harmonizome has 3 main features:
1. **entity type search:** (full list of entities, e.g. genes, gene sets, proteins)

2. **href search:** (in-depth retrieval of named, specified entity, e.g. NANOG, CHST8, AADAT_HUMAN)

3. **knowledge graph:** (via Harmonizome-KG API)

## API Documentation

### Entity Type Search

Returns the full list of entity type.

**Parameters:** 
- entity type
- cursor (optional)

Entity type can include:
- Attribute
- Dataset
- Gene
- Gene Set
- HGNC Family
- Naming Authority
- Protein
- Resource

Entity lists are paginated using a cursor. By default, the search will return first 100 entities. Cursor specifies a start index other than 0.


**Example code**

```python
import requests

entity_type = "gene"
cursor = 3141

response = requests.get(
    f"https://maayanlab.cloud/Harmonizome/api/1.0/{entity_type}",
    params={"cursor": cursor}
)

response.raise_for_status()

print(response.json())
```

**Example output**

```python
{
        "count": 58358,
        "selection": [3141, 3241],
        "next": "/api/1.0/gene?cursor=3241",
        "entities": [
            {
                "symbol": "MAP1LC3B2",
                "href": "/api/1.0/gene/MAP1LC3B2"
                },
                {
                    "symbol": "LACAT1",
                    "href": "/api/1.0/gene/LACAT1"
                },
                {
                    "symbol":"LGMN",
                    "href":"/api/1.0/gene/LGMN"
                },
                ...
            ]
    }    
```

Href property returned can be used in the URL to retrieve specific information for that entity.


### Href Search

Returns the specific information of a certain entity using its href.

**Parameters:**
- href property (entity)
- showAssociations (Boolean, only applicable for entity type gene or gene set)

If showAssociations is true, a list of associated entities is returned in addition to that entity’s base information. All associations have a threhsold value that measure the strength of the associations within a dataset or gene set. Unsigned and positive associations have a threshold value of 1, while negative associations have a threshold value of -1.

**Example code**
```python
import requests

gene = "NANOG"

response = requests.get(
    f"https://maayanlab.cloud/Harmonizome/api/1.0/gene/{gene}",
    params={"showAssociations": "true"}
)

response.raise_for_status()

print(response.json())
```

**Example output**
```python
{
            "symbol": "NANOG",
            "synonyms":[],
            "name": "Nanog homeobox",
            "description":"..."
            "ncbiEntrezGeneId": 79923,
            "ncbiEntrezGeneUrl": "http://www.ncbi.nlm.nih.gov/gene/79923",
            ...
            "associations": [
                {
                    "geneSet": {
                        "name": "V/Allen Brain Atlas Adult Human Brain Tissue Gene Expression Profiles",
                        "href": "/api/1.0/gene_set/V/Allen+Brain+Atlas+Adult+Human+Brain+Tissue+Gene+Expression+Profiles"
                    },
                    "thresholdValue": 1,
                    "standardizedValue": 1.33291
                },
                ...
            ]
        }
```

### Knowledge Graph

Harmonizome-KG, the knowledge graph visualization of Harmonizome, can be accessed via the URL: https://harmonizome-kg.maayanlab.cloud/api/knowledge_graph

**Parameters:**
```python
       {
            "start": "string",
            "start_field": "label",
            "start_term": "string",
            "end": "string",
            "end_field": "string",
            "end_term": "string",
            "limit": 5,
            "relation": [
              {
                "name": "string",
                "limit": 5,
              }
            ],
            "path_length": 1,
            "remove": [
              "string"
            ]
          }
```

Below are some examples of common queries using various example inputs.

**1. Single term search**

Returns a subnetwork containing the immediate neighbor of STAT3.

```python
import requests
import json

payload = {
    "start": "Gene", 
    # metadata field to query (default: label)
    "start_field": "label", 
    "start_term": "STAT3",
    "limit": 10
    
}

res = requests.get("https://harmonizome-kg.maayanlab.cloud/api/knowledge_graph", params={"filter": json.dumps(payload)})
if res.ok:
    results = res.json()
```

**2. Query only certain relationships**

Returns subnetwork containing STAT3's participation in GO Biological Process.

```python
import requests
import json

payload = {
    "start": "Gene", 
    # metadata field to query (default: label)
    "start_field": "label", 
    "start_term": "STAT3",
    "relation": [{
        "name": "participates_in_(GO Bio Process 2023)",
        "limit": 5
    }]
    
}

res = requests.get("https://harmonizome-kg.maayanlab.cloud/api/knowledge_graph", params={"filter": json.dumps(payload)})
if res.ok:
    results = res.json()
```

**3. Removing a node**

To remove a node:
```python
import requests
import json

payload = {
    "start": "Gene", 
    # metadata field to query (default: label)
    "start_field": "label", 
    "start_term": "STAT3",
    "relation": [{
        "name": "participates_in_(GO Bio Process 2023)",
        "limit": 5
    }],
    "remove": [
        "GO:0045944"
    ]
}

res = requests.get("https://harmonizome-kg.maayanlab.cloud/api/knowledge_graph", params={"filter": json.dumps(payload)})
if res.ok:
    results = res.json()
```

**4. Starting from a term and end with a node type**

Finds HPO nodes that are connected with the gene STAT3 via shortest path.

```python
import requests
import json

payload = {
    "start": "Gene", 
    "start_field": "label", 
    "start_term": "STAT3",
    "end": "HPO",
}

res = requests.get("https://harmonizome-kg.maayanlab.cloud/api/knowledge_graph", params={"filter": json.dumps(payload)})
if res.ok:
    results = res.json()
```

**5. Two term search**

Finds shortest path between STAT3 and MAPK1.

```python
import requests
import json

payload = {
    "start": "Gene", 
    "start_field": "label", 
    "start_term": "STAT3",
    "end": "Gene",
    "end_field": "label",
    "end_term": "MAPK1",
}

res = requests.get("https://harmonizome-kg.maayanlab.cloud/api/knowledge_graph", params={"filter": json.dumps(payload)})
if res.ok:
    results = res.json()
```


## Additional Resources
- Harmonizome documentation: https://maayanlab.cloud/Harmonizome/documentation
- Harmonizome-KG: https://harmonizome-kg.maayanlab.cloud/
- Requests library documentation: https://pypi.org/project/requests/

## Citations
- Diamant I, Clarke DJB, Evangelista JE, Lingam N, Ma'ayan A. Harmonizome 3.0: integrated knowledge about genes and proteins from diverse multi-omics resources. Nucleic Acids Res. 2024 Nov 20. pii: 53(1):D1016-D1028.
- Rouillard AD, Gundersen GW, Fernandez NF, Wang Z, Monteiro CD, McDermott MG, Ma'ayan A. The harmonizome: a collection of processed datasets gathered to serve and mine knowledge about genes and proteins. Database (Oxford). 2016 Jul 3;2016. pii: baw100.