---
name: Enrichr
description: >
  Gene-list enrichment analysis tool. Use for checking if input set of genes significantly overlaps with annotated gene sets, returning most over-represented gene sets from library databases.
license: CC-BY-NC-SA-4.0
metadata:
  version: 2.0.0
---

# Enrichr

## Overview

Enrichr is Ma'ayan Lab's enrichment analysis tool that uses a set of Entrez gene symbols as input and returns a ranked set of terms for each gene set library along with their scores. Can be performed with or without background. Each gene set within Enrichr is associated with a functional term or an enrichment term.


## When to Use This Skill

Use this skill when:
- figuring out if input gene set is over-represented (enrichment analysis) with or without background
- searching libary database for all gene sets containing specific term
- searching library database for terms containing specific gene
- expanding a gene, term, or variant into a gene set to use for analysis

## Outputs

Enrichr implements four scores to report enrichment results: *p-value, q-value, rank (Z-score),* and *combined score*. They are explained below:

**p-value**:
- computed using Fisher's exact test or the hypergeometric test (a binomial proportion test assuming binomial distribution and independence for probability of any gene belonging to any set)

**q-value**:
- adjusted p-value using Benjamini-Hochberg method for correction for multiple hypotheses testing

**combined score**:

`c = -log(p) * oddsRatio` where **c** is *combined score* and **p** is *p-value*

The  **oddsRatio** is:

 `oddsRatio = (1.0 * a * d) / Math.max(1.0 * b * c, 1)` where **a** are *overlapping genes*, **b** are *genes in anotated set - overlapping genes*, **c** are *genes in input set - overlapping genes*, **d** are *total background genes - genes in annotated set - genes in input set + overlapping genes*

## Installation

To install the requests library, run in terminal:

```bash
$ python -m pip install requests
```

## Core Capabilities

### 1. Gene Set Analysis (Without Background)

Upload set of gene symbols to receive unique IDs for enrichment.

See `scripts/run_enrichment_analysis.py` for performing analysis.
Unless specified otherwise, run analysis for all current 228 libraries.

**Parameters**
- Newline-separated **list** of gene symbols to enrich
- **description** (optional **string**) describing what the gene symbols represent

**Returns**

- JSON object with unique ID for analysis results


**Example code**
```python
import json
import requests


ENRICHR_URL = 'https://maayanlab.cloud/Enrichr/addList'
genes_str = '\n'.join([
    'PHF14', 'RBM3', 'MSL1', 'PHF21A', 'ARL10', 'INSR', 'JADE2', 'P2RX7',
    'LINC00662', 'CCDC101', 'PPM1B', 'KANSL1L', 'CRYZL1', 'ANAPC16', 'TMCC1',
    'CDH8', 'RBM11', 'CNPY2', 'HSPA1L', 'CUL2', 'PLBD2', 'LARP7', 'TECPR2', 
    'ZNF302', 'CUX1', 'MOB2', 'CYTH2', 'SEC22C', 'EIF4E3', 'ROBO2',
    'ADAMTS9-AS2', 'CXXC1', 'LINC01314', 'ATF7', 'ATP5F1'
])
description = 'Example gene list'
payload = {
    'list': (None, genes_str),
    'description': (None, description)
}

response = requests.post(ENRICHR_URL, files=payload)
if not response.ok:
    raise Exception('Error analyzing gene list')

data = json.loads(response.text)
print(data)
```

**Example results**

```python
{
    "userListId": 363320,
    "shortId": "59lh"
}
```

### 2. Viewing Added Gene Set

Using unique IDs obtained from Gene Set Analysis, retrieves the gene list for that ID

**Parameters**
- ID returned from Gene Set Analysis (userListId)

**Returns**
- Gene list matching unique ID (JSON object)

**Example code**
```python
import json
import requests


ENRICHR_URL = 'https://maayanlab.cloud/Enrichr/view?userListId=%s'
user_list_id = 363320
response = requests.get(ENRICHR_URL % user_list_id)
if not response.ok:
    raise Exception('Error getting gene list')
    
data = json.loads(response.text)
print(data)
```


**Example results**
```python
{
    "genes": [
        "PHF14", "RBM3", "MSL1", "PHF21A", "ARL10", "INSR", "JADE2",
        "P2RX7", "LINC00662", "CCDC101", "PPM1B", "KANSL1L", "CRYZL1",
        "ANAPC16", "TMCC1", "CDH8", "RBM11", "CNPY2", "HSPA1L", "CUL2",
        "PLBD2", "LARP7", "TECPR2", "ZNF302", "CUX1", "MOB2", "CYTH2",
        "SEC22C", "EIF4E3", "ROBO2", "ADAMTS9-AS2", "CXXC1", "LINC01314",
        "ATF7", "ATP5F1"
    ],
    "description": "Example gene list"
}
```

### 3. Get Enrichment Results (Without Background)

**Parameters**
- ID returned from Gene Set Analysis (userListId)
- Gene set library to enrich against (backgroundType)


**Returns**
- Rank, Term name, P-value, Odds ratio, Combined score, Overlapping genes, Adjusted p-value, Old p-value, Old adjusted p-value


**Example code**
```python
import json
import requests


ENRICHR_URL = 'https://maayanlab.cloud/Enrichr/enrich'
query_string = '?userListId=%s&backgroundType=%s'
user_list_id = 363320
gene_set_library = 'KEGG_2015'
response = requests.get(
    ENRICHR_URL + query_string % (user_list_id, gene_set_library)
 )
if not response.ok:
    raise Exception('Error fetching enrichment results')

data = json.loads(response.text)
print(data)
```

**Example results**
```python
{
    "KEGG_2015": [
        [
            1, 
            "ubiquitin mediated proteolysis", 
            0.06146387620182772, 
            -1.8593425456520887, 
            2.8168673182384705, 
            ["CUL2"], 
            0.21981251622012696
        ], 
        [
            2, 
            "type ii diabetes mellitus", 
            0.06594375486603808, 
            -1.799654722223511, 
            2.7264414418952905, 
            ["INSR"], 
            0.21981251622012696
        ],
        ...
    ]
}
```

### 4. Gene Set Analysis with a Background

In performing gene set enrichment analysis with a background, Enrichr directly interfaces with the Speedrichr API. Note that IDs generated by Speedrichr are not persistent.

See `scripts/run_enrichment_analysis.py` for performing analysis.
Unless specified otherwise, run analysis for all current 228 libraries.

**Parameters**
- Newline-separated **list** of gene symbols to enrich
- **description** (optional **string**) describing what the gene symbols represent

**Returns**	
- JSON object with unique ID for analysis results

**Example code**
```python
import requests

base_url = "https://maayanlab.cloud/speedrichr"

genes = [
    'PHF14', 'RBM3', 'MSL1', 'PHF21A', 'ARL10', 'INSR', 'JADE2', 'P2RX7',
    'LINC00662', 'CCDC101', 'PPM1B', 'KANSL1L', 'CRYZL1', 'ANAPC16', 'TMCC1',
    'CDH8', 'RBM11', 'CNPY2', 'HSPA1L', 'CUL2', 'PLBD2', 'LARP7', 'TECPR2', 
    'ZNF302', 'CUX1', 'MOB2', 'CYTH2', 'SEC22C', 'EIF4E3', 'ROBO2',
    'ADAMTS9-AS2', 'CXXC1', 'LINC01314', 'ATF7', 'ATP5F1'
]

description = "sample gene set with background"

res = requests.post(
    base_url+'/api/addList',
    files=dict(
      list=(None, '\n'.join(genes)),
      description=(None, description),
    )
  )
if res.ok:
	userlist_response = res.json()
	print(userlist_response)
```

**Example results**
```python
	
{
	"userListId": 667152768,
	"shortId": "27c3f180"
}
```

**Uploading your Background**

**Parameters**
- Newline-separated set of background gene symbols

**Returns**	
- JSON object with background id

**Example code**
```python
import requests

base_url = "https://maayanlab.cloud/speedrichr"

background = [
	'NSUN3','POLRMT','NLRX1','SFXN5','ZC3H12C','SLC25A39','ARSG',
	'DEFB29','PCMTD2','ACAA1A','LRRC1','2810432D09RIK','SEPHS2',
	'SAC3D1','TMLHE','LOC623451','TSR2','PLEKHA7','GYS2','ARHGEF12',
	'HIBCH','LYRM2','ZBTB44','ENTPD5','RAB11FIP2','LIPT1',
	'INTU','ANXA13','KLF12','SAT2','GAL3ST2','VAMP8','FKBPL',
	'AQP11','TRAP1','PMPCB','TM7SF3','RBM39','BRI3','KDR','ZFP748',
	'NAP1L1','DHRS1','LRRC56','WDR20A','STXBP2','KLF1','UFC1',
	'CCDC16','9230114K14RIK','RWDD3','2610528K11RIK','ACO1',
	'CABLES1', 'LOC100047214','YARS2','LYPLA1','KALRN','GYK',
	'ZFP787','ZFP655','RABEPK','ZFP650','4732466D17RIK','EXOSC4',
	'WDR42A','GPHN','2610528J11RIK','1110003E01RIK','MDH1','1200014M14RIK',
	'AW209491','MUT','1700123L14RIK','2610036D13RIK',
	'PHF14', 'RBM3', 'MSL1', 'PHF21A', 'ARL10', 'INSR', 'JADE2', 
	'P2RX7', 'LINC00662', 'CCDC101', 'PPM1B', 'KANSL1L', 'CRYZL1', 
	'ANAPC16', 'TMCC1','CDH8', 'RBM11', 'CNPY2', 'HSPA1L', 'CUL2', 
	'PLBD2', 'LARP7', 'TECPR2', 'ZNF302', 'CUX1', 'MOB2', 'CYTH2', 
	'SEC22C', 'EIF4E3', 'ROBO2', 'ADAMTS9-AS2', 'CXXC1', 'LINC01314', 'ATF7', 
	'ATP5F1''COX15','TMEM30A','NSMCE4A','TM2D2','RHBDD3','ATXN2','NFS1',
	'3110001I20RIK','BC038156','C330002I19RIK','ZFYVE20','POLI','TOMM70A',
	'LOC100047782','2410012H22RIK','RILP','A230062G08RIK',
	'PTTG1IP','RAB1','AFAP1L1', 'LYRM5','2310026E23RIK',
	'SLC7A6OS','MAT2B','4932438A13RIK','LRRC8A','SMO','NUPL2'
]



res = requests.post(
	base_url+'/api/addbackground',
	data=dict(background='\n'.join(background)),
  )

if res.ok:
	background_response = res.json()
	print(background_response)
```

**Example results**
```python
{
	"backgroundid": "3ff7ef9d"
}
```

**Get Enrichment Results (with background)**

**Parameters**
- ID from Enrichment Analysis with Background (userListId)
- background ID from Uploading your Background (backgroundId)
- Gene set library to enrich against (backgroundType)

**Returns**
- Rank, Term name, P-value, Odds ratio, Combined score, Overlapping genes, Adjusted p-value, Old p-value, Old adjusted p-value

**Example code**
```python
import requests

base_url = "https://maayanlab.cloud/speedrichr"

res = requests.post(
        base_url+'/api/backgroundenrich',
        data=dict(
        userListId=667152768,
        backgroundid="3ff7ef9d",
        backgroundType="ChEA_2022",
        )
    )
if res.ok:
	results = res.json()
	print(results)
```

**Example results**
```python
{
	"ChEA_2022": [
		[
			1,
			"VDR 24787735 ChIP-Seq THP-1 Human",
			0.000842494387359289,
			13.092592592592593,
			92.6843425047622,
			[
				"P2RX7",
				"ROBO2",
				"CUX1",
				"INSR",
				"CRYZL1",
				"CUL2",
				"TMCC1"
			],
			0.5054966324155734,
			0,
			0
		],
		[
			2,
			"VDR 24763502 ChIP-Seq THP-1 Human",
			0.0030556207159606777,
...
			0
		]
	]
}
```

### 5. Find Terms that Contain a Given Gene (Gene Search)

**Parameters**
- **gene** to use in search for terms
- **json** (optional) :	Set "true" to return JSON rather plaintext
- **setup** (optional) : Set "true" to category information for the libraries

**Returns**
- Terms containing the specified gene, along with descriptions and optional categorizations

**Example code**
```python
import json
import requests

ENRICHR_URL = 'https://maayanlab.cloud/Enrichr/genemap'
query_string = '?json=true&setup=true&gene=%s'
gene = 'AKT1'
response = requests.get(ENRICHR_URL + query_string % gene)
if not response.ok:
    raise Exception('Error searching for terms')
    
data = json.loads(response.text)
print(data)
```

**Example results**
```python
{
    "gene": {
        "GeneSigDB": [
            "18535662-TableS2b",
            "17671232-TableS2a",
            ...
        ],
        "TRANSFAC_and_JASPAR_PWMs": [...],
        ...   
    },
    "descriptions": [
        {
            "name": "GeneSigDB",
            "description": "The GeneSigDB gene-set library was borrowed from 
                the GeneSigDB database (PMID:22110038). The database contains 
                gene lists extracted manually from the supporting tables of 
                thousands of publications; most are from cancer related 
                studies."
        },
    	...
    ],
    "categories": [
        {
            "name": "Transcription",
            "libraries": [
                {
                    "name": "ChEA_2015",
                    "isFuzzy": true,
                    "hasGrid": true,
                    "format": "{1} binds to the promoter region of {0}."
                },
                ...
            },
            ...
        },
        ...
    ]
}
```

### 6. Term Search

**Parameters**
- **term** to use in search for
- **json** (optional) :	Set "true" to return JSON rather plaintext

**Returns**
- all gene sets that are related to the input term

**Example code**
```python
import json
import requests

ENRICHR_URL = 'https://maayanlab.cloud/Enrichr/termmap'
query_string = '?json=%s&meta=%s'

option = 'true'
term = "breast%20cancer"

response = requests.get(ENRICHR_URL + query_string % (option, term)
    )

if not response.ok:
    raise Exception('Error fetching enrichment results')

data = json.loads(response.text)
print(data)
```

**Example results**
```python
{
  "terms": {
    "DisGeNET": [
      "bilateral breast cancer",
      "Intermediate Grade Ductal Breast Carcinoma In Situ",
      "Sporadic Breast Carcinoma",
      "Contralateral breast cancer",
      "Unilateral Breast Carcinoma",
      "Unilateral Breast Neoplasms",
      "Stage 0 Breast Carcinoma",
      "Adenoid cystic breast carcinoma",
      "Carcinoma breast stage IV",
      "Columnar Cell Change of the Breast",
      "Columnar Cell Hyperplasia of the Breast",
      "Stage III Breast Cancer AJCC v6",
      "Stage III Breast Cancer AJCC v7",
      ...
      ]
  }
}

```

### 7. Download File of Enrichment Results

**Parameters**
- ID from Gene Set Analysis (userListId)
- name of text file download (filename)
- Gene set library for which to download results (backgroundType)

**Returns**
- Text file of enrichment analysis results

**Example code**
```python
import json
import requests


ENRICHR_URL = 'https://maayanlab.cloud/Enrichr/export'
query_string = '?userListId=%s&filename=%s&backgroundType=%s'
user_list_id = 363320
filename = 'example_enrichment'
gene_set_library = 'KEGG_2015'

url = ENRICHR_URL + query_string % (user_list_id, filename, gene_set_library)
response = requests.get(url, stream=True)

with open(filename + '.txt', 'wb') as f:
    for chunk in response.iter_content(chunk_size=1024): 
        if chunk:
            f.write(chunk)
```

## Additional Resources
- **How to use**: https://maayanlab.cloud/Enrichr/help#basics
- **API Documentation**: https://maayanlab.cloud/Enrichr/help#api


## Enrichr Citation 
- Chen EY, Tan CM, Kou Y, Duan Q, Wang Z, Meirelles GV, Clark NR, Ma'ayan A. Enrichr: interactive and collaborative HTML5 gene list enrichment analysis tool. BMC Bioinformatics. 2013;128(14)
- Kuleshov MV, Jones MR, Rouillard AD, Fernandez NF, Duan Q, Wang Z, Koplev S, Jenkins SL, Jagodnik KM, Lachmann A, McDermott MG, Monteiro CD, Gundersen GW, Ma'ayan A. Enrichr: a comprehensive gene set enrichment analysis web server 2016 update. Nucleic Acids Research. 2016; gkw377.
- Xie Z, Bailey A, Kuleshov MV, Clarke DJB., Evangelista JE, Jenkins SL, Lachmann A, Wojciechowicz ML, Kropiwnicki E, Jagodnik KM, Jeon M, & Ma’ayan A. Gene set knowledge discovery with Enrichr. Current Protocols, 1, e90. 2021. doi: 10.1002/cpz1.90