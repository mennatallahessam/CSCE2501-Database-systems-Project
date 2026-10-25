# -*- coding: utf-8 -*-
"""Quick recon probe: fetch 5 sample property detail pages and inspect __NEXT_DATA__."""
import sys, os, re, json, time
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

import requests
from pathlib import Path
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0 (student project, CSCE 2501 AUC)',
    'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}
s = requests.Session()
s.headers.update(HEADERS)

repo_root = Path(__file__).resolve().parent.parent.parent
urls_path = repo_root / "samples" / "property_urls.txt"
urls = urls_path.read_text('utf-8').strip().split('\n')
# Pick a diverse sample (positions 0, 100, 500, 1000, 2000)
sample_urls = [urls[i] for i in [0, 100, 500, 1000, 2000] if i < len(urls)]

for i, url in enumerate(sample_urls):
    print(f'\n=== Detail page {i+1}: {url} ===')
    r = s.get(url, timeout=20)
    slug = url.split('/')[-1]
    print(f'Status: {r.status_code}  Bytes: {len(r.content)}')

    soup = BeautifulSoup(r.content, 'lxml')
    title = soup.title.string if soup.title else ''
    print(f'Title: {title}')

    if 'just a moment' in title.lower() or 'cloudflare' in title.lower():
        print('CLOUDFLARE CHALLENGE - stopping')
        break

    # Save raw HTML
    Path(f'./samples/detail_{i+1}_{slug[:8]}.html').write_bytes(r.content)

    # Check for __NEXT_DATA__
    next_data_el = soup.find('script', {'id': '__NEXT_DATA__'})
    if next_data_el:
        try:
            data = json.loads(next_data_el.string)
            print('Found __NEXT_DATA__!')
            page = data.get('props', {}).get('pageProps', {})
            print(f'  pageProps keys: {list(page.keys())}')
            
            # Find the opportunity/property data
            opp = None
            for key in ['opportunity', 'property', 'listing', 'data', 'unit']:
                if key in page:
                    opp = page[key]
                    print(f'  Property data at pageProps.{key}')
                    break
            
            if opp is None:
                # Try to find any dict with 'price' or 'area'
                for key, val in page.items():
                    if isinstance(val, dict) and any(k in str(val).lower() for k in ['price', 'area', 'bedroom']):
                        opp = val
                        print(f'  Property-like data at pageProps.{key}')
                        break
            
            if opp:
                print(f'  Keys in property object: {list(opp.keys())[:30]}')
                # Save the property data
                Path(f'./samples/detail_{i+1}_{slug[:8]}_data.json').write_text(
                    json.dumps(opp, ensure_ascii=False, indent=2), encoding='utf-8')
            else:
                print(f'  No obvious property object found')
                # Save full pageProps
                Path(f'./samples/detail_{i+1}_{slug[:8]}_page_props.json').write_text(
                    json.dumps(page, ensure_ascii=False, indent=2), encoding='utf-8')
        except Exception as e:
            print(f'  Parse error: {e}')
    else:
        print('  No __NEXT_DATA__ found')
        # Check for other embedded data
        for script in soup.find_all('script')[:10]:
            txt = (script.string or '')[:200]
            if any(k in txt.lower() for k in ['price', 'bedroom', 'area', 'opportunity']):
                print(f'  Script snippet: {txt[:150]}')

    time.sleep(3)

print('\nRecon done!')
