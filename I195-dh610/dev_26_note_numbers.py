# the closed-form numbers quoted in the note (w2_highprec.md), from the identified relations; no fit data
import mpmath as mp
mp.mp.dps = 50
ln2, z3, pi2 = mp.log(2), mp.zeta(3), mp.pi**2
om1 = 2*pi2/3 + 8*ln2**2
om2 = 80*z3 - mp.mpf(8)/3*pi2*ln2 - mp.mpf(32)/3*ln2**3
print("Omega1 = 2 pi^2/3 + 8 ln^2 2      =", mp.nstr(om1, 30))
print("Omega2 = 80 zeta3 - 8/3 pi^2 ln2 - 32/3 ln^3 2 =", mp.nstr(om2, 30))
print("third term coefficient of 1/(D-3): Omega1/2 = pi^2/3 + 4 ln^2 2 =", mp.nstr(om1/2, 25))
print("fourth term coefficient of 1/(D-3)^2: Omega2/4 = 20 zeta3 - 2/3 pi^2 ln2 - 8/3 ln^3 2 =", mp.nstr(om2/4, 25))
om3 = mp.mpf("-652.8401075700561254352393037996")
print("Omega3/8 (coefficient of 1/(D-3)^3, fit) =", mp.nstr(om3/8, 20))
for D in (50, 200, 500, 1000, 2000):
    s = 2*(D-3)
    print(D, "Omega1/s", mp.nstr(om1/s, 6), "Omega2/s^2", mp.nstr(om2/s**2, 6), "Omega3/s^3", mp.nstr(om3/s**3, 6))
print("digits of the PSLQ residual 2.67e-44 against Omega2:", mp.nstr(mp.log10(om2/mp.mpf("2.67e-44")), 4))
print("digits of the P1 residual 2.41e-49 against Omega1:", mp.nstr(mp.log10(om1/mp.mpf("2.41e-49")), 4))
