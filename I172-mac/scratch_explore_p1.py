import sympy as sp, time
t,x,rho,phi = sp.symbols("t x rho phi", positive=True)
X4=[t,x,rho,phi]
u = sp.Function("u")(x,rho)
gm = sp.Matrix([[-1+u**2,u,0,0],[u,1,0,0],[0,0,1,0],[0,0,0,rho**2]])
def ricci(gm,X):
    n=len(X); gi=gm.inv().applyfunc(sp.simplify)
    dg=[[[sp.diff(gm[b,c],X[a]) for c in range(n)] for b in range(n)] for a in range(n)]
    Gam=[[[sp.simplify(sum(gi[a,d]*(dg[b][d][c]+dg[c][d][b]-dg[d][b][c]) for d in range(n))/2) for c in range(n)] for b in range(n)] for a in range(n)]
    Ric=sp.zeros(n,n)
    for b in range(n):
        for c in range(b,n):
            s=0
            for a in range(n):
                s+=sp.diff(Gam[a][b][c],X[a])-sp.diff(Gam[a][a][b],X[c])
                for d in range(n):
                    s+=Gam[a][a][d]*Gam[d][b][c]-Gam[a][c][d]*Gam[d][a][b]
            Ric[b,c]=Ric[c,b]=sp.simplify(s)
    return Ric
t0=time.time()
Rc=ricci(gm,X4)
print(time.time()-t0)
# frame comps
Rt,Rx,Rr=0,1,2
R00 = Rc[0,0]-2*u*Rc[0,1]+u**2*Rc[1,1]
R01 = Rc[0,1]-u*Rc[1,1]
R02 = Rc[0,2]-u*Rc[1,2]
R11=Rc[1,1]; R12=Rc[1,2]; R22=Rc[2,2]
ux,ur=u.diff(x),u.diff(rho)
P=-(u*u.diff(x,2)+ux**2); Q=-(u.diff(rho,2)+ur/rho)/2; Z=u.diff(x,rho)/2; Y=u*u.diff(x,rho)/2+ux*ur; h=ur**2/2
print([sp.simplify(e) for e in [R00-(P-h), R01-Q, R02-Z, R11-(-P-h), R12-Y, R22-h]])
print([sp.simplify(Rc[3,i]) for i in range(4)])
