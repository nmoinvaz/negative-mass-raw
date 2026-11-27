exec(open("/tmp/claude-1000/-home-nathan-Source-negative-mass-i226/6ce098f9-1c29-4ea1-b637-485e454079a0/scratchpad/slab.py").read())
Tc = 4.0
for D, hs in ((5, [0.01/2**0.5, 0.005/2**0.5, 0.0025/2**0.5, 0.00125/2**0.5]), (6, [0.005, 0.0025, 0.00125, 0.000625])):
    print("=== static D =", D)
    recs = [go(D, h, "static", 0.0, Tc, 6.0, "static double") for h in hs]
    print("   ratios:", ["%.3f" % (recs[k]["max"] / recs[k + 1]["max"]) for k in range(3)])
    for a in (16.0, 256.0):
        recs = [go(D, h, "static", 0.0, Tc, 6.0, f"static noise {a:g}", engine="diag", noise=a * 2.0 ** -52) for h in hs[:3]]
        print(f"   noise {a:g} ratios:", ["%.3f" % (recs[k]["max"] / recs[k + 1]["max"]) for k in range(2)])
    go(D, hs[2], "static", 0.0, Tc, 6.0, "static quad", engine="diag", dtype="f16")
