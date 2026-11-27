exec(open("/tmp/claude-1000/-home-nathan-Source-negative-mass-i226/6ce098f9-1c29-4ea1-b637-485e454079a0/scratchpad/slab.py").read())
for D, hn, Tc, X in ((6, "0.005", 8.0, 12.0), (5, "0.00707107", 10.0, 15.0)):
    h, ps = pstar(D, hn)
    base = go(D, h, "S", ps - 1e-8, Tc, X, "S- base")
    for a in (16.0, 256.0):
        r = go(D, h, "S", ps - 1e-8, Tc, X, f"S- noise {a:g}", engine="diag", noise=a * 2.0 ** -52)
        print(f"     x{r['max']/base['max']:.3f}")
