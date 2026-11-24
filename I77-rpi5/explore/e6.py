import sys, time, random
import sympy as sp
r, c, S = sp.symbols("r c S")
Wd = sp.symbols("W0:7")
W0, W1, W2 = Wd[:3]
def Dr(E):
    return sp.expand(sp.diff(E, r) + sum(Wd[k+1]*sp.diff(E, Wd[k]) for k in range(6)))
def Dth(E):
    return sp.expand(-S*sp.diff(E, c) + c*sp.diff(E, S))
w = W0
R00 = -(2*w*W1*S**2 + 2*r*w*W2*c**2 + r*W1**2*(1+c**2))/(2*r)
R01 = -(W1*(1+c**2) + r*W2*S**2)/(2*r)
R0p = (r*W2 - W1)*S*c/(2*r)
R11 = (2*w*W1*S**2 + 2*r*w*W2*c**2 + r*W1**2*(3*c**2-1))/(2*r)
R1p = (w*(r*W2 - W1) + 2*r*W1**2)*S*c/(2*r)
Rpp = W1**2*S**2/2
htt = R00 + 2*w*R01 + w**2*R11
htr = c*(R01 + w*R11) + S*(R0p + w*R1p)
hth = r*(-S*(R01 + w*R11) + c*(R0p + w*R1p))
hrr = c**2*R11 + 2*c*S*R1p + S**2*Rpp
hrth = r*(-c*S*R11 + (c**2 - S**2)*R1p + c*S*Rpp)
hthth = r**2*(S**2*R11 - 2*c*S*R1p + c**2*Rpp)
h = sp.Matrix([[htt, htr, hth], [htr, hrr, hrth], [hth, hrth, hthth]]).applyfunc(lambda e: sp.expand(e))
t0 = time.time()
psi = h[0,0]
dpsi = [0, Dr(psi), Dth(psi)]
Fm = sp.zeros(3,3)
Fm[1,0] = dpsi[1]; Fm[0,1] = -dpsi[1]; Fm[2,0] = dpsi[2]; Fm[0,2] = -dpsi[2]
Fm[1,2] = Dr(h[0,2]) - Dth(h[0,1]); Fm[2,1] = -Fm[1,2]
print("built", time.time()-t0, flush=True)
def at(pt):
    hv = h.subs(pt); hi = hv.inv(); Fv = Fm.subs(pt)
    dp = sp.Matrix([sp.sympify(x).subs(pt) for x in dpsi])
    F2 = sum(Fv[a,b]*Fv[c_,d]*hi[a,c_]*hi[b,d] for a in range(3) for b in range(3) for c_ in range(3) for d in range(3))
    Xt = 2*(hv[0,0]*Fv[1,2] + hv[0,1]*Fv[2,0] + hv[0,2]*Fv[0,1])
    det = hv.det()
    return det, F2, Xt**2/abs(det)
random.seed(5)
jets = {W: sp.Rational(random.randint(-9,9), random.randint(1,9)) for W in Wd}
jets[W1] += sp.Rational(1,2)
for (rv, cv, sv) in [(sp.Rational(5,7), sp.Rational(4,5), sp.Rational(3,5)), (sp.Rational(5,7), sp.Rational(12,13), sp.Rational(5,13)), (sp.Rational(5,7), sp.Rational(3,5), sp.Rational(4,5))]:
    pt = dict(jets); pt.update({r: rv, c: cv, S: sv})
    d, F2, J2 = at(pt)
    print(float(d), float(F2), float(J2), flush=True)
print(time.time()-t0)
