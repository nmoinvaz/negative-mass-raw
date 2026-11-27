#!/usr/bin/env python3
"""Design prototype of the singularity locator (#191): mpmath at the lane's precision (53, 106, 212 bits).

Not the library: a design study on EXPLORATION cases that are not the planted suite of the README.
  A_d : ratio fit  r_k = c_k/c_(k-1) = b0 + b1/k + ... + bd/k^d          (Domb-Sykes; exact at d = 1 for (1-u/s)^a)
  B_d : three-term (1+1/k) c_(k+1) = (pi0 + .. + pid/k^d) c_k - (th0 + .. + thd/k^d) c_(k-1)
        (exact at d = 2 for a conjugate pair (1-u/s)^a + conj, or two real singularities of one exponent)
"""
import sys
import mpmath as mp

mp.mp.prec = 53


def set_prec(bits):
    mp.mp.prec = bits


def mpf(x):
    return mp.mpf(x)


# ---------------------------------------------------------------- planted series (exploration only)
def binom_series(alpha, sigma, K, amp=1):
    """coefficients of amp*(1 - u/sigma)^alpha, orders 0..K, sigma real or mpc"""
    alpha = mpf(alpha)
    c = [mp.mpmathify(amp)]
    for k in range(1, K + 1):
        c.append(c[-1] * (k - 1 - alpha) / (k * sigma))
    return c


def series_mul(a, b, K):
    return [mp.fsum(a[i] * b[k - i] for i in range(k + 1)) for k in range(K + 1)]


def exp_series(beta, K):
    out = [mpf(1)]
    for k in range(1, K + 1):
        out.append(out[-1] * beta / k)
    return out


def real_part(c):
    return [mp.re(v) for v in c]


# ---------------------------------------------------------------- fits
def lstsq(cols, rhs):
    """least squares by mpmath's Householder QR; cols: list of columns"""
    m = len(rhs)
    n = len(cols)
    A = mp.matrix(m, n)
    for j in range(n):
        for i in range(m):
            A[i, j] = cols[j][i]
    b = mp.matrix(rhs)
    x, res = mp.qr_solve(A, b)
    return [x[i] for i in range(n)], res


def ratio_fit(c, k0, d):
    K = len(c) - 1
    ks = [k for k in range(max(k0, 1), K + 1) if c[k - 1] != 0]
    if len(ks) < d + 3:
        return None
    r = [c[k] / c[k - 1] for k in ks]
    cols = [[(mpf(K) / k) ** j for k in ks] for j in range(d + 1)]
    try:
        x, res = lstsq(cols, r)
    except (ZeroDivisionError, ValueError):
        return None
    # r = sum_j B_j (K/k)^j = sum_j (B_j K^j) k^-j, so b_j = B_j K^j
    b = [x[j] * mpf(K) ** j for j in range(d + 1)]
    return b, res


def real_estimate(b):
    b0, b1 = b[0], b[1]
    if b0 == 0:
        return None
    return dict(sre=1 / b0, sim=mpf(0), alpha=-1 - b1 / b0)


def three_term_fit(c, k0, d):
    K = len(c) - 1
    ks = [k for k in range(max(k0, 1), K) if True]
    n = 2 * (d + 1)
    if len(ks) < n + 3:
        return None
    rows_rhs, colsA, colsB = [], [[] for _ in range(d + 1)], [[] for _ in range(d + 1)]
    rhs = []
    for k in ks:
        env = max(abs(c[k + 1]), abs(c[k]), abs(c[k - 1]))
        if env == 0:
            return None
        rhs.append((1 + mpf(1) / k) * c[k + 1] / env)
        for j in range(d + 1):
            colsA[j].append(c[k] * (mpf(K) / k) ** j / env)
            colsB[j].append(-c[k - 1] * (mpf(K) / k) ** j / env)
    try:
        x, res = lstsq(colsA + colsB, rhs)
    except (ZeroDivisionError, ValueError):
        return None
    pi = [x[j] * mpf(K) ** j for j in range(d + 1)]
    th = [x[d + 1 + j] * mpf(K) ** j for j in range(d + 1)]
    return pi, th, res


def three_term_estimate(pi, th):
    """nearest singularity (and the other) from the first-order coefficients; returns dict list, kind"""
    P0, P1 = pi[0], pi[1] - pi[0]
    Q0, Q1 = th[0], th[1] - th[0]
    disc = P0 * P0 - 4 * Q0
    if disc < 0:
        s = mp.sqrt(-disc) / 2
        z1 = mp.mpc(P0 / 2, -s)  # Im z < 0 so that sigma = 1/z has Im > 0
        z2 = mp.conj(z1)
        g1 = (P1 - Q1 / z1) / (z1 - z2)
        sg = 1 / z1
        return "pair", [dict(sre=mp.re(sg), sim=mp.im(sg), alpha=-1 - mp.re(g1), skew=abs(mp.im(g1)))]
    s = mp.sqrt(disc) / 2
    za, zb = P0 / 2 + s, P0 / 2 - s
    if abs(za) < abs(zb):
        za, zb = zb, za
    if za == 0:
        return None, []
    g1 = (P1 - Q1 / za) / (za - zb)
    out = [dict(sre=1 / za, sim=mpf(0), alpha=-1 - g1)]
    if zb != 0:
        g2 = -(P1 - Q1 / zb) / (za - zb)
        out.append(dict(sre=1 / zb, sim=mpf(0), alpha=-1 - g2))
    return "real2", out


# ---------------------------------------------------------------- cells, spreads, selection
PHIS = [0.2, 0.3, 0.4, 0.5, 0.6]


def cells_A(c, degs, phis=PHIS):
    K = len(c) - 1
    tab = {}
    for i, ph in enumerate(phis):
        k0 = max(2, int(round(ph * K)))
        for d in degs:
            f = ratio_fit(c, k0, d)
            if f is None:
                continue
            e = real_estimate(f[0])
            if e is not None:
                tab[(i, d)] = e
    return tab


def cells_B(c, degs, phis=PHIS):
    K = len(c) - 1
    tab = {}
    for i, ph in enumerate(phis):
        k0 = max(2, int(round(ph * K)))
        for d in degs:
            f = three_term_fit(c, k0, d)
            if f is None:
                continue
            kind, ests = three_term_estimate(f[0], f[1])
            if kind is not None and ests:
                e = dict(ests[0])
                e["kind"] = kind
                e["second"] = ests[1] if len(ests) > 1 else None
                tab[(i, d)] = e
    return tab


def dist(a, b):
    return abs(mp.mpc(a["sre"] - b["sre"], a["sim"] - b["sim"]))


def local_spread(tab, key, degs):
    i, d = key
    e = tab[key]
    nb = [(i - 1, d), (i + 1, d), (i, d - 1), (i, d + 1)]
    nb = [k for k in nb if k in tab]
    if len(nb) < 2:
        return None
    sig = abs(mp.mpc(e["sre"], e["sim"]))
    s_sigma = max(dist(e, tab[k]) for k in nb) / sig
    s_alpha = max(abs(e["alpha"] - tab[k]["alpha"]) for k in nb)
    return s_sigma, s_alpha


def select(tab, degs):
    best = None
    for key in tab:
        sp = local_spread(tab, key, degs)
        if sp is None:
            continue
        if best is None or sp[0] < best[1][0]:
            best = (key, sp)
    return best


def locate(c, degsA=(1, 2, 3, 4, 5), degsB=(2, 3, 4, 5), phis=PHIS, verbose=False):
    ta = cells_A(c, degsA, phis)
    tb = cells_B(c, degsB, phis)
    ba = select(ta, degsA)
    bb = select(tb, degsB)
    out = dict(A=None, B=None)
    if ba:
        out["A"] = dict(cell=ba[0], est=ta[ba[0]], bar_sigma_rel=ba[1][0], bar_alpha=ba[1][1])
    if bb:
        out["B"] = dict(cell=bb[0], est=tb[bb[0]], bar_sigma_rel=bb[1][0], bar_alpha=bb[1][1])
    return out


def fmt(x, n=3):
    return mp.nstr(x, n)


def report(name, c, truth, bits):
    r = locate(c)
    ts = abs(mp.mpc(truth["sre"], truth["sim"]))
    for fam in ("A", "B"):
        o = r[fam]
        if o is None:
            print(f"  {name} [{bits}] {fam}: none")
            continue
        e = o["est"]
        es = dist(e, truth) / ts
        ea = abs(e["alpha"] - truth["alpha"])
        extra = e.get("kind", "")
        print(
            f"  {name} [{bits}] {fam} cell {o['cell']} {extra:5s} sigma_rel_err {fmt(es)} (bar {fmt(o['bar_sigma_rel'])}"
            f" {'cov' if es <= o['bar_sigma_rel'] else 'MISS'}) alpha_err {fmt(ea)} (bar {fmt(o['bar_alpha'])}"
            f" {'cov' if ea <= o['bar_alpha'] else 'MISS'})"
        )


if __name__ == "__main__":
    pass
