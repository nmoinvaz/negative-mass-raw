"""dev_06: can README.md's 'A fit of the r-integration values in 1/D gives W^2 a^2 - 2(D - 2) = -4.77259 +- 1e-5' be reproduced?
No script in the repository produced it (git log -S: e9c2c47, a notes commit). Try polynomial fits y = W^2 - 2(D-2) in x = 1/D
and in x = 1/(D-3) on the old csv rows (613e866) and the new ones, several degrees and D ranges. Reported only."""
import csv, subprocess, sys
import numpy as np
def rows(text): return {int(r["D"]): float(r["W2a2"]) for r in csv.DictReader(text.splitlines())}
old = rows(subprocess.run(["git", "-C", "/home/nathan/Source/negative-mass-i200", "show", "613e866:notes/wormhole_largeD/growth.csv"], capture_output=True, text=True).stdout)
new = rows(open("/home/nathan/Source/negative-mass-i200/notes/wormhole_largeD/growth.csv").read())
target = -2 - 4 * np.log(2)
print(f"target -2 - 4 ln 2 = {target:.7f}")
for name, data in (("old", old), ("new", new)):
    for var in ("1/D", "1/(D-3)"):
        for dmin in (20, 50):
            Ds = np.array([D for D in sorted(data) if D >= dmin], float)
            y = np.array([data[int(D)] - 2 * (D - 2) for D in Ds])
            x = 1 / Ds if var == "1/D" else 1 / (Ds - 3)
            out = []
            for deg in (1, 2, 3, 4):
                if len(Ds) > deg + 1:
                    c = np.polyfit(x, y, deg)
                    out.append(f"deg {deg}: {c[-1]:.6f} ({c[-1] - target:+.1e})")
            print(f"{name} rows, x = {var:8s}, D >= {dmin:2d}: " + "; ".join(out))
