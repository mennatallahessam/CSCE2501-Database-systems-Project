# -*- coding: utf-8 -*-
"""Inspect saved sample HTML pages to map site fields to schema columns."""
import sys, os, re, json
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
from bs4 import BeautifulSoup

def inspect_page(html_path: Path):
    print(f'\n{"="*60}')
    print(f'File: {html_path.name}')
    soup = BeautifulSoup(html_path.read_bytes(), 'lxml')

    # Title contains: ProjectName — TypeSize m² · Bedrooms غرف · Location · PayMethod Price
    title = soup.title.string if soup.title else ''
    print(f'Title: {title}')

    # ALL text content in structured tags (dl, table, etc)
    print('\n--- Definition Lists (dl/dt/dd) ---')
    for dl in soup.find_all('dl'):
        for dt, dd in zip(dl.find_all('dt'), dl.find_all('dd')):
            print(f'  {dt.get_text(strip=True)}: {dd.get_text(strip=True)[:100]}')

    print('\n--- Table cells ---')
    for table in soup.find_all('table')[:3]:
        for row in table.find_all('tr')[:10]:
            cells = [td.get_text(strip=True)[:50] for td in row.find_all(['td', 'th'])]
            if any(cells):
                print(f'  {cells}')

    # Look for price/area/bedrooms in common patterns
    print('\n--- Common CSS classes with data ---')
    for cls in ['price', 'area', 'bedroom', 'bathroom', 'type', 'location',
                 'developer', 'project', 'amenity', 'description', 'payment',
                 'down', 'installment', 'gain', 'contract', 'floor', 'finish']:
        els = soup.find_all(class_=re.compile(cls, re.I))[:3]
        for el in els:
            txt = el.get_text(strip=True)[:100]
            if txt:
                print(f'  [{cls}] <{el.name} class="{" ".join(el.get("class", [])[:3])}">'
                      f' {txt}')

    # Structured data attributes (data-*)
    print('\n--- data-* attributes ---')
    for el in soup.find_all(lambda t: any(a.startswith('data-') for a in t.attrs)):
        attrs = {k: v for k, v in el.attrs.items() if k.startswith('data-')}
        txt = el.get_text(strip=True)[:60]
        if attrs:
            print(f'  <{el.name}> {attrs} | text: {txt}')
        if len(list(soup.find_all(lambda t: any(a.startswith('data-') for a in t.attrs)))) > 30:
            break

    # Find all numbers that look like prices
    page_text = soup.get_text()
    prices = re.findall(r'[\d,]+(?:\.\d+)?\s*(?:EGP|ج\.م|مليون)', page_text)
    print(f'\n--- Price-like strings ---')
    for p in prices[:10]:
        print(f'  {p}')

    areas = re.findall(r'[\d]+\s*(?:م²|sqm|m²|متر)', page_text)
    print(f'\n--- Area-like strings ---')
    for a in areas[:10]:
        print(f'  {a}')

    # Check for JSON in script tags
    print('\n--- Script tags with JSON-like content ---')
    for script in soup.find_all('script'):
        txt = script.string or ''
        if len(txt) > 100 and ('{' in txt or 'opportunity' in txt.lower()):
            # Look for JSON objects
            matches = re.findall(r'\{[^{}]{20,200}\}', txt)
            for m in matches[:3]:
                print(f'  {m[:200]}')

    # Print first 200 chars of ALL text content grouped by section
    print('\n--- All paragraphs/sections (first 20) ---')
    for el in soup.find_all(['h1', 'h2', 'h3', 'p', 'span', 'li'])[:20]:
        txt = el.get_text(strip=True)[:100]
        if txt and len(txt) > 5:
            print(f'  <{el.name}> {txt}')

# Inspect the first 2 saved samples
samples = list(Path('./samples').glob('detail_*.html'))
for p in samples[:2]:
    inspect_page(p)
