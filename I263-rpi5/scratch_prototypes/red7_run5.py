import sys, time, pickle
src = open('red7_run.py').read().split("view(\"start\")")[0]
exec(src)
I, Fs = pickle.load(open('red7_state4.pkl', 'rb'))
I = sp.expand(I)
cp = sp.expand(coeff(I, 0, 0, 0))
cu = sp.collect(cp, u, evaluate=False)
c1 = sp.expand(cu.get(u, 0))
print("u part of pure:", c1)
pc = sp.Poly(c1, lt, th)
for (b, j), cf in pc.terms():
    # cf u th^j lt^b : F = -cf th^j lt^(b+1)/(b+1)
    apply(f"P_u_th{j}_lt{b}", -cf * th**j * lt**(b + 1) / (b + 1))
I = sp.expand(I)
assert not I.has(u) and not I.has(ui), "u left"
view("final")
pickle.dump((I, Fs), open('red7_state5.pkl', 'wb'))
# list masters
P = sp.Poly(I, C, D3, K2, th, lt)
mons = {}
for m, cf in P.terms():
    mons[m] = cf
print(len(mons), "master monomials (C, D3, K2, th, lt):")
for m in sorted(mons, key=lambda m: (-sum(m[:3]), m)):
    print(m)
