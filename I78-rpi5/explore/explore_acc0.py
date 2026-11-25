import sys, time, pickle
sys.path.insert(0,'/home/nathan/Source/negative-mass-i78/notes/warp')
import sympy as sp
import phantom_source as ps
t0=time.time()
c = sp.Symbol("c", real=True); S = sp.Symbol("S", real=True)
W0,W1,W2 = ps.W
Ra = ps.shift_tetrad_ricci(-ps.VS[0]*ps.F[0], ps.bubble_rule(False), False)
print("route D", time.time()-t0)
A, U, Vs, R = sp.Symbol("A", real=True), sp.Symbol("U", real=True), sp.Symbol("V", real=True), ps.R
jsub = {ps.F[0]: (U - W0)/Vs, ps.F[1]: -W1/Vs, ps.F[2]: -W2/Vs, ps.VS[1]: A*Vs, ps.XS[1]: U, ps.VS[0]: Vs}
R3a = sp.zeros(3,3)
for i in range(3):
    for j in range(i,3):
        e = Ra[i,j].subs(ps.z,0).subs(jsub).subs({ps.X: R*c, ps.y: R*S})
        R3a[i,j]=R3a[j,i]=sp.factor(sp.expand(e))
print(time.time()-t0)
for i in range(3):
    for j in range(i,3):
        print(i,j,R3a[i,j])
print("I2:", sp.simplify((R3a[0,0]+R3a[1,1]+2*R3a[2,2]).subs(S, sp.sqrt(1-c**2))))
pass
