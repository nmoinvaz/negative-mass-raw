import sympy as sp, time
G,p,q,s = sp.symbols('G p q sigma')
A0 = p**2*(p**4-q**2)
A1 = G**2*p**2*q**2 + 4*G*p**4*q - 2*G*q**3 + 4*p**6 - 3*p**2*q**2
A2 = 2*(G*(q-p)+p**2)*(G**2*q**2 + 2*G*p**3 + 2*G*p**2*q + 2*p**4 - q**2)
N = A0 + s*A1 + s**2*A2
w = sp.symbols('w')
Nw = sp.expand(N.subs(q, w-p**2))
K=6
e = [0]
t0=time.time()
# solve order by order: Nw(w = sum s^k e_k) = O(s^{K+1})
wser = 0
for k in range(1,K+1):
    ek = sp.Symbol('ek')
    trial = wser + s**k*ek
    r = sp.expand(Nw.subs(w, trial))
    c = r.coeff(s,k)
    sol = sp.solve(c, ek)[0]
    sol = sp.factor(sol)
    e.append(sol)
    wser = wser + s**k*sol
    print(k, sol, time.time()-t0, flush=True)
