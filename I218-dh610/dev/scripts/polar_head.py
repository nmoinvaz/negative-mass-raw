#!/usr/bin/env python3
"""Polar l = 1, 2 modes of the phantom black universes and the Ellis wormhole; radial modes of the M-AdS wormholes.  See polar.md.

    polar.py planted [--mutate=M]                       Ellis polar quasinormal modes (l = 2, 3, 4) against [ABCKY23] Table 1; the Ellis l = 1 problem;
                                                        the Ellis bound-state plant; the c -> 0+ limit of the M-AdS radial mode
    polar.py count ELL c [--res=R1|R2] [--out=F.json]   growing polar modes, l = ELL = 1 or 2, member c <= 0 (c = 0: Ellis), shooting, real W
    polar.py mads c [--res=R1|R2] [--out=F.json]        growing radial modes of the M-AdS wormhole c > 0 (Dirichlet at the AdS end)
    polar.py spectral DIR                               Chebyshev check of the M-AdS counts in DIR/mads_*_R2.json
    polar.py report DIR                                 tables, R1 against R2
    polar.py controls                                   runs every --mutate=M and asserts that its target fires

Units b = min R = 1.  Background and linearization: polar_derive.py (checked there); the coefficient table at the end of this file is its output.
Exit status 1 when a check fails (a mutated run is meant to exit 1).
"""
import glob
import json
import math
import os
import re
import subprocess
import sys
import time

os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/nm_i218_numba")
import numpy as np
from numba import njit
from scipy.integrate import ode, solve_ivp
from scipy.optimize import brentq, minimize_scalar, root

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import stability as st

# ------------------------------------------------------------------------------------------------ declared settings
W_LO, W_HI = 0.01, 8.0                                          # range searched, units 1/b
RES = {
    "R1": dict(rtol=1e-9, rmax0=150.0, rmaxW=30.0, nW=60, nWm=70, z0=0.04, nfrob=10, delta=0.3, ads=1.0),
    "R2": dict(rtol=1e-12, rmax0=300.0, rmaxW=45.0, nW=150, nWm=176, z0=0.03, nfrob=12, delta=0.2, ads=2.0),
}
W_HI_M = 24.0                                                   # M-AdS: the root grows like c^(0.7) (W = 5.2 at c = 3)
MEMBERS = st.MEMBERS + [0.0]                                    # #212's 20 black universes and the Ellis wormhole
ADS_C = [1e-4, 1e-3, 1e-2, 0.03, 0.1, 0.2, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0]
PROBES = [0.01, 0.1, 1.0, 3.0, 8.0]                              # W at which R1 and R2 determinants are compared
DIP_RATIO = 1e-3                                                # an interior minimum of |D| below this fraction of its neighbors counts as a double root
MUT = set()


def mutating(name):
    return name in MUT
