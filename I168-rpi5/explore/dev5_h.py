import sys, math
sys.argv=["x","--only=none"]
sys.path.insert(0,"/home/nathan/Source/negative-mass-i168/notes/warp")
import conical_attraction as ca
Nf,Nq=ca.direct_funs()
def run(G0,z0,h):
    s0=1/(1000*(1+G0*G0))
    def rhs_red(t,Y):
        sg=s0*math.exp(-2*t); x,eh=ca.huge_state(math.exp(Y[0]),sg,Y[1]); return [sg*Y[1],Y[1]*(4-Y[1])/2-sg*Y[1]**2+eh/2]
    def rhs_dir(t,Y):
        Gv,pv=Y; sg=s0*math.exp(-2*t); qv=-pv*pv/(2*Gv*sg)
        for _ in range(60):
            nn=Nf(Gv,pv,qv,math.sqrt(sg)); dq=nn/Nq(Gv,pv,qv,math.sqrt(sg)); qv-=dq
            if abs(dq)<=1e-14*abs(qv): break
        return [pv,qv]
    Yr,Yd,t=[math.log(G0),4+z0],[G0,s0*G0*(4+z0)],0.0
    for k in range(int(round(6/h))):
        Yr=ca.rk4(rhs_red,t,Yr,h); Yd=ca.rk4(rhs_dir,t,Yd,h); t+=h
    sg=s0*math.exp(-2*t)
    return abs(math.exp(Yr[0])-Yd[0]), abs(Yr[1]-Yd[1]/(sg*Yd[0]))
for h in [1/100,1/200,1/400,1/800,1/1600]:
    print(h,[("%.2e"%a,"%.2e"%b) for a,b in (run(1.0,0.2,h),run(0.3,-0.2,h))])
