"""Run he_type_exact of a given he_type.py on the tiny-D tensors of #103 (the old code is main 29e395d's he_type.py).

usage: probe_old_code.py <dir holding he_type.py and phantom_source.py> <case>
cases: Irat  Type I, R = (eps/3) [[1,1,0],[1,1,3],[0,3,0]], eps = 10^-10 (rational entries; D(R0) = 729 = 3^6)
       Irad  Type I, R = mu diag(0, 1, -1), mu = 10^-10 2^(-1/3)
       IVrad Type IV, R = mu [[0,1,0],[1,0,0],[0,0,0]]
All three are boosted and rotated like planted_cases, with e_3 entry -5/11 times the scale. D = 10^-60, 10^-60, -10^-60.
"""
import sys, time
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
import sympy as sp
import he_type as ht
Q = sp.Rational
B1 = sp.Matrix([[Q(5, 3), Q(4, 3), 0], [Q(4, 3), Q(5, 3), 0], [0, 0, 1]])
B2 = sp.Matrix([[Q(13, 12), 0, Q(5, 12)], [0, 1, 0], [Q(5, 12), 0, Q(13, 12)]])
Rot = sp.Matrix([[1, 0, 0], [0, Q(3, 5), -Q(4, 5)], [0, Q(4, 5), Q(3, 5)]])
L = B1 * Rot * B2
eps = Q(1, 10**10)
mu = eps * sp.Integer(2)**Q(-1, 3)
case = sys.argv[2]
T3, scale = {"Irat": (eps / 3 * sp.Matrix([[1, 1, 0], [1, 1, 3], [0, 3, 0]]), eps / 3),
             "Irad": (mu * sp.diag(0, 1, -1), mu),
             "IVrad": (mu * sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]), mu)}[case]
T3 = L.T * T3 * L
T4 = sp.zeros(4, 4)
T4[:3, :3] = T3
T4[3, 3] = Q(-5, 11) * scale
c2, c1, c0 = ht.cubic(ht.mixed_block([[T4[a, b] for b in range(3)] for a in range(3)]))
D = ht.disc(c2, c1, c0)
print(f"{case}: D = {D}, sp.nsimplify(D) = {sp.nsimplify(D)}", flush=True)
t = time.time()
print(f"he_type_exact -> {ht.he_type_exact(T4)} in {time.time() - t:.1f} s", flush=True)
