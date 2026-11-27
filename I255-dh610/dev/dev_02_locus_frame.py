import sys, os, numpy as np
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i255/notes/wormhole_evolution"))
import throat_locus as tl
raw = os.path.expanduser("~/Source/negative-mass-raw/I225-dh610/runs/stall")
D = int(sys.argv[1]); h = sys.argv[2]
n = D - 2
La = tl.load_run(f"{raw}/stall_D{D}_h{h}_side-1.npz")
Lb = tl.load_run(f"{raw}/stall_D{D}_h{h}_side1.npz")
common = np.intersect1d(La["s"], Lb["s"])
ia, ib = np.searchsorted(La["s"], common), np.searchsorted(Lb["s"], common)
def m(key):
    return 0.5*(La[key][ia] + Lb[key][ib])
t, r, f, v, l, tau = m("t"), m("r"), m("f"), m("v"), m("l"), m("tau")
php = 0.5*(La["php"][ia]+Lb["php"][ib]); phm = 0.5*(La["phm"][ia]+Lb["phm"][ib]); phi = 0.5*(La["phi"][ia]+Lb["phi"][ib])
rp = m("rp"); rm_ = m("rm")
ef = np.exp(f)
# fields: 0 ghost (eps -1), 1 normal (+1)
print("t  r_th  v  f | ghost: phi+ phi- | normal: phi+ phi- | rho_g rho_n (locus frame) | q_g flux rate, q_n rate")
H = np.gradient(np.log(r), tau)
for tt in (3,4,5,6,7,8,9,10,11,12,13):
    k = np.argmin(abs(t-tt))
    vv = v[k]
    Tpp = [(-1.0 if i==0 else 1.0)*php[k,i]**2 for i in range(2)]
    Tmm = [(-1.0 if i==0 else 1.0)*phm[k,i]**2 for i in range(2)]
    g2 = 1/(1-vv**2)
    Ttt = [ef[k]*(Tpp[i]+Tmm[i])/2 for i in range(2)]
    Ttl = [ef[k]*(Tpp[i]-Tmm[i])/2 for i in range(2)]
    rho = [g2*((1+vv**2)*Ttt[i] + 2*vv*Ttl[i]) for i in range(2)]
    rho_eq = -n*(n-1)/(2*r[k]**2)
    qrate = [r[k]**n*(phm[k,i]*(1-vv) - php[k,i]*(1+vv))/np.sqrt(2) for i in range(2)]
    print(f"t={t[k]:5.2f} r {r[k]:.4f} v {vv:+.4f} f {f[k]:+.4f} H {H[k]:+.4f} | g {php[k,0]:+.5f} {phm[k,0]:+.5f} | n {php[k,1]:+.5f} {phm[k,1]:+.5f} | rho_g {rho[0]:+.5f} rho_n {rho[1]:+.2e} rho_eq(r_th) {rho_eq:+.5f} ratio {rho[0]/rho_eq:.4f} | qrate_g {qrate[0]:+.5f} qrate_n {qrate[1]:+.2e}")
