import sympy as sp, time
from sympy.polys.matrices import DomainMatrix
from sympy import QQ
exec(open("/tmp/claude-1000/-home-nathan-Source-negative-mass-i169/331aac0b-19cd-46a3-93e4-a8cf021dbd98/scratchpad/probe3.py").read().split("# case (b)")[0])
t=time.time()
kap,mu,io,z1,z2,w1,w2=sp.symbols("kap mu io z1 z2 w1 w2")
def Mmat(Dn):
    xv=(A0,A1,A2,B0,B1,B2); rv=(a0,a1,a2,b0,b1,b2)
    Pl=sp.Poly(Dn,*xv,*rv); rows,cols,ent={},{},{}
    for mon,co in Pl.terms():
        ri=rows.setdefault(mon[:6],len(rows)); ci=cols.setdefault(mon[6:],len(cols)); ent[(ri,ci)]=co
    return ent,rows,cols
for vv in (0,sp.Rational(1,3)):
    Dn=sp.expand(Dpoly().subs(v,vv))
    ent,rows,cols=Mmat(Dn)
    xv=(A0,A1,A2,B0,B1,B2); rv=(a0,a1,a2,b0,b1,b2)
    # x side: X1=z1 (lam1=1), X2=z2 (lam2=kap): jets (z1,z1,z1,z2,kap z2,kap^2 z2)
    xsub=[z1,z1,z1,z2,kap*z2,kap**2*z2]
    Fm=[sp.Mul(*[s**e for s,e in zip(xsub,mon)]) for mon in rows]
    # Phi_j = sum_i M_ij F_i
    Phi={}
    for (i,j),co in ent.items(): Phi[j]=Phi.get(j,0)+co*Fm[i]
    mons={}; rowsP=[]
    for j in sorted(Phi):
        P=sp.Poly(sp.expand(Phi[j]),z1,z2); rowsP.append(P)
        for m in P.monoms(): mons.setdefault(m,len(mons))
    K=QQ.frac_field(kap)
    M1=sp.zeros(len(rowsP),len(mons))
    for r_,P in enumerate(rowsP):
        for m,c in P.terms(): M1[r_,mons[m]]=c
    dF=DomainMatrix.from_Matrix(M1).convert_to(K).rank()
    # rho side: R1=w1 (mu1=1): jets (R,R',S)=(w1, w1, (1+io) w1); R2=w2 (mu2=mu): (w2, mu w2, (mu^2+io mu) w2)
    rsub=[w1,w1,(1+io)*w1,w2,mu*w2,(mu**2+io*mu)*w2]
    Gm=[sp.Mul(*[s**e for s,e in zip(rsub,mon)]) for mon in cols]
    Psi={}
    for (i,j),co in ent.items(): Psi[i]=Psi.get(i,0)+co*Gm[j]
    mons2={}; rowsQ=[]
    for i in sorted(Psi):
        P=sp.Poly(sp.expand(Psi[i]),w1,w2,io); rowsQ.append(P)
        for m in P.monoms(): mons2.setdefault(m,len(mons2))
    M2=sp.zeros(len(rowsQ),len(mons2))
    for r_,P in enumerate(rowsQ):
        for m,c in P.terms(): M2[r_,mons2[m]]=c
    K2=QQ.frac_field(mu)
    dG=DomainMatrix.from_Matrix(M2).convert_to(K2).rank()
    full=DomainMatrix.from_Matrix(sp.Matrix(len(rows),len(cols),lambda i,j: ent.get((i,j),0))).convert_to(QQ).rank()
    print("v=",vv,"r2=",full,"d_F(exp pair)=",dF,"d_G(exp pair)=",dG,"sum",dF+dG, time.time()-t, flush=True)
