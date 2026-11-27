#!/usr/bin/env python3
"""diagnostic (not a run of ind183): the end state of ind183's scipy integration at (0.2, -30)"""
import sys
sys.argv = ["ind183.py"]
src = open("ind183.py").read().split("CANDS = ")[0]
exec(src)
from fractions import Fraction
import mpmath as mp
F, F1, F2 = [float(x) for x in cg.series_mp(Fraction(0.2), Fraction(-30), mp.mpf(200), 1)]
ev = lambda eta, y: abs(y[1]) - 1e8
ev.terminal = True
sol = solve_ivp(rhs, (200, 1e-6), [F, F1, F2], method="DOP853", rtol=1e-12, atol=1e-14, events=[ev])
print("status", sol.status, sol.message)
print("t_events", sol.t_events, "y_events", sol.y_events)
print("last t", sol.t[-1], "last y", sol.y[:, -1])
print("F^2 - eta^2 - 1 at end", sol.y[0, -1]**2 - sol.t[-1]**2 - 1)
