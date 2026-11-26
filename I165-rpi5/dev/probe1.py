import time, sympy as sp
from sympy import QQ
from sympy.polys.fields import field
t0=time.time()
K, rho,u,a,b,s = field("rho,u,a,b,s", QQ)
N1 = 1+s**2
D = u*(1-s**2)-2*s
v0 = b*(1-s**2)/N1; v1 = 2*s*b/N1; v2 = a*N1/D
Phi1 = (v0**2+v2**2-a**2)/u
Psi = -2*v0*v2
Phi3 = -b/rho + 2*v0*v1
def d(f,x): return f.diff(x)
# E = coefficient form
def Dx_parts(f): return d(f,u)*a + d(f,a)*Phi1 + d(f,b)*Psi, d(f,s)
def Dr_parts(f): return d(f,rho)+d(f,u)*b + d(f,a)*Psi + d(f,b)*Phi3, d(f,s)
x1,xs1 = Dx_parts(Psi); r1,rs1 = Dr_parts(Phi1)
x2,xs2 = Dx_parts(Phi3); r2,rs2 = Dr_parts(Psi)
# E1 = r1 + rs1*sr - x1 - xs1*sx ; E2 = r2 + rs2*sr - x2 - xs2*sx
E1z = r1-x1; E2z = r2-x2
# matrix M [sx,sr]^T = -[E1z,E2z]: M = [[-xs1, rs1],[-xs2, rs2]]
det = (-xs1)*rs2 - rs1*(-xs2)
sx = (-(E1z*rs2 - rs1*E2z))/det
sr = (-((-xs1)*E2z - (-xs2)*E1z))/det
print("det num/den", det.numer.as_expr().__class__, time.time()-t0)
print("det factor:", sp.factor(det.as_expr()))
print("sx den", sp.factor(sx.denom.as_expr()))
print("sr den", sp.factor(sr.denom.as_expr()))
print("sx num terms", len(sx.numer.terms()), "sr", len(sr.numer.terms()), time.time()-t0)
def Dx(f): return d(f,u)*a + d(f,a)*Phi1 + d(f,b)*Psi + d(f,s)*sx
def Dr(f): return d(f,rho)+d(f,u)*b + d(f,a)*Psi + d(f,b)*Phi3 + d(f,s)*sr
C = Dr(sx) - Dx(sr)
print("C numer terms", len(C.numer.terms()), "denom terms", len(C.denom.terms()), time.time()-t0)
print("C denom factor", sp.factor(C.denom.as_expr()))
Cn = C.numer.as_expr()
fl = sp.factor_list(Cn)
print("C numer factors", [(len(sp.Poly(f,*sp.symbols('rho u a b s')).terms()), m, sp.Poly(f,*sp.symbols('rho u a b s')).total_degree()) for f,m in fl[1]], time.time()-t0)
for f,m in fl[1]:
    if len(sp.Poly(f).terms())<12: print(m, f)
