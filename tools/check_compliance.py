#!/usr/bin/env python3
"""Техническая самопроверка статической сборки; не заменяет юридическую проверку бизнеса."""
from pathlib import Path
from bs4 import BeautifulSoup
import re, sys

ROOT = Path(__file__).resolve().parents[1]
errors, warnings = [], []
html_files = list(ROOT.glob('*.html'))
for path in html_files:
    text = path.read_text(encoding='utf-8')
    for bad in ['fonts.googleapis.com','fonts.gstatic.com','instagram.com','facebook.com','wa.me','google-analytics.com','googletagmanager.com']:
        if bad in text.lower(): errors.append(f'{path.name}: найдена внешняя ссылка/сервис {bad}')
    tokens = re.findall(r'\[\[[A-Z0-9_]+\]\]', text)
    if tokens: errors.append(f'{path.name}: не заполнены реквизиты: {", ".join(sorted(set(tokens)))}')
    soup = BeautifulSoup(text, 'html.parser')
    for tag, attr in [('img','src'),('link','href'),('script','src')]:
        for el in soup.find_all(tag):
            value = el.get(attr)
            if not value or value.startswith(('http://','https://','data:','//','mailto:','tel:','sms:','#','/')):
                continue
            target = (ROOT/value.split('#',1)[0].split('?',1)[0]).resolve()
            if not target.exists(): errors.append(f'{path.name}: отсутствует локальный ресурс {value}')

index = (ROOT/'index.html').read_text(encoding='utf-8')
for needed in ['privacy.html','legal.html','Content-Security-Policy']:
    if needed not in index: errors.append(f'index.html: отсутствует {needed}')
if 'cookie' in index.lower() or 'localStorage' in index or 'document.cookie' in index:
    warnings.append('index.html: обнаружено упоминание cookies/storage — проверьте необходимость согласия')

print('ТЕХНИЧЕСКАЯ ПРОВЕРКА')
if warnings:
    print('\nПредупреждения:')
    for item in warnings: print(' -', item)
if errors:
    print('\nОшибки:')
    for item in errors: print(' -', item)
    sys.exit(1)
print('\nОшибок не найдено. Отдельно проверьте SSL, российский хостинг, реестр РКН и фактические бизнес-процессы.')
