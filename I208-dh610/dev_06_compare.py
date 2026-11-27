"""dev_06: digits between the Omega3 (and Omega0 .. Omega2) of the development grids dev_01 .. dev_05, parsed from their logs"""
import re, sys, glob
import mpmath as mp
mp.mp.dps = 300
logs = {"B1 N40 w.5 V18 d120": "dev_01_grid_B1.log", "B2 N50 w.4 V20 d140": "dev_02_grid_50_0.4_20_140.log",
        "N60 w.4 V24 d200": "dev_03_grid_60_0.4_24_200.log", "N60 w.4 V24 d240": "dev_04_grid_60_0.4_24_240.log",
        "N70 w1/3 V26 d240": "dev_05_grid_70_0.3333333333333333333.log"}
val = {}
for n, f in logs.items():
    t = open(f).read()
    val[n] = [mp.mpf(re.search(rf"Omega{i} = (\S+)", t).group(1)) for i in range(4)]
    m = re.search(r"\s(\d+) s\n", t.split("panels=")[1]) if "panels=" in t else None
names = list(val)
ref = val["N70 w1/3 V26 d240"]
for n in names:
    print(f"{n:22s} digits against the N70 grid: " + " ".join(f"{float(-mp.log10(abs(val[n][i]-ref[i])/abs(ref[i]))) if val[n][i]!=ref[i] else 999:.1f}" for i in range(4)))
a, b = val["N60 w.4 V24 d200"], val["N60 w.4 V24 d240"]
print("same grid N60, dps 200 vs 240, digits: " + " ".join(f"{float(-mp.log10(abs(a[i]-b[i])/abs(a[i]))):.1f}" for i in range(4)))
