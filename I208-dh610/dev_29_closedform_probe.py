"""dev_29: the P2 relation of run_02 as a closed form for Omega3, against the Omega3 of run_02's grids (run_02_evals.json); no gate"""
import json
import mpmath as mp
mp.mp.dps = 300
ev = json.load(open("run_02_evals.json"))
pi, ln2, z3 = mp.pi, mp.ln2, mp.zeta(3)
cf = (22 * pi**4 + 240 * pi**2 * ln2**2 + 480 * ln2**4 - 14400 * z3 * ln2 - 17280 * z3) / 45
print("closed form  ", mp.nstr(cf, 60))
for n, e in ev.items():
    o = mp.mpf(e["Om3"])
    d = abs(o - cf)
    print(f"{n}: Omega3 - closed form = {mp.nstr(o - cf, 5)}  ({float(-mp.log10(d / abs(o))):.1f} digits)")
print("alternative form 22 pi^4/45 + 16 pi^2 ln^2 2/3 + 32 ln^4 2/3 - 320 zeta(3) ln 2 - 384 zeta(3):",
      mp.nstr(abs(cf - (22 * pi**4 / 45 + 16 * pi**2 * ln2**2 / 3 + 32 * ln2**4 / 3 - 320 * z3 * ln2 - 384 * z3)), 5))
print("-64 zeta(3)(5 ln2 + 6) + ... split:", mp.nstr(-64 * z3 * (5 * ln2 + 6), 30))
print("1/(D-3) coefficient Omega3/8 =", mp.nstr(cf / 8, 30))
