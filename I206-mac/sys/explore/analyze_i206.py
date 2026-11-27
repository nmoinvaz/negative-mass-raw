"""I206-mac: coverage of the exploration rows (mode 8, the eight-neighbor spread), the gate and its control.

    python analyze_i206.py <rows.json>...

Gate (README, criterion 2): at factor 2 the bar of s covers the error of s in at least 254 of the resolved cells (bar of
s below 5% of |s|), and in all but at most 2 of them. Control: the same count at factor 0.002 (the bars shrunk a
thousand times) must fall below 254, so that the check fails on a wrong input. The baseline of I191 (dev_02_analyze2.log):
256 resolved, 254 covered at factor 2.
"""
import json, statistics as st, sys

rows = []
for p in sys.argv[1:]:
    rows += json.load(open(p))
sel = [r for r in rows if r["mode"] == 8]
res = [r for r in sel if r["bs"] < 0.05]
print("rows (mode 8):", len(sel), "resolved (bar of s < 5% of |s|):", len(res))
out = {}
for fac in (0.002, 1, 2, 3):
    cov_s = sum(r["es"] <= fac * r["bs"] for r in res)
    cov_a = sum(r["ea"] <= fac * r["ba"] for r in res)
    right = sum((r["kd"] == "pair") == (r["kind"] == "pair") for r in res)
    out[fac] = (cov_s, cov_a)
    print(f"fac {fac}: resolved {len(res)} sigma cov {cov_s} (misses {len(res) - cov_s}) alpha cov {cov_a} kind right {right}")
for lane in ("f64", "dd", "qd"):
    rl = [r for r in sel if r["lane"] == lane]
    rr = [r for r in rl if r["bs"] < 0.05]
    ratios = [r["bs"] / max(r["es"], 1e-300) for r in rr]
    print(lane, "rows", len(rl), "resolved", len(rr), "median bar/err", st.median(ratios) if ratios else None,
          "median err", st.median([r["es"] for r in rr]) if rr else None)
print("unresolved (bs>=0.05):", [(r["ci"], r["kind"], r["lane"], round(r["bs"], 2), r["p"].get("alpha")) for r in sel if r["bs"] >= 0.05])
print("resolved misses at fac 2:")
for r in res:
    if r["es"] > 2 * r["bs"] or r["ea"] > 2 * r["ba"]:
        print(r)
cov2, miss2 = out[2][0], len(res) - out[2][0]
gate = cov2 >= 254 and miss2 <= 2
control_fires = out[0.002][0] < 254
print(f"GATE (covered >= 254 and misses <= 2 at factor 2): {'MET' if gate else 'NOT MET'} (covered {cov2} of {len(res)}, misses {miss2})")
print(f"CONTROL (factor 0.002 covers fewer than 254): {'FIRES' if control_fires else 'SILENT'} (covered {out[0.002][0]})")
