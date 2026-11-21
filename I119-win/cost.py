"""Solve time of the 36 sectors of #119 at floor 0.04 (this folder's logs) against floor 0.07 (#111's and #118's logs,
including their pilots), per sector and by k reached. Reads `m = X: ... n = N, arpack (K eigenvalues to |mu| v_c = F ...),
T s` lines under each log's `== solve sigma R = S, disc D` header. Prints the totals and the ratio range by k."""
import glob
import os
import re
from collections import defaultdict

RAW = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(pattern):
    out = {}
    for f in sorted(glob.glob(os.path.join(RAW, pattern))):
        sig = disc = None
        for ln in open(f, encoding="utf-8-sig"):
            h = re.match(r"== solve sigma R = (\d+), disc ([AB])", ln)
            if h:
                sig, disc = float(h.group(1)), h.group(2)
            r = re.match(r"\s+m = ([\d.]+): h = .*n = (\d+), arpack \((\d+) eigenvalues to \|mu\| v_c = ([\d.]+).*, (\d+) s$", ln)
            if r:
                out[(sig, disc, float(r.group(1)))] = dict(n=int(r.group(2)), k=int(r.group(3)), floor=float(r.group(4)),
                                                           t=int(r.group(5)))
    return out


old = {}
for p in ("I111-win/solve-*.log", "I111-win/pilot-*.log", "I118-win/solve-*.log", "I118-win/pilot-*.log"):
    old.update(read(p))
new = read("I119-win/*.log")
SECT = [(2.0, d, m + 0.5) for d in "AB" for m in range(11)] + [(4.0, d, m + 0.5) for d in "AB" for m in range(4, 11)]
miss = [s for s in SECT if s not in old or s not in new]
print(f"sectors {len(SECT)}, missing in old or new: {miss}")
t_old = sum(old[s]["t"] for s in SECT if s in old and s in new)
t_new = sum(new[s]["t"] for s in SECT if s in old and s in new)
print(f"solve time at floor 0.07: {t_old} s = {t_old / 3600:.1f} h; at floor 0.04: {t_new} s = {t_new / 3600:.1f} h; ratio {t_new / t_old:.2f}")
by = defaultdict(list)
for s in SECT:
    if s in old and s in new:
        by[(old[s]["k"], new[s]["k"])].append((new[s]["t"] / old[s]["t"], s))
for (ko, kn), v in sorted(by.items()):
    lo, hi = min(v), max(v)
    print(f"k {ko} -> {kn}: {len(v)} sectors, ratio {lo[0]:.2f} (sigma R {lo[1][0]:g} {lo[1][1]} m {lo[1][2]:g}) to "
          f"{hi[0]:.2f} (sigma R {hi[1][0]:g} {hi[1][1]} m {hi[1][2]:g})")
print("new k by sector count:", {k: sum(1 for s in SECT if new[s]["k"] == k) for k in sorted({new[s]["k"] for s in SECT})})
print("new smallest |mu| v_c over the 36 files:", min(new[s]["floor"] for s in SECT), "largest:", max(new[s]["floor"] for s in SECT))
