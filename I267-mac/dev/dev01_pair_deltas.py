"""dev01: the pair p*_h -/+ 10^-e through #266's member_cmd for e = 5 .. 12 at one h (development: timing, departure times, member rows, events inside the triangle).
Reads p*_h from #266's raw (read only). usage: dev01_pair_deltas.py H E1,E2,... OUTDIR"""
import json, os, sys, time
sys.argv, args = sys.argv[:1], sys.argv[1:]
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i267/notes/wormhole_evolution"))
import settled_mass_b as b
h = float(args[0]); es = [float(x) for x in args[1].split(",")]; out = args[2]
pdir = os.path.expanduser("~/Source/negative-mass-raw/I266-mac/runs")
for e in es:
    t0 = time.time()
    o = os.path.join(out, f"e{e:g}", f"h{h:g}")
    b.member_cmd("G", 0.1, h, o, pdir, e=e)
    m = json.load(open(o + "/member.json"))
    print(f"e = {e:g} h = {h:g}: {time.time() - t0:.0f} s, t_dep {m['t_dep']}, cross_a {m['cross_a']}, cross_b {m['cross_b']}, ev40_a {m['ev40_a']}, ev40_b {m['ev40_b']}", flush=True)
