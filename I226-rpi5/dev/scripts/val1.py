import sys, time, numpy as np
sys.path.insert(0, "/home/nathan/Source/negative-mass-i226/notes/wormhole_evolution")
import dn, constraint_plateau as cp
# validate streaming vs dn.constraints on a small static grid and a small pulse grid
for fam, A, n, h, X in (("static", 0.0, 3, 0.05, 6.0), ("S", 0.02, 3, 0.05, 8.0)):
    d = cp.make_data(n, h, X, fam, A)
    t0 = time.time()
    res = dn.evolve(d, store=True, stop=False)
    Cpp, Cmm = dn.constraints(res)
    t1 = time.time()
    st, info = cp.stream(d, stop=False)
    t2 = time.time()
    N = d.N
    # brute-force prefix maxima from dn.constraints arrays
    worst = 0.0
    for k in range(st.nx):
        If = st.If[k]
        for which, C, off in (("pp", Cpp, 1), ("mm", Cmm, 0)):
            # C[i_index, j]; pp: i = idx+1; mm: j = idx+1, i = idx
            if which == "pp":
                A_ = np.abs(np.nan_to_num(C, nan=0.0))            # [i-1, j]
                m = A_[: max(If, 0), :]  # nodes i = 1..If
                m = m[:, : If + 1] if m.size else m
                bf = m.max() if m.size else 0.0
                got = st.pv[: If + 1, k].max()
            else:
                A_ = np.abs(np.nan_to_num(C, nan=0.0))            # [i, j-1]
                m = A_[: If + 1, : If]  # i = 0..If, j = 1..If
                bf = m.max() if m.size else 0.0
                got = st.mv[: If + 1, k].max()
            worst = max(worst, abs(bf - got))
    print(fam, "N", N, "evolve+constraints %.2fs stream %.2fs" % (t1 - t0, t2 - t1), "max|C|", np.nanmax(np.abs(Cpp)), np.nanmax(np.abs(Cmm)), "worst prefix-max difference", worst)
