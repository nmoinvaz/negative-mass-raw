# Development: one canonical star near the crossing by ind194's shooting, timed, with the turning radius (not a criterion run).
import sys, time
sys.argv = ["ind194.py", "--only=none"]
exec(open("ind194.py").read().split("if OPT.scan:")[0])
P = 2.0504432387354122617e-04
t0 = time.time()
n = [0]
_shoot = shoot
def shoot(*a, **k):
    n[0] += 1
    return _shoot(*a, **k)
for rt in (1e-12,):
    st = ground(P, 1, rt)
    print(f"rtol {rt}: {n[0]} shots, {time.time() - t0:.1f} s; omega {st['omega']:.15f} M {st['M']:.15e} N {st['N']:.15e} alpha_c {st['alpha_c']:.12f} r_turn {st['r']:.2f} phi_r {st['phi_r']:.3e}", flush=True)
print("crate at omega 0.92584444: M 8.0657e-3 (crossing_p.txt row 0.92550: 0.008064656 at 0.92500)")
