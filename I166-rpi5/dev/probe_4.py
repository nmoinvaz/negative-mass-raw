# probe 4: Lemma Z elimination ideals; branch B separation; dsolve feasibility
import sys, time
sys.path.insert(0, "/home/nathan/Source/negative-mass-i166/notes/warp")
import sympy as sp
t0=time.time()
v0,v1,v2,P,Q,Y,h = sp.symbols("v0 v1 v2 P Q Y h")
# branch A: v0 = 0
GA = sp.groebner([P+v2**2, Q, Y+v1*v2, 2*h-v1**2], v1, v2, P, Q, Y, h, order="lex")
elA = [g for g in GA.exprs if not g.has(v1) and not g.has(v2)]
print("A elim:", elA, f"{time.time()-t0:.1f}s")
# claim <Q, 2hP + Y^2> ; mutually contained?
GAc = sp.groebner([Q, 2*h*P+Y**2], P, Q, Y, h, order="lex")
print("A claim in elim:", all(GA.reduce(g)[1]==0 for g in GAc.exprs), "elim in claim:", all(GAc.reduce(g)[1]==0 for g in elA))
GB = sp.groebner([P+v0**2, Q+v0*v1, Y, 2*h-v0**2-v1**2], v0, v1, P, Q, Y, h, order="lex")
elB = [g for g in GB.exprs if not g.has(v0) and not g.has(v1)]
print("B elim:", elB, f"{time.time()-t0:.1f}s")
GBc = sp.groebner([Y, Q**2+P*(2*h+P)], P, Q, Y, h, order="lex")
print("B claim in elim:", all(GB.reduce(g)[1]==0 for g in GBc.exprs), "elim in claim:", all(GBc.reduce(g)[1]==0 for g in elB))
# mutated
GAm = sp.groebner([Q, 2*h*P-Y**2], P, Q, Y, h, order="lex")
print("A mut in elim:", all(GA.reduce(g)[1]==0 for g in GAm.exprs))
# separation
p1,p2,m1,m2,Fa,Fb,ga,gb,s = sp.symbols("p1 p2 m1 m2 Fa Fb ga gb s")
def EB(p,m,F,g): return m**2*g - p*m**2*F + p**2
eqs=[EB(p1,m1,Fa,ga),EB(p1,m1,Fb,gb),EB(p2,m2,Fa,ga),EB(p2,m2,Fb,gb)]
sat = p1*p2*m1*m2*(Fa-Fb)
Gs = sp.groebner(eqs+[1-s*sat], s, p1,p2,m1,m2,Fa,Fb,ga,gb, order="grevlex")
print("sep basis size", len(Gs.exprs), f"{time.time()-t0:.1f}s")
for tgt in (p1-p2, m1**2-m2**2, m1-m2):
    print("member", tgt, Gs.reduce(tgt)[1]==0)
# kappa const f case
f0,rb,ra = sp.symbols("f0 rb ra")
eqs2=[EB(p1,m1,f0**2,f0**2/(4*ra**2)), EB(p1,m1,f0**2,f0**2/(4*rb**2))]
Gu = sp.groebner(eqs2+[1-s*p1*m1*f0*(ra-rb)*ra*rb], s,p1,m1,f0,ra,rb, order="grevlex")
print("const f case:", Gu.exprs, f"{time.time()-t0:.1f}s")
# dsolve
t = sp.Symbol("t"); kap = sp.Function("kappa")(t); G = sp.Function("G")(t)
print(sp.dsolve(sp.Eq(G.diff(t), 2*kap*G), G))
rho = sp.Symbol("rho", positive=True); Rf = sp.Function("R")(rho)
print(sp.dsolve(sp.Eq(Rf.diff(rho,2)+Rf.diff(rho)/rho,0), Rf))
c = sp.Function("c")(t); Cf = sp.Function("C")(t)
gam = Cf.diff(t)/(2*Cf)
print(sp.dsolve(sp.Eq(c.diff(t), 2*gam*c-gam**2), c))
