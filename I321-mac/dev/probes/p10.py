import sys
sys.path.insert(0,'.')
from p8_log import go, F3
import sympy as sp
r=go(1,None,6,F3,'VR',True,sym=True)
r=go(1,None,6,F3,'R',True,sym=True)
r=go(2,None,6,F3,'VR',True,sym=True)
