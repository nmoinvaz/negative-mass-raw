import sys; sys.path.insert(0,'/tmp/claude-1000/-home-nathan-Source-negative-mass-i168/8e4f5756-108b-457a-974a-8882f6064c2d/scratchpad')
from ia import *
from fractions import Fraction as Fr
U=Fr(1,500)          # u <= 1/500
# parameters: sigma in [0,U], b in [0,U], sigma+b<=U, a^2=sigma b so a<=U/2
def iv(lo,hi): return Iv(Fr(lo),Fr(hi))
S=iv(0,U); B=iv(0,U); A=iv(0,U/2)
kap=1-B+S; mu=1+3*S-B+2*S**2-6*B*S; c=1+2*S
print("kappa",kap,"mu",mu,"c",c)
for om in [iv(-100,100),iv(-1,1)]:
    M=mu+(B-S)*om
    print("om",om,"M",M)
# (S1) shape: with M in [Mlo,Mhi], kappa in [klo,khi] (om in [-100,100])
om=iv(-100,100); M=mu+(B-S)*om
# 4M-3kappa>0 : P'(-1/(4a))>0 ; 
print("4M-3kap:", 4*M-3*kap)
# 32a^2 P(-1/(4a)) = kap-2M+32 a^2 (c^2-c-om^2)
print("32a^2P(-1/4a):", kap-2*M+32*A**2*(c**2-c-om**2))
# P(-2)=16 a kap -4M -8 a c + c^2 - om^2 ; P(2) = -16 a kap -4M +8ac + c^2 - om^2   (use om range wide; sign needs c^2-om^2 term)
P_m2 = 16*A*kap - 4*M - 8*A*c + c**2 - om**2
P_p2 = -16*A*kap - 4*M + 8*A*c + c**2 - om**2
print("P(-2):",P_m2," P(2):",P_p2)
# sharper: for |om|<=100 om^2 up to 1e4 only helps negative; need max of P(+-2): 
# P(+-2) <= 16a kap -4M +8ac + c^2 (drop -om^2<=0)
print("P(+-2) upper (drop om^2):", 16*A*kap - 4*M + 8*A*c + c**2)
# small roots exist only if om^2 <= c^2+16 a kap+8 a c
print("om^2 bound:", c**2+16*A*kap+8*A*c)
# for |om|<=1/2: P(0)=c^2-om^2>0 ; P(+-1/2)>0 : P(1/2)= -a kap/4 - M/4 + 2ac + c^2-om^2 
om5=iv(Fr(-1,2),Fr(1,2)); M5=mu+(B-S)*om5
print("P(1/2) lower:", -A*kap*Fr(1,4)-M5*Fr(1,4)+2*A*c*0 + c**2 - om5**2)   # 2ac>=0 dropped
print("P(-1/2) lower:", A*kap*Fr(1,4)-M5*Fr(1,4)-2*A*c + c**2 - om5**2)
# Xi bound: |e|<= y^2 [ |kap-mu-(b-s)om| + 16 a^2 c + 16 a^2 |om^2 - c^2| ]/kap  with om=2/y
def ehat_bound(ylo,yhi):
    Y=iv(ylo,yhi); omg=2*Fr(1)/Y if False else None
best=Fr(0)
import itertools
def sup_over_box(ylo,yhi,n=40):
    worst=Fr(0)
    for i in range(n):
        y0=Fr(ylo)+(Fr(yhi)-Fr(ylo))*i/n; y1=Fr(ylo)+(Fr(yhi)-Fr(ylo))*(i+1)/n
        Y=iv(y0,y1)
        omg=iv(2/y1,2/y0)
        # worst over sigma,b in simplex scaled by u: take sigma=u*f, b=u*(1-f): bound with intervals F in [0,1]
        Fv=iv(0,1)
        Sg=Fv*U; Bb=(1-Fv)*U; Aa2=Sg*Bb  # a^2 = s b
        kp=1-Bb+Sg; mu_=1+3*Sg-Bb+2*Sg**2-6*Bb*Sg; cc=1+2*Sg
        num = (-1)*(2*Sg+2*Sg**2-6*Bb*Sg) - (Bb-Sg)*omg   # kap-mu-(b-s)om
        mag = num.mag() + 16*Aa2.hi*cc.hi + 16*Aa2.hi*max(abs((omg**2-cc**2).lo),abs((omg**2-cc**2).hi))
        val = (Y.hi**2*mag/kp.lo)/U
        worst=max(worst,val)
    return worst
print("c_e on y in [7/2,9/2] (num bound):", float(sup_over_box(Fr(7,2),Fr(9,2))))
