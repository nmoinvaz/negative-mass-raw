import pickle, sympy as sp, collections
u,a,b,s = sp.symbols('u a b s')
f = pickle.load(open("NC4.pkl","rb"))[0]
P = sp.Poly(f,u,a,b,s)
ms = P.monoms()
print("terms",len(ms))
print("deg u,a,b,s:", [max(m[i] for m in ms) for i in range(4)], "min", [min(m[i] for m in ms) for i in range(4)])
print("a,b exponent pairs:", sorted(collections.Counter((m[1],m[2]) for m in ms).items()))
print("parity (a+b):", collections.Counter((m[1]+m[2])%2 for m in ms), "parity a", collections.Counter(m[1]%2 for m in ms), "parity b", collections.Counter(m[2]%2 for m in ms))
print("s parity", collections.Counter(m[3]%2 for m in ms), "u par", collections.Counter(m[0]%2 for m in ms))
print("joint parities (a,b,u+s?):", collections.Counter((m[1]%2,m[2]%2,(m[0]+m[3])%2) for m in ms))
print("coeff size", max(abs(c) for c in P.coeffs()))
