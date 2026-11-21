"""Lists what differs between two wide reports (old, new), aligned by sigma R and m: the changed fields of each table row
(the directory column and the sign of the imaginary part of the leading mu are listed apart), the changed or added or
removed check lines, the speed-bound lines and the closing line. Usage, with the venv python and -X utf8:
    python -X utf8 diff_wide.py OLD NEW"""
import re
import sys


def parse(path):
    rows, checks, other = {}, {}, []
    sig = None
    for ln in open(path, encoding="utf-8-sig").read().splitlines():
        m = re.match(r"== sigma R = (\S+),", ln)
        if m:
            sig = m.group(1)
            continue
        m = re.match(r"\s+\[(PASS|FAIL)\] (\w+) (sR=\S+ m=\S+|sR=\S+): ", ln)
        if m:
            checks[(m.group(2), m.group(3))] = ln.strip()
            continue
        m = re.match(r"\s*([\d.]+) \| (\d+ / \d+) \|", ln)
        if m:
            rows[(sig, m.group(1))] = [c.strip() for c in ln.split("|")]
            continue
        if ln.strip():
            other.append(ln.strip())
    return rows, checks, other


old, new = parse(sys.argv[1]), parse(sys.argv[2])
HEAD = ["m", "n", "leading mu v_c (A)", "|mu| v_c A", "B", "#75", "rel #75", "window 1e-5 / 1e-4 (#75)", "set by",
        "eigs in window", "real A / B", "next A", "next B", "next #75", "rel next", "A - B", "dir"]
print(f"rows: {len(old[0])} old, {len(new[0])} new")
for key in sorted(set(old[0]) | set(new[0])):
    a, b = old[0].get(key), new[0].get(key)
    if a is None or b is None:
        print(f"row {key}: only in {'old' if b is None else 'new'}")
        continue
    ch = [(HEAD[i] if i < len(HEAD) else str(i), x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
    cosmetic = [c for c in ch if c[0] in ("dir", "leading mu v_c (A)")]
    real = [c for c in ch if c not in cosmetic]
    if real or cosmetic:
        print(f"row sR={key[0]} m={key[1]}: " + "; ".join(f"{n}: {x!r} -> {y!r}" for n, x, y in real)
              + ("  [cosmetic: " + ", ".join(n for n, _, _ in cosmetic) + "]" if cosmetic else ""))
nch = 0
for key in sorted(set(old[1]) | set(new[1])):
    a, b = old[1].get(key), new[1].get(key)
    if a != b:
        nch += 1
        print(f"check {key[0]} {key[1]}:\n   old: {a}\n   new: {b}")
print(f"checks: {len(old[1])} old, {len(new[1])} new, {nch} differ")
print("other lines only in old:", [x for x in old[2] if x not in new[2] and not x.startswith("wall")])
print("other lines only in new:", [x for x in new[2] if x not in old[2] and not x.startswith("wall")])
