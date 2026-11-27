#!/usr/bin/env python3
"""I192-mac D2: a prototype of the Taylor table's rule and lookup in 90-digit decimal arithmetic (not library code),
on the planted problems PA to PG of README.md, with the controls' effects, and PH (a plane stepper through the table).

    python proto_table.py [--cases PA,PB,...] [--lanes f64,dd,qd] [--controls] [--steps-json OUT.json] [--ph]

The rule (README): for the series c_0 .. c_(nb-1) of every function about the step start b, the width w is the largest
h with |c_k| h^k <= tail * sum_j |c_j| h^j for k = nb-last .. nb-1 (bisection), the step is min(fraction w, limit),
limit = min(valid_to - b, rest of the path, hmax); breakpoints are f64 numbers. The lookup shifts the series of the
step that starts at or before x0 by delta = x0 - start (exact here: both are f64 values).
The planted coefficients are the exact recurrences below; the references are the closed forms; the table shares no
code with either.
"""
import argparse
import json
import math
import sys
import time
from decimal import Decimal as D, getcontext
from fractions import Fraction

getcontext().prec = 90

LANES = {
    "f64": dict(nb=20, tail=D("1e-13"), eps=D(1.1102230246251565e-16)),
    "dd": dict(nb=30, tail=D("1e-25"), eps=D(1.232595164407831e-32)),
    "qd": dict(nb=60, tail=D("1e-55"), eps=D(1.504632769052528e-64)),
}
FRACTION = D("0.3")
INF = D("Infinity")


def f64(x):
    """the f64 nearest to x, as a Decimal"""
    return D(float(x))


def dpow(x, n):
    r = D(1)
    for _ in range(n):
        r *= x
    return r


# ---------------------------------------------------------------- planted functions: (coefficients about x0, value)
class Fn:
    def __init__(self, name, coef, val):
        self.name, self.coef, self.val = name, coef, val


def c_inv2(x0, nb):
    c = [1 / (x0 * x0)]
    for k in range(nb - 1):
        c.append(-c[-1] * (k + 2) / ((k + 1) * x0))
    return c


def c_inv1(x0, nb):
    c = [1 / x0]
    for _ in range(nb - 1):
        c.append(-c[-1] / x0)
    return c


def c_far(x0, nb, a=30):
    c = [1 / (a - x0)]
    for _ in range(nb - 1):
        c.append(c[-1] / (a - x0))
    return c


def c_ramp(x0, nb):
    c = [D(0)] * nb
    if x0 >= 5:
        c = [3 * (x0 - 5) ** 2, 6 * (x0 - 5), D(3)] + [D(0)] * (nb - 3)
    return c


def c_pair(x0, nb):
    d = x0 - 12
    q = d * d + D("0.04")
    c = [1 / q, -2 * d / (q * q)]
    for k in range(2, nb):
        c.append((-2 * d * c[k - 1] - c[k - 2]) / q)
    return c[:nb]


def c_poly40(x0, nb):
    u = 1 + x0 / 4
    c = [dpow(u, 40)]
    for k in range(nb - 1):
        c.append(c[-1] * (40 - k) / ((k + 1) * 4 * u))
    return c


def c_cube(x0, nb):
    den = 1 - x0 ** 3
    c = []
    for k in range(nb):
        r = D(1 if k == 0 else 0)
        if k >= 1:
            r += 3 * x0 * x0 * c[k - 1]
        if k >= 2:
            r += 3 * x0 * c[k - 2]
        if k >= 3:
            r += c[k - 3]
        c.append(r / den)
    return c


def c_pole5(x0, nb):
    c = [1 / (x0 - 5)]
    for _ in range(nb - 1):
        c.append(-c[-1] / (x0 - 5))
    return c


def add(*cs):
    return lambda x0, nb: [sum(t) for t in zip(*[c(x0, nb) for c in cs])]


F_INV2 = Fn("1/x^2", c_inv2, lambda x: 1 / (x * x))
F_INV1 = Fn("1/x", c_inv1, lambda x: 1 / x)
F_FAR = Fn("1/(30-x)", c_far, lambda x: 1 / (30 - x))
F_PB = Fn("1/(30-x)+3(x-5)_+^2", add(c_far, c_ramp), lambda x: 1 / (30 - x) + 3 * max(x - 5, D(0)) ** 2)
F_PAIR = Fn("1/((x-12)^2+0.04)", c_pair, lambda x: 1 / ((x - 12) ** 2 + D("0.04")))
F_POLY = Fn("(1+x/4)^40", c_poly40, lambda x: dpow(1 + x / 4, 40))
F_CUBE = Fn("1/(1-x^3)", c_cube, lambda x: 1 / (1 - x ** 3))
F_POLE5 = Fn("1/(x-5)", c_pole5, lambda x: 1 / (x - 5))


def c_pp(x0, nb):
    # 1 + 2x + 3x^2 - x^4 about x0
    c = [1 + 2 * x0 + 3 * x0 ** 2 - x0 ** 4, 2 + 6 * x0 - 4 * x0 ** 3, 3 - 6 * x0 ** 2, -4 * x0, D(-1)]
    return c + [D(0)] * (nb - 5)


F_PP = Fn("1+2x+3x^2-x^4", c_pp, lambda x: 1 + 2 * x + 3 * x ** 2 - x ** 4)


def c_ps(x0, nb):
    # 1/(1 + 1e5 x) about x0: c_k = (-1e5)^k / (1 + 1e5 x0)^(k+1)
    den = 1 + 100000 * x0
    c = [1 / den]
    for _ in range(nb - 1):
        c.append(-100000 * c[-1] / den)
    return c


F_PS = Fn("1/(1+1e5 x)", c_ps, lambda x: 1 / (1 + 100000 * x))


def valid_pieces6(x, dirn):
    """pieces of length 6: the series about x is valid to the end of the piece that starts at x in direction dirn"""
    if dirn > 0:
        return D(math.floor(x / 6) * 6 + 6)
    return D(math.ceil(x / 6) * 6 - 6)


def valid_ramp(x, dirn):
    assert dirn > 0
    return D(5) if x < 5 else INF


def valid_none(x, dirn):
    return INF if dirn > 0 else -INF


class Case:
    def __init__(self, name, funcs, xa, xb, valid=valid_none, hmax=INF, lanes=("f64", "dd", "qd"), last=2):
        self.name, self.funcs, self.xa, self.xb, self.valid, self.hmax, self.lanes, self.last = (
            name, funcs, f64(xa), f64(xb), valid, hmax, lanes, last)


CASES = {
    "PA": Case("PA", [F_INV2, F_INV1, F_FAR], "1e-3", 25, valid_pieces6),
    "PB": Case("PB", [F_PB], 0, 20, valid_ramp),
    "PC": Case("PC", [F_PAIR], 10, 14),
    "PD": Case("PD", [F_POLY], 0, 3),
    "PE": Case("PE", [F_CUBE], 0, "0.9", hmax=D("0.5"), lanes=("dd", "qd")),
    "PF": Case("PF", [F_INV2, F_INV1, F_FAR], 25, "1e-3", valid_pieces6),
    "PG": Case("PG", [F_POLE5], 0, 10),
    "PP": Case("PP", [F_PP], "0.1", 3),
    "PS": Case("PS", [F_PS], 0, 1, lanes=("qd",)),
}


# ---------------------------------------------------------------- the rule
def tail_ok(sers, h, tail, last):
    for c in sers:
        nb = len(c)
        s = D(0)
        hk = D(1)
        worst = D(0)
        for k in range(nb):
            t = abs(c[k]) * hk
            s += t
            if k + last >= nb and t > worst:
                worst = t
            hk *= h
        if s != 0 and worst > tail * s:
            return False
    return True


def tail_ok_plain(sers, h, tail, last):
    """the same test in plain f64 (no scaling by powers of two): |c_k| h^k can underflow to 0 where c_k is large"""
    h = float(h)
    for c in sers:
        nb = len(c)
        s = 0.0
        hk = 1.0
        worst = 0.0
        for k in range(nb):
            t = abs(float(c[k])) * hk
            s += t
            if k + last >= nb and t > worst:
                worst = t
            hk *= h
        if s != 0 and worst > float(tail) * s:
            return False
    return True


def width(sers, cap, tail, last, iters=110, plain=False):
    if plain:
        ok = lambda h: tail_ok_plain(sers, h, tail, last)  # noqa: E731
        if ok(cap):
            return cap
        lo, hi = D(0), cap
        for _ in range(iters):
            mid = (lo + hi) / 2
            if ok(mid):
                lo = mid
            else:
                hi = mid
        return lo
    return width_exact(sers, cap, tail, last, iters)


def width_exact(sers, cap, tail, last, iters=110):
    if tail_ok(sers, cap, tail, last):
        return cap
    lo, hi = D(0), cap
    for _ in range(iters):
        mid = (lo + hi) / 2
        if tail_ok(sers, mid, tail, last):
            lo = mid
        else:
            hi = mid
    return lo


class Table:
    pass


def build(case, lane, ctl=None, last=None, tail=None, fraction=None, max_steps=20000, nb=None):
    """the table of `case` in the lane's parameters; ctl: None, 'wide', 'fraction_one', 'loose_tail', 'ignore_valid_to'"""
    P = LANES[lane]
    nb = nb or P["nb"]
    tail = tail if tail is not None else P["tail"]
    if ctl == "loose_tail":
        tail = D("1e-5")
    frac = fraction if fraction is not None else FRACTION
    if ctl == "fraction_one":
        frac = D(1)
    last = last if last is not None else case.last
    xa, xb = case.xa, case.xb
    dirn = 1 if xb >= xa else -1
    t = Table()
    t.dir, t.nb, t.tail, t.last, t.lane = dirn, nb, tail, last, lane
    t.start, t.end, t.width, t.valid, t.sers = [], [], [], [], []
    t.error = None
    b = xa
    while (xb - b) * dirn > 0:
        if len(t.start) >= max_steps:
            t.error = ("TooManySteps", b)
            break
        sers = [f.coef(b, nb) for f in case.funcs]
        v = case.valid(b, dirn)
        rest = abs(xb - b)
        limit = min(rest, case.hmax)
        if ctl != "ignore_valid_to":
            limit = min(limit, abs(v - b))
        w = width(sers, limit / frac, tail, last, plain=(ctl == "unscaled"))
        h = min(frac * w, limit)
        if ctl == "wide":
            h = limit
        if h >= rest:
            x1 = xb
        else:
            x1 = f64(b + dirn * h)
            if ctl != "ignore_valid_to" and v != INF and v != -INF and (x1 - v) * dirn > 0:
                x1 = v
        if x1 == b:
            t.error = ("Stall", b)
            break
        t.start.append(b)
        t.end.append(x1)
        t.width.append(w)
        t.valid.append(v)
        t.sers.append(sers)
        b = x1
    return t


# ---------------------------------------------------------------- the lookup and C1
def shift(c, delta, kk):
    """first kk coefficients of the series c about start, shifted by delta (repeated synthetic division)"""
    c = list(c)
    nb = len(c)
    for i in range(min(kk, nb)):
        for m in range(nb - 2, i - 1, -1):
            c[m] = c[m] + delta * c[m + 1]
    return c[:kk]


def jets_at(t, i, fidx, x0, ctl=None):
    delta = x0 - t.start[i]
    if ctl == "no_shift":
        delta = D(0)
    elif ctl == "shift_f64":
        delta = D(float(x0) - float(t.start[i]))  # the difference formed in f64 (rounded), then widened
    return shift(t.sers[i][fidx], delta, t.nb)


T_SAMPLES = [D(0), D("0.25"), D("0.5"), D("0.75"), D(1)]
U_SAMPLES = T_SAMPLES


def c1(case, t, ctl=None):
    """C1: the largest E over steps, functions, x0 and h; also where. E = |sum jets_k tt^k - f(x0 + tt)| / sum |jets_k| h^k"""
    worst = (D(0), None)
    dirn = t.dir
    for i in range(len(t.start)):
        s, e = t.start[i], t.end[i]
        V = t.valid[i]
        for ts in T_SAMPLES:
            x0 = f64(s + ts * (e - s))
            # a step that ends past xb or its valid_to by a control is sampled at its own end
            for fi, f in enumerate(case.funcs):
                jets = jets_at(t, i, fi, x0, ctl)
                room = (V - x0) * dirn if V not in (INF, -INF) else INF
                hmax_u = max(D(0), min(D("0.7") * t.width[i], room))
                for us in U_SAMPLES:
                    h = us * hmax_u
                    tt = dirn * h
                    x = x0 + tt
                    p = D(0)
                    for k in range(len(jets) - 1, -1, -1):
                        p = p * tt + jets[k]
                    sc = D(0)
                    hk = D(1)
                    for k in range(len(jets)):
                        sc += abs(jets[k]) * hk
                        hk *= h
                    try:
                        ref = f.val(x)
                    except Exception:  # the reference is infinite there (a pole): the polynomial is wrong by everything
                        err = INF
                        if err > worst[0]:
                            worst = (err, (i, fi, float(x0), float(h)))
                        continue
                    err = abs(p - ref) / sc if sc != 0 else abs(p - ref)
                    if err > worst[0]:
                        worst = (err, (i, fi, float(x0), float(h)))
    return worst


def c2(case, t):
    """C2 stats: max and min over steps of len / (0.3 w), steps cut by valid_to, hmax or xb counted apart, and violations
    of contiguity, direction and valid_to"""
    hi, lo, uncut = D(0), INF, 0
    viol = 0
    for i in range(len(t.start)):
        s, e = t.start[i], t.end[i]
        ln = abs(e - s)
        r = ln / (D("0.3") * t.width[i])
        cut = (e == case.xb) or (t.valid[i] not in (INF, -INF) and e == t.valid[i]) or ln >= case.hmax
        hi = max(hi, r)
        if not cut:
            lo = min(lo, r)
            uncut += 1
        if i + 1 < len(t.start) and t.end[i] != t.start[i + 1]:
            viol += 1
        if (e - s) * t.dir <= 0:
            viol += 1
        if t.valid[i] not in (INF, -INF) and (e - t.valid[i]) * t.dir > 0:
            viol += 1
    return hi, lo, uncut, viol


def fmt(x, n=3):
    if x is None:
        return "-"
    return f"{float(x):.{n}e}"


def run_case(name, lanes, controls, steps_out, lasts=None):
    case = CASES[name]
    for lane in lanes:
        if lane not in case.lanes:
            continue
        for last in (lasts or [case.last]):
            t0 = time.time()
            t = build(case, lane, last=last)
            bar = 10 * LANES[lane]["tail"]
            if t.error:
                print(f"{name} {lane} last={last}: ERROR {t.error[0]} at x={float(t.error[1])!r} after {len(t.start)} steps")
                steps_out[f"{name}/{lane}/last{last}"] = dict(error=t.error[0], x=float(t.error[1]), steps=len(t.start))
                continue
            err, where = c1(case, t)
            hi, lo, uncut, viol = c2(case, t)
            ln = [abs(t.end[i] - t.start[i]) for i in range(len(t.start))]
            print(
                f"{name} {lane:<3} last={last} nb={t.nb}: steps {len(t.start):5d}  len min {fmt(min(ln))} max {fmt(max(ln))}  "
                f"C1 maxE {fmt(err)} (bar {fmt(bar)}) {'PASS' if err <= bar else 'FAIL'} at {where}  "
                f"C2 len/(0.3w) max {fmt(hi, 6)} min-uncut {fmt(lo, 6)} viol {viol}  [{time.time()-t0:.0f}s]"
            )
            steps_out[f"{name}/{lane}/last{last}"] = dict(
                steps=len(t.start), start=[float(x) for x in t.start], end=[float(x) for x in t.end],
                width=[float(x) for x in t.width])
            if controls and last == (lasts or [case.last])[0]:
                for ctl in ("wide", "fraction_one", "loose_tail", "ignore_valid_to", "no_shift", "shift_f64"):
                    if ctl == "ignore_valid_to" and name not in ("PA", "PB", "PF"):
                        continue
                    tc = build(case, lane, ctl=ctl if ctl not in ("no_shift", "shift_f64") else None)
                    if tc.error:
                        print(f"   control {ctl:<16}: ERROR {tc.error[0]} at {float(tc.error[1])!r}")
                        continue
                    ec, wh = c1(case, tc, ctl if ctl in ("no_shift", "shift_f64") else None)
                    hc, lc, uc, vc = c2(case, tc)
                    print(
                        f"   control {ctl:<16}: steps {len(tc.start):5d}  C1 maxE {fmt(ec)} {'(fires)' if ec > bar else '(SILENT)'}  "
                        f"C2 len/(0.3w) max {fmt(hc, 4)} viol {vc}  {'(C2 fires)' if hc > D('1.000000000001') or vc else ''}"
                    )


# ---------------------------------------------------------------- PH: the plane stepper through the table of 1/x
def fr_inv(m):
    n = len(m)
    a = [[Fraction(m[i][j]) for j in range(n)] + [Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if a[r][c] != 0)
        a[c], a[p] = a[p], a[c]
        d = a[c][c]
        a[c] = [x / d for x in a[c]]
        for r in range(n):
            if r != c and a[r][c] != 0:
                f = a[r][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
    return [row[n:] for row in a]


def fr_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


PMAT = [[1, 1, 0, 1], [1, 2, 1, 1], [0, 1, 2, 1], [1, 1, 1, 3]]


def mmat():
    p = [[Fraction(x) for x in r] for r in PMAT]
    d = [[Fraction(0)] * 4 for _ in range(4)]
    for i, v in enumerate((1, -2, 3, -1)):
        d[i][i] = Fraction(v)
    m = fr_mul(fr_mul(p, d), fr_inv(PMAT))
    assert all(x.denominator == 1 for r in m for x in r)
    return [[D(int(x)) for x in r] for r in m]


def optimal_kt(tol, w=20):
    e = math.frexp(float(tol))[1] - 1
    m = float(tol) / 2.0 ** e
    L = -(e + (m - 1.0)) * math.log(2)
    k = 2
    while k * (2 * k + w) < L * (k + w):
        k += 1
    return k


def mgs2(cols):
    """modified Gram-Schmidt twice, columns as lists; returns the diagonal of R"""
    diag = []
    for c in range(len(cols)):
        for _ in range(2):
            for p in range(c):
                d = sum(a * b for a, b in zip(cols[p], cols[c]))
                cols[c] = [x - d * y for x, y in zip(cols[c], cols[p])]
        nrm = sum(x * x for x in cols[c]).sqrt()
        cols[c] = [x / nrm for x in cols[c]]
        diag.append(nrm)
    return diag


def run_ph(lane, fraction=None, ctl=None, report=True):
    P = LANES[lane]
    eps = P["eps"]
    tol = 100 * eps
    kt = optimal_kt(tol)
    nb = kt + 12
    case = Case("PH", [F_INV1], "1e-3", 40, valid_none)
    t = build(case, lane, tail=eps, nb=nb, fraction=fraction, ctl=ctl)
    assert not t.error, t.error
    M = mmat()
    xa, xb = case.xa, case.xb
    cols = [[D(PMAT[i][c]) for i in range(4)] for c in range(2)]
    diag = mgs2(cols)
    ln_gram = sum(d.ln() for d in diag)
    ln_vol = ln_gram
    x0 = xa
    steps = 0
    worst_reach = D(0)
    over = 0
    starts = t.start
    import bisect
    while x0 < xb:
        if steps >= 3000:  # a runaway (the table's jets are garbage and the planner's steps collapse): the check has failed
            if report:
                print(f"PH {lane} fraction={float(fraction if fraction is not None else FRACTION)} ctl={ctl}: STOPPED after {steps} plane steps at x = {float(x0):.6g} (a plane integration of 90 steps is the bar): FAIL")
            return False, INF
        i = max(0, bisect.bisect_right([float(s) for s in starts], float(x0)) - 1) if steps == 0 or True else 0
        delta = x0 - t.start[i]
        jets = shift(t.sers[i][0], delta, kt)
        co = [[[D(0)] * (kt + 1) for _ in range(4)] for _ in range(2)]
        for c in range(2):
            for r in range(4):
                co[c][r][0] = cols[c][r]
        for m in range(kt):
            for c in range(2):
                for r in range(4):
                    s = D(0)
                    for l in range(4):
                        if M[r][l] == 0:
                            continue
                        for j in range(m + 1):
                            s += M[r][l] * jets[j] * co[c][l][m - j]
                    co[c][r][m + 1] = s / (m + 1)
        e1 = max(abs(co[c][r][kt - 1]) for c in range(2) for r in range(4))
        e2 = max(abs(co[c][r][kt]) for c in range(2) for r in range(4))
        h1 = (tol / max(e1, D("1e-300"))) ** (D(1) / (kt - 1))
        h2 = (tol / max(e2, D("1e-300"))) ** (D(1) / kt)
        h = min(h1, h2, D(1))
        rest = xb - x0
        if h >= rest:
            h = rest
        elif h > D("0.6") * rest:
            h = D("0.5") * rest
        x1 = xb if h == rest else f64(x0 + h)
        hh = x1 - x0
        reach = (x1 - t.start[i]) / t.width[i]
        worst_reach = max(worst_reach, reach)
        if reach > 1:
            over += 1
        for c in range(2):
            for r in range(4):
                v = co[c][r][kt]
                for m in range(kt - 1, -1, -1):
                    v = v * hh + co[c][r][m]
                cols[c][r] = v
        dg = mgs2(cols)
        ln_vol += sum(d.ln() for d in dg)
        steps += 1
        x0 = x1
        if report and steps % 25 == 0:
            print(f"  .. PH {lane} plane step {steps} x = {float(x0):.6g} h = {float(hh):.3e} reach/w {float(reach):.4f}", flush=True)
    # exact plane: span P[:, :2]
    q = [[D(PMAT[i][c]) for i in range(4)] for c in range(2)]
    mgs2(q)
    # (I - Pi) Y
    err2 = D(0)
    for c in range(2):
        y = cols[c]
        for qq in q:
            d = sum(a * b for a, b in zip(qq, y))
            y = [a - d * b for a, b in zip(y, qq)]
        err2 += sum(a * a for a in y)
    perr = err2.sqrt()
    ref = ln_gram_ref() - (xb / xa).ln()
    lerr = abs(ln_vol - ref)
    pbar, lbar = 10000 * eps, 10000 * eps * max(D(1), abs(ref))
    if report:
        print(
            f"PH {lane:<3} fraction={float(fraction if fraction is not None else FRACTION)} ctl={ctl}: kt {kt} nb {nb} tail {fmt(eps)} "
            f"table steps {len(t.start)} plane steps {steps}  plane err {fmt(perr)} (bar {fmt(pbar)}) {'PASS' if perr <= pbar else 'FAIL'}  "
            f"ln_vol err {fmt(lerr)} (bar {fmt(lbar)}) {'PASS' if lerr <= lbar else 'FAIL'}  "
            f"max (shift+step)/w {fmt(worst_reach, 4)}, plane steps past w: {over}"
        )
    return perr <= pbar and lerr <= lbar, worst_reach


def ln_gram_ref():
    return D(5).ln() / 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default="PA,PB,PC,PD,PE,PF,PG,PP")
    ap.add_argument("--lanes", default="f64,dd,qd")
    ap.add_argument("--controls", action="store_true")
    ap.add_argument("--steps-json", default=None)
    ap.add_argument("--ph", action="store_true")
    ap.add_argument("--ph-fractions", default="0.3")
    ap.add_argument("--ph-controls", action="store_true")
    ap.add_argument("--ph-ctls", default="wide,fraction_one,loose_tail")
    a = ap.parse_args()
    out = {}
    lanes = a.lanes.split(",")
    for name in [c for c in a.cases.split(",") if c]:
        if name == "PE":
            run_case("PE", lanes, a.controls, out, lasts=[2, 3])
        elif name == "PS":
            case = CASES["PS"]
            for ctl in (None, "unscaled"):
                t = build(case, "qd", ctl=ctl)
                err, where = c1(case, t)
                bar = 10 * LANES["qd"]["tail"]
                print(f"PS qd ctl={ctl}: steps {len(t.start)} first step [{float(t.start[0])!r}, {float(t.end[0])!r}] width {fmt(t.width[0])}  C1 maxE {fmt(err)} (bar {fmt(bar)}) {'PASS' if err <= bar else 'FAIL'}")
        elif name == "PG":
            case = CASES["PG"]
            for lane in lanes:
                t = build(case, lane, max_steps=5000)
                print(f"PG {lane}: {t.error} after {len(t.start)} steps; last start {float(t.start[-1])!r}")
                t2 = build(Case("PG2", [Fn('1/(x-15)', lambda x0, nb: [(-1) ** k / (x0 - 15) ** (k + 1) for k in range(nb)], lambda x: 1 / (x - 15))], 0, 10), lane, max_steps=5000)
                print(f"PG {lane} with the pole moved to 15: error {t2.error}, steps {len(t2.start)}")
        else:
            run_case(name, lanes, a.controls, out)
    if a.ph:
        for fr in a.ph_fractions.split(","):
            for lane in lanes:
                run_ph(lane, fraction=D(fr))
        if a.ph_controls:
            for lane in lanes:
                for ctl in a.ph_ctls.split(","):
                    run_ph(lane, ctl=ctl)
    if a.steps_json:
        json.dump(out, open(a.steps_json, "w"))


if __name__ == "__main__":
    main()
