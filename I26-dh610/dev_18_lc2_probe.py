import mpmath as mp
mp.mp.dps = 40
q = mp.log(2)
def F(t):
    L1, Lt = mp.log(1+t), mp.log(t)
    w = 1/(1+t)
    i1 = Lt*L1**2 - mp.mpf(2)/3*L1**3 - 2*L1*mp.polylog(2, w) - 2*mp.polylog(3, w)      # int ln^2(1+t)/t
    i2 = q**2*Lt                                                                          # q^2/t
    i3 = Lt**3/12                                                                         # (1/4) ln^2 t / t
    i4 = -2*q*(-mp.polylog(2, -t))                                                        # -2q ln(1+t)/t
    i5 = -(-Lt*mp.polylog(2, -t) + mp.polylog(3, -t))                                     # - ln(1+t) ln t / t
    i6 = q*Lt**2/2                                                                        # q ln t / t
    return i1 + i2 + i3 + i4 + i5 + i6
def Lc2(th):
    t = mp.exp(2j*th)
    return (F(t) - F(mp.mpf(1)))/(2j)
for th in [mp.mpf("0.3"), mp.mpf("0.9"), mp.mpf("1.4")]:
    print(th, Lc2(th), mp.quad(lambda p: mp.log(mp.cos(p))**2, [0, th]))
