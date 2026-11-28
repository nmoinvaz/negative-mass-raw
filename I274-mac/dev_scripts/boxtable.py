"""markdown table of the 35 boxes for the README: reads recount_i274.py --list (run from phase2/nonradial)"""
import subprocess, sys, os
PY = sys.executable
out = subprocess.run([PY, "recount_i274.py", "--list"], capture_output=True, text=True, check=True).stdout.splitlines()
print("| box | source | l | eps, omega | region | extra options | R_s (log) | stored winding | max step | min abs D | planted (stored) |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for ln in out[:-1]:
    parts = ln.split("|"); name, src, a, st, rs = parts[0], parts[1], parts[2], "|".join(parts[3:-1]), parts[-1]
    tok = a.split()
    pos = [t for t in tok if not t.startswith("--")]
    opts = " ".join(t for t in tok if t.startswith("--") and not t.startswith("--plant") and not t.startswith("--guard"))
    plant = [t for t in tok if t.startswith("--plant")][0][8:]
    y0 = [t[5:] for t in tok if t.startswith("--y0=")]
    region = f"Re s [{pos[3]}, {pos[4]}], " + (f"Im s [{y0[0]}, {pos[5]}]" if y0 else f"abs(Im s) ≤ {pos[5]}")
    import re
    m = re.match(r"winding (\S+), max step (\S+), min\|D\| (\S+), planted (\S+) of (\d) PASS", st)
    print(f"| {name} | {src} | {pos[2]} | {pos[0]}, {pos[1]} | {region} | {opts or '-'} | {rs[4:]} | {m.group(1)} | {m.group(2)} | {m.group(3)} | {m.group(4)} of {m.group(5)} at {plant} |")
