---
name: Gene-Set-Foundation-Model
description: >
    Query the Gene Set Foundation Model (GSFM) website for gene function predictions, run live GSFM inference on custom gene sets, and run GSFM-based GSEA enrichment. Use when a user asks about predicted gene functions/associations, wants to look up what a model predicts for a gene, wants to submit a custom gene list for augmentation/inference, or wants to run enrichment analysis against gene set libraries using GSFM.
license: BSD-3-Clause license
---

# Gene Set Foundation Model

## Overview

GSFM (Gene Set Foundation Model) is a transformer-style foundation model trained on millions of gene sets, used to predict gene function and recover missing genes from a set.

## When to Use This Skill

- requests related to gene function prediction, gene set completion, or enrichment analysis
- gene set augmentation or missing-member prediction
- GSFM model/version discovery

## Core Capabilities & API Documentation

GSFM website exposes its backend as a single **tRPC** endpoint.

**Base endpoint:** ``https://gsfm.maayanlab.cloud/api/trpc/{functionName}``

### Functions

GSFM functions are under three categories in plain HTTP:
- **Queries:** `GET` request, input passed as a URL-encoded JSON query param named `input`, wrapped as `{"json": <value>}`.
- **Mutations:** `POST` request, JSON body `{"json": <value>}`.
- **Subscriptions:** Server-Sent Events stream (used only by `enrich`).


### Queries

**1. Gene Info**

Look up metadata for a single gene.
- **Input:** `string` — gene symbol (case-insensitive fallback built in)
- **Returns:** row from the `app.gene` table

```python
import requests, json

resp = requests.get(
    "https://gsfm.maayanlab.cloud/api/trpc/gene_info",
    params={"input": json.dumps({"json": "TP53"})},
)
gene = resp.json()["result"]["data"]["json"]
print(gene)
```

**2. Gene Autocomplete**

Fuzzy-match gene symbols, useful for search-as-you-type.
- **Input:** `string` — partial gene symbol
- **Returns:** up to 10 matching symbols, ranked by similarity

```python
import requests, json

resp = requests.get(
    "https://gsfm.maayanlab.cloud/api/trpc/gene_autocomplete",
    params={"input": json.dumps({"json": "TP5"})},
)
matches = resp.json()["result"]["data"]["json"]
print(matches)
```

**3. Models**

List all GSFM model variants that have predictions in the database.
- **Input:** none
- **Returns:** `[{ model, pagerank }]`, sorted by pagerank desc

```python
import requests

resp = requests.get("https://gsfm.maayanlab.cloud/api/trpc/models")
models = resp.json()["result"]["data"]["json"]
print(models)
```

**4. Models With Predictions for Gene**

Which model variants have predictions available for a given gene.
- **Input:** `{ gene: string }`
- **Returns:** `string[]` of model names, sorted by pagerank desc

```python
import requests, json

resp = requests.get(
    "https://gsfm.maayanlab.cloud/api/trpc/modelsWithPredictionsForGene",
    params={"input": json.dumps({"json": {"gene": "TP53"}})},
)
models = resp.json()["result"]["data"]["json"]
print(models)
```

**5. Sources**

List the annotation sources (e.g. GO, GTEx, KEGG) that have predictions for a gene, under a given model.
- **Input:** `{ model?: string (default "latest"), gene: string }`
- **Returns:** `[{ source, count, pagerank }]`

```python
import requests, json

resp = requests.get(
    "https://gsfm.maayanlab.cloud/api/trpc/sources",
    params={"input": json.dumps({"json": {"model": "latest", "gene": "TP53"}})},
)
sources = resp.json()["result"]["data"]["json"]
print(sources)
```

**6. Term Genes**

Count how many genes are predicted for a given source/term pair.
- **Input:** `{ model?: string (default "latest"), source: string, term: string }`
- **Returns:** `{ count: number }`

```python
import requests, json

resp = requests.get(
    "https://gsfm.maayanlab.cloud/api/trpc/termGenes",
    params={"input": json.dumps({
        "json": {"model": "latest", "source": "GO", "term": "apoptosis"}
    })},
)
count = resp.json()["result"]["data"]["json"]
print(count)
```

**7. Predictions**

The core lookup: paginated, sortable list of term predictions for a single gene, within
one source/model, optionally text-filtered on term. Joins in model performance stats
(ROC AUC, uniqueness) where available.
- **Input:**
  ```
  {
    model?: string (default "latest"),
    source: string,
    gene: string,
    orderBy?: "proba asc" | "proba desc" | "zscore asc" | "zscore desc"
            | "known asc" | "known desc" | "auroc asc" | "auroc desc"
            | "uniqueness asc" | "uniqueness desc"  (default "proba desc"),
    filter?: string,       # substring match on term
    offset: number,
    limit: number           # capped at 100
  }
  ```
- **Returns:** array of prediction rows (proba, zscore, known, roc_auc, etc.)

```python
import requests, json

resp = requests.get(
    "https://gsfm.maayanlab.cloud/api/trpc/predictions",
    params={"input": json.dumps({
        "json": {
            "model": "latest",
            "source": "GO",
            "gene": "TP53",
            "orderBy": "proba desc",
            "offset": 0,
            "limit": 20,
        }
    })},
)
predictions = resp.json()["result"]["data"]["json"]
print(predictions)
```

**8. Term Predictions**

Same as `predictions` but pivoted the other way: given a source + term, list the genes
predicted for it (optionally filtered by gene substring).
- **Input:**
  ```
  {
    model?: string (default "latest"),
    source: string,
    term: string,
    orderBy?: same enum as above (default "proba desc"),
    filter?: string,        # substring match on gene
    offset: number,
    limit: number             # capped at 100
  }
  ```
- **Returns:** array of prediction rows

```python
import requests, json

resp = requests.get(
    "https://gsfm.maayanlab.cloud/api/trpc/termPredictions",
    params={"input": json.dumps({
        "json": {
            "model": "latest",
            "source": "GO",
            "term": "apoptosis",
            "offset": 0,
            "limit": 20,
        }
    })},
)
gene_predictions = resp.json()["result"]["data"]["json"]
print(gene_predictions)
```

**9. Get List**

Retrieve a previously-submitted user gene set by id (see `addList` below).
- **Input:** `{ id: string }`
- **Returns:** `{ gene_set: string }` (newline-joined gene symbols)

```python
import requests, json

resp = requests.get(
    "https://gsfm.maayanlab.cloud/api/trpc/getList",
    params={"input": json.dumps({"json": {"id": "<uuid>"}})},
)
gene_set = resp.json()["result"]["data"]["json"]
print(gene_set)
```


### Mutations

**1. Augment**

Run **live GSFM inference** on an arbitrary gene set — predicts missing/related genes.
This is the direct model-inference endpoint (equivalent to loading the model in Python
yourself via the `gsfm` package, but hosted). The submitted set is also stored server-side.
- **Input:**
  ```
  {
    model?: string (default "latest"),
    gene_set: string[],       # list of gene symbols
    description?: string
  }
  ```
- **Returns:** inference result from GSFM (predicted/ranked genes)

```python
import requests

resp = requests.post(
    "https://gsfm.maayanlab.cloud/api/trpc/augment",
    json={"json": {
        "model": "latest",
        "gene_set": ["ACE1", "ACE2", "AGT"],
        "description": "RAS pathway test",
    }},
)
result = resp.json()["result"]["data"]["json"]
print(result)
```

**2. Add List**

Store a user-submitted gene set (used as a prerequisite step before `enrich`).
- **Input:** `{ gene_set: string[] (non-empty), description?: string }`
- **Returns:** `string` — the new gene set's id (UUID), pass this as `gene_set_id` to `enrich`

```python
import requests

resp = requests.post(
    "https://gsfm.maayanlab.cloud/api/trpc/addList",
    json={"json": {"gene_set": ["ACE1", "ACE2", "AGT"]}},
)
gene_set_id = resp.json()["result"]["data"]["json"]
print(gene_set_id)
```

**3. Add Library**

Upload a custom gene set library file (multipart form, field name
`gene_set_library_file`) to enrich against later. This one is `FormData`-based, not
JSON — call it as an ordinary multipart POST rather than the JSON pattern above.
- **Input:** multipart form field `gene_set_library_file`
- **Returns:** `string` — sha256-based id for the uploaded library

```python
import requests

with open("my_library.gmt", "rb") as f:
    resp = requests.post(
        "https://gsfm.maayanlab.cloud/api/trpc/addLibrary",
        files={"gene_set_library_file": f},
    )
library_id = resp.json()["result"]["data"]["json"]
print(library_id)
```

### Subscription

**1. Enrich**

Runs a GSFM-powered GSEA-style enrichment job against a gene set (from `addList`) and a
gene set library (built-in by name, or user-uploaded via `addLibrary`). Streams
progress/status events and finally result rows over Server-Sent Events — this is not a
simple request/response call.
- **Input:**
  ```
  {
    lastEventId?: string | null,   # for SSE resume
    model: string,                  # must map to a known HF model id
    gene_set_id: string,            # from addList
    gene_set_library_name?: string, # built-in library name
    gene_set_library_id?: string    # from addLibrary, for custom libraries
  }
  ```
- **Streams:** `{ status: string }` progress updates, then
  `{ data: [{ Term, es, nes, pval, sidak, geneset_size, leading_edge, plot }, ...] }`

tRPC subscriptions over the fetch adapter are served as Server-Sent Events. In Python,
read them incrementally with `requests` streaming (or the `sseclient-py` package) rather
than a single blocking call:

```python
import requests, json

params = {"input": json.dumps({
    "json": {
        "model": "gsfm-rummagene",   # must map to a known HF model id
        "gene_set_id": "<uuid from addList>",
        "gene_set_library_name": "GO_Biological_Process",
    }
})}

with requests.get(
    "https://gsfm.maayanlab.cloud/api/trpc/enrich",
    params=params,
    stream=True,
    headers={"Accept": "text/event-stream"},
) as resp:
    for line in resp.iter_lines(decode_unicode=True):
        if not line or not line.startswith("data:"):
            continue
        event = json.loads(line[len("data:"):].strip())
        if "status" in event:
            print("status:", event["status"])
        elif "data" in event:
            print("results:", event["data"])
```


## Best Practices & Tips

- 1. For repeated use, wrap query and mutation patterns in two small helpers:

```python
import requests, json

BASE = "https://gsfm.maayanlab.cloud/api/trpc"

def trpc_query(procedure, input_value=None):
    params = {"input": json.dumps({"json": input_value})} if input_value is not None else None
    resp = requests.get(f"{BASE}/{procedure}", params=params)
    resp.raise_for_status()
    return resp.json()["result"]["data"]["json"]

def trpc_mutation(procedure, input_value):
    resp = requests.post(f"{BASE}/{procedure}", json={"json": input_value})
    resp.raise_for_status()
    return resp.json()["result"]["data"]["json"]

# ex: trpc_query("gene_info", "TP53")
# ex: trpc_mutation("augment", {"gene_set": ["ACE1", "ACE2"]})
```

- 2. API responses are wrapped tRPC-style: `{"result":{"data":{"json": <value>}}}` on success, or an `error` object on failure. Example codes mentioned above use `requests`, `json.dumps` to encode the input, and unwrap that envelope with `resp.json()["result"]["data"]["json"]`.


- 3. Miscellaneous tips:
    - `model` defaults to `"latest"` almost everywhere; call `models` first if you need to offer a user a specific version (e.g. `gsfm-rummagene`, `gsfm-rummageo`, `gsfm-rummage`).
    - To browse "what does GSFM predict for gene X": `sources` → pick a source → `predictions`.
    - To browse "what genes does GSFM predict for this GO term/pathway": `termGenes` (count) → `termPredictions` (paged list).
    - To get a raw model prediction on a gene set you provide (no stored annotation needed): use `augment` directly.
    - To run enrichment against a full library: `addList` (get `gene_set_id`) → optionally `addLibrary` (get `gene_set_library_id`) → `enrich`.
    - Bulk downloads of the full prediction tables (used to seed this API) are available at https://gsfm.maayanlab.cloud/downloads if an agent needs offline/bulk access instead of paging through `predictions`/`termPredictions`.


## Additional Resources
- Website / API: https://github.com/MaayanLab/gsfm-predictions
- Model training/inference code: https://github.com/MaayanLab/gsfm


## Citations
Clarke, D. J. B., Marino, G. B. & Ma'ayan, A. GSFM: A gene set foundation model pre-trained on a massive collection of diverse gene sets. Patterns 101565 (2026) doi:10.1016/j.patter.2026.101565