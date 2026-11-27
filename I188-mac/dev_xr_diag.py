"""dev (#188): why the stripped D depends on R_s. At two points of box b1 the crate (dd) at R_s = 100 ... 1200: the stripped phase relative to R_s = 1200,
with the exterior mass M and with M = 0 (mutate=mext0). If the dependence is a 1/R_s tail it falls like 1/R_s; a logarithm of a Coulomb tail would fall like ln R_s."""
import sys, json, subprocess, numpy as np
sys.argv = [sys.argv[0]]
w, rm = 0.7603, 24.10980364018201
ST = ["pc=3.86682473052039692307928581646122e-04", "zc=9.81119726886341895704711519478970e-01"]
B = "/Users/nathan/Source/negative-mass-i188/phase2/nonradial/taylor_polar/target/bins/new_complex"
pts = [complex(0.1, 1.0), complex(2.0, 2.5)]
Rs = [100.0, 150.0, 200.0, 300.0, 450.0, 600.0, 900.0, 1200.0]
def strip(s, rs):
    kp = np.sqrt(1 + (s - 1j*w)**2); km = np.sqrt(1 + (s + 1j*w)**2)
    return np.exp(-1j * ((kp + km) * (rs - rm) + (kp + km + s) * rm).imag)
for mut in (None, "mext0"):
    for l in (2, 6):
        for s in pts:
            vals = []
            for rs in Rs:
                args = ["nice", "-n", "10", B, "dc", "lane=f64", f"l={l}", *ST, f"rsfix={rs}", f"re={s.real!r}", f"im={s.imag!r}"] + ([f"mutate={mut}"] if mut else [])
                o = [json.loads(x) for x in subprocess.run(args, capture_output=True, text=True).stdout.splitlines() if '"dc"' in x[:12]][0]
                vals.append(complex(*o["d_f64"]) * strip(s, rs))
            ph = [float(np.angle(v / vals[-1])) for v in vals]
            md = [abs(abs(v) / abs(vals[-1]) - 1) for v in vals]
            print(f"mutate={mut} l={l} s={s}: phase vs R_s=1200: " + " ".join(f"{r:.0f}:{p:+.2e}" for r, p in zip(Rs, ph)) + f" | modulus max {max(md):.1e}", flush=True)
