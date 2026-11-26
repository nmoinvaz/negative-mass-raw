# probe 3: general symbolic identity R = lam (g - rho^2 dphi^2) - alpha alpha for b = c(t) x + C(t) ln rho with the ODE; block of X(t,x)+R(t,rho)
import sys, time
sys.path.insert(0, "/home/nathan/Source/negative-mass-i166/notes/warp")
import sympy as sp
import phantom_source as ps
import same_sign_scalars as sss
t0=time.time()
t, x, rho, ph = sp.symbols("t x rho phi", positive=True)
Xg=[t,x,rho,ph]
c=sp.Function("c")(t); C=sp.Function("C")(t); d=sp.Function("d")(t)
b = c*x + C*sp.log(rho) + d
g = sp.Matrix([[-1+b**2,b,0,0],[b,1,0,0],[0,0,1,0],[0,0,0,rho**2]])
Ric = ps.ricci(g, Xg, lambda E,k: sp.diff(E,Xg[k]), sp.simplify)
print("ricci", f"{time.time()-t0:.0f}s", flush=True)
gam = sp.diff(C,t)/(2*C)
cp = 2*gam*c - gam**2
sub = {sp.Derivative(c,t): cp}
lam = C**2/(2*rho**2) + (gam-c)**2
v1 = C/rho; v2 = gam - c
alpha = sp.Matrix([v1*b, v1, v2, 0])  # alpha = v1 (dx + b dt) + v2 drho -> components (dt, dx, drho, dphi)
alpha = sp.Matrix([v1*b, v1, v2, 0])
dph = sp.Matrix([0,0,0,rho])
Mt = lam*(g - dph*dph.T) - alpha*alpha.T
diff = (Ric - Mt).applyfunc(lambda e: sp.simplify(sp.simplify(e).subs(sub)))
print(diff, f"{time.time()-t0:.0f}s")
# wrong ode
sub2 = {sp.Derivative(c,t): 2*gam*c + gam**2}
diff2 = (Ric - Mt).applyfunc(lambda e: sp.simplify(sp.simplify(e).subs(sub2)))
print("wrong ode ->", diff2.is_zero_matrix)
# the block of X(t,x)+R(t,rho)
Xf=sp.Function("X")(t,x); Rf=sp.Function("R")(t,rho)
b2 = Xf+Rf
g2 = sp.Matrix([[-1+b2**2,b2,0,0],[b2,1,0,0],[0,0,1,0],[0,0,0,rho**2]])
Ric2 = ps.ricci(g2, Xg, lambda E,k: sp.diff(E,Xg[k]), sp.simplify)
E_ = sp.Matrix([[1,0,0,0],[-b2,1,0,0],[0,0,1,0],[0,0,0,1/rho]])
Rf_ = (E_.T*Ric2*E_).applyfunc(sp.simplify)
P = sp.diff(Xf,t,x) - b2*sp.diff(Xf,x,2) - sp.diff(Xf,x)**2
S = sp.diff(Rf,rho,2)+sp.diff(Rf,rho)/rho
Q = -S/2; Y = -sp.diff(Rf,t,rho)/2 + sp.diff(Xf,x)*sp.diff(Rf,rho); h = sp.diff(Rf,rho)**2/2
blk = sp.Matrix([[P-h,Q,0,0],[Q,-P-h,Y,0],[0,Y,h,0],[0,0,0,0]])
print("block diff", (Rf_-blk).applyfunc(sp.simplify), f"{time.time()-t0:.0f}s")
