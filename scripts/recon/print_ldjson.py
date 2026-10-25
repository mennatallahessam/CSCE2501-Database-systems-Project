# -*- coding: utf-8 -*-
"""Print FULL ld+json from first sample."""
import sys, os, json
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from bs4 import BeautifulSoup

for p in sorted(Path('./samples').glob('detail_*.html'))[:3]:
    print(f'\n{"="*70}\nFILE: {p.name}')
    soup = BeautifulSoup(p.read_bytes(), 'lxml')
    for i, script in enumerate(soup.find_all('script', type='application/ld+json')):
        try:
            data = json.loads(script.string)
            print(f'\n--- ld+json block [{i}] @type={data.get("@type")} ---')
            print(json.dumps(data, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f'Error: {e}')
    
    print('\n--- dl/dt/dd ---')
    for dl in soup.find_all('dl'):
        for dt, dd in zip(dl.find_all('dt'), dl.find_all('dd')):
            print(f'  {dt.get_text(strip=True)}: {dd.get_text(strip=True)}')
    
    print('\n--- All page text (first 3000 chars) ---')
    print(soup.get_text(separator='\n', strip=True)[:3000])
