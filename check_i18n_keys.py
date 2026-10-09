import re
import json
from pathlib import Path
from app.core.i18n import TRANSLATIONS

with open('templates/index.html', encoding='utf-8') as f:
    content = f.read()

keys = sorted(list(set(re.findall(r'data-i18n=[\'"]([^\'"]+)[\'"]', content))))
print(f"Total data-i18n keys in index.html: {len(keys)}")

for lang in ['en', 'mr', 'hi']:
    cat = TRANSLATIONS.get(lang, {})
    missing = [k for k in keys if k not in cat]
    print(f"Missing in {lang}: ({len(missing)}) {missing}")
