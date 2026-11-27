import sys, os, numpy as np
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i255/notes/wormhole_evolution"))
import throat_locus as tl
raw = os.path.expanduser("~/Source/negative-mass-raw/I225-dh610/runs/stall")
for D, hs in ((5, ("0.00707107", "0.00353553", "0.00176777")), (4, ("0.02", "0.01", "0.005"))):
    for h in hs:
        La = tl.load_run(f"{raw}/stall_D{D}_h{h}_side-1.npz")
        Lb = tl.load_run(f"{raw}/stall_D{D}_h{h}_side1.npz")
        print(f"D={D} h={h}: slices {len(La['s'])},{len(Lb['s'])}; crossings a {La['cross']} b {Lb['cross']}")
        common = np.intersect1d(La["s"], Lb["s"])
        ia, ib = np.searchsorted(La["s"], common), np.searchsorted(Lb["s"], common)
        t = La["t"][ia]
        for tt in (4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15):
            k = np.argmin(abs(t - tt))
            print(f"  t={t[k]:5.2f} r- {La['r'][ia[k]]:.5f} r+ {Lb['r'][ib[k]]:.5f} mean {0.5*(La['r'][ia[k]]+Lb['r'][ib[k]]):.5f} | l- {La['l'][ia[k]]:+.4f} l+ {Lb['l'][ib[k]]:+.4f} | f- {La['f'][ia[k]]:+.4f} f+ {Lb['f'][ib[k]]:+.4f}")
