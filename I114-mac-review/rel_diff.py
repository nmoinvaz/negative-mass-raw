"""Recompute #114's two top-gamma rtol 1e-12 checks from the stored partial files, sharing no code with convergence.py.

Usage: python3 rel_diff.py [--mutate=sign]   (run from this folder; reads ../I114-win/convergence_l{5,6}_w0.7603.partial.csv)
Pass: both rtol 1e-12 values have D < 0 and lie within 2.1e-4 relative of the base (#114's first acceptance criterion),
and each partial file holds 66 results with a `done` record for the rtol 1e-12 task and no `capped` or `died` record.
--mutate=sign flips the sign of each rtol 1e-12 value; the check must then fail. Exits 1 on any failure.
"""
import json, os, sys

MUT = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--mutate=')), None)
assert MUT in (None, 'sign')
HERE = os.path.dirname(os.path.abspath(__file__))
BASE, RTOL, BAR = 'base (rtol1e-10, phi_cut1e-9, R60)', 'rtol 1e-12', 2.1e-4
ok = True
for l, g in ((5, 6000.0), (6, 12000.0)):
    path = os.path.join(HERE, '..', 'I114-win', f'convergence_l{l}_w0.7603.partial.csv')
    rows, recs = {}, []
    for line in open(path):
        r = json.loads(line)
        if isinstance(r, list):
            rows[(r[0], r[1])] = r[2]
        else:
            recs.append(r)
    d, b = rows[(RTOL, g)], rows[(BASE, g)]
    if MUT == 'sign':
        d = -d  # planted failure
    rel = abs(d - b) / abs(b)
    done = any(r.get('done') == [RTOL, g] for r in recs)
    bad = [r for r in recs if 'capped' in r or 'died' in r]
    good = d < 0 and rel <= BAR and len(rows) == 66 and done and not bad
    ok &= good
    print(f"l={l} gamma={g:g}: D_rtol={d:+.12e} D_base={b:+.12e} rel={rel:.3e} results={len(rows)} "
          f"done={done} capped_or_died={len(bad)} -> {'pass' if good else 'FAIL'}")
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
