import sympy as sp
G,p,q,nu=sp.symbols('G p q nu')
r,s,sig,y,m,e,g2,w,om=sp.symbols('r s sigma y m e g2 w omega')
A0 = p**2*(p**2-q)*(p**2+q)
A1 = G**2*p**2*q**2 + 4*G*p**4*q - 2*G*q**3 + 4*p**6 - 3*p**2*q**2
A2 = 2*(G*(q-p)+p**2)*(G**2*q**2+2*G*p**3+2*G*p**2*q+2*p**4-q**2)
N = sp.expand(A0+nu**2*A1+nu**4*A2)
Rr = sp.expand(sp.cancel(sp.expand(N.subs({p:nu**2*r,q:nu**2*s}))/nu**8)).subs(nu,sp.sqrt(sig))
Rr = sp.expand(Rr)
# scaled in (y, e): r = G y, s = G m, m=(e - y^2)/2, G^2=g2
rho = sp.expand(sp.expand(Rr.subs({r:G*y, s:G*(e-y**2)/2},simultaneous=True)/G**4).subs(G,sp.sqrt(g2)))
print("rho =",sp.collect(rho,sig))
K1 = sp.factor(sp.expand(rho.coeff(sig,1)/((e-y**2)**2/4)))
print("K1 =",sp.expand(K1))
K2 = sp.expand(rho.coeff(sig,2)/y**2)
print("K2 =",sp.collect(K2,g2))
print("sig3:",sp.factor(rho.coeff(sig,3)),"sig4:",sp.factor(rho.coeff(sig,4)))
# the cubic in w: N/p^6 with q=p^2 w, omega=2 G nu^2/p
Pw = sp.expand(sp.simplify(N.subs(q,p**2*w)/p**6))
print(sp.collect(Pw,w))
# claim P(w) = -2G s kappa w^3 - (mu + (G^2-1) s om) w^2 + 4 G s c w + c^2 - om^2, s=nu^2, om=2 G nu^2/p
S=nu**2; kap=1-(G**2-1)*S; mu=1+3*S-G**2*S+2*S**2-6*G**2*S**2; c=1+2*S
Pclaim = -2*G*S*kap*w**3 - (mu+(G**2-1)*S*om)*w**2 + 4*G*S*c*w + c**2 - om**2
print("P claim diff:", sp.simplify(Pclaim.subs(om,2*G*nu**2/p)-Pw))
