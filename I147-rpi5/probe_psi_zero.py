"""#147 probe: does a singular master-variable map reach E.5a? master_reduce (zerilli_derivation_lib.py, read only) is called with
psi = 0 on a two-dimensional flow; the prediction in README.md is ZeroDivisionError before any check could read det = 0."""
import os
import sys
sys.path.insert(0, '/home/nathan/Source/negative-mass-i147/phase2/dg_proof')
from zerilli_derivation_lib import *
u = [jet_sym('K', 0), jet_sym('H1', 0)]
flow = [u[1] / r + u[0] * s, -u[0] / r + u[1] * (1 / r)]       # any linear flow with nonzero coefficients
f = 1 - 2 * M / r
for name, psi in (('psi = u0 (control: must work)', u[0]), ('psi = 0', sp.Integer(0))):
    try:
        out = master_reduce(u, flow, psi, f)
        print('%-30s returned det = %s' % (name, sp.factor(out[2])))
    except Exception as e:
        print('%-30s raised %s: %s' % (name, type(e).__name__, e))
