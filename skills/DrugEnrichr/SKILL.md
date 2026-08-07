---
name: DrugEnrichr
description: >
    Enrichment analysis tool for drug sets. Used for checking whether an input set of drugs significantly overlaps with annotated drug sets, returning most over-represented drug sets from library databases.
---

# DrugEnrichr

## Overview

DrugEnrichr is a drug set enrichment analysis platform that enables users to analyze lists of drugs against a large collection of curated drug-set libraries. Given an input list of drugs, DrugEnrichr identifies biological targets, mechanisms of action, pathways, disease associations, side effects, ontologies, and other functional annotations that are significantly enriched. Supports enrichment analysis using curated drug-set libraries compiled from published studies, biomedical databases, and resources developed specifically for DrugEnrichr. DrugEnrichr also provides a drug lookup function which finds all enrichment terms and drug-set libraries associated with a specific drug.

A common workflow used in combination with other Ma'ayan Lab skills: Perturb-Seqr results into DrugEnrichr.

## When to Use This Skill

- performing enrichment analysis on drug lists
- identifying enriched drug targets, mechanisms of action, pathways, and disease associations
- interpreting drug screening and repurposing results
- comparing enrichment across multiple drug-set libraries
- retrieving annotations for individual drugs

## API Documentation

### 1. Analyze drug list

Retrieves IDs for analysis results.

**Parameters:** 
- list (newline-separated list of drug symbols to enrich)
- description (optional, string describing what the drug symbols represent)

**Example code**
```python
import json
import requests


ENRICHR_URL = 'http://amp.pharm.mssm.edu/DrugEnrichr/addList'
drugs_str = '\n'.join([
    "ac1ndss5", "adoprazine", "ai-10-49", "alisporivir", "almitrine",
    "alvocidib", "am 580", "amg-9810", "amuvatinib", "amuvatinib",
    "antimycin a", "apixaban", "as-252424", "avasimibe", "avatrombopag"
])
description = 'Example drug list'
payload = {
    'list': (None, drugs_str),
    'description': (None, description)
}

response = requests.post(ENRICHR_URL, files=payload)
if not response.ok:
    raise Exception('Error analyzing drug list')

data = json.loads(response.text)
print(data)
```

**Example outputs**
```python
{
    "userListId": 363320,
    "shortId": "59lh"
}
```

### 2. View added drug list

**Parameters:** userListId (identifier returned from addList endpoint)

**Example code**
```python
import json
import requests


ENRICHR_URL = 'http://amp.pharm.mssm.edu/DrugEnrichr/view?userListId=%s'
user_list_id = 363320
response = requests.get(ENRICHR_URL % user_list_id)
if not response.ok:
    raise Exception('Error getting drug list')
    
data = json.loads(response.text)
print(data)
```

**Example output**
```python
{
    "drugs": ["ac1ndss5", "adoprazine", "ai-10-49", "alisporivir", "almitrine",
    "alvocidib", "am 580", "amg-9810", "amuvatinib", "amuvatinib",
    "antimycin a", "apixaban", "as-252424", "avasimibe", "avatrombopag"
    ],
    "description": "Example drug list"
}
```

### 3. Get enrichment results

Retrieves the following: Rank, Term name, P-value, Z-score, Combined score, Overlapping drugs, Adjusted p-value, Old p-value, Old adjusted p-value. Please note that response rows contain 9 columns and that a mismatch in the number of columns may cause parsing issues.

**Parameters:**
- userListId (identifier returned from addList endpoint)
- backgroundType (drug set library to enrich against)

**Example code**
```python
	
import json
import requests


ENRICHR_URL = 'http://amp.pharm.mssm.edu/DrugEnrichr/enrich'
query_string = '?userListId=%s&backgroundType=%s'
user_list_id = 363320
drug_set_library = 'DrugBank_Small-molecule_Carrier'
response = requests.get(
    ENRICHR_URL + query_string % (user_list_id, drug_set_library)
 )
if not response.ok:
    raise Exception('Error fetching enrichment results')

data = json.loads(response.text)
print(data)
```

**Example output**
```python
{
    "SIDER_Side_Effects": [
        [
            1, 
            "keratoacanthoma",
            0.06146387620182772, 
            -1.8593425456520887, 
            2.8168673182384705, 
            ["sorafenib"],
            0.21981251622012696
        ], 
        [
            2, 
            "sedation",
            0.06594375486603808, 
            -1.799654722223511, 
            2.7264414418952905, 
            ["papaverine"],
            0.21981251622012696
        ],
        ...
    ]
}
```

### 4. Drug lookup

Retrieve terms containing the specified drug, along with descriptions and optional categorizations.

**Parameters:**
- drug (drug to use in search for terms)
- json (optional, set "true" to return JSON rather plaintext)
- setup (optional, set "true")

**Example code**
```python
import json
import requests


ENRICHR_URL = 'http://amp.pharm.mssm.edu/DrugEnrichr/drugmap'
query_string = '?json=true&setup=true&drug=%s'
drug = 'AKT1'
response = requests.get(ENRICHR_URL + query_string % drug)
if not response.ok:
    raise Exception('Error searching for terms')
    
data = json.loads(response.text)
print(data)
```

**Example output**
```python
{
    "drug": {
        "ATC": [
            "thimerosal",
            ...
        ],
        "CREEDS_Signature_down": [...],
        ...   
    },
    "descriptions": [
        {
            "name": "ATC",
            "description": "A classification system used to organize small molecules by chemical, therapeutic, pharmacological subgroups, cut off at the fourth level"
        },
    	...
    ],
    "categories": [
        {
            "name": "Targets",
            "libraries": [
                {
                    "name": "ATC",
                    "isFuzzy": false,
                    "hasGrid": false,
                    "format": "MoA of {0} is {1}."
                },
                ...
            },
            ...
        },
        ...
    ]
}
```

### 5. Download file of enrichment results

Downloads text file of enrichment analysis results.

**Parameters:**
- userListId (identifier returned from addList endpoint)
- filename (name of text file download)
- backgroundType (drug set library for which to download results)

**Example code**
```python
import json
import requests


ENRICHR_URL = 'http://amp.pharm.mssm.edu/DrugEnrichr/export'
query_string = '?userListId=%s&filename=%s&backgroundType=%s'
user_list_id = 363320
filename = 'example_enrichment'
drug_set_library = 'SIDER_Side_Effects'

url = ENRICHR_URL + query_string % (user_list_id, filename, drug_set_library)
response = requests.get(url, stream=True)

with open(filename + '.txt', 'wb') as f:
    for chunk in response.iter_content(chunk_size=1024): 
        if chunk:
            f.write(chunk)
```

## Available Drug-set Libraries

Below are a list of the available drug-set libraries DrugEnrichr has access to:

- ATC
- CREEDS_Signature_Down
- CREEDS_Signature_Up	
- Drug_Repurposing_Hub_Mechanism_of_Action
- Drug_Repurposing_Hub_Target	
- DrugCentral_Target
- Geneshot_Associated	
- Geneshot_Predicted_Enrichr
- Geneshot_Predicted_from_AutoRIF	
- Geneshot_Predicted_from_Co-expression
- Geneshot_Predicted_GeneRIF	
- Geneshot_Predicted_Tagger
- KinomeScan_Kinase
- L1000FWD_GO_Biological_Processes_Down
- L1000FWD_GO_Biological_Processes_Up	
- L1000FWD_GO_Cellular_Component_Down		
- L1000FWD_GO_Cellular_Component_Up	
- L1000FWD_GO_Molecular_Function_Down	
- L1000FWD_GO_Molecular_Function_Up	
- L1000FWD_KEGG_Pathways_Down	
- L1000FWD_KEGG_Pathways_Up	
- L1000FWD_Predicted_Side_Effects	
- L1000FWD_Signature_Down	
- L1000FWD_Signature_Up	
- PharmGKB_OFFSIDES_Side_Effects	
- PharmGKB_SNV
- SIDER_Indications
- SIDER_Side_Effects
- STITCH_Target

## Additional Resources
DrugEnrichr background information: https://maayanlab.cloud/DrugEnrichr/help#background

## Citations
- Kuleshov MV, Diaz JEL, Flamholz ZN, Keenan AB, Lachmann A, Wojciechowicz ML, Cagan RL, Ma'ayan A. modEnrichr: a suite of gene set enrichment analysis tools for model organisms. Nucleic Acids Res. 2019 May 9. pii: gkz347
- Chen EY, Tan CM, Kou Y, Duan Q, Wang Z, Meirelles GV, Clark NR, Ma'ayan A. Enrichr: interactive and collaborative HTML5 gene list enrichment analysis tool. BMC Bioinformatics. 2013;128(14)
- Kuleshov MV, Jones MR, Rouillard AD, Fernandez NF, Duan Q, Wang Z, Koplev S, Jenkins SL, Jagodnik KM, Lachmann A, McDermott MG, Monteiro CD, Gundersen GW, Ma'ayan A. Enrichr: a comprehensive gene set enrichment analysis web server 2016 update. Nucleic Acids Research. 2016; gkw377.