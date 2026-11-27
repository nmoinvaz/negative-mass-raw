from core import *
import sys
fam = Fam(0.0)
# Ellis check: V-hat for A=1: 2/r^2 + 1/R^4 - 2/R^2
r = 0.7
print(Vhat(fam, r), 2/r**2 + 1/(r*r+1)**2 - 2/(r*r+1))

def shoot_ellis(W, rmax=60.0, rm=0.5, delta=0.3, rtol=1e-12, atol=1e-30, rr=0.0):
    """left: from -rmax with decaying BC to -delta, arc, right segment to rm ; right: from +rmax inward to rm"""
    fam = Fam(0.0)
    # left start: u = Y/rho, u_x/u = W + Vhat/(2W);  Y = rho u:  Y_x/Y = 1/rho + u_x/u   (A = 1)
    r0 = -rmax
    lg = W + Vhat(fam, r0)/(2*W)
    Y0 = 1.0; Yx0 = (1/r0 + lg)*Y0
    f = rhs_x(fam, W)
    ev = lambda x, s: s[0] + delta
    ev.terminal = True; ev.direction = 1
    sol = solve_ivp(f, [0, 10*rmax], [r0, Y0, Yx0], method='DOP853', rtol=rtol, atol=atol, events=ev)
    s = sol.y[:, -1]
    r_, Y_, Yx_ = s
    # arc from -delta to +delta through upper half plane: theta pi -> 0
    fc = rhs_rho_complex(fam, W)
    sol2 = solve_ivp(lambda th, y: fc(th, y, delta, 1), [np.pi, 0.0], [Y_ + 0j, Yx_/fam.A(-delta) + 0j], method='DOP853', rtol=rtol, atol=atol)
    Yc, Yrc = sol2.y[:, -1]
    # right segment from +delta to rm (x-form)
    ev2 = lambda x, s: s[0] - rm
    ev2.terminal = True; ev2.direction = 1
    sol3 = solve_ivp(f, [0, 10*rmax], [delta, Yc.real, (Yrc*fam.A(delta)).real], method='DOP853', rtol=rtol, atol=atol, events=ev2)
    L = sol3.y[:, -1]
    # right solution inward
    rR = rmax
    lg = -W - Vhat(fam, rR)/(2*W)
    YR0 = 1.0; YRx0 = (1/rR + lg)*YR0
    ev3 = lambda x, s: s[0] - rm
    ev3.terminal = True; ev3.direction = -1
    sol4 = solve_ivp(f, [0, -10*rmax], [rR, YR0, YRx0], method='DOP853', rtol=rtol, atol=atol, events=ev3)
    R_ = sol4.y[:, -1]
    nl = np.hypot(L[1], L[2]); nr = np.hypot(R_[1], R_[2])
    D = (L[1]*R_[2] - L[2]*R_[1])/(nl*nr)
    return D, abs(Yc.imag)/abs(Yc), sol2.y[0,-1]

for W in [0.5, 1.0, 1.1, 1.2, 1.3]:
    D, imagpart, _ = shoot_ellis(W)
    print(W, D, 'imag/real of Y after arc:', imagpart)
f = lambda W: shoot_ellis(W)[0]
Wr = brentq(f, 1.0, 1.3, xtol=1e-14)
print('W =', Wr, 'W^2 =', repr(Wr**2), 'target 1.39705243433350684', Wr**2 - 1.39705243433350684)
