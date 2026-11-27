exec(open("/tmp/claude-1000/-home-nathan-Source-negative-mass-i226/6ce098f9-1c29-4ea1-b637-485e454079a0/scratchpad/slab.py").read())
for D, hn, hx, Tc, X in ((6, "0.00125", 0.000625, 8.0, 12.0), (5, "0.00176777", 0.00125/2**0.5, 10.0, 15.0)):
    for side in (-1, 1):
        for hh in ([pstar(D, hn)[0]], [hx]):
            h = hh[0]; ps = pstar(D, hn)[1]  # p*_h for the extension h: needs its own bisection; use finest #40 p* scaled by h^2 (dev only)
            if hh[0] == hx:
                ps = ps * (hx / pstar(D, hn)[0]) ** 2
            go(D, h, "S", ps + side * 1e-8, Tc, X, f"S side {side:+d}")
