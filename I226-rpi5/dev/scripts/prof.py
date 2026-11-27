import sys, json, time, numpy as np
sys.path.insert(0, "/home/nathan/Source/negative-mass-i226/notes/wormhole_evolution")
import constraint_plateau as cp, dn
RAW = "/home/nathan/Source/negative-mass-raw/I40-dh610/runs/"
D, hname, fam = int(sys.argv[1]), sys.argv[2], sys.argv[3]
X = {5: 18.0, 6: 15.0}[D]; n = D - 2
sm = json.load(open(RAW + f"D{D}_{fam}_h{hname}/summary.json")); ck = json.load(open(RAW + f"D{D}_{fam}_h{hname}/constraints.json"))
h = sm["h"]; A = ck["lo"]["A"]
d = cp.make_data(n, h, X, fam, A)
st, info = cp.stream(d, stop=True)
out = dict(D=D, h=h, A=A, events={k: list(v) for k, v in info["events"].items()},
           t=((np.arange(st.nT) + 0.5) * cp.TW).tolist(), pp=st.tv["pp"].tolist(), mm=st.tv["mm"].tolist(),
           ppi=st.ti["pp"].tolist(), ppj=st.tj["pp"].tolist())
json.dump(out, open(sys.argv[4], "w"))
print(D, h, info["events"])
