import re, sys, collections
p = int(sys.argv[2]) if len(sys.argv) > 2 else 32003
VARS = ("t", "u", "b", "v")

def parse_poly(txt):
    txt = txt.strip().replace(" ", "")
    if txt == "0":
        return {}
    out = {}
    # split into signed terms
    terms = re.findall(r"[+-]?[^+-]+", txt)
    for tm in terms:
        sgn = 1
        if tm[0] == "+":
            tm = tm[1:]
        elif tm[0] == "-":
            sgn = -1
            tm = tm[1:]
        coef = 1
        mon = [0, 0, 0, 0]
        for f in tm.split("*"):
            if f.isdigit():
                coef *= int(f)
            else:
                m = re.fullmatch(r"([tubv])(?:\^(\d+))?", f)
                if m is None:
                    raise ValueError(f"cannot parse factor {f!r} in {tm!r}")
                mon[VARS.index(m.group(1))] += int(m.group(2) or 1)
        out[tuple(mon)] = (out.get(tuple(mon), 0) + sgn * coef) % p
    return out

def load(fn):
    data = collections.OrderedDict()
    cur = None
    for line in open(fn):
        line = line.rstrip("\n")
        if line.startswith("S "):
            parts = line.split()
            k = int(parts[1])
            cur = {"G1": parts[3], "n": parts[5], "C": {}}
            data[k] = cur
        elif line.startswith("C "):
            _, i, rest = line.split(" ", 2)
            cur["C"][int(i)] = parse_poly(rest)
    return data

def polymul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] = (r[i + j] + x * y) % p
    return r

def interp(xs, ys):
    # Newton interpolation -> coefficient list (low to high)
    n = len(xs)
    coef = list(ys)
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) * pow(xs[i] - xs[i - j], -1, p) % p
    poly = [coef[-1]]
    for i in range(n - 2, -1, -1):
        poly = polymul(poly, [(-xs[i]) % p, 1])
        poly[0] = (poly[0] + coef[i]) % p
    return poly

def trim(a):
    while a and a[-1] == 0:
        a = a[:-1]
    return a

def polydivmod(a, b):
    a = a[:]
    q = [0] * max(1, len(a) - len(b) + 1)
    inv = pow(b[-1], -1, p)
    while len(trim(a)) >= len(b) and trim(a):
        a = trim(a)
        d = len(a) - len(b)
        c = a[-1] * inv % p
        q[d] = c
        for i, y in enumerate(b):
            a[i + d] = (a[i + d] - c * y) % p
        a = trim(a)
    return trim(q), trim(a)

def ratrecon(xs, ys):
    """Rational function reconstruction by the extended Euclid on (M, L); returns (num, den) low-to-high."""
    M = [1]
    for x in xs:
        M = polymul(M, [(-x) % p, 1])
    L = trim(interp(xs, ys))
    r0, r1 = M, L
    t0, t1 = [0], [1]
    n = len(xs)
    while len(trim(r1)) - 1 >= n // 2 + (n % 2):
        q, r = polydivmod(r0, r1)
        r0, r1 = r1, r
        t_new = trim([(a - b) % p for a, b in zip(t0 + [0] * (len(polymul(q, t1)) - len(t0)), polymul(q, t1) + [0] * (len(t0) - len(polymul(q, t1))))])
        t0, t1 = t1, t_new
    return trim(r1), trim(t1)

def evalpoly(a, x):
    r = 0
    for c in reversed(a):
        r = (r * x + c) % p
    return r

if __name__ == "__main__":
    data = load(sys.argv[1])
    ks = list(data)
    print("slices", len(ks), ks[0], ks[-1])
    for i in range(1, 6):
        sizes = [len(data[k]["C"][i]) for k in ks]
        degs = [max(sum(m) for m in data[k]["C"][i]) if data[k]["C"][i] else -1 for k in ks]
        supp_all = set.intersection(*[set(data[k]["C"][i]) for k in ks])
        print(f"cofactor {i}: terms min/max {min(sizes)}/{max(sizes)}, deg {min(degs)}/{max(degs)}, common support {len(supp_all)}")
    # Thiele-style test on a few monomials of the smallest cofactor
    i = 4
    common = sorted(set.intersection(*[set(data[k]["C"][i]) for k in ks]))
    for mon in common[:: max(1, len(common) // 6)][:6]:
        xs = ks
        ys = [data[k]["C"][i][mon] for k in ks]
        h = len(xs) // 2
        # use first 2/3 to reconstruct, last 1/3 to test
        n1 = (2 * len(xs)) // 3
        num, den = ratrecon(xs[:n1], ys[:n1])
        ok = all(evalpoly(num, x) == y * evalpoly(den, x) % p for x, y in zip(xs[n1:], ys[n1:]))
        print(f"cofactor {i} monomial {mon}: deg num {len(num)-1}, deg den {len(den)-1}, predicts held-out {ok}")
