#!/usr/bin/env python3
"""compare_outputs.py BASE_LOG ON_LOG [BASE_DUMP ON_DUMP]

README criterion 5: the same eta*, class and kind to the printed digits. Written from the baseline's lines before the
analysis of the feature-on logs. Rules, fixed here:
 - a log line is normalized: numbers in scientific notation with exponent <= -6 (error sizes, residuals, bars), timings
   ("(12 s)", "12 s", "elapsed"), and step counts ("114 steps", "55 and 67 steps", "106 to 215 steps") are replaced by tokens;
   what remains (labels, eta*, kinds, counts of classes, 10-digit results) must be equal as strings;
 - dump records (jsonl, one per verdict): class, kind, stop, tiny_kind, through, converged equal as strings; xstar (and
   xstar_true) equal as printed with 10 significant digits; steps, bar and the error sizes are listed, not compared.
Prints every difference and a summary; exit 1 if a gated difference exists."""
import json, os, re, sys

def norm(line):
    line = re.sub(r"\(\d+ s\)", "(<t>)", line)
    line = re.sub(r"\b\d+ s\b", "<t> s", line)
    line = re.sub(r"Elapsed.*", "Elapsed <t>", line)
    line = re.sub(r"\d+(?: (?:and|to) \d+)? steps", "<n> steps", line)
    line = re.sub(r"[-+]?\d+\.?\d*[eE]-(?:0[6-9]|[1-9]\d)\b", "<err>", line)
    line = re.sub(r"\b0\.0+[1-9]\d*[eE][-+]\d+\b", "<err>", line)
    return line.rstrip()

def log_lines(path):
    out = []
    for l in open(path):
        if l.startswith("#") or l.startswith("\t") or l.startswith("Command being") or not l.strip():
            continue
        if re.match(r"\s*\(series through eta\^-\d+ solved in \d+ s\)", l):
            continue  # the pickle's build, in the first run only
        out.append(norm(l))
    return out

def gated_log(a, b):
    la, lb = log_lines(a), log_lines(b)
    diffs = []
    if len(la) != len(lb):
        diffs.append(f"line counts differ: {len(la)} against {len(lb)}")
    for i, (x, y) in enumerate(zip(la, lb)):
        if x != y:
            diffs.append(f"line {i}:\n  base {x[:600]}\n  on   {y[:600]}")
    return len(la), diffs

STR = ("class", "kind", "stop", "tiny_kind", "through", "converged", "outcome")
DIG = ("xstar", "xstar_true")

def walk(a, b, path, out, stats):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in a:
            if k in b:
                walk(a[k], b[k], path + [k], out, stats)
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            walk(x, y, path + [i], out, stats)
    else:
        k = path[-1] if path and isinstance(path[-1], str) else None
        if k in STR:
            stats["str"] += 1
            if a != b:
                out.append((path, a, b))
        elif k in DIG and isinstance(a, (int, float)) and isinstance(b, (int, float)):
            stats["dig"] += 1
            if f"{a:.10g}" != f"{b:.10g}":
                out.append((path, a, b))
                stats["worst"] = max(stats["worst"], abs(a - b) / max(abs(a), 1e-300))
            stats["maxrel"] = max(stats["maxrel"], abs(a - b) / max(abs(a), 1e-300))
        elif k == "steps" and a != b:
            stats["steps_differ"] += 1

def gated_dump(da, db):
    stats = dict(str=0, dig=0, worst=0.0, maxrel=0.0, steps_differ=0, records=0, files=0, missing=0)
    diffs = []
    for f in sorted(os.listdir(da)):
        if not os.path.exists(os.path.join(db, f)):
            stats["missing"] += 1
            continue
        stats["files"] += 1
        ra = [json.loads(l) for l in open(os.path.join(da, f)) if l.startswith("{")]
        rb = [json.loads(l) for l in open(os.path.join(db, f)) if l.startswith("{")]
        if len(ra) != len(rb):
            diffs.append(f"{f}: {len(ra)} records against {len(rb)}")
        for i, (x, y) in enumerate(zip(ra, rb)):
            stats["records"] += 1
            out = []
            walk(x, y, [], out, stats)
            for p, u, v in out:
                diffs.append(f"{f} record {i} {'.'.join(map(str, p))}: base {u} on {v}")
    return stats, diffs

if __name__ == "__main__":
    n, d = gated_log(sys.argv[1], sys.argv[2])
    print(f"log lines compared: {n}; gated differences: {len(d)}")
    for x in d[:40]:
        print(x)
    bad = len(d)
    if len(sys.argv) > 4:
        st, dd = gated_dump(sys.argv[3], sys.argv[4])
        print(f"dump: {st['files']} files, {st['records']} records, {st['str']} string fields, {st['dig']} eta* values compared; "
              f"files missing in on: {st['missing']}; eta* differing in the 10 printed digits: {len([x for x in dd if 'xstar' in x])}, "
              f"largest relative difference of any eta* {st['maxrel']:.2e} (of the differing ones {st['worst']:.2e}); records whose step count differs: {st['steps_differ']}")
        for x in dd[:40]:
            print(x)
        bad += len(dd) + st["missing"]
    sys.exit(1 if bad else 0)
