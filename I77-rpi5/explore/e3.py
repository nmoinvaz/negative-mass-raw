import sys, time, random
import sympy as sp
from sympy.polys.fields import field
from sympy import QQ
F, u, r, W0, W1, W2, W3, W4, W5 = field("u,r,W0,W1,W2,W3,W4,W5", QQ)
W = [W0, W1, W2, W3, W4, W5]
c = (1 - u**2) / (1 + u**2)
S = 2 * u / (1 + u**2)
R00 = -(-2*W0*W1*c**2 + 2*W0*W1 + 2*W0*W2*r*c**2 + W1**2*r*c**2 + W1**2*r)/(2*r)
R01 = -(-W1*S**2 + 2*W1 + W2*r*S**2)/(2*r)
R0p = (-W1 + W2*r)*S*c/(2*r)
R11 = (-2*W0*W1*c**2 + 2*W0*W1 + 2*W0*W2*r*c**2 + 3*W1**2*r*c**2 - W1**2*r)/(2*r)
R1p = (-W0*W1 + W0*W2*r + 2*W1**2*r)*S*c/(2*r)
Rpp = W1**2*S**2/2
w = W0
htt = R00 + 2*w*R01 + w**2*R11
htr = c*(R01 + w*R11) + S*(R0p + w*R1p)
hth = r*(-S*(R01 + w*R11) + c*(R0p + w*R1p))
hrr = c**2*R11 + 2*c*S*R1p + S**2*Rpp
hrth = r*(-c*S*R11 + (c**2 - S**2)*R1p + c*S*Rpp)
hthth = r**2*(S**2*R11 - 2*c*S*R1p + c**2*Rpp)
h = [[htt, htr, hth], [htr, hrr, hrth], [hth, hrth, hthth]]
def Dr(E):
    out = E.diff(r)
    for k in range(5):
        out += W[k+1] * E.diff(W[k])
    return out
def Dth(E):
    return (1 + u**2) / 2 * E.diff(u)
def det3(m):
    return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1]) - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0]) + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
def inv3(m):
    d = det3(m)
    cof = [[None]*3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            rows = [k for k in range(3) if k != i]; cols = [k for k in range(3) if k != j]
            minor = m[rows[0]][cols[0]]*m[rows[1]][cols[1]] - m[rows[0]][cols[1]]*m[rows[1]][cols[0]]
            cof[i][j] = (-1)**(i+j) * minor
    return [[cof[j][i]/d for j in range(3)] for i in range(3)]
t0=time.time()
hi = inv3(h); dh = det3(h)
psi = htt
# Xi_i = h[0][i]; F_{rt} = d_r psi, F_{tht} = d_th psi, F_{rth} = d_r h_tth - d_th h_tr
Fm = [[F.zero]*3 for _ in range(3)]
Fm[1][0] = Dr(psi); Fm[0][1] = -Fm[1][0]
Fm[2][0] = Dth(psi); Fm[0][2] = -Fm[2][0]
Fm[1][2] = Dr(hth) - Dth(htr); Fm[2][1] = -Fm[1][2]
F2 = sum(Fm[a][b]*Fm[c_][d]*hi[a][c_]*hi[b][d] for a in range(3) for b in range(3) for c_ in range(3) for d in range(3))
Xt = 2*(htt*Fm[1][2] + htr*Fm[2][0] + hth*Fm[0][1])   # [abc] Xi_a F_bc : indices (t,r,th): a=t:F_{r th}; a=r: F_{th t}; a=th: F_{t r}
J2 = Xt**2/ (-dh)   # |det h| = -det h for signature (2,1); sign check below
gradpsi2 = hi[1][1]*Dr(psi)**2 + 2*hi[1][2]*Dr(psi)*Dth(psi) + hi[2][2]*Dth(psi)**2
print("built", time.time()-t0, flush=True)
# numeric tests
random.seed(1)
def rnd(): return QQ(random.randint(-9,9), random.randint(1,9))
for trial in range(3):
    pt = {u: QQ(random.randint(1,9),random.randint(10,19)), r: QQ(random.randint(1,9),random.randint(1,5)), W0: rnd(), W1: rnd()+QQ(1,3), W2: rnd(), W3: rnd(), W4:rnd(), W5:rnd()}
    def ev(E): 
        return E.evaluate(list(pt.items())) if hasattr(E, 'evaluate') else None
    vals = {}
    for nm, E in [("psi", psi), ("F2", F2), ("J2", J2), ("gradpsi2", gradpsi2), ("det", dh)]:
        vals[nm] = E.as_expr().subs({sp.Symbol(str(k)): sp.Rational(v.numerator, v.denominator) for k, v in pt.items()})
    res = vals["gradpsi2"] - vals["F2"]*vals["psi"]/2 - vals["J2"]/4
    print(trial, {k: sp.nsimplify(v) if False else float(v) for k, v in vals.items()}, "S3 residual", float(res), flush=True)
# derivative of F2 wrt theta, r at the point
for trial in range(2):
    pt = {u: QQ(random.randint(1,9),random.randint(10,19)), r: QQ(random.randint(1,9),random.randint(1,5)), W0: rnd(), W1: rnd()+QQ(1,3), W2: rnd(), W3: rnd(), W4:rnd(), W5:rnd()}
    sub = {sp.Symbol(str(k)): sp.Rational(v.numerator, v.denominator) for k, v in pt.items()}
    print("dth F2", float(Dth(F2).as_expr().subs(sub)), "dr F2", float(Dr(F2).as_expr().subs(sub)), "dth J2", float(Dth(J2).as_expr().subs(sub)))
