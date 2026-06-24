---
name: PrismEXP
description: >
  .
license: Apache-2.0 license (software)
---

# PrismEXP

## Overview

PrismEXP is a gene annotation prediction tool that uses stratified gene-gene co-expression patterns to predict biological functions, pathways, and regulatory associations for human genes.

PrismEXP leverages large-scale gene expression datasets by clustering samples into groups with similar expression profiles and generating multiple context-specific gene correlation matrices. A machine learning model integrates these co-expression signals to rank likely gene annotations.

Users input a human gene symbol and receive predicted biological annotations from gene set libraries, along with known annotations for comparison. Based on gene-gene co-expression matrices from ARCHS4 and selected gene set libraries from Enrichr.

PrismEXP is available as a Python package, through Appyters, and through its website.

## When to Use This Skill

* predicting biological functions and pathway annotations for human genes
* retrieving known and predicted gene annotations
* annotating poorly characterized genes
* identifying regulatory, pathway, phenotype, and ontology associations
* prioritizing functional hypotheses from large-scale gene expression data
* exploring gene-gene relationships and extending gene sets


## Core Capabilities

### Gene Annotation Prediction

**Parameters:** gene (human gene symbol)

**Returns:**

* gene set library analyzed (e.g., ChEA, GO Biological Process, KEGG)
* ranked predicted annotations for the queried gene
* three scores: gene AUC, association score, set reliability
* indication of previously known annotations when available

Gene AUC reflects how well known gene functions of the input gene could be retrieved. AUC of 1 represents perfect ranking and 0.5 means random rank.

Set Reliability is the AUC capturing how well known associated genes are ranked in the PrismEXP prediction.

Example code below.
```python
import requests 

gene = "APOE"

response = requests.get(
   f"https://maayanlab.cloud/prismexp/gene/{gene}" 
) 

response.raise_for_status() 
results = response.json()

print(results)
```



Context-Specific Co-expression Modeling
Leverages multiple gene-gene co-expression matrices derived from clustered ARCHS4 RNA-seq data to capture tissue- and cell-type-specific relationships.

Machine Learning Ranking
Uses a LightGBM model to combine co-expression features and rank candidate gene annotations.

Hypothesis Generation for Understudied Genes
Predict functions and biological associations for poorly characterized genes, including non-coding genes and splice variants.



## Additional Resources
PrismEXP Python package: https://github.com/maayanlab/prismexp
PrismEXP website: https://maayanlab.cloud/prismexp/help

## Citations
Lachmann A, Rizzo KA, Bartal A, Jeon M, Clarke DJB, Ma’ayan A. 2023. PrismEXP: gene annotation prediction from stratified gene-gene co-expression matrices. PeerJ 11:e14927 https://doi.org/10.7717/peerj.14927