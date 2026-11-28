import sys, os, time
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i266/notes/wormhole_evolution"))
import settled_mass_b as b
for g1 in (0.0, 0.00293, 0.0483, 0.0755, 0.3):
    for h in (0.02, 0.01, 0.005):
        t0 = time.time()
        r = b.planted_member_case(h, 13.0, g1)
        print(f"g1 {g1:7.5f} h {h:5.3f}: g1_rec {r['g1_rec']:+.6f} (err {r['g1_rec']-g1:+.1e}) rth {r['rth']:.6f} rec {r['rth_rec']:.6f} (err {r['rth_rec']-r['rth']:+.1e}) fit rms {r['rms']:.1e} | m+ {r['mp']:+.5f} rec {r['mp_rec']:+.5f}  m- {r['mm']:+.5f} rec {r['mm_rec']:+.5f} ({time.time()-t0:.1f} s)", flush=True)
