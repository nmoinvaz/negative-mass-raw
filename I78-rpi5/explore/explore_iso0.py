import mpmath as mp, random
mp.mp.dps = 30
def ent(r, c, w, w1, w2):
    s2 = 1-c*c; s = mp.sqrt(s2)
    u = r*w2 - w1; v = w*u + 2*r*w1**2
    R00 = -(2*w*w1*s2 + 2*r*w*w2*c*c + r*w1**2*(1+c*c))/(2*r)
    R01 = -(w1*(1+c*c) + r*w2*s2)/(2*r)
    R0p = u*s*c/(2*r)
    R11 = (2*w*w1*s2 + 2*r*w*w2*c*c + r*w1**2*(3*c*c-1))/(2*r)
    R1p = v*s*c/(2*r)
    Rpp = w1**2*s2/2
    return R00,R01,R0p,R11,R1p,Rpp
def resid(r,c,w,w1,w2):
    R00,R01,R0p,R11,R1p,Rpp = ent(r,c,w,w1,w2)
    # rank-1: F=0 and C1
    F = R01*(R0p**2+R1p**2) + 2*Rpp*R0p*R1p
    lam = Rpp - R0p*R1p/R01
    N = mp.matrix([[R00+lam,R01,R0p],[R01,R11-lam,R1p],[R0p,R1p,Rpp-lam]])
    # minors
    m = [N[0,0]*N[1,1]-N[0,1]**2, N[0,0]*N[2,2]-N[0,2]**2, N[1,1]*N[2,2]-N[1,2]**2, N[0,0]*N[1,2]-N[0,1]*N[0,2], N[1,1]*N[0,2]-N[0,1]*N[1,2], N[2,2]*N[0,1]-N[0,2]*N[1,2]]
    return F, m
random.seed(5)
found=[]
for trial in range(int(__import__("sys").argv[1])):
    r = mp.mpf(random.uniform(0.5,2)); w1 = mp.mpf(random.uniform(-2,2)); w2 = mp.mpf(random.uniform(-3,3))
    w0 = mp.mpf(random.uniform(-3,3)); c = mp.mpf(random.uniform(0.1,0.95))
    try:
        sol = mp.findroot(lambda W,C: [resid(r,C,W,w1,w2)[1][0], resid(r,C,W,w1,w2)[1][3]], (w0,c), tol=1e-20, maxsteps=60)
    except Exception as e:
        continue
    W,C = sol
    if not (abs(C)<1 and abs(C)>1e-3): continue
    F,m = resid(r,C,W,w1,w2)
    mx = max(abs(x) for x in m)
    if mx < 1e-15:
        found.append((r,W,w1,w2,C,mx))
print(len(found))
for f in found[:8]:
    print([mp.nstr(x,8) for x in f])
