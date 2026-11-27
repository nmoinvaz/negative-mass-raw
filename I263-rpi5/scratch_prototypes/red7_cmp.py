import re
import mpmath as mp
mp.mp.dps = 160
q, pi, z3, z5 = mp.ln2, mp.pi, mp.zeta(3), mp.zeta(5)
om5 = (mp.mpf(256)/45*q**6 + mp.mpf(64)/9*pi**2*q**4 - mp.mpf(2560)/3*q**3*z3 - 3072*q**2*z3 + mp.mpf(176)/45*pi**4*q**2 - 12288*q*z3 + 640*pi**2*q*z3
       + mp.mpf(9728)/45*pi**4*q + 41728*q*z5 - mp.mpf(38812)/315*pi**6 - 36864*z3 - mp.mpf(256)/3*pi**2*z3 + 3200*z3**2 + 74240*z5 + mp.mpf(39424)/45*pi**4)
txt = open('/home/nathan/Source/negative-mass-raw/I263-rpi5/dev_05_grid_100_0.25_30_260.log').read()
vals = {int(m.group(1)): mp.mpf(m.group(2)) for m in re.finditer(r"    Omega(\d) = (\S+)", txt)}
print(mp.nstr(om5, 70))
print(mp.nstr(vals[5], 70))
print("digits:", mp.nstr(-mp.log10(abs(om5 - vals[5]) / vals[5]), 6))
