import requests
import json
import os
import re
import time

BASE_URL = "https://maayanlab.cloud/speedrichr"

# Read gene set
with open('gene_set.txt') as f:
    genes = [line.strip() for line in f if line.strip()]

# Read background (large)
with open('background.txt') as f:
    background = [line.strip() for line in f if line.strip()]

print(f"Read {len(genes)} genes and {len(background)} background genes")

# Upload background
print('Uploading background...')
res_bg = requests.post(
    BASE_URL + '/api/addbackground',
    data=dict(background='\n'.join(background))
)
if not res_bg.ok:
    print('Background upload failed:', res_bg.status_code, res_bg.text)
else:
    bg_json = res_bg.json()
    print('Background upload response:', json.dumps(bg_json, indent=2))
    backgroundid = bg_json.get('backgroundid') or bg_json.get('backgroundId')

# Upload gene list
print('Uploading gene list...')
res_list = requests.post(
    BASE_URL + '/api/addList',
    files=dict(
        list=(None, '\n'.join(genes)),
        description=(None, 'skilltest gene set')
    )
)
if not res_list.ok:
    print('Gene list upload failed:', res_list.status_code, res_list.text)
else:
    list_json = res_list.json()
    print('Gene list upload response:', json.dumps(list_json, indent=2))
    userListId = list_json.get('userListId')

# Run enrichment with background if both ids present
if 'backgroundid' in locals() and 'userListId' in locals():
    # Try to fetch available libraries from Speedrichr
    print('Fetching available libraries...')
    libs = None
    try:
        rlibs = requests.get(BASE_URL + '/api/libraries', timeout=30)
        if rlibs.ok:
            libs = rlibs.json()
            # Expecting a list of library names or a dict; normalize
            if isinstance(libs, dict):
                # dict mapping maybe categories -> lists; flatten
                flattened = []
                for v in libs.values():
                    if isinstance(v, list):
                        flattened.extend(v)
                libs = flattened
    except Exception as e:
        print('Failed to get libraries from Speedrichr:', str(e))

    # Fallback: scrape Enrichr landing page for library names
    if not libs:
        try:
            print('Falling back to scraping Enrichr landing page for libraries...')
            enr_page = requests.get('https://maayanlab.cloud/Enrichr', timeout=30)
            if enr_page.ok:
                text = enr_page.text
                # Look for JavaScript array named 'libraries' or for options like value: 'LIBRARY_NAME'
                candidates = re.findall(r"['\"]([A-Za-z0-9_\-]+)['\"]\s*:\s*\[", text)
                # Also try to find occurrences like '"name":"LIBRARY_NAME"'
                candidates += re.findall(r'"([A-Za-z0-9_\-]+)"\s*:\s*\{"description"', text)
                # As a last resort, look for common library tokens with underscore
                candidates += re.findall(r'([A-Za-z0-9_]+_[0-9]{4})', text)
                libs = list(dict.fromkeys([c for c in candidates if len(c) > 3]))
        except Exception as e:
            print('Failed to scrape Enrichr page for libraries:', str(e))

    if not libs:
        print('Could not determine library list automatically. Falling back to a default library list.')
        # Reasonable fallback set of commonly-used libraries
        libs = [
            'BioPlanet_2019', 'KEGG_2019_Human', 'WikiPathways_2019_Human',
            'Reactome_2016', 'GO_Biological_Process_2018', 'GO_Cellular_Component_2018',
            'GO_Molecular_Function_2018', 'ChEA_2016', 'TRANSFAC_and_JASPAR_PWMs',
            'ENCODE_and_ChEA_Consensus_TFs_from_ChIP-X', 'DSigDB', 'MSigDB_Hallmark_2020'
        ]

    # Iterate over whichever libs we have (discovered or fallback)
    # If there's a local libraries.json file, prefer that explicit list (user-supplied)
    if os.path.exists('libraries.json'):
        try:
            with open('libraries.json') as lj:
                ljd = json.load(lj)
                if isinstance(ljd, dict) and 'libraries' in ljd:
                    libs_from_file = [entry.get('library') for entry in ljd['libraries'] if entry.get('library')]
                    if libs_from_file:
                        libs = libs_from_file
                        print(f'Using {len(libs)} libraries from libraries.json')
        except Exception as e:
            print('Failed to read libraries.json, continuing with discovered/fallback libs:', str(e))

    print(f'Found {len(libs)} libraries; will iterate and save results to results/<library>.json')
    os.makedirs('results', exist_ok=True)
    for i, libname in enumerate(libs, 1):
        safe_name = re.sub(r'[^A-Za-z0-9_.-]', '_', libname)
        out_fname = os.path.join('results', f'enrich_results_{safe_name}.json')
        print(f'[{i}/{len(libs)}] Requesting enrichment for {libname} -> {out_fname}')
        try:
            res_enrich = requests.post(
                BASE_URL + '/api/backgroundenrich',
                data=dict(
                    userListId=userListId,
                    backgroundid=backgroundid,
                    backgroundType=libname,
                ),
                timeout=60,
            )
            if not res_enrich.ok:
                print(f'  Failed ({res_enrich.status_code}): {res_enrich.text[:200]}')
                continue
            enrich_json = res_enrich.json()
            with open(out_fname, 'w') as out_f:
                json.dump(enrich_json, out_f, indent=2)
            print(f'  Wrote {out_fname} ({len(json.dumps(enrich_json))} bytes)')
        except Exception as e:
            print(f'  Error requesting enrichment for {libname}:', str(e))
        # short pause to avoid hammering the service
        time.sleep(0.25)
else:
    print('Missing backgroundid or userListId; skipping enrichment')