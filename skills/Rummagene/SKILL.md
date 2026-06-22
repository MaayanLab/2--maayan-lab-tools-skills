---
name: Rummagene
description: >
    Gene set search tool. Used for finding human and mouse gene sets by extracting from PubMed Central (PMC) publications.
license: CC-BY-NC-SA-4.0
---

# Rummagene

## Overview

Rummagene is a gene set database built from open access PubMed Central (PMC) articles. Extracts human and mouse gene sets for users.

Features 3 search functions. Users can either submit own gene sets to find overlapping gene sets or query through PMC papers and extracted table titles for gene sets.

All data is accessible via a GraphQL API.


## When to Use This Skill
- identify gene sets for transcription factor / kinase / pathway enrichment
- retrieve gene sets from relevant PMC studies or tables with specific title terms
- search gene sets by experimental description or keywords
- predictions of cell types for single cell RNA-seq data
- gene function predictions
- find unexpected relationships by combining gene set similarity with abstract similarity


## Core Capabilities

Rummagene uses GraphQL API with three main query modes:

1. Gene Set Search (enrichment)
2. PMC Search (articles)
3. Table Title Search (tables)


### Gene Set Search

Finds statistically similar gene sets and the PMC article they are extracted from.
Example code below.

**Run enrichment search**

```python
import requests

URL = "https://rummagene.com/graphql"

genes = ["STAT3"]

query = """
query EnrichmentQuery($genes: [String]!, $filterTerm: String = "", $offset: Int = 0, $first: Int = 10) {
  currentBackground {
    enrich(
      genes: $genes,
      filterTerm: $filterTerm,
      offset: $offset,
      first: $first
    ) {
      totalCount
      nodes {
        geneSetHash
        pvalue
        adjPvalue
        oddsRatio
        nOverlap

        geneSets {
          nodes {
            id
            term
            description
            nGeneIds

            geneSetPmcsById(first: 1) {
              nodes {
                pmcInfoByPmcid {
                  pmcid
                  title
                  yr
                  doi
                }
              }
            }
          }
        }
      }
    }
  }
}
"""

payload = {
    "operationName": "EnrichmentQuery",
    "query": query,
    "variables": {
        "genes": genes,
        "filterTerm": "",
        "offset": 0,
        "first": 10
    }
}

response = requests.post(URL, json=payload)
response.raise_for_status()

data = response.json()["data"]["currentBackground"]["enrich"]["nodes"]

for hit in data:
    gene_set = hit["geneSets"]["nodes"][0]

    print("\n==============================")
    print("Gene Set:", gene_set["term"])
    print("ID:", gene_set["id"])
    print("Overlap:", hit["nOverlap"])
    print("P-value:", hit["pvalue"])
    print("Odds Ratio:", hit["oddsRatio"])

    pmc_nodes = gene_set["geneSetPmcsById"]["nodes"]

    if pmc_nodes:
        pmc = pmc_nodes[0]["pmcInfoByPmcid"]
        print("PMC:", pmc["pmcid"])
        print("Title:", pmc["title"])
        print("Year:", pmc.get("yr"))
```


### PMC Search

First retrieves PMC IDs, then searches for associated gene sets. Finally, uses view gene set to examine gene set.
Example codes below.

**1. Retrieve PMC IDs**
```python
import requests

search_term = "type 2 diabetes"

response = requests.get(
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
    params={
        "db": "pmc",
        "term": search_term,
        "sort": "relevance",
        "retmode": "json",
        "retmax": 100
    }
)

response.raise_for_status()

pmcids = [
    f"PMC{pmcid}"
    for pmcid in response.json()["esearchresult"]["idlist"]
]

print(f"Found {len(pmcids)} PMC articles")
print(pmcids[:10])
```

**2. Query for associated gene sets**
```python
import requests

RUMMAGENE_URL = "https://rummagene.com/graphql"

pmcids = [
    "PMC8264408",
    "PMC6400201",
    "PMC7477520"
]

query = """
query TermsPmcs($pmcids: [String]!) {
  termsPmcsCount(pmcids: $pmcids) {
    nodes {
      pmc
      id
      term
      count
    }
  }
}
"""

response = requests.post(
    RUMMAGENE_URL,
    json={
        "operationName": "TermsPmcs",
        "query": query,
        "variables": {
            "pmcids": pmcids
        }
    }
)

response.raise_for_status()

results = response.json()["data"]["termsPmcsCount"]["nodes"]

for result in results[:10]:
    print(result)
```

**Example output for query**
```python
{
    "pmc": "PMC8264408",
    "id": "957bfb56-2209-42ce-8bfc-9a187f86c855",
    "term": "Differentially expressed genes in pancreatic islets",
    "count": 412
}
```

**3. Metadata for PMC articles**
```python
import requests

RUMMAGENE_URL = "https://rummagene.com/graphql"

pmcids = [
    "PMC10002095",
    "PMC10036033",
    "PMC10200926"
]

query = """
query GetPmcInfoByIds($pmcids: [String]!) {
  getPmcInfoByIds(pmcids: $pmcids) {
    nodes {
      pmcid
      title
      yr
      doi
    }
  }
}
"""

response = requests.post(
    RUMMAGENE_URL,
    json={
        "operationName": "GetPmcInfoByIds",
        "query": query,
        "variables": {
            "pmcids": pmcids
        }
    }
)

response.raise_for_status()

papers = response.json()["data"]["getPmcInfoByIds"]["nodes"]

for paper in papers:
    print(
        paper["pmcid"],
        paper["yr"],
        paper["title"]
    )
```



### Table Title Search

Find gene sets with experiments related to input term.
Example code below.

**Term search**
```python
import requests

URL = "https://rummagene.com/graphql"

payload = {
    "operationName": "TermSearch",
    "query": """
        query TermSearch(
            $terms: [String]!,
            $offset: Int = 0,
            $first: Int = 10
        ) {
            geneSetTermSearch(
                terms: $terms,
                offset: $offset,
                first: $first
            ) {
                nodes {
                    id
                    term
                    nGeneIds
                    __typename
                }
                totalCount
                __typename
            }
        }
    """,
    "variables": {
        "offset": 0,
        "first": 10000,
        "terms": ["neuron"]
    }
}

response = requests.post(URL, json=payload)
response.raise_for_status()

data = response.json()

print(f"Found {data['data']['geneSetTermSearch']['totalCount']} gene sets")

for result in data["data"]["geneSetTermSearch"]["nodes"][:10]:
    print(
        result["id"],
        result["term"],
        result["nGeneIds"]
    )
```

### View Gene Set

Should be performed at the end of each search to view retrieved gene set.
Example code below.


**View gene set**
```python
import requests

RUMMAGENE_URL = "https://rummagene.com/graphql"

gene_set_id = "957bfb56-2209-42ce-8bfc-9a187f86c855"

query = """
query ViewGeneSet($id: UUID!) {
  geneSet(id: $id) {
    genes {
      nodes {
        symbol
        ncbiGeneId
        description
        summary
      }
    }
  }
}
"""

response = requests.post(
    RUMMAGENE_URL,
    json={
        "operationName": "ViewGeneSet",
        "query": query,
        "variables": {
            "id": gene_set_id
        }
    }
)

response.raise_for_status()

genes = response.json()["data"]["geneSet"]["genes"]["nodes"]

for gene in genes[:20]:
    print(gene["symbol"])
```


## Additional Resources
- GraphQL Explorer: https://rummagene.com/graphiql
- Requests library: https://pypi.org/project/requests/

## Citations
Clarke, D. J. B., Marino, G. B., Deng, E. Z., Xie, Z., Evangelista, J. E. & Ma'ayan, A. Rummagene: massive mining of gene sets from supporting materials of biomedical research publications. Commun Biol 7, (2024). https://doi.org/10.1038/s42003-024-06177-7