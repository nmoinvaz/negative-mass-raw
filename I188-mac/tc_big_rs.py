"""#188, for the note on #116: the crate's time per D at the l = 2 box's point 0.1 + 1i as the scalar plane's start radius R_s grows
(dd and f64), and the strip's argument. Not a check."""
import json, subprocess, sys, numpy as np
ST = ["pc=3.86682473052039692307928581646122e-04", "zc=9.81119726886341895704711519478970e-01"]
B = sys.argv[1] if len(sys.argv) > 1 else "/Users/nathan/Source/negative-mass-i188/phase2/nonradial/taylor_polar/target/bins/new_complex"
w, rm = 0.7603, 24.10980364018201
s = complex(0.1, 1.0)
print("# l = 2, s = 0.1 + 1i; time per D by R_s (one process, nice 10)")
print("# lane R_s steps_y steps_q steps_s t_y t_s wall strip_argument")
for lane in ("f64", "dd"):
    for rs in (405.0, 1000.0, 2000.0, 4000.0, 8000.0):
        args = ["nice", "-n", "10", B, "dc", f"lane={lane}", "l=2", *ST, f"rsfix={rs}", f"re={s.real!r}", f"im={s.imag!r}"]
        o = [json.loads(x) for x in subprocess.run(args, capture_output=True, text=True).stdout.splitlines() if x.startswith('{"cmd":"dc",')][0]
        kp = np.sqrt(1 + (s - 1j*w)**2); km = np.sqrt(1 + (s + 1j*w)**2)
        arg = ((kp + km) * (rs - rm) + (kp + km + s) * rm).imag
        print(f"{lane} {rs:.0f} {o['steps_y']} {o['steps_q']} {o['steps_s']} {o['t_y']:.3f} {o['t_s']:.3f} {o['wall']:.3f} {arg:.1f}", flush=True)
