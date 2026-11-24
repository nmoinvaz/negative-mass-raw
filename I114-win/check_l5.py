"""Reads a convergence partial file (argv[1]) and prints, for the gamma in argv[2], the five D values, the relative
difference of the rtol 1e-12 value from the base, its sign, the spread over the same-r_m variants as convergence.py
computes it, and the wall and cpu seconds of the rtol 1e-12 evaluation from its `done` record. Independent of
convergence.py's printing code."""
import json
import sys

path, g = sys.argv[1], float(sys.argv[2])
D, done = {}, None
for line in open(path, encoding="utf-8"):
    r = json.loads(line)
    if isinstance(r, list) and r[1] == g and r[0] != "q":
        D[r[0]] = r[2]
    elif isinstance(r, dict) and r.get("done") == ["rtol 1e-12", g]:
        done = r
base = D["base (rtol1e-10, phi_cut1e-9, R60)"]
rt = D["rtol 1e-12"]
for k, v in D.items():
    print(f"{k:38s} {v:+.12e}")
print(f"rtol 1e-12 against base: relative difference {abs(rt - base) / abs(base):.3e} (limit 2.1e-4), "
      f"sign {'negative' if rt < 0 else 'NOT negative'}")
same = [v for k, v in D.items() if "phi_cut" not in k]
print(f"spread over the {len(same)} same-r_m variants: {(max(same) - min(same)) / abs(sum(same) / len(same)):.3e}")
nr = [v for k, v in D.items() if "phi_cut" not in k and k != "rtol 1e-12"]
print(f"spread without rtol 1e-12: {(max(nr) - min(nr)) / abs(sum(nr) / len(nr)):.3e}")
print(f"all five D negative: {all(v < 0 for v in D.values())}")
if done:
    print(f"rtol 1e-12 evaluation: wall {done['wall']:.0f} s ({done['wall'] / 3600:.2f} h), cpu {done['cpu']:.0f} s, "
          f"worker pid {done['pid']}")
