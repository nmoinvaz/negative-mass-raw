import sys, math
sys.argv=[sys.argv[0]]
from explore1 import *
def run(Fv, Cv):
    # adaptive-ish: step relative to distance to singularity is unknown; use small steps, stop when F small
    f, f1 = start(Fv, Cv, 200.0)
    pp = 200*f1; q0 = -pp**2*200**2/(2*f); f2g = (q0-pp)/200**2
    br = Branch(f2g); e=200.0; y=np.array([f,f1])
    def rhs(e,y):
        f2,c = br.f2at(y[0],y[1],e); return np.array([y[1], f2])
    while e>1e-9:
        # step: limit relative change of F and F1
        h = min(0.003*max(e,0.02), e)
        # shrink with curvature
        f2 = br.f2
        scale = min(abs(y[0]/(abs(y[1])+1e-300))*0.02, abs(y[1]/(abs(f2)+1e-300))*0.02+1e-12)
        h = max(min(h, scale), 1e-9)
        h = min(h, e)
        try:
            k1=rhs(e,y); k2=rhs(e-h/2,y-h/2*k1); k3=rhs(e-h/2,y-h/2*k2); k4=rhs(e-h,y-h*k3)
        except RuntimeError: return ("noroot", e, y, br.f2)
        yn = y-h/6*(k1+2*k2+2*k3+k4)
        try: f2n,_ = br.f2at(yn[0],yn[1],e-h)
        except RuntimeError: return ("noroot", e, y, br.f2)
        if abs(f2n-br.f2) > 0.5*abs(f2n)+10: return ("jump", e, y, br.f2)
        y=yn; e-=h; br.f2=f2n
        if y[0] < 1e-3*abs(Fv)*0+1e-6: return ("F->0", e, y, f2n)
        if abs(y[0])>1e6: return ("blow", e, y, f2n)
    return ("reached0", e, y, br.f2)
for Fv in (0.5, 1.0, 2.0, 3.0):
    for Cv in (-300., -100., -30., -10., 0., 10., 30., 100., 300., 1000., 3000.):
        r = run(Fv, Cv)
        print("Finf=%.2f C=%8.1f"%(Fv,Cv), r[0], "eta=%.5g"%r[1], "F=%.5g F'=%.5g F2=%.5g"%(r[2][0], r[2][1], r[3]), flush=True)
