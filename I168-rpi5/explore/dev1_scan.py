import numpy as np, random
random.seed(1); np.random.seed(1)
def coeffs(G,sig,om):
    b=G*G*sig; a=G*sig
    kap=1-b+sig; mu=1+3*sig-b+2*sig**2-6*b*sig; c=1+2*sig
    M=mu+(b-sig)*om
    return [-2*a*kap, -M, 4*a*c, c*c-om*om], a,b,M,c,kap
bad=0; n=0
stats=dict(maxsmall=0, nreal1=0, nreal3=0, minhuge_ratio=1e9, smallomega_max=0)
for _ in range(200000):
    u=10**random.uniform(-6,np.log10(1/500))
    f=random.random(); sig=u*f; b=u*(1-f)
    if sig==0 or b<0: continue
    G=np.sqrt(b/sig)  # b=G^2 sig
    om=random.choice([random.uniform(-100,100), random.uniform(-1.2,1.2), random.uniform(-3,3)])
    co,a,b_,M,c,kap=coeffs(G,sig,om)
    assert M>0.5
    rts=np.roots(co); real=sorted([z.real for z in rts if abs(z.imag)<1e-9*max(1,abs(z))])
    n+=1
    huge=[w for w in real if w<=-1/(4*a)]
    small=[w for w in real if w>-1/(4*a)]
    if len(huge)!=1: bad+=1; print("huge count",len(huge),G,sig,om,real); continue
    if any(abs(w)>=2 for w in small): bad+=1; print("small root out of (-2,2)",G,sig,om,real); continue
    if small and abs(om)>1.05: bad+=1; print("small root with |om|>1.05",om)
    if len(real)==3 and abs(om)<=0.5 and not (small[0]<-0.5 and small[1]>0.5): bad+=1; print("sep fail",om,small)
    if len(real) not in (1,3): bad+=1; print("count",len(real))
    stats['nreal1']+= len(real)==1; stats['nreal3']+= len(real)==3
    if small: stats['smallomega_max']=max(stats['smallomega_max'],abs(om))
print(n,"cases, bad:",bad,stats)
