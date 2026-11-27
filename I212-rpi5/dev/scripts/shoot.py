from core import *

def left_solution(fam, W, rm, rtol=1e-12, atol=1e-30, delta=None, chunk=None):
    """Y, Y_x at rho = rm of the solution regular at the horizon (decaying toward it), through the throat if present."""
    delta = delta or fam.delta
    # --- horizon start: state (zeta, Y, Yx)
    z0 = fam.z0
    if fam.rh == 0.0:
        s0 = [np.log(z0), 1.0, fam.A1 + W]       # Y ~ rho^{1 + W/A1}
    else:
        s0 = [np.log(z0), 1.0, W]                # Y ~ z^{W/A1}
    f = rhs_zeta(fam, W)
    # stop where rho = rstop
    if fam.rh < 0:
        rstop = -min(delta, 0.5*abs(fam.rh))
    else:
        rstop = rm
    ev = lambda x, s: fam.rh + np.exp(s[0]) - rstop
    ev.terminal = True; ev.direction = 1
    lognorm = 0.0
    s = np.array(s0, float); x = 0.0
    # integrate in chunks, renormalizing
    while True:
        L = 6.0/max(W, 1e-3) if chunk is None else chunk
        sol = solve_ivp(f, [x, x + L], s, method='DOP853', rtol=rtol, atol=[1e-12, atol, atol], events=ev)
        s = sol.y[:, -1]; x = sol.t[-1]
        n = np.hypot(s[1], s[2]); s[1:] /= n; lognorm += np.log(n)
        if sol.status == 1: break
        if x > 1e5: raise RuntimeError('no event')
    if fam.rh >= 0:
        r = fam.rh + np.exp(s[0])
        return r, s[1], s[2], lognorm
    # ---- throat crossing (rh < 0): arc in rho-plane
    r = fam.rh + np.exp(s[0]); Y, Yx = s[1], s[2]
    d = -r
    fc = rhs_rho_complex(fam, W)
    sol2 = solve_ivp(lambda th, y: fc(th, y, d, 1), [np.pi, 0.0], [Y + 0j, Yx/fam.A(r) + 0j], method='DOP853', rtol=rtol, atol=atol)
    Yc, Yrc = sol2.y[:, -1]
    s = np.array([d, Yc.real, (Yrc*fam.A(d)).real])
    fx = rhs_x(fam, W)
    ev2 = lambda x, ss: ss[0] - rm
    ev2.terminal = True; ev2.direction = 1
    x = 0.0
    while True:
        L = 6.0/max(W, 1e-3) if chunk is None else chunk
        sol = solve_ivp(fx, [x, x + L], s, method='DOP853', rtol=rtol, atol=atol, events=ev2)
        s = sol.y[:, -1]; x = sol.t[-1]
        n = np.hypot(s[1], s[2]); s[1:] /= n; lognorm += np.log(n)
        if sol.status == 1: break
    return s[0], s[1], s[2], lognorm

def right_solution(fam, W, rm, rtol=1e-12, atol=1e-30, rmax=None):
    rmax = rmax or max(300.0, 45.0/W)
    r0 = rmax
    lg = -W - Vhat(fam, r0)/(2*W)
    s = np.array([r0, 1.0, (1/r0 + lg)*fam.A(r0)/1.0*0 + 0.0])
    # Y_x = A u + rho u_x ; Y = rho u, u=1/rho -> Y=1 : Y_x/Y = A/rho + u_x/u
    s[2] = fam.A(r0)/r0 + lg
    fx = rhs_x(fam, W)
    ev = lambda x, ss: ss[0] - rm
    ev.terminal = True; ev.direction = -1
    x = 0.0
    while True:
        L = 6.0/max(W, 1e-3)
        sol = solve_ivp(fx, [x, x - L], s, method='DOP853', rtol=rtol, atol=atol, events=ev)
        s = sol.y[:, -1]; x = sol.t[-1]
        n = np.hypot(s[1], s[2]); s[1:] /= n
        if sol.status == 1: break
    return s[0], s[1], s[2]

def mismatch(fam, W, rm=None, **kw):
    if rm is None:
        rm = 1.0 if fam.rh is None or fam.rh < 0.5 else fam.rh + 1.0
    rl, Yl, Ylx, _ = left_solution(fam, W, rm, **kw)
    rr, Yr, Yrx = right_solution(fam, W, rm, **{k: v for k, v in kw.items() if k in ('rtol', 'atol')})
    return Yl*Yrx - Ylx*Yr   # both unit-normalized

def scan(fam, Ws, **kw):
    return np.array([mismatch(fam, W, **kw) for W in Ws])
