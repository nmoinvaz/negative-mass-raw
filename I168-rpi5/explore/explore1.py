import sympy as sp
G,p,q,nu=sp.symbols('G p q nu')
r,s,sig,y,m=sp.symbols('r s sigma y m')
A0 = p**2*(p**2-q)*(p**2+q)
A1 = G**2*p**2*q**2 + 4*G*p**4*q - 2*G*q**3 + 4*p**6 - 3*p**2*q**2
A2 = 2*(G*(q-p)+p**2)*(G**2*q**2+2*G*p**3+2*G*p**2*q+2*p**4-q**2)
N = sp.expand(A0+nu**2*A1+nu**4*A2)
print("N =",N)
# reduced
E = sp.expand(N.subs({p:nu**2*r, q:nu**2*s}))
R = sp.expand(sp.cancel(E/nu**8)).subs(nu,sp.sqrt(sig)); R=sp.expand(R)
print("R =", sp.collect(R, sig))
print("R sym under (G,r,s)->(-G,-r,-s):", sp.expand(R - R.subs({G:-G,r:-r,s:-s},simultaneous=True)))
# scaled y,m: r=G y, s=G m
Rs = sp.expand(R.subs({r:G*y, s:G*m},simultaneous=True)/G**4)
print("R/G^4 =", sp.collect(Rs, sig))
for k in range(0,8):
    print(k, sp.factor(Rs.coeff(sig,k)))
# N as cubic in q, coefficients in p
Pq = sp.Poly(N, q)
for k,c in zip(range(3,-1,-1),Pq.all_coeffs()):
    print("q^%d:"%k, sp.factor(c))
