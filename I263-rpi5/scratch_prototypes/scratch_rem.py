import sys, re
sys.path.insert(0, '/home/nathan/Source/negative-mass-i263/notes/wormhole_largeD')
sys.argv = sys.argv[:1]
import mpmath as mp
import order7 as o7
mp.mp.dps = 200
RAW = '/home/nathan/Source/negative-mass-raw/I263-rpi5'
txt = open(RAW + '/dev_05_grid_100_0.25_30_260.log').read()
vals = {int(m.group(1)): mp.mpf(m.group(2)) for m in re.finditer(r"    Omega(\d) = (\S+)", txt)}
ev = {n: {f"Om{i}": vals[i] for i in vals} for n in ("G1", "G2")}
for n in ev:
    ev[n]["grid"] = "N=100 dps=260"
o7.W2FILE = '/home/nathan/Source/negative-mass-i263/notes/wormhole_largeD/w2_output.txt'
o7.W2RAW = RAW + '/inputs_w2_growthD.txt'
o7.check_remainder(ev)
