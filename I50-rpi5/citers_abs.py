"""Print stored abstracts of INSPIRE citers of [SH02].
usage: python -I citers_abs.py page1.json ctx|abs RECID...
  ctx: for each recid (or all with 'ALLCRIT'), the text around term matches
  abs: full abstract
"""
import json, re, sys
d = json.load(open(sys.argv[1]))
mode = sys.argv[2]
want = sys.argv[3:]
byid = {h['id']: h['metadata'] for h in d['hits']['hits']}
CRIT = r'critical|threshold|fine[- ]tun|scaling|exponent|choptuik|type[- ]?i\b|universal'
if want == ['ALLCRIT']:
    want = [i for i, m in byid.items() if re.search(CRIT, (m['titles'][0]['title'] + ' ' + ' '.join(a['value'] for a in m.get('abstracts', []))).lower())]
for i in want:
    m = byid[i]
    t = m['titles'][0]['title']
    a = ' '.join(x['value'] for x in m.get('abstracts', []))
    arx = (m.get('arxiv_eprints') or [{}])[0].get('value', '-')
    print(f'## {i} {arx} {t[:110]}')
    if mode == 'abs':
        print(a)
    else:
        for mt in re.finditer(CRIT, (t + ' ' + a).lower()):
            s = (t + ' ' + a)
            print('   ...' + s[max(0, mt.start() - 90): mt.end() + 90].replace('\n', ' ') + '...')
    print()
