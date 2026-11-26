import numpy as np, sys, time, itertools
class Ser:
    def __init__(self,p,q):
        self.p,self.q=p,q
        n=(p+1)*(q+1); self.n=n
        idx=np.full((n,n),n,dtype=np.int64)  # index n = zero slot
        for i in range(p+1):
            for j in range(q+1):
                for k in range(i+1):
                    for l in range(j+1):
                        idx[i*(q+1)+j, k*(q+1)+l] = (i-k)*(q+1)+(j-l)
        self.idx=idx
    def mul(self,a,b):
        bp=np.concatenate([b,[0.0]])
        return (a[None,:]*bp[self.idx]).sum(1)
def build(unk,S,v,rho0,case):
    p,q=S.p,S.q; n=S.n
    N0=unk[:4].reshape(2,2); k=4
    al=unk[k:k+p+1]; k+=p+1
    be=unk[k:k+p+1]; k+=p+1
    ga=unk[k:k+q+1]; k+=q+1
    de=unk[k:k+q+1]
    if case in ("a","b"): al=np.zeros(p+1)
    if case in ("a","c"): de=np.zeros(q+1)
    F=np.zeros((p+1,2,2)); F[0]=np.eye(2)
    for m in range(p):
        r0=F[:m+1,0,:]; r1=F[:m+1,1,:]
        F[m+1,0,:]=F[m,1,:]/(m+1)
        F[m+1,1,:]=(al[:m+1][::-1]@r0 + be[:m+1][::-1]@r1)/(m+1) if False else (np.einsum('i,ic->c',al[:m+1],r0[::-1])+np.einsum('i,ic->c',be[:m+1],r1[::-1]))/(m+1)
    G=np.zeros((q+1,2,2)); G[0]=np.eye(2)
    for m in range(q):
        c0=G[:m+1,:,0]; c1=G[:m+1,:,1]
        G[m+1,:,0]=G[m,:,1]/(m+1)
        G[m+1,:,1]=(np.einsum('i,ir->r',de[:m+1],c0[::-1])+np.einsum('i,ir->r',ga[:m+1],c1[::-1]))/(m+1)
    # N[a,b](i,j) = F[i][a,:] N0 G[j][:,b]
    Nn=np.einsum('iac,cd,jdb->abij',F,N0,G).reshape(2,2,n)
    n0=Nn[0,0]; n1=Nn[1,0]; n2=Nn[0,1]; n3=Nn[1,1]
    def emb_s(a):
        o=np.zeros((p+1,q+1)); o[:,0]=a; return o.reshape(-1)
    def emb_t(a):
        o=np.zeros((p+1,q+1)); o[0,:]=a; return o.reshape(-1)
    ALs=emb_s(al); BEs=emb_s(be); GAt=emb_t(ga); DEt=emb_t(de)
    io=np.array([(-1)**j/rho0**(j+1) for j in range(q+1)])
    IOt=emb_t(io)
    M=S.mul
    u=n0.copy(); u[0]+=v
    pi_=M(ALs,n0)+M(BEs,n1)
    lam=M(GAt+IOt,n2)+M(DEt,n0)
    P=-(M(n1,n1)+M(u,pi_))
    Q2=-lam; Z2=n3
    Y2=2*M(n1,n2)+M(u,n3)
    h2=M(n2,n2)
    Y2s=M(Y2,Y2); Z2s=M(Z2,Z2); Ps=M(P,P); Q2s=M(Q2,Q2)
    D=M(M(h2,h2),h2)-4*M(h2,Ps)-M(h2,Q2s)+M(h2,Y2s)+M(h2,Z2s)-2*M(P,Y2s-Z2s)+2*M(M(Q2,Y2),Z2)
    return D, (N0,al,be,ga,de)
def nunk_of(p,q,case):
    return 4+2*(p+1)+2*(q+1)
def solve(p,q,v,rho0,case,ntry,seed,maxit=200):
    S=Ser(p,q); nunk=nunk_of(p,q,case)
    rng=np.random.default_rng(seed); out=[]
    for tr in range(ntry):
        x=rng.normal(size=nunk)*rng.choice([0.5,1.0,2.0])
        dd=rng.choice([-1,1])*rng.uniform(0.3,3.0)
        def f(z):
            r_=build(z,S,v,rho0,case)[0]
            N0_=z[:4].reshape(2,2)
            return np.concatenate([r_,[N0_[0,0]*N0_[1,1]-N0_[0,1]*N0_[1,0]-dd]])
        r=f(x); cost=r@r; lam_=1e-2
        for it in range(maxit):
            J=np.zeros((len(r),nunk))
            for k in range(nunk):
                dx=np.zeros(nunk); h=1e-6*(1+abs(x[k])); dx[k]=h
                J[:,k]=(f(x+dx)-f(x-dx))/(2*h)
            A=J.T@J; g=J.T@r
            acc=False
            while lam_<1e12:
                step=np.linalg.solve(A+lam_*np.diag(np.diag(A)+1e-12),-g)
                xn=x+step; rn=f(xn); cn=rn@rn
                if cn<cost: x,r,cost=xn,rn,cn; lam_=max(lam_/3,1e-14); acc=True; break
                lam_*=4
            if not acc or cost<1e-28: break
        N0,al,be,ga,de=build(x,S,v,rho0,case)[1]
        out.append((cost,np.linalg.det(N0),x.copy()))
    return out
if __name__=="__main__":
    p,q=int(sys.argv[1]),int(sys.argv[2]); seed=int(sys.argv[3]); case=sys.argv[4]; ntry=int(sys.argv[5]); v=float(sys.argv[6])
    t=time.time(); R=solve(p,q,v,1.0,case,ntry,seed); R.sort(key=lambda r:r[0])
    print(f"p={p} q={q} case={case} v={v} neq={(p+1)*(q+1)}+1 nunk={nunk_of(p,q,case)} tries={ntry} time {time.time()-t:.1f}s",flush=True)
    for c,d,x in R[:6]: print(f"  cost {c:.2e}  detN0 {d:.3f}",flush=True)
