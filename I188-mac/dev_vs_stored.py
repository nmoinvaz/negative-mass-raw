"""dev (#188): the complex crate against stored winding2 values at a few points of the box (strip applied here)."""
import sys, json, pickle, subprocess, numpy as np
cache = pickle.load(open(sys.argv[1], 'rb')); l = int(sys.argv[2]); lane = sys.argv[3]; rs = sys.argv[4]; binp = sys.argv[5]
targets = [complex(t) for t in sys.argv[6].split(';')]
w, rm = 0.7603, 24.10980364018201
pts = []
for t in targets:
    k = min(cache, key=lambda c: abs(c - t))
    if k not in pts: pts.append(k)
ST = ["pc=3.86682473052039692307928581646122e-04", "zc=9.81119726886341895704711519478970e-01"]
args = [binp, "dc", f"lane={lane}", f"l={l}", *ST, f"rsfix={rs}", "re=" + ",".join(repr(p.real) for p in pts), "im=" + ",".join(repr(p.imag) for p in pts)]
out = subprocess.run(["nice", "-n", "10"] + args, capture_output=True, text=True).stdout
for line, s in zip([json.loads(x) for x in out.splitlines() if '"dc"' in x[:12]], pts):
    kp = np.sqrt(1 + (s - 1j*w)**2); km = np.sqrt(1 + (s + 1j*w)**2)
    strip = np.exp(-1j * ((kp + km) * (float(rs) - rm) + (kp + km + s) * rm).imag)
    d = complex(line['d_f64'][0], line['d_f64'][1]) * strip
    st = cache[s]
    print(f"s={s:.4f} crate {d:.6e} stored {st:.6e} rel {abs(abs(d)/abs(st)-1):.1e} phase {abs(np.angle(d/st)):.1e} wall {line['wall']:.2f}s steps {line['steps_y']}/{line['steps_q']}/{line['steps_s']} r_s {line['r_s']}")
