#!/usr/bin/env python3
"""loc_report.py RUN_DUMP [BASE_DUMP]

The records of a feature-on dump (`loc` key: the counts of `multisolver::locate` along the walk that ended the record, and the
f64 fit of #167/#183 run beside it on the same steps) in four tables:
 1. totals per kind of dump file (offgrid, conical_global) and per record class;
 2. the records where `locate` said `Unresolved` or gave nothing at a step inside the gate, with what the old fit said on those
    steps (`unres_old_real`: steps where the old fit was a real singularity ahead and locate was not; `old_step`, `old_xstar`:
    where the f64 stop rule would have stopped, 0 and null if it would not have by then);
 3. the records where `locate` read a pair at some step, same columns;
 4. the records whose stop is not the old rule's (step differs from old_step, or old_xstar is null), and the largest
    differences between eta* and the old rule's eta* on the same steps.
With BASE_DUMP the class and kind of the baseline's record of the same position are added (files paired as `compare_run.py`
pairs them). A record is identified by the file's command line, F_inf and C."""
import json, os, shutil, sys, tempfile

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import compare_run as cr  # noqa: E402


def load(d):
    out = {}
    for f in sorted(os.listdir(d)):
        lines = open(os.path.join(d, f)).read().splitlines()
        if not lines:
            continue
        out[f] = (lines[0], [json.loads(l) for l in lines[1:] if l.startswith("{")])
    return out


def fmt(x):
    return "-" if x is None else (f"{x:.10g}" if isinstance(x, float) else str(x))


def main():
    run = load(sys.argv[1])
    base = None
    if len(sys.argv) > 2:
        tmp = tempfile.mkdtemp(prefix="loc_report_")
        cr.pair_dump(sys.argv[2], sys.argv[1], tmp)
        # the run's files under the base's names
        base = load(sys.argv[2])
        run = load(tmp)
        shutil.rmtree(tmp, ignore_errors=True)
    rows = []
    for f, (head, recs) in run.items():
        kindfile = f.split("_")[0]
        for i, r in enumerate(recs):
            if not isinstance(r, dict) or "loc" not in r:
                continue
            b = base[f][1][i] if base and f in base and i < len(base[f][1]) else None
            rows.append((kindfile, head, i, r, b))
    n = len(rows)
    print(f"records with a `loc` key: {n}")
    # table 1
    tot = {}
    for kf, head, i, r, b in rows:
        key = (kf, r.get("class"))
        t = tot.setdefault(key, dict(n=0, calls=0, unres=0, pair=0, nothing=0, shifted=0, no_old=0))
        L = r["loc"]
        t["n"] += 1
        t["calls"] += 1 if L["calls"] else 0
        t["unres"] += 1 if L["unresolved"] else 0
        t["pair"] += 1 if L["pair"] else 0
        t["nothing"] += 1 if L["nothing"] else 0
        if r.get("class") == "SINGULAR":
            t["shifted"] += 1 if (L["old_step"] and L["step"] != L["old_step"]) else 0
            t["no_old"] += 1 if not L["old_step"] else 0
    print("\n1. totals (records; records with calls of locate; with an Unresolved step; with a pair step; with no result at a step; "
          "SINGULAR records whose stop step differs from the old rule's; SINGULAR records the old rule would not have stopped by then)\n")
    print("| file kind | class | records | with calls | Unresolved | pair | nothing | stop step differs | old rule no stop |")
    print("|---|---|---|---|---|---|---|---|---|")
    for (kf, cl), t in sorted(tot.items(), key=lambda kv: (kv[0][0], str(kv[0][1]))):
        print(f"| {kf} | {cl} | {t['n']} | {t['calls']} | {t['unres']} | {t['pair']} | {t['nothing']} | {t['shifted']} | {t['no_old']} |")

    def table(title, pick):
        sel = [x for x in rows if pick(x[3]["loc"])]
        print(f"\n{title}: {len(sel)} records\n")
        if not sel:
            return
        print("| file command (start) | F_inf | C | class | kind | base class:kind | steps | calls | real | Unresolved | nothing | pair | "
              "old real | locate not real while old real | stop step | old stop step | eta* | old eta* |")
        print("|" + "---|" * 18)
        for kf, head, i, r, b in sel:
            L = r["loc"]
            c = r.get("c")
            c = c[0] if isinstance(c, list) else c
            bc = f"{b.get('class')}:{b.get('kind')}" if b else "-"
            print(f"| {head[:40]} | {fmt(r.get('fi'))} | {fmt(c)} | {r.get('class')} | {r.get('kind')} | {bc} | {r.get('steps')} | "
                  f"{L['calls']} | {L['real']} | {L['unresolved']} | {L['nothing']} | {L['pair']} | {L['old_real']} | {L['unres_old_real']} | "
                  f"{L['step']} | {L['old_step'] or '-'} | {fmt(r.get('xstar'))} | {fmt(L['old_xstar'])} |")

    table("2. records where locate said Unresolved or gave nothing at a gated step", lambda L: L["unresolved"] > 0 or L["nothing"] > 0)
    table("3. records where locate read a pair at a gated step", lambda L: L["pair"] > 0)
    table("4. records whose stop is not the old rule's", lambda L: L["old_step"] != 0 and L["step"] != L["old_step"])
    # the eta* against the old rule's on the same steps
    d = []
    for kf, head, i, r, b in rows:
        L = r["loc"]
        if r.get("class") == "SINGULAR" and L["old_xstar"] is not None and r.get("xstar") is not None:
            d.append((abs(r["xstar"] - L["old_xstar"]) / max(1.0, abs(r["xstar"])), r, head))
    d.sort(key=lambda t: -t[0])
    print(f"\n5. eta* against the old rule's eta* on the same steps: {len(d)} SINGULAR records with both; "
          f"largest |difference| / max(1, eta*) {d[0][0] if d else 0:.3e}; above 1e-12: {sum(t[0] > 1e-12 for t in d)}; "
          f"above 1e-10: {sum(t[0] > 1e-10 for t in d)}\n")
    for t in d[:8]:
        r = t[1]
        print(f"  {t[0]:.3e}  F_inf {r.get('fi')} C {r.get('c')}  eta* {r.get('xstar')!r}  old {r['loc']['old_xstar']!r}  [{t[2][:60]}]")


main()
