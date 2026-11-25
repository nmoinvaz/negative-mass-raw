import pickle, time, sympy as sp, sys
gens, a1 = pickle.load(open('gens.pkl','rb'))
U0, U2 = sp.symbols('U0 U2')
P = [sp.Poly(g, U0, U2) for g in gens]
print('degrees', [p.total_degree() for p in P], 'max coeff digits', max(len(str(abs(c.p))) + len(str(c.q)) for p in P for c in p.coeffs()), flush=True)
want = sp.groebner([2*U0 - a1, (a1 + U2)**2], U0, U2, order='lex')
# membership I in J, exact and cheap
print('I in J:', all(want.reduce(g)[1] == 0 for g in gens), flush=True)
meth = sys.argv[1]
T = time.time()
if meth == 'f5b':
    gb = sp.groebner(gens, U0, U2, order='lex', method='f5b')
elif meth == 'fglm':
    gb = sp.groebner(gens, U0, U2, order='grevlex').fglm('lex')
print(meth, round(time.time() - T, 1), gb.exprs, list(gb.exprs) == list(want.exprs), flush=True)
