import sys, os, numpy as np
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i255/notes/wormhole_evolution"))
import throat_locus as tl
raw = os.path.expanduser("~/Source/negative-mass-raw/I225-dh610/runs/stall")
D = int(sys.argv[1]); h = sys.argv[2]; n = D-2
Ra = [float(x) for x in sys.argv[3].split(",")]
L = tl.load_run(f"{raw}/stall_D{D}_h{h}_side-1.npz")
print("t  r_th | M+(R) ... | M-(R) ...  (absolute R =", Ra, ")")
for sk in sorted(L["prof"]):
    k = np.searchsorted(L["s"], sk)
    if k >= len(L["s"]) or L["s"][k] != sk: continue
    t = L["t"][k]; rth = L["r"][k]
    Mp, Mm, rn_, ic, M = tl.slice_masses(L, sk, n, np.array(Ra))
    print(f"t={t:5.2f} r_th {rth:.4f} v {L['v'][k]:+.3f} | +: " + " ".join(f"{x:+.4f}" for x in Mp) + " | -: " + " ".join(f"{x:+.4f}" for x in Mm))
