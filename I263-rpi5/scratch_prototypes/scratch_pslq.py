import sys, re, time
sys.path.insert(0, '/home/nathan/Source/negative-mass-i263/notes/wormhole_largeD')
sys.argv = sys.argv[:1]
import mpmath as mp
import order7 as o7
mp.mp.dps = 260
RAW = '/home/nathan/Source/negative-mass-raw/I263-rpi5'
txt = open(RAW + '/dev_05_grid_100_0.25_30_260.log').read()
vals = {int(m.group(1)): mp.mpf(m.group(2)) for m in re.finditer(r"    Omega(\d) = (\S+)", txt)}
ev = {n: {f"Om{i}": vals[i] for i in vals} for n in ("G1", "G2")}
for n in ev:
    ev[n]["grid"] = "N=100 dps=260"
o7.PSLQ_CAP = 140
o7.BASES_SEL = sys.argv_extra if hasattr(sys, 'argv_extra') else ["Q1", "Q3", "Q5"]
t0 = time.time()
o7.check_pslq(ev)
print(time.time() - t0)
