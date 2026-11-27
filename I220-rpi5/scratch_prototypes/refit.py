"""prototype: Omega4 from #195's 64 W^2 values with Omega0 .. Omega3 fixed (closed forms), polynomial extrapolation in 1/s"""
import json
import re
import sys
import mpmath as mp

mp.mp.dps = 120
w2file = "/home/nathan/Source/negative-mass-i220/notes/wormhole_largeD/w2_output.txt"
lst = {}
for line in open(w2file):
    m = re.match(r"\s*D=(\d+)\s+(\S+)\s+digits qd/od", line)
    if m:
        lst[int(m.group(1))] = mp.mpf(m.group(2))
ev = json.load(open("/home/nathan/Source/negative-mass-raw/I220-rpi5/dev_07_cnom.json"))
om4 = mp.mpf(ev["G1"]["Om4"])
pi, ln2, z3 = mp.pi, mp.ln2, mp.zeta(3)
O = [-4 * ln2, 2 * pi**2 / 3 + 8 * ln2**2, 80 * z3 - mp.mpf(8) / 3 * pi**2 * ln2 - mp.mpf(32) / 3 * ln2**3,
     22 * pi**4 / 45 + mp.mpf(16) / 3 * pi**2 * ln2**2 + mp.mpf(32) / 3 * ln2**4 - 320 * z3 * ln2 - 384 * z3]
Ds = sorted(lst)
print(len(Ds), Ds[:3], Ds[-3:])
pts = []
for D in Ds:
    s = mp.mpf(2 * (D - 3))
    y = (lst[D] - (s + O[0] + O[1] / s + O[2] / s**2 + O[3] / s**3)) * s**4
    pts.append((1 / s, y))
# extrapolate to t = 0 with K points: choose the K points of the window [a, a + K)
print("Omega4 (G1 of dev_07) =", mp.nstr(om4, 40))
for K in (6, 10, 14, 18, 22, 26, 30, 36, 44):
    for a in (len(pts) - K, len(pts) - K - 6 if len(pts) - K - 6 >= 0 else 0, 0):
        w = pts[a:a + K]
        # Lagrange value at 0
        est = mp.mpf(0)
        for i, (ti, yi) in enumerate(w):
            L = mp.mpf(1)
            for j, (tj, _) in enumerate(w):
                if j != i:
                    L *= (0 - tj) / (ti - tj)
            est += L * yi
        print(f"K = {K:2d} window start {a:2d}: est - Omega4 = {mp.nstr(est - om4, 5)}")
