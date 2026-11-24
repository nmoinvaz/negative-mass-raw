#!/usr/bin/env python3
"""ind51: the coordinator's independent check of #51 (novelty reading gaps and rerun searches). Criteria K1-K6 in I51-mac/README.md.

Fetches its own sources (GET only) into --dl; reads DG08 from I149-rpi5 (sha256 verified by I149-mac/ind149.py).
Shares no code with I51-rpi5's scripts.
"""
import argparse
import gzip
import io
import json
import os
import re
import sys
import tarfile
import urllib.error
import urllib.parse
import urllib.request

ap = argparse.ArgumentParser()
ap.add_argument('--raw', required=True)
ap.add_argument('--dl', required=True)
ap.add_argument('--mutate', default='')
args = ap.parse_args()
MUT = args.mutate
FAIL = []
UA = {'User-Agent': 'research-client/1.0'}


def check(name, ok, msg):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}", flush=True)
    if not ok:
        FAIL.append(name)


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()


def norm(t):
    return re.sub(r'\s+', ' ', t)


def eprint_text(url, out):
    data = get(url)
    os.makedirs(out, exist_ok=True)
    try:
        raw = gzip.decompress(data)
    except OSError:
        return ''
    if tarfile.is_tarfile(io.BytesIO(raw)):
        with tarfile.open(fileobj=io.BytesIO(raw)) as tf:
            tf.extractall(out, filter='data')
        t = ''
        for root, _, files in os.walk(out):
            for f in files:
                if f.endswith('.tex'):
                    t += open(os.path.join(root, f), encoding='utf-8', errors='replace').read() + '\n'
        return t
    return raw.decode('utf-8', 'replace')


# K1: Shirokov 2608.24577
abs_s = norm(get('https://arxiv.org/abs/2608.24577').decode('utf-8', 'replace'))
v2date = re.search(r'\[v2\][^<]*?</strong>\s*([^<]*?)\s*\(', abs_s) or re.search(r'\[v2\](.{0,120})', abs_s)
okd = bool(re.search(r'\[v2\].{0,200}26 Oct 2026', abs_s))
t1 = norm(eprint_text('https://arxiv.org/e-print/2608.24577v1', os.path.join(args.dl, 'shi_v1')))
t2 = norm(eprint_text('https://arxiv.org/e-print/2608.24577v2', os.path.join(args.dl, 'shi_v2')))
need_absent_v2 = ['0.63', '0.995']
if MUT == 'v2num':
    ok_v2 = '0.995' in t2
else:
    ok_v2 = not any(x in t2 for x in need_absent_v2)
ok1 = okd and '0.63' in t1 and '0.995' in t1 and ok_v2 and 'no sign of instability' in t2
check('K1', ok1, f"v2 dated 26 Oct 2026 {okd}; v1 has 0.63 {'0.63' in t1}, 0.995 {'0.995' in t1}; v2 has 0.63 {'0.63' in t2}, "
      f"0.995 {'0.995' in t2}, 'no sign of instability' {'no sign of instability' in t2}")

# K2: Paranjape 2025
q = urllib.parse.quote('t "Puzzles with Negative Mass"')
ins = json.loads(get(f'https://inspirehep.net/api/literature?q={q}&fields=titles,abstracts'))
abst = ' '.join(a.get('value', '') for h in ins.get('hits', {}).get('hits', []) for a in h['metadata'].get('abstracts', []))
src = 'INSPIRE'
if not abst:
    try:
        abst = re.sub(r'<[^>]+>', ' ', get('https://link.springer.com/chapter/10.1007/978-3-031-91266-5_14').decode('utf-8', 'replace'))
        src = 'Springer'
    except urllib.error.URLError as e:
        src = f'none ({e})'
abst = norm(abst)
has_possible = re.search(r'\bpossible\b', abst, re.I) is not None
ok2 = 'dynamically stable configuration' in abst and (has_possible if MUT == 'possible' else not has_possible)
check('K2', ok2, f"abstract from {src}, {len(abst)} chars: 'dynamically stable configuration' {'dynamically stable configuration' in abst}; "
      f"'possible' {has_possible}")

# K3: Ivanov 1204.1269
ia = norm(re.sub(r'<[^>]+>', ' ', get('https://arxiv.org/abs/1204.1269').decode('utf-8', 'replace')))
hg = 'Havas and Goldberg 1963' if MUT == 'havas' else 'Havas and Goldberg'
ok3 = hg in ia and 'equivalent' in ia
check('K3', ok3, f"'{hg}' {hg in ia}; 'equivalent' {'equivalent' in ia}")

# K4: Laguna 2611.14482
la = norm(re.sub(r'<[^>]+>', ' ', get('https://arxiv.org/abs/2611.14482').decode('utf-8', 'replace')))
le = norm(eprint_text('https://arxiv.org/e-print/2611.14482', os.path.join(args.dl, 'laguna')))
both = la + ' ' + le
if MUT == 'laguna':
    ok_nr = re.search(r'(?<!non)radial perturbations of singustars in a forthcoming', both) is not None
else:
    ok_nr = re.search(r'nonradial perturbations[^.]{0,80}forthcoming', both) is not None
ok4 = ok_nr and 'stable only for' in both
check('K4', ok4, f"nonradial perturbations ... forthcoming {ok_nr}; 'stable only for' {'stable only for' in both}")

# K5: DG08 versions
dd = os.path.join(args.raw, 'I149-rpi5')
tex = {}
for v, f in (('v1', 'dg08_v1/nm8.tex'), ('v2', 'dg08_v2/ivps02.tex'), ('v3', 'dg08_v3/ivps03.tex')):
    tex[v] = norm(open(os.path.join(dd, f), encoding='utf-8', errors='replace').read())
ws = {v: bool(re.search(r'We will set.{0,80}1/', t)) for v, t in tex.items()}
ms = {v: 'missing in the spectrum' in t for v, t in tex.items()}
ok5 = all(ws.values()) and ms['v2'] and ms['v3'] and not ms['v1']
check('K5', ok5, f"'We will set ... 1/' {ws}; 'missing in the spectrum' {ms}")

# K6: Price 1993
try:
    body = get('https://doi.org/10.1119/1.17293').decode('utf-8', 'replace')
    st = 200
    article = len(body) > 20000 and 'Just a moment' not in body and re.search(r'Newton', body) is not None
except urllib.error.HTTPError as e:
    st, article = e.code, False
check('K6', not article, f"doi.org status {st}; article body {article}")

print('ALL PASS' if not FAIL else 'FAILED: ' + ', '.join(FAIL))
sys.exit(1 if FAIL else 0)
