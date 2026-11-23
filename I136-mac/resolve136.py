#!/usr/bin/env python3
"""Re-solve of one case of #136: G(0) = lim P/z^24 at both walls from the coordinator's hand expansion.
f = K/(K + u), u = cosh z - 1, K = 1 + C: phi = v z^2/(2K) + O(z^4), y = B' - A' = -v z^4 (K - 6)/(3 K^2) + O(z^6), and
#136's weight-24 part 774144 phi^8 delta^2 gives G(0) = 774144 (v/(2K))^8 (v (K - 6)/(3 K^2))^2. Also y/z^4 at z = 1e-4 from
the tanh form against -v (K - 6)/(3 K^2)."""
import mpmath as mp
mp.mp.dps = 120
for name, s, Rb, v, printed in (('le', 8, 1, mp.mpf(1) / 2, '1.09451e-67'), ('rodal', 4, 5, mp.mpf(1), '6.58941e-169')):
    C = mp.cosh(2 * s * Rb); K = 1 + C
    G0 = 774144 * (v / (2 * K))**8 * (v * (K - 6) / (3 * K**2))**2
    z = mp.mpf('1e-4'); r = z / (2 * s)
    tp, tm, t0 = mp.tanh(s * (r + Rb)), mp.tanh(s * (r - Rb)), mp.tanh(s * Rb)
    hp, hm = mp.sech(s * (r + Rb))**2, mp.sech(s * (r - Rb))**2
    a = v * r * s * (hp - hm) / (2 * t0); b = v * r**2 * (-2 * s**2) * (hp * tp - hm * tm) / (2 * t0)
    d0 = -v * (K - 6) / (3 * K**2)
    print(f"{name}: G(0) = {mp.nstr(G0, 8)} (printed {printed}, relative {mp.nstr(abs(G0 / mp.mpf(printed) - 1), 2)}); "
          f"y/z^4 at z = 1e-4: {mp.nstr((b - a) / z**4, 10)}, hand -v(K - 6)/(3K^2) = {mp.nstr(d0, 10)}")
