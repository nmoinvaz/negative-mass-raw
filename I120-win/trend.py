"""Trend of the leading |mu| v_c of sectors m = 23/2 to 41/2 (#120), from the stored eigenvalues. Reads eig/ beside this
file. Shares nothing with tanh_spectrum_check.py but the .npz layout. Prints, per sigma R and sector: A's and B's leading
|mu| v_c, the signed (A - B) / A, m |mu| v_c, the step of m |mu| v_c from the sector before, the local exponent
d ln|mu| / d ln m between the two sectors, the margin to the speed-bound line, and ARPACK's count and smallest |mu| v_c.
The m = 21/2 row is #75's printed leading value (the script's REF). Run with the venv python from any directory."""
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
R75 = {2: 0.083018, 4: 0.094358}  # #75's leading |mu| v_c at m = 21/2 (tanh_spectrum.md section 4)
LINE = {2: 0.0830, 4: 0.0944}
for sig in (2, 4):
    print(f"\nsigma R = {sig}, line {LINE[sig]}")
    print("  m    | lead A     | lead B     | (A-B)/A  | m lead  | step    | local exponent | lead/line | "
          "eigs A/B | smallest |mu| v_c A / B | worst residual")
    prev_m, prev_l = 10.5, R75[sig]
    print(f"  {prev_m:4g} | {prev_l:.6f}   | (#75)      |          | {prev_m * prev_l:.5f} |")
    prev_ml = prev_m * prev_l
    signs = []
    for k in range(23, 42, 2):
        m = k / 2
        A = np.load(os.path.join(HERE, "eig", f"s{sig}_A_m{k}.npz"))
        B = np.load(os.path.join(HERE, "eig", f"s{sig}_B_m{k}.npz"))
        la, lb = abs(A["mu"][0]) * float(A["vc"]), abs(B["mu"][0]) * float(B["vc"])
        sma, smb = abs(A["mu"][-1]) * float(A["vc"]), abs(B["mu"][-1]) * float(B["vc"])
        ml = m * la
        expo = np.log(la / prev_l) / np.log(m / prev_m)
        signs.append(np.sign(la - lb))
        print(f"  {m:4g} | {la:.6f}   | {lb:.6f}   | {(la - lb) / la:+.1e} | {ml:.5f} | {ml - prev_ml:+.5f} | "
              f"{expo:+.4f}        | {la / LINE[sig]:.4f}    | {len(A['mu'])}/{len(B['mu'])}     | {sma:.4f} / {smb:.4f}"
              f"            | {max(float(A['res']), float(B['res'])):.0e}")
        prev_m, prev_l, prev_ml = m, la, ml
    print(f"  sign of |mu|_A - |mu|_B over the 10 sectors: {''.join('+' if s > 0 else ('-' if s < 0 else '0') for s in signs)}")
