import re, sys, pickle, time
from fractions import Fraction
import sympy as sp
from sympy import QQ
from sympy.polys.rings import ring

VARS = ("t", "u", "b", "v")

def parse_signed(txt):
    txt = txt.strip().replace(" ", "")
    if txt == "0":
        return {}
    out = {}
    for tm in re.findall(r"[+-]?[^+-]+", txt):
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
                mon[VARS.index(m.group(1))] += int(m.group(2) or 1)
        out[tuple(mon)] = out.get(tuple(mon), 0) + sgn * coef
    return out

def load_prime(fn):
    C = {}
    G1 = None
    for line in open(fn):
        line = line.rstrip("\n")
        if line.startswith("G1"):
            G1 = line.split()[1]
        elif line.startswith("C "):
            _, i, rest = line.split(" ", 2)
            C[int(i)] = parse_signed(rest)
    return G1, C

def crt(res, mods):
    x, M = 0, 1
    for r, m in zip(res, mods):
        # solve x + M*k = r mod m
        k = ((r - x) * pow(M, -1, m)) % m
        x += M * k
        M *= m
    return x, M

def ratrec(a, M):
    """Rational reconstruction of a mod M with |num|, den <= sqrt(M/2); returns Fraction or None."""
    a %= M
    bound = int((M // 2) ** 0.5) if M < 10**300 else int(sp.integer_nthroot(M // 2, 2)[0])
    r0, r1 = M, a
    s0, s1 = 0, 1
    while r1 > bound:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    if s1 == 0 or abs(s1) > bound:
        return None
    return Fraction(r1, s1) if s1 > 0 else Fraction(-r1, -s1)

def reconstruct(files, primes):
    data = [load_prime(f) for f in files]
    out = {}
    nc = len(data[0][1])
    for i in range(1, nc + 1):
        mons = set()
        for _, C in data:
            mons |= set(C[i])
        pol = {}
        for mon in mons:
            res = [C[i].get(mon, 0) % p for (_, C), p in zip(data, primes)]
            x, M = crt(res, primes)
            fr = ratrec(x, M)
            if fr is None:
                return None, i, mon
            if fr != 0:
                pol[mon] = fr
        out[i] = pol
    return out, None, None

if __name__ == "__main__":
    tag = sys.argv[1]
    s0 = sp.Rational(sys.argv[2])
    primes = [int(x) for x in open(f"{tag}_primes.txt").read().split()]
    G = pickle.load(open("gens_l2.pkl", "rb"))
    Dl = sp.sympify(pickle.load(open("delta.pkl", "rb"))[0])
    U, B, V, S = sp.symbols("u b v s")
    R, t, u, b, v = ring("t,u,b,v", QQ)
    def slice_ring(d):
        out = {}
        for (mu, mb, mv, ms), c in d.items():
            key = (0, mu, mb, mv)
            out[key] = out.get(key, 0) + sp.Rational(c) * s0**ms
        return R.from_dict({k: QQ(x.p, x.q) for k, x in out.items() if x != 0})
    fs = [slice_ring(G[nm]) for nm in ["f0", "f1", "f2", "f11"]]
    Dls = R.from_expr(sp.expand(Dl.subs(S, s0)).subs({U: sp.Symbol("u"), B: sp.Symbol("b"), V: sp.Symbol("v")}))
    Dps = R.from_expr(sp.expand(U * (1 - s0**2) - 2 * s0).subs(U, sp.Symbol("u")))
    P = u * v * b * Dps * Dls
    gens = fs + [1 - t * P]
    for k in range(3, len(primes) + 1):
        files = [f"{tag}_p{p}.txt" for p in primes[:k]]
        t0 = time.time()
        C, bad_i, bad_m = reconstruct(files, primes[:k])
        if C is None:
            print(f"{k} primes: rational reconstruction fails at cofactor {bad_i} monomial {bad_m}")
            continue
        tot = R.zero
        for i, g in enumerate(gens, start=1):
            c = R.from_dict({m: QQ(x.numerator, x.denominator) for m, x in C[i].items()})
            tot += c * g
        print(f"{k} primes: identity sum c_i g_i == {tot if len(tot.terms()) < 3 else '(non-constant, %d terms)' % len(tot.terms())}  [{time.time()-t0:.1f} s]")
        if tot == R.one or (len(tot.terms()) == 1 and tot.terms()[0][0] == (0, 0, 0, 0)):
            maxnum = max(abs(x.numerator) for c in C.values() for x in c.values())
            maxden = max(x.denominator for c in C.values() for x in c.values())
            print(f"  verified over Q; max |numerator| {len(str(maxnum))} digits, max denominator {len(str(maxden))} digits; terms {[len(C[i]) for i in C]}")
            break
