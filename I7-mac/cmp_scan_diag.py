#!/usr/bin/env python3
"""Compare a scan_growing.py CSV (gamma,D) with a serial diagnostic's jsonl ({"i","g","D"}) at every grid point.

    python3 cmp_scan_diag.py SCAN.csv DIAG.jsonl [--tol=1e-8] [--selftest]

Exit 1 if the grids differ in length or g, or if any |D_scan - D_diag| / |D_diag| exceeds tol.
--selftest scales one D of the diagnostic by 1 + 10 tol and requires the check to fail on it.
"""
import json
import sys


def load(csv_path, jsonl_path):
    scan = [tuple(map(float, l.split(","))) for l in open(csv_path).read().split("\n")[1:] if l.strip()]
    diag = [(r["g"], r["D"]) for r in map(json.loads, open(jsonl_path)) if "D" in r]
    return scan, diag


def compare(scan, diag, tol):
    if len(scan) != len(diag):
        return False, f"lengths differ: scan {len(scan)}, diagnostic {len(diag)}"
    worst, at = 0.0, None
    for (gs, ds), (gd, dd) in zip(scan, diag):
        if abs(gs - gd) > 1e-12 * abs(gd):
            return False, f"grid differs at g {gd!r}: scan {gs!r}"
        rel = abs(ds - dd) / abs(dd)
        if rel > worst:
            worst, at = rel, gd
    return worst <= tol, f"{len(scan)} points, largest relative difference {worst:.2e} at g = {at}, tol {tol:.0e}"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = dict(a[2:].split("=", 1) if "=" in a else (a[2:], "1") for a in sys.argv[1:] if a.startswith("--"))
    tol = float(opts.get("tol", 1e-8))
    scan, diag = load(*args)
    if "selftest" in opts:
        k = len(diag) // 2
        bent = list(diag)
        bent[k] = (bent[k][0], bent[k][1] * (1 + 10 * tol))
        ok, msg = compare(scan, bent, tol)
        print(f"selftest (D at index {k} scaled by 1 + {10 * tol:.0e}): {'FIRED' if not ok else 'DID NOT FIRE'}: {msg}")
        if ok:
            sys.exit(1)
    ok, msg = compare(scan, diag, tol)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
