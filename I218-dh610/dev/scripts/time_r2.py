import sys, time
sys.path.insert(0, "/home/nathan/Source/negative-mass-i218/notes/black_universe")
import _dev_polar as P
for c in (-10.0, -3.0, -0.3, 0.0):
  fam = P.st.Fam(c, "R2")
  for W in (0.01, 1.0, 5.0, 8.0):
    row = []
    for res in ("R1", "R2"):
        p = P.RES[res]
        t0 = time.time(); d2 = P.D_l2(W, fam, p); t1 = time.time(); d1 = P.D_l1(W, fam, p); row.append((d2, round(t1 - t0, 2), d1, round(time.time() - t1, 2)))
    print(c, W, "l2 R1 %.10e (%ss) R2 %.10e (%ss) | l1 R1 %.8e (%ss) R2 %.8e (%ss)" % (row[0][0], row[0][1], row[1][0], row[1][1], row[0][2], row[0][3], row[1][2], row[1][3]), flush=True)
