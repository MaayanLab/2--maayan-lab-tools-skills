import argparse
import requests
import json
import os
import re
import time
import sys

BASE_URL = "https://maayanlab.cloud"


def read_genes(path='gene_set.txt'):
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]


def load_libraries():

    url = f"{BASE_URL}/Enrichr/datasetStatistics"

    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()

        data = response.json()

        if "statistics" not in data:
            raise ValueError("Unexpected response format")

        libraries = [
            entry["libraryName"]
            for entry in data["statistics"]
            if "libraryName" in entry
        ]

        return libraries

    except Exception as e:
        print(f"Failed to load libraries from Enrichr: {e}")
        return []


def enrich_no_background(genes, libs, limit=None):
    """Use Enrichr (no background) flow per skilltest.md section 3."""
    ENRICHR_ADD = BASE_URL + '/Enrichr/addList'
    ENRICHR_ENRICH = BASE_URL + '/Enrichr/enrich'

    print('Uploading gene list to Enrichr (no background)...')
    res_list = requests.post(
        ENRICHR_ADD,
        files=dict(
            list=(None, '\n'.join(genes)),
            description=(None, 'skilltest gene set')
        ),
        timeout=60,
    )
    if not res_list.ok:
        print('Gene list upload failed:', res_list.status_code, res_list.text)
        return
    list_json = res_list.json()
    print('Gene list upload response:', json.dumps(list_json, indent=2))
    userListId = list_json.get('userListId') or list_json.get('userlistId')
    if not userListId:
        print('No userListId returned; aborting')
        return

    os.makedirs('results', exist_ok=True)
    total = len(libs) if limit is None else min(len(libs), limit)
    for i, libname in enumerate(libs[:total], 1):
        safe_name = re.sub(r'[^A-Za-z0-9_.-]', '_', libname)
        out_fname = os.path.join('results', f'enrich_results_{safe_name}.json')
        print(f'[{i}/{total}] Requesting enrichment for {libname} -> {out_fname}')
        try:
            query = f'?userListId={userListId}&backgroundType={libname}'
            res_enrich = requests.get(ENRICHR_ENRICH + query, timeout=60)
            if not res_enrich.ok:
                print(f'  Failed ({res_enrich.status_code}): {res_enrich.text[:200]}')
                continue
            enrich_json = res_enrich.json()
            with open(out_fname, 'w') as out_f:
                json.dump(enrich_json, out_f, indent=2)
            print(f'  Wrote {out_fname} ({len(json.dumps(enrich_json))} bytes)')
        except Exception as e:
            print(f'  Error requesting enrichment for {libname}:', str(e))
        time.sleep(0.25)


def enrich_with_background(genes, limit=None):
    # Read background (large)
    if not os.path.exists('background.txt'):
        print('background.txt not found; cannot run background enrichment')
        return
    with open('background.txt') as f:
        background = [line.strip() for line in f if line.strip()]

    print(f'Read {len(genes)} genes and {len(background)} background genes')

    # Upload background
    print('Uploading background...')
    res_bg = requests.post(
        BASE_URL + '/speedrichr/api/addbackground',
        data=dict(background='\n'.join(background)),
        timeout=60,
    )
    if not res_bg.ok:
        print('Background upload failed:', res_bg.status_code, res_bg.text)
        return
    bg_json = res_bg.json()
    print('Background upload response:', json.dumps(bg_json, indent=2))
    backgroundid = bg_json.get('backgroundid') or bg_json.get('backgroundId')

    # Upload gene list to speedrichr
    print('Uploading gene list...')
    res_list = requests.post(
        BASE_URL + '/speedrichr/api/addList',
        files=dict(
            list=(None, '\n'.join(genes)),
            description=(None, 'skilltest gene set')
        ),
        timeout=60,
    )
    if not res_list.ok:
        print('Gene list upload failed:', res_list.status_code, res_list.text)
        return
    list_json = res_list.json()
    print('Gene list upload response:', json.dumps(list_json, indent=2))
    userListId = list_json.get('userListId')

    # Discover libraries
    libs = load_libraries()
    print(f'Found {len(libs)} libraries; will iterate and save results to results/<library>.json')
    os.makedirs('results', exist_ok=True)
    total = len(libs) if limit is None else min(len(libs), limit)
    for i, libname in enumerate(libs[:total], 1):
        safe_name = re.sub(r'[^A-Za-z0-9_.-]', '_', libname)
        out_fname = os.path.join('results', f'enrich_results_{safe_name}.json')
        print(f'[{i}/{total}] Requesting enrichment for {libname} -> {out_fname}')
        try:
            res_enrich = requests.post(
                BASE_URL + '/speedrichr/api/backgroundenrich',
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
        time.sleep(0.25)


def main():
    parser = argparse.ArgumentParser(description='Run skilltest enrichment (with or without background)')
    parser.add_argument('--no-background', action='store_true', help='Run Enrichr enrichment without a background (uses Enrichr endpoints)')
    parser.add_argument('--limit', type=int, default=None, help='Limit number of libraries to process (useful for testing)')
    args = parser.parse_args()

    try:
        genes = read_genes()
    except FileNotFoundError:
        print('gene_set.txt not found in current directory; aborting')
        sys.exit(1)

    if args.no_background:
        libs = load_libraries()
        enrich_no_background(genes, libs, limit=args.limit)
    else:
        enrich_with_background(genes, limit=args.limit)


if __name__ == '__main__':
    main()
