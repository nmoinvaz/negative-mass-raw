# Route D's frame block at v_s = 0 (instants where the bubble is momentarily at rest)
import sys
sys.path.insert(0, '/home/nathan/Source/negative-mass-i78/notes/warp')
import sympy as sp
import phantom_source as ps
Ra = ps.shift_tetrad_ricci(-ps.VS[0]*ps.F[0], ps.bubble_rule(False), False)
c, S = sp.symbols('c S', real=True)
R3v = Ra[:3,:3].subs(ps.z, 0).subs({ps.VS[0]: 0}).subs({ps.X: ps.R*c, ps.y: ps.R*S})
print(R3v.applyfunc(sp.factor).tolist())
print("free symbols:", R3v.free_symbols)
