"""Coverage statistics of the randomized exploration rows (rows_1.json + rows_2.json): mode 8 (8-neighbour spread)."""
import json, statistics as st, sys
rows = []
for p in sys.argv[1:]:
    rows += json.load(open(p))
sel = [r for r in rows if r["mode"] == 8]
print("rows (mode 8):", len(sel))
for fac in (1, 2, 3):
    res = [r for r in sel if r["bs"] < 0.05]
    print("fac", fac, "resolved", len(res), "of", len(sel), "sigma cov", sum(r["es"] <= fac * r["bs"] for r in res),
          "alpha cov", sum(r["ea"] <= fac * r["ba"] for r in res),
          "kind right", sum((r["kd"] == "pair") == (r["kind"] == "pair") for r in res))
for lane in ("f64", "dd", "qd"):
    res = [r for r in sel if r["bs"] < 0.05 and r["lane"] == lane]
    ratios = [r["bs"] / max(r["es"], 1e-300) for r in res]
    print(lane, "n", len(res), "median bar/err", st.median(ratios), "median err", st.median([r["es"] for r in res]))
print("unresolved (bs>=0.05):", [(r["ci"], r["kind"], r["lane"], round(r["bs"], 2), r["p"].get("alpha")) for r in sel if r["bs"] >= 0.05])
print("resolved misses at fac 2:")
for r in sel:
    if r["bs"] < 0.05 and (r["es"] > 2 * r["bs"] or r["ea"] > 2 * r["ba"]):
        print(r)
