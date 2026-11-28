import sympy as sp, time, sys
sys.path.insert(0,'/Users/nathan/Source/negative-mass-i172/notes/warp')
import det_classify as dc
eta,rho=sp.symbols("eta rho",positive=True)
F0,F1,F2,F3,F4=sp.symbols("F0 F1 F2 F3 F4")
Fs=[F0,F1,F2,F3,F4]
def Deta(e):
    return sp.diff(e,eta)+sum(sp.diff(e,Fs[i])*Fs[i+1] for i in range(4))
def dx(e): return Deta(e)/rho
def dr(e): return sp.diff(e,rho)-eta*Deta(e)/rho
u=F0
ux,ur=dx(u),dr(u)
P=-(u*dx(ux)+ux**2); Q=-(dr(ur)+ur/rho)/2; Z=dx(ur)/2; Y=u*dx(ur)/2+ux*ur; h=ur**2/2
A=P-h; B=-P-h
S11=sp.together(B-Y**2/h); S01=sp.together(Q-Z*Y/h); S00=sp.together(A-Z**2/h)
D=sp.factor(sp.together(h*(S00*S11-S01**2)))
Nt=dc.conical_N()
print(sp.simplify(D*8*rho**6-Nt.subs({dc.F0_:F0,dc.F1_:F1,dc.F2_:F2,dc.ETA:eta})))
L2=sp.Matrix([Z/h,Y/h,1]); L1=sp.Matrix([S01/S11,1,0]); w2=sp.together(-S11/h)
print("w2=",sp.factor(w2))
# covector comps in coordinates (t,x,rho): k_t = al + be u, k_x = be, k_r = ga
def coord(L): return sp.Matrix([L[0]+L[1]*u, L[1], L[2]])
def Wd(a,b):
    a=coord(a); b=coord(b)
    return a[0]*(dx(b[2])-dr(b[1]))+a[1]*dr(b[0])+a[2]*(-dx(b[0]))
def wedge3(a,b,c):
    return sp.Matrix.hstack(coord(a),coord(b),coord(c)).det()
dw2=sp.Matrix([0,dx(w2),dr(w2)])
t0=time.time()
Ecoef=Wd(L2,L2)+w2*Wd(L1,L1)
# L2 ^ dw2 ^ L1 : treat dw2 as covector comps (0, dx, dr) directly in coord basis
det3=sp.Matrix.hstack(coord(L2),dw2,coord(L1)).det()
Bcoef=Wd(L2,L1)+Wd(L1,L2)+det3/(2*w2)
print("built",time.time()-t0)
for nm,e in (("E",Ecoef),("B",Bcoef)):
    e=sp.together(e); print(nm, sp.count_ops(e))
import pickle
pickle.dump((Ecoef,Bcoef,w2,h,N:=Nt),open("EB.pkl","wb"))
