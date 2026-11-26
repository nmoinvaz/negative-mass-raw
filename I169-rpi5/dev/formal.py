import numpy as np, sys, time
rng = np.random.default_rng(int(sys.argv[3]) if len(sys.argv)>3 else 1)
def ser_mul(a,b,p,q):
    # 2D truncated product: arrays shape (p+1,q+1)
    out=np.zeros((p+1,q+1))
    for i in range(p+1):
        for j in range(q+1):
            if a[i,j]==0: continue
            out[i:,j:]+= a[i,j]*b[:p+1-i,:q+1-j]
    return out
def ser_mul_fast(a,b,p,q):
    from numpy.fft import rfft2, irfft2
    # direct small convolution via loops over nonzero a
    return ser_mul(a,b,p,q)
def build(unk,p,q,v,rho0,case):
    """unk -> residual vector. unk = [N0(4), al(p+1), be(p+1), ga(q+1), de(q+1)]."""
    N0=unk[:4].reshape(2,2); k=4
    al=unk[k:k+p+1]; k+=p+1
    be=unk[k:k+p+1]; k+=p+1
    ga=unk[k:k+q+1]; k+=q+1
    de=unk[k:k+q+1]
    if case in ("a","b"): al=np.zeros(p+1)
    if case in ("a","c"): de=np.zeros(q+1)
    if case=="a": be=be   # beta free
    # F(s): 2x2 series, rows (phi; phi'), F' = K^T F, K^T=[[0,1],[al,be]], F(0)=I
    # work with 1D series in s up to order p, then similarly G(t)
    def ser1_mul(a,b,n):
        return np.convolve(a,b)[:n+1]
    F=np.zeros((p+1,2,2)); F[0]=np.eye(2)
    for m in range(p):
        # F'_m coefficients: (m+1)F[m+1] = row-structure
        # d/ds F = KT(s) F(s): row0' = row1 ; row1' = al*row0 + be*row1
        row0=F[:,0,:]; row1=F[:,1,:]
        new0=row1[m]
        new1=np.zeros(2)
        for c in range(2):
            new1[c]=sum(al[i]*row0[m-i,c]+be[i]*row1[m-i,c] for i in range(m+1))
        F[m+1,0,:]=new0/(m+1); F[m+1,1,:]=new1/(m+1)
    # G(t): columns (psi | psi'), G' = G Kr, Kr=[[0,de],[1,ga]] : col0' = col1 ; col1' = de*col0 + ga*col1
    G=np.zeros((q+1,2,2)); G[0]=np.eye(2)
    for m in range(q):
        c0=G[:,:,0]; c1=G[:,:,1]
        G[m+1,:,0]=c1[m]/(m+1)
        new=np.zeros(2)
        for r in range(2):
            new[r]=sum(de[i]*c0[m-i,r]+ga[i]*c1[m-i,r] for i in range(m+1))
        G[m+1,:,1]=new/(m+1)
    # N(s,t)=F(s) N0 G(t): entries as 2D arrays (p+1,q+1)
    Nn=np.zeros((2,2,p+1,q+1))
    for a_ in range(2):
        for b_ in range(2):
            for i in range(p+1):
                for j in range(q+1):
                    Nn[a_,b_,i,j]=(F[i][a_,:]@N0@G[j][:,b_])
    n0=Nn[0,0]; n1=Nn[1,0]; n2=Nn[0,1]; n3=Nn[1,1]   # N=[[n0,n2],[n1,n3]]
    def emb_s(a): 
        o=np.zeros((p+1,q+1)); o[:,0]=a[:p+1]; return o
    def emb_t(a):
        o=np.zeros((p+1,q+1)); o[0,:]=a[:q+1]; return o
    ALs=emb_s(al); BEs=emb_s(be); GAt=emb_t(ga); DEt=emb_t(de)
    # iota(t) = 1/(rho0+t) series
    io=np.array([(-1)**j/rho0**(j+1) for j in range(q+1)])
    IOt=emb_t(io)
    M=lambda a,b: ser_mul(a,b,p,q)
    u=n0.copy(); u[0,0]+=v
    pi_=M(ALs,n0)+M(BEs,n1)
    lam=M(GAt+IOt,n2)+M(DEt,n0)
    P=-(M(n1,n1)+M(u,pi_))
    Q2=-lam; Z2=n3
    Y2=2*M(n1,n2)+M(u,n3)
    h2=M(n2,n2)
    Y2s=M(Y2,Y2); Z2s=M(Z2,Z2); Ps=M(P,P); Q2s=M(Q2,Q2)
    D=M(M(h2,h2),h2)-4*M(h2,Ps)-M(h2,Q2s)+M(h2,Y2s)+M(h2,Z2s)-2*M(P,Y2s-Z2s)+2*M(M(Q2,Y2),Z2)
    return D.flatten(), (N0,al,be,ga,de)
def solve(p,q,v,rho0,case,ntry,seed,verbose=True,d0=None):
    nunk=4+2*(p+1)+2*(q+1)
    res=[]
    rng=np.random.default_rng(seed)
    for tr in range(ntry):
        x=rng.normal(size=nunk)
        lam_=1e-2
        dd = d0 if d0 is not None else rng.choice([-1,1])*rng.uniform(0.3,3.0)
        def f(z):
            r_=build(z,p,q,v,rho0,case)[0]
            N0_=z[:4].reshape(2,2)
            return np.concatenate([r_,[N0_[0,0]*N0_[1,1]-N0_[0,1]*N0_[1,0]-dd]])
        r=f(x); cost=r@r
        for it in range(300):
            J=np.zeros((len(r),nunk))
            for k in range(nunk):
                dx=np.zeros(nunk); h=1e-7*(1+abs(x[k])); dx[k]=h
                J[:,k]=(f(x+dx)-f(x-dx))/(2*h)
            A=J.T@J; g=J.T@r
            while True:
                try: step=np.linalg.solve(A+lam_*np.diag(np.diag(A)+1e-12),-g)
                except np.linalg.LinAlgError: lam_*=10; continue
                xn=x+step; rn=f(xn); cn=rn@rn
                if cn<cost: x,r,cost=xn,rn,cn; lam_=max(lam_/3,1e-12); break
                lam_*=4
                if lam_>1e12: break
            if lam_>1e12 or cost<1e-26: break
        N0,al,be,ga,de=build(x,p,q,v,rho0,case)[1]
        res.append((cost,np.linalg.det(N0),x.copy()))
    return res
if __name__=="__main__":
    p,q=int(sys.argv[1]),int(sys.argv[2]); case=sys.argv[4]; ntry=int(sys.argv[5]); v=float(sys.argv[6]) if len(sys.argv)>6 else 0.0
    t=time.time()
    R=solve(p,q,v,1.0,case,ntry,int(sys.argv[3]))
    R.sort(key=lambda r:r[0])
    print(f"p={p} q={q} case={case} v={v} neq={(p+1)*(q+1)} nunk={4+2*(p+1)+2*(q+1)}  time {time.time()-t:.1f}s")
    for c,d,x in R[:8]: print(f"  cost {c:.2e}  detN0 {d:.3f}")
