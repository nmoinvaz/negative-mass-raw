import time, sympy as sp
from sympy import QQ
from sympy.polys.fields import field
t0=time.time()
K, u,a,b,s = field("u,a,b,s", QQ)   # rho = 1 (invariants A=rho a, B=rho beta)
N1 = 1+s**2
D = u*(1-s**2)-2*s
v0 = b*(1-s**2)/N1; v1 = 2*s*b/N1; v2 = a*N1/D
Phi1 = (v0**2+v2**2-a**2)/u
Psi = -2*v0*v2
Phi3b = 4*s*(1-s**2)*b**2/N1**2        # b + rho^2 Phi3 at rho = 1
d=lambda f,x: f.diff(x)
# Xbar1 = a d_u + Phi1 d_a + Psi d_b + sx d_s ; Xbar2 = b d_u + (a+Psi) d_a + Phi3b d_b + sr d_s
# compat: E1 = Dr(Phi1)-Dx(Psi), E2 = Dr(Psi)-Dx(Phi3) in 5D; at rho=1 use Euler: d_rho f = W f + a f_a + b f_b with W=weight
# weights: Phi1 has weight -2... do 5D with rho symbolic is safer; here do via rho derivative by Euler:
# Phi1 weight: Phi1=u_xx ~ k^-2 => W=-2 ; Psi: -2 ; Phi3: -2
def drho(f,W): return W*f + a*d(f,a) + b*d(f,b)
Phi3 = Phi3b - b   # rho=1
def Dx(f,sx): return d(f,u)*a + d(f,a)*Phi1 + d(f,b)*Psi + d(f,s)*sx
def Dr(f,W,sr): return drho(f,W) + d(f,u)*b + d(f,a)*Psi + d(f,b)*Phi3 + d(f,s)*sr
# E1 = Dr(Phi1) - Dx(Psi), weights -2
x1,xs1 = Dx(Psi,0), d(Psi,s)
r1,rs1 = Dr(Phi1,-2,0), d(Phi1,s)
x2,xs2 = Dx(Phi3,0), d(Phi3,s)
r2,rs2 = Dr(Psi,-2,0), d(Psi,s)
E1z=r1-x1; E2z=r2-x2
det = (-xs1)*rs2 - rs1*(-xs2)
sx = (-(E1z*rs2 - rs1*E2z))/det
sr = (-((-xs1)*E2z - (-xs2)*E1z))/det
print("sx,sr", time.time()-t0)
print("sx den:", sp.factor(sx.denom.as_expr()))
print("sr den:", sp.factor(sr.denom.as_expr()))
sxb, srb = sx, sr  # sigma-bar = rho*sigma at rho=1 : weight -1 -> value at rho=1 same
def X1(f): return d(f,u)*a + d(f,a)*Phi1 + d(f,b)*Psi + d(f,s)*sxb
def X2(f): return d(f,u)*b + d(f,a)*(a+Psi) + d(f,b)*Phi3b + d(f,s)*srb
Cb = X1(srb) - X2(sxb) + sxb
print("Cbar time", time.time()-t0, len(Cb.numer.terms()), len(Cb.denom.terms()))
fl = sp.factor_list(Cb.numer.as_expr())
print([(len(sp.Poly(f,*sp.symbols('u a b s')).terms()), m, sp.Poly(f,*sp.symbols('u a b s')).total_degree()) for f,m in fl[1]])
for f,m in fl[1]:
    if len(sp.Poly(f).terms())<12: print(m, f)
print("den", sp.factor(Cb.denom.as_expr()))
import pickle
big=[f for f,m in fl[1] if len(sp.Poly(f).terms())>12]
pickle.dump(big,open("NC4.pkl","wb"))
print("done", time.time()-t0)
