import json, sys, statistics as st
rows = json.load(open(sys.argv[1]))
for mode in (4, 8):
    for fac in (1, 2, 3):
        sel = [r for r in rows if r["mode"]==mode]
        cs = sum(r["es"] <= fac*r["bs"] for r in sel); ca = sum(r["ea"] <= fac*r["ba"] for r in sel)
        # classification
        ok = sum((r["kd"]=="pair")==(r["kind"]=="pair") for r in sel)
        good = [r for r in sel if r["bs"] < 1e-3]
        print(f"mode {mode} fac {fac}: sigma covered {cs}/{len(sel)}, alpha covered {ca}/{len(sel)}, kind right {ok}/{len(sel)}; with bar<1e-3: {len(good)} cells,"
              f" sigma cov {sum(r['es']<=fac*r['bs'] for r in good)}, alpha cov {sum(r['ea']<=fac*r['ba'] for r in good)}")
sel=[r for r in rows if r["mode"]==8]
print("misses (mode 8, fac 1) sigma:")
for r in sel:
    if r["es"] > r["bs"]:
        print(f"  c{r['ci']} {r['kind']} {r['lane']} fam {r['fam']} {r['kd']} es {r['es']:.2e} bs {r['bs']:.2e} ea {r['ea']:.2e} ba {r['ba']:.2e} noise {r['noise']:.0e} {r['p']}")
print("wrong kind (mode 8):")
for r in sel:
    if (r["kd"]=="pair")!=(r["kind"]=="pair"):
        print(f"  c{r['ci']} {r['kind']} {r['lane']} fam {r['fam']} {r['kd']} es {r['es']:.2e} bs {r['bs']:.2e} {r['p']}")
