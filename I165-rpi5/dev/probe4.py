import time, sympy as sp, collections, pickle
from sympy import QQ
from sympy.polys.fields import field
t0=time.time()
K, u,b,v,s = field("u,b,v,s", QQ)   # rho = 1 invariants: b = rho*beta, v = rho*v2
N1 = 1+s**2
c = (1-s**2)/N1; sg = 2*s/N1
w = u*c - sg                  # = D/N1
A = v*w                       # a (invariant)
Phi1 = (b**2*c**2 + v**2 - A**2)/u
Psi = -2*b*c*v
Phi3b = 4*s*(1-s**2)*b**2/N1**2   # b + rho^2 Phi3
d=lambda f,x: f.diff(x)
# --- old-coordinate sigma via the same E1,E2 but expressed through functions of (u,A,B,s): derive via old formulas
# old coords fields: (u,A,B,s). Build sigma by solving E1,E2 in old coords then substitute A=v*w.
Ko, uo,ao,bo,so = field("u,a,b,s", QQ)
N1o=1+so**2; Do=uo*(1-so**2)-2*so
v0o=bo*(1-so**2)/N1o; v1o=2*so*bo/N1o; v2o=ao*N1o/Do
Phi1o=(v0o**2+v2o**2-ao**2)/uo; Psio=-2*v0o*v2o; Phi3o=4*so*(1-so**2)*bo**2/N1o**2 - bo
dd=lambda f,x: f.diff(x)
def drho(f,W): return W*f + ao*dd(f,ao) + bo*dd(f,bo)
def Dx(f,sx): return dd(f,uo)*ao + dd(f,ao)*Phi1o + dd(f,bo)*Psio + dd(f,so)*sx
def Dr(f,W,sr): return drho(f,W) + dd(f,uo)*bo + dd(f,ao)*Psio + dd(f,bo)*Phi3o + dd(f,so)*sr
x1,xs1 = Dx(Psio,0), dd(Psio,so); r1,rs1 = Dr(Phi1o,-2,0), dd(Phi1o,so)
x2,xs2 = Dx(Phi3o,0), dd(Phi3o,so); r2,rs2 = Dr(Psio,-2,0), dd(Psio,so)
E1z=r1-x1; E2z=r2-x2
det=(-xs1)*rs2 - rs1*(-xs2)
sxo=(-(E1z*rs2 - rs1*E2z))/det
sro=(-((-xs1)*E2z - (-xs2)*E1z))/det
# substitute a -> v*w, u,b,s same : evaluate rational function at a = v*w
def sub(fo):
    num = fo.numer.as_expr(); den = fo.denom.as_expr()
    U,Aa,Bb,S = sp.symbols('u a b s'); Vv=sp.Symbol('v')
    W_ = sp.Symbol('u')*(1-S**2)/(1+S**2) - 2*S/(1+S**2)
    return K.from_expr(num.subs(Aa, Vv*W_)) / K.from_expr(den.subs(Aa, Vv*W_))
sx = sub(sxo); sr = sub(sro)
print("sigma new coords", time.time()-t0)
print("sx den:", sp.factor(sx.denom.as_expr()))
print("sr den:", sp.factor(sr.denom.as_expr()))
# new-coordinate fields: components (u,b,v,s)
w_s = (-(u*sg + c))*2/N1
def comp(Yu, Yb, Ys, YA):      # YA = Y(A) in old coords
    Yw = Yu*c + w_s*Ys
    Yv = YA/w - v*Yw/w
    return (Yu, Yb, Yv, Ys)
# X1: Y(u)=A, Y(A)=Phi1, Y(B)=Psi, Y(s)=sx ; X2: Y(u)=b, Y(A)=a+Psi, Y(B)=Phi3b, Y(s)=sr
X1c = comp(A, Psi, sx, Phi1)
X2c = comp(b, Phi3b, sr, A+Psi)
def X(F,Y): return d(F,u)*Y[0] + d(F,b)*Y[1] + d(F,v)*Y[2] + d(F,s)*Y[3]
Cb = X(X2c[3] if False else sr, X1c) - X(sx, X2c) + sx      # X1(sr) - X2(sx) + sx
print("Cbar", time.time()-t0, len(Cb.numer.terms()), len(Cb.denom.terms()))
fl = sp.factor_list(Cb.numer.as_expr())
U_,B_,V_,S_=sp.symbols('u b v s')
print([(len(sp.Poly(f,U_,B_,V_,S_).terms()), m, sp.Poly(f,U_,B_,V_,S_).total_degree()) for f,m in fl[1]])
print("den", sp.factor(Cb.denom.as_expr()))
big=[f for f,m in fl[1] if len(sp.Poly(f,U_,B_,V_,S_).terms())>12]
P=sp.Poly(big[0],U_,B_,V_,S_); ms=P.monoms()
print("deg u,b,v,s", [max(m[i] for m in ms) for i in range(4)])
print("(b,v) pairs", sorted(collections.Counter((m[1],m[2]) for m in ms).items()))
pickle.dump(big,open("NC4new.pkl","wb"))
print("done", time.time()-t0)
