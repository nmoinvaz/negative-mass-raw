"""Tabulate INSPIRE's citers of [SH02] (read from the stored JSON) and flag titles/abstracts by term.

usage: python -I citers.py inspire_sh02/page1.json OUTDIR
writes OUTDIR/citers.tsv (all citers: recid, date, arXiv id, first author, title, flags) and prints counts.
Flags are string matches on title + abstract, for sorting only; the verdict per paper is made by reading.
"""
import json, re, sys
src, out = sys.argv[1], sys.argv[2]
d = json.load(open(src))
hits = d['hits']['hits']
assert d['hits']['total'] == len(hits), (d['hits']['total'], len(hits))
TERMS = {
    'wormhole': r'wormhole|throat|traversible|traversable|ellis|drainhole|bronnikov',
    'collapse': r'collaps|black[- ]hole|horizon|trapped',
    'critical': r'critical|threshold|fine[- ]tun|scaling|exponent|choptuik|type[- ]?i\b|universal',
    'ghost': r'ghost|phantom|exotic|negative[- ]energy|nec\b|null energy',
    'dynamic': r'dynamic|evolution|numerical|simulat|stabil|instabil|unstable',
}
rows = []
for h in hits:
    m = h['metadata']
    title = m['titles'][0]['title']
    abst = ' '.join(a['value'] for a in m.get('abstracts', []))
    arx = (m.get('arxiv_eprints') or [{}])[0].get('value', '')
    au = (m.get('authors') or [{}])[0].get('full_name', '')
    date = m.get('earliest_date', '')
    text = (title + ' ' + abst).lower()
    flags = [k for k, p in TERMS.items() if re.search(p, text)]
    pub = ''
    if m.get('publication_info'):
        p = m['publication_info'][0]
        pub = ' '.join(str(p.get(k, '')) for k in ('journal_title', 'journal_volume', 'artid', 'year')).strip()
    rows.append((h['id'], date, arx, au, title.replace('\t', ' '), ','.join(flags), pub, len(abst)))
rows.sort(key=lambda r: r[1])
with open(out + '/citers.tsv', 'w') as f:
    f.write('recid\tdate\tarxiv\tfirst_author\ttitle\tflags\tpublication\tabstract_chars\n')
    for r in rows:
        f.write('\t'.join(str(x) for x in r) + '\n')
n = len(rows)
print('citers:', n, 'with arXiv id:', sum(1 for r in rows if r[2]), 'with abstract:', sum(1 for r in rows if r[7] > 0))
for k in TERMS:
    print(k, sum(1 for r in rows if k in r[5].split(',')))
print('wormhole+collapse:', sum(1 for r in rows if 'wormhole' in r[5] and 'collapse' in r[5]))
print('wormhole+critical:', sum(1 for r in rows if 'wormhole' in r[5] and 'critical' in r[5]))
print('wormhole+(collapse|critical)+dynamic:', sum(1 for r in rows if 'wormhole' in r[5] and ('collapse' in r[5] or 'critical' in r[5]) and 'dynamic' in r[5]))
