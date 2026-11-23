"""Cross-load: #133's P table (he_type3.shadow(), the runner's trusted table) against the coordinator's P from the
Ricci route (ind133b.py's D1). Criterion fixed before the run: the two are equal term by term in (phi, A', B')."""
import sys, sympy as sp
sys.argv = ['x']
ns = {}
exec(compile(open('ind133b.py').read().split('# ---- D6 exact ----')[0], 'ind133b-head', 'exec'), ns)
mine = {m: cf for m, cf in ns['P'].terms()}
sys.path.insert(0, sys.argv0 if False else '/Users/nathan/Source/negative-mass-wt133/notes/warp')
import he_type3 as H3
sh = H3.shadow()
theirs = {m: cf for m, cf in sp.Poly(sh["P"], H3.ph, H3.Ap, H3.Bp).terms()}
same = mine == theirs
print(f"coordinator P {len(mine)} terms, he_type3.shadow() P {len(theirs)} terms, equal term by term: {same}")
if not same:
    diff = set(mine.items()) ^ set(theirs.items())
    print("differing", sorted(diff)[:6])
sys.exit(0 if same else 1)
