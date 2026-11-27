"""dev11: I0 = int_0^inf 2K rho e^{-2H(rho)} / (A R^2) d rho (e^{kappa x} = rho^{1/2} e^{H}); check beta* = pi/4 - 1/I0 against the ODE value (dev05)."""
import sys, time
sys.path.insert(0, ".")
import mpmath as mp
import cm_core as cm
K = cm.setup(50)
t0 = time.time()
hs = cm.h_series(K, 100)
def Hs(r):
    return sum(hk * r ** (k + 1) / (k + 1) for k, hk in enumerate(hs))
Af = lambda r: -r * r + K * (r + (1 + r * r) * mp.atan(r))
hf = lambda r: K / Af(r) - 1 / (2 * r)
def f_series(r):      # integrand for r <= 0.25
    return 2 * K * r * mp.exp(-2 * Hs(r)) / (Af(r) * (1 + r * r))
edges = [mp.mpf(0), mp.mpf("0.25")]
while edges[-1] < 110:
    edges.append(edges[-1] * 2)
total = mp.mpf(0)
Hleft = Hs(mp.mpf("0.25"))
# panel 0: series region (A(r)/r computed directly is fine for the integrand: 2K r/A -> 1; use a(r) series to avoid 0/0)
A_s = cm.bg_series0(K, 100)
a_s = A_s[1:99]
def a_of(r):
    return sum(c * r ** j for j, c in enumerate(a_s))
def f_small(r):
    return 2 * K * mp.exp(-2 * Hs(r)) / (a_of(r) * (1 + r * r))
total += mp.quad(f_small, [0, mp.mpf("0.25")])
for i in range(1, len(edges) - 1):
    L, Rr = edges[i], edges[i + 1]
    def f(r, L=L, Hleft=Hleft):
        H = Hleft + mp.quad(hf, [L, r])
        return 2 * K * r * mp.exp(-2 * H) / (Af(r) * (1 + r * r))
    total += mp.quad(f, [L, Rr])
    Hleft = Hleft + mp.quad(hf, [L, Rr])
    print("panel", mp.nstr(L, 5), mp.nstr(Rr, 5), " partial I0 =", mp.nstr(total, 30), " time", round(time.time() - t0, 1), flush=True)
I0 = total
beta_star = mp.mpf("-0.1999170825208707808649977307814104850014")
print("I0 =", mp.nstr(I0, 40))
print("1/I0 =", mp.nstr(1 / I0, 40))
print("pi/4 - beta* (ODE, dev05) =", mp.nstr(mp.pi / 4 - beta_star, 40))
print("beta* from I0 =", mp.nstr(mp.pi / 4 - 1 / I0, 40))
print("relative difference:", mp.nstr(abs((mp.pi / 4 - 1 / I0) - beta_star) / abs(beta_star), 5))
s = -(mp.pi / 2) * (mp.pi / 4 - 1 / I0)
print("slope d(W/kappa)/dc =", mp.nstr(s, 40), "   dW/dc = 1/I0 - 2/pi =", mp.nstr(1 / I0 - 2 / mp.pi, 40))
