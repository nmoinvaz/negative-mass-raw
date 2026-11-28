import sys
sys.path.insert(0,'.')
from p8_log import go, F3
import sympy as sp
F5=F3+['hv','hu']
print('--- other members')
go(1,sp.Rational(2,3),6,F3,'VR',True)
go(2,sp.Rational(1,3),6,F3,'VR',True)
go(sp.Rational(3,2),sp.Rational(5,7),6,F3,'VR',True)
print('--- N=7, 8')
go(1,1,7,F3,'VR',True)
go(1,1,8,F3,'VR',True)
print('--- general gauge (5 fields)')
go(1,1,5,F5,'VR',False)
go(1,1,5,F5,'VR',True)
go(1,1,5,F5,'R',True)
