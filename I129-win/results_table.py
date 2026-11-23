"""Reads phase2/nonradial/harm_circles_output.txt (the table of `harm_circles.py --collect`) and prints the pivot that
RESULTS.md §5.5's #129 paragraph quotes: one row per point with the ratio |lap| L^2 / limit at both radii for S8, S10, S12
(F marks a failure), the worst ratio per setting, and the smallest point error that explains each setting's largest
|lap| L^2 under the script's bound (1600 eps at 0.05 L, 6400 eps at 0.025 L).
Usage: python results_table.py <harm_circles_output.txt>"""
import sys, re, collections

rows = []
for ln in open(sys.argv[1], encoding='utf-8'):
    c = [x.strip() for x in ln.strip().strip('|').split('|')]
    if len(c) == 9 and c[3] in ('S8', 'S10', 'S12'):
        rows.append(dict(box=c[0], pt=int(c[1]), s0=c[2], st=c[3], rho=float(c[4]), lap=float(c[5]), lim=float(c[6]),
                         ratio=float(c[7]), ok=(c[8] == 'pass')))
assert len(rows) == 4 * 3 * 3 * 2, len(rows)
by = collections.defaultdict(dict)
for r in rows:
    by[(r['box'], r['pt'], r['s0'])][(r['st'], r['rho'])] = r


def cell(r):
    return f"{r['ratio']:.3g}" + ("" if r['ok'] else " F")


print("| box | point | s0 | S8 0.05 L | S8 0.025 L | S10 0.05 L | S10 0.025 L | S12 0.05 L | S12 0.025 L | first passing |")
print("|---|---|---|---|---|---|---|---|---|---|")
for (box, pt, s0), d in by.items():
    first = next((st for st in ('S8', 'S10', 'S12') if all(d[(st, rho)]['ok'] for rho in (0.05, 0.025))), 'none')
    print(f"| {box} | {pt} | {s0} | " + " | ".join(cell(d[(st, rho)]) for st in ('S8', 'S10', 'S12') for rho in (0.05, 0.025))
          + f" | {first} |")
print()
for st in ('S8', 'S10', 'S12'):
    rs = [r for r in rows if r['st'] == st]
    nf = sum(1 for r in rs if not r['ok'])
    pts = {k for k, d in by.items() if not all(d[(st, rho)]['ok'] for rho in (0.05, 0.025))}
    w = max(rs, key=lambda r: r['ratio'])
    lo = min(rs, key=lambda r: r['ratio'])
    big = max(rs, key=lambda r: r['lap'] / (1600 if r['rho'] == 0.05 else 6400))
    eps = big['lap'] / (1600 if big['rho'] == 0.05 else 6400)
    print(f"{st}: {len(rs) - nf} of {len(rs)} rows pass, {len(by) - len(pts)} of {len(by)} points pass at both radii; "
          f"ratio {lo['ratio']:.3g} to {w['ratio']:.3g} (worst {w['box']} point {w['pt']} rho {w['rho']} L); "
          f"largest |lap| L^2 {max(r['lap'] for r in rs):.3e}, point error at least {eps:.2e} "
          f"({big['box']} point {big['pt']} rho {big['rho']} L)")
