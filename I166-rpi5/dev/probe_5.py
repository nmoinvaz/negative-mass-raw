import sys, time
sys.path.insert(0, "/home/nathan/Source/negative-mass-i166/notes/warp")
import sympy as sp
t0=time.time()
p1,m1,f0,ra,rb,ia,ib,s = sp.symbols("p1 m1 f0 ra rb ia ib s")
def EB(p,m,F,g): return m**2*g - p*m**2*F + p**2
eqs2=[EB(p1,m1,f0**2,f0**2*ia**2/4), EB(p1,m1,f0**2,f0**2*ib**2/4), ia*ra-1, ib*rb-1]
Gu = sp.groebner(eqs2+[1-s*p1*m1*f0*(ra-rb)], s,p1,m1,f0,ra,rb,ia,ib, order="grevlex")
print("const f case:", Gu.exprs, f"{time.time()-t0:.1f}s")
# mutated EB sign: m^2 g + p m^2 F + p^2  -> still contradiction? and separation
p2,m2,Fa,Fb,ga,gb = sp.symbols("p2 m2 Fa Fb ga gb")
def EBm(p,m,F,g): return m**2*g + p*m**2*F + p**2
eqs=[EBm(p1,m1,Fa,ga),EBm(p1,m1,Fb,gb),EBm(p2,m2,Fa,ga),EBm(p2,m2,Fb,gb)]
Gs = sp.groebner(eqs+[1-s*p1*p2*m1*m2*(Fa-Fb)], s, p1,p2,m1,m2,Fa,Fb,ga,gb, order="grevlex")
for tgt in (p1-p2, m1**2-m2**2): print("mut member", tgt, Gs.reduce(tgt)[1]==0)
t = sp.Symbol("t"); kap = sp.Function("kappa")(t); G = sp.Function("G")(t)
print(sp.dsolve(sp.Eq(G.diff(t), 2*kap*G), G))
rho = sp.Symbol("rho", positive=True); Rf = sp.Function("R")(rho)
print(sp.dsolve(sp.Eq(Rf.diff(rho,2)+Rf.diff(rho)/rho,0), Rf))
c = sp.Function("c")(t); Cf = sp.Function("C")(t)
gam = Cf.diff(t)/(2*Cf)
try:
    print(sp.dsolve(sp.Eq(c.diff(t), 2*gam*c-gam**2), c))
except Exception as e: print("dsolve c failed", type(e).__name__, str(e)[:100])
