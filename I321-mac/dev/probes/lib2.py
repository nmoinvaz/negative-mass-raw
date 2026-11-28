import sympy as sp, pickle, time
import lib1 as L
from lib1 import Ser, DOM

V, U = sp.symbols('V U')
FIELDS = ['dr', 'dOm', 'dth', 'hv', 'hu']
BGF = ['r0', 'Om0', 'Th0']

def to_jets(expr):
    reps = {}
    for d in expr.atoms(sp.Derivative):
        a = b = 0
        for var, n in d.variable_count:
            if var == V: a += n
            else: b += n
        reps[d] = sp.Symbol(f"{d.expr.func.__name__}_{a}_{b}")
    for fn in FIELDS + BGF:
        reps[sp.Function(fn)(V, U)] = sp.Symbol(f"{fn}_0_0")
    return expr.xreplace(reps)

def load_ops():
    E0, E1 = pickle.load(open('E01.pkl', 'rb'))
    E0j = {k: to_jets(e) for k, e in E0.items()}
    ops = {}
    for k, e in E1.items():
        ej = to_jets(e)
        ops[k] = []
        for fn in FIELDS:
            for sym in sorted([s for s in ej.free_symbols if s.name.startswith(fn + '_')], key=lambda s: s.name):
                a, b = map(int, sym.name.split('_')[1:])
                co = sp.diff(ej, sym)
                assert not any(s.name.startswith(f + '_') for s in co.free_symbols for f in FIELDS), (k, fn, co)
                ops[k].append((fn, a, b, co))
    return E0j, ops

def evaluate(expr, env, memo=None):
    memo = {} if memo is None else memo
    def ev(e):
        if e in memo: return memo[e]
        if e.is_Symbol: out = env[e.name]
        elif e.is_Integer or e.is_Rational: out = Ser({(0, 0): L.cv(e)})
        elif e.is_Add:
            out = ev(e.args[0])
            for a in e.args[1:]: out = out + ev(a)
        elif e.is_Mul:
            out = ev(e.args[0])
            for a in e.args[1:]: out = out * ev(a)
        elif e.is_Pow:
            base, ex = e.args
            assert ex.is_Integer, e
            out = ev(base) ** int(ex)
        else: raise ValueError(e)
        memo[e] = out
        return out
    return ev(expr)

def make_env(bg):
    env = {}
    r0 = L.pi_to_ser(bg['r']); Om0 = L.pi_to_ser(bg['Om']); Th0 = L.pi_to_ser(bg['th'])
    for nm, s in (('r0', r0), ('Om0', Om0), ('Th0', Th0)):
        for a in range(4):
            for b in range(4):
                env[f"{nm}_{a}_{b}"] = s.jet(a, b)
    for nm in ('P0', 'P1', 'P2'):
        env[nm] = L.pi_to_ser(bg[nm])
    return env
