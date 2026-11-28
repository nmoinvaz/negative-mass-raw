#!/usr/bin/env python3
"""make_jobs.py: writes the job files of the controls, dev_jobs_*.txt (development runs, to read the targets) and ctl_jobs_*.txt (controls of record), lines "name|command".
Commands run from notes/wormhole_largeD with env PY (python), RAW (this folder). dev: the controls' own stand-ins (dev_cgrids.json from the nominal T1 run, dev_planted_f8.json);
ctl: the saved Omega's of record (G1.json, G2.json) for T2, T2b, T2bxf; the planted f8 for ST."""
import os

raw = os.path.dirname(os.path.abspath(__file__))
REF = "--ref282=$RAW/inputs_I282_G1.json,$RAW/inputs_I282_G2.json --w2raw=$RAW/inputs_w2_growthD.txt"
groups = {
    "chk": ("sym struct cache", ["nominal", "wrong_h", "wrong_c6", "wrong_c7", "wrong_c8", "wrong_c9", "stale_cache", "ln2_struct"], 10),
    "zvc": ("zv", ["nominal", "zeta53_wrong"], 11),
    "t1": (None, ["cnom", "wrong_h", "wrong_c6", "wrong_c7", "wrong_c8", "wrong_c9", "wrong_Om0", "wrong_Om1", "wrong_Om2", "wrong_Om3", "wrong_Om4", "wrong_Om5", "wrong_Om6",
                  "coarse_B", "short_tail", "stale_cache"], 12),
    "t2": (None, ["nominal", "pslq_wrong_basis", "pslq_wrong_target", "wrong_Om7_series", "wrong_closed5", "wrong_closed6"], 13),
    "t2b": (None, ["nominal", "pslq_wrong_basis", "pslq_wrong_target"], 14),
    "st": (None, ["nominal", "ln2_leak", "f8_rel", "ln2_zl", "zeta53_wrong"], 15),
    "t2bxf": (None, ["nominal", "pslq_wrong_basis", "pslq_wrong_target"], 16),
}


def cmd(group, ctl, dev):
    mut = "" if ctl in ("nominal", "cnom") else f" --mutate={ctl}"
    if group in ("chk", "zvc"):
        return f"$PY -I order9.py {groups[group][0]}{mut}"
    if group == "t1":
        save = " --save=$RAW/dev_cgrids.json" if (dev and ctl == "cnom") else ""
        return f"$PY -I order9.py evals values remainder pslq --cgrids --bases=F1,F3 --no-real {REF}{save}{mut}"
    load = "$RAW/dev_cgrids.json" if dev else "$RAW/G1.json,$RAW/G2.json"
    if group == "t2":
        return f"$PY -I order9.py values pslq remainder --no-real --bases=F1,F3,F5 --pslq-cap=200 --load={load} {REF}{mut}"
    plant = "$RAW/dev_planted_f8.json"
    if group == "t2b":
        return f"$PY -I order9.py pslq --no-real --bases=F2,F4,F6,F7,F7m,X1,X2,X3 --pslq-cap=300 --load={plant if dev else load}{mut}"
    if group == "t2bxf":
        return f"$PY -I order9.py pslq --no-real --bases=XF --pslq-cap=300 --load={plant if dev else load}{mut}"
    if group == "st":
        nm = f"{'dev' if dev else 'ctl'}_st_{ctl}"
        return f"$PY -I order9.py pslq --bases=F7 --pslq-cap=300 --save-rel=$RAW/{nm}_rel.json closed7 --rel=$RAW/{nm}_rel.json --load={plant}{mut}"


for dev in (True, False):
    for g, (_, ctls, num) in groups.items():
        pre = f"dev_{num}_{g}" if dev else f"ctl_{g}"
        with open(os.path.join(raw, ("dev_jobs_" if dev else "ctl_jobs_") + g + ".txt"), "w") as f:
            for c in ctls:
                f.write(f"{pre}_{c}|{cmd(g, c, dev)}\n")
print("written")
