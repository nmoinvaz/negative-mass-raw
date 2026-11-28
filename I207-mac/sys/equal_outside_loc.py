#!/usr/bin/env python3
"""equal_outside_loc.py DUMP_A DUMP_B

C8: the two dumps hold the same files (same names, same first lines) and the same records, every value equal after parsing
(floats bit for bit: the text of a float is its shortest round-trip form), except the `loc` key of a record, whose counts the
gate changes by design (calls of `locate`). Prints the numbers; exit 1 on any difference. `--mutate=eta` moves one `xstar` of a
copy of B by one ulp and `--mutate=count` changes one `steps`, to show the check fails."""
import json, math, os, shutil, sys, tempfile

def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k != "loc"}
    if isinstance(o, list):
        return [strip(x) for x in o]
    return o

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    mut = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
    a, b = args
    if mut:
        tmp = tempfile.mkdtemp(prefix="eq_loc_")
        shutil.copytree(b, os.path.join(tmp, "b"))
        b = os.path.join(tmp, "b")
        done = False
        for f in sorted(os.listdir(b)):
            if done:
                break
            p = os.path.join(b, f)
            lines = open(p).read().split("\n")
            for i, l in enumerate(lines):
                if l.startswith("{"):
                    o = json.loads(l)
                    if mut == "eta" and isinstance(o.get("xstar"), float):
                        o["xstar"] = math.nextafter(o["xstar"], math.inf)
                    elif mut == "count" and isinstance(o.get("steps"), int):
                        o["steps"] += 1
                    else:
                        continue
                    lines[i] = json.dumps(o)
                    open(p, "w").write("\n".join(lines))
                    done = True
                    break
        print(f"mutated a copy of B ({mut})")
    fa, fb = sorted(os.listdir(a)), sorted(os.listdir(b))
    bad = []
    if fa != fb:
        bad.append(f"file lists differ: {len(fa)} against {len(fb)}; only in A {sorted(set(fa) - set(fb))[:3]}; only in B {sorted(set(fb) - set(fa))[:3]}")
    nrec = nloc = 0
    for f in sorted(set(fa) & set(fb)):
        la, lb = open(os.path.join(a, f)).read().splitlines(), open(os.path.join(b, f)).read().splitlines()
        if la[:1] != lb[:1]:
            bad.append(f"{f}: first lines differ")
            continue
        ra = [json.loads(l) for l in la[1:] if l.startswith("{") or l.startswith("[")]
        rb = [json.loads(l) for l in lb[1:] if l.startswith("{") or l.startswith("[")]
        if len(ra) != len(rb):
            bad.append(f"{f}: {len(ra)} records against {len(rb)}")
            continue
        for i, (x, y) in enumerate(zip(ra, rb)):
            nrec += 1
            nloc += isinstance(x, dict) and "loc" in x
            if strip(x) != strip(y):
                bad.append(f"{f} record {i} differs outside loc")
    print(f"files {len(fa)} and {len(fb)}; records compared {nrec} ({nloc} with a loc key); differences outside loc: {len(bad)}")
    for x in bad[:10]:
        print("  " + x)
    print("RESULT:", "equal outside loc" if not bad else "differ")
    sys.exit(1 if bad else 0)

main()
