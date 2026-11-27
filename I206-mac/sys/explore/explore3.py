"""I206-mac: the randomized exploration of I191 (explore3_i191_orig.py, same cases, same random stream), with the first
orders of the windows (PHIS) taken from the environment and every series dumped for the Rust port.

    DMAX=9 PHIS=0.2,0.3,0.4,0.5,0.6,0.7,0.8 OUT=<prefix> python explore3.py <n cases> <seed>

writes <prefix>_rows.json (the rows of explore3_i191_orig.py) and <prefix>_series.txt, one line per (case, lane):

    ci lane kind noise K re im alpha c_0 ... c_K

where every number is its parts p0,p1,... (non-overlapping f64: 1 in f64, 2 in double-double, 4 in quad-double, the
value at the lane's precision is their sum) written with repr, which Rust parses back exactly; (re, im, alpha) is the
planted truth of the nearest singularity.
"""
import sys, time, random, json, os

sys.path.insert(0, ".")
from proto import *
import mpmath as mp
from helpers import inv_pairs, noisy

LANES = [("f64", 53, 30, 1.1e-16), ("dd", 106, 60, 1.2e-32), ("qd", 212, 120, 6e-64)]
NPARTS = {"f64": 1, "dd": 2, "qd": 4}
PHIS = [float(x) for x in os.environ.get("PHIS", "0.2,0.3,0.4,0.5,0.6").split(",")]
DMAX = int(os.environ.get("DMAX", "5"))
OUT = os.environ.get("OUT", "")
DA = tuple(range(1, DMAX + 1))
DB = tuple(range(2, DMAX + 1))


def nbrs(key, tab, mode):
    i, d = key
    if mode == 4:
        cand = [(i - 1, d), (i + 1, d), (i, d - 1), (i, d + 1)]
    else:
        cand = [(i + a, d + b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a, b) != (0, 0)]
    return [k for k in cand if k in tab]


def spread(tab, key, mode):
    nb = nbrs(key, tab, mode)
    if len(nb) < 2:
        return None
    e = tab[key]
    sig = abs(mp.mpc(e["sre"], e["sim"]))
    return (max(dist(e, tab[k]) for k in nb) / sig, max(abs(e["alpha"] - tab[k]["alpha"]) for k in nb))


def choose(tab, mode):
    best = None
    for key in tab:
        sp = spread(tab, key, mode)
        if sp is None:
            continue
        if best is None or sp[0] < best[1][0]:
            best = (key, sp)
    return best


def make_case(rng):
    kind = rng.choice(["real", "real", "pair", "two"])
    alpha = rng.choice([-2, -1, -1.5, -0.5, -0.3, 0.2, 0.5, 0.7, 1.5, 1e-6])
    tau = rng.choice([0, 3, 4, 6])
    amp = rng.uniform(0.5, 3)
    mod = rng.uniform(1.0, 2.5)
    if kind == "real":
        sg = mod * rng.choice([1, -1])
        return kind, dict(alpha=alpha, sigma=sg, tau=tau, amp=amp)
    if kind == "pair":
        return kind, dict(alpha=alpha, mod=mod, ang=rng.uniform(0.35, 1.4), tau=tau, amp=amp)
    a2 = rng.choice([-1, -0.5, 0.5, 1.5])
    ratio = rng.uniform(1.3, 2.0)
    return kind, dict(a1=alpha, s1=mod * rng.choice([1, -1]), a2=a2, ratio=ratio * rng.choice([1, -1]), r=rng.uniform(0.5, 2))


def build(kind, p, K, noise):
    if kind == "real":
        c = binom_series(p["alpha"], mpf(p["sigma"]), K, p["amp"])
        if p["tau"]:
            c = series_mul(c, inv_pairs(K, p["tau"]), K)
        tr = dict(sre=mpf(p["sigma"]), sim=mpf(0), alpha=mpf(p["alpha"]))
    elif kind == "pair":
        s = mp.mpc(mpf(p["mod"]) * mp.cos(mpf(p["ang"])), mpf(p["mod"]) * mp.sin(mpf(p["ang"])))
        c = [2 * v for v in real_part(binom_series(p["alpha"], s, K, p["amp"]))]
        if p["tau"]:
            c = series_mul(c, inv_pairs(K, p["tau"]), K)
        tr = dict(sre=mp.re(s), sim=mp.im(s), alpha=mpf(p["alpha"]))
    else:
        s2 = mpf(p["s1"]) * mpf(p["ratio"])
        c1 = binom_series(p["a1"], mpf(p["s1"]), K, 1)
        c2 = binom_series(p["a2"], s2, K, p["r"])
        c = [x + y for x, y in zip(c1, c2)]
        tr = dict(sre=mpf(p["s1"]), sim=mpf(0), alpha=mpf(p["a1"]))
    return noisy(c, noise, 11), tr


def parts(x, n):
    """x at the current precision as n non-overlapping f64 parts"""
    out, r = [], mp.mpf(x)
    for _ in range(n):
        f = float(r)
        out.append(f)
        r = r - mp.mpf(f)
    return ",".join(repr(f) for f in out)


def main(n, seed, series_file):
    rng = random.Random(seed)
    rows = []
    for ci in range(n):
        kind, p = make_case(rng)
        for lane, bits, K, eps in LANES:
            set_prec(bits)
            noise = 0 if ci % 3 else eps**0.6
            c, tr = build(kind, p, K, noise)
            if series_file is not None:
                npart = NPARTS[lane]
                tok = [str(ci), lane, kind, repr(float(noise)), str(K), parts(tr["sre"], npart), parts(tr["sim"], npart), parts(tr["alpha"], npart)]
                tok += [parts(v, npart) for v in c]
                series_file.write(" ".join(tok) + "\n")
            ta = cells_A(c, DA, PHIS)
            tb = cells_B(c, DB, PHIS)
            for mode in (4, 8):
                ca = choose(ta, mode)
                cb = choose(tb, mode)
                cands = []
                if ca:
                    cands.append(("A", ca, ta))
                if cb:
                    cands.append(("B", cb, tb))
                if not cands:
                    continue
                fam, (key, sp), tab = min(cands, key=lambda t: t[1][1][0])
                e = tab[key]
                es = float(dist(e, tr) / abs(mp.mpc(tr["sre"], tr["sim"])))
                ea = float(abs(e["alpha"] - tr["alpha"]))
                kd = "pair" if (fam == "B" and e.get("kind") == "pair") else "real"
                rows.append(dict(ci=ci, kind=kind, lane=lane, mode=mode, fam=fam, es=es, bs=float(sp[0]), ea=ea, ba=float(sp[1]), kd=kd, noise=float(noise), p=p))
        print("case", ci, "of", n, flush=True)
    return rows


if __name__ == "__main__":
    n = int(sys.argv[1])
    seed = int(sys.argv[2])
    t = time.time()
    print("PHIS", PHIS, "DMAX", DMAX, "seed", seed, "n", n, flush=True)
    sf = open(OUT + "_series.txt", "w") if OUT else None
    rows = main(n, seed, sf)
    if sf:
        sf.close()
    json.dump(rows, open(OUT + "_rows.json" if OUT else f"rows_d{DMAX}_{seed}.json", "w"))
    print("time", time.time() - t, "rows", len(rows))
