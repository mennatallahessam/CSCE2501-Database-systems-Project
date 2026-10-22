# -*- coding: utf-8 -*-
"""Extract and display all ld+json structured data from sample pages."""
import sys, os, re, json
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
from bs4 import BeautifulSoup

def extract_all(html_path: Path):
    print(f'\n{"="*70}')
    print(f'FILE: {html_path.name}')
    soup = BeautifulSoup(html_path.read_bytes(), 'lxml')

    # 1. Extract ALL ld+json blocks
    print('\n--- ld+json blocks ---')
    for i, script in enumerate(soup.find_all('script', type='application/ld+json')):
        try:
            data = json.loads(script.string)
            print(f'\n  [{i}] @type: {data.get("@type")}')
            print(f'       {json.dumps(data, ensure_ascii=False, indent=4)[:2000]}')
        except:
            print(f'  [{i}] parse error')

    # 2. Extract ALL dl/dt/dd pairs
    print('\n--- dl/dt/dd pairs ---')
    for dl in soup.find_all('dl'):
        dts = dl.find_all('dt')
        dds = dl.find_all('dd')
        for dt, dd in zip(dts, dds):
            print(f'  DT: {dt.get_text(strip=True):<50} DD: {dd.get_text(strip=True)[:80]}')

    # 3. h1 and nearby metadata
    print('\n--- Page header ---')
    h1 = soup.find('h1')
    if h1:
        print(f'  H1: {h1.get_text(strip=True)}')
        # Next sibling paragraphs
        for sib in h1.find_next_siblings(['p', 'span', 'div'])[:5]:
            txt = sib.get_text(strip=True)[:100]
            if txt:
                print(f'  sibling <{sib.name}>: {txt}')

    # 4. All spans with "U-" pattern (listing ID)
    uid_spans = soup.find_all(string=re.compile(r'U-\d+'))
    print(f'\n--- Unit IDs ---')
    for s in uid_spans:
        print(f'  {s.strip()}')

    # 5. Description text (look for long text blocks)
    print('\n--- Long text blocks (description candidates) ---')
    for tag in ['p', 'div', 'section']:
        for el in soup.find_all(tag):
            txt = el.get_text(strip=True)
            if 100 < len(txt) < 2000 and not el.find_all(tag):  # leaf-ish element
                print(f'  <{tag}> ({len(txt)} chars): {txt[:200]}')
                if len(txt) > 150:
                    break

    # 6. Amenities / features list
    print('\n--- Lists (amenities candidates) ---')
    for ul in soup.find_all(['ul', 'ol']):
        items = [li.get_text(strip=True)[:60] for li in ul.find_all('li')]
        if items and any(items):
            print(f'  {items[:10]}')

    # 7. Breadcrumb for location
    print('\n--- Breadcrumb ---')
    for el in soup.find_all(attrs={'aria-label': re.compile('breadcrumb', re.I)}):
        print(f'  {el.get_text(separator=" > ", strip=True)[:200]}')
    for el in soup.find_all(class_=re.compile('breadcrumb', re.I)):
        print(f'  {el.get_text(separator=" > ", strip=True)[:200]}')

samples = sorted(Path('./samples').glob('detail_*.html'))
for p in samples:
    extract_all(p)
