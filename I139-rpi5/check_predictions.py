#!/usr/bin/env python3
"""
Compares the planted-case and control runs of step3.sh with the predictions written in README.md before any run.
usage: check_predictions.py planted | controls      writes verdicts_<which>.md, exits 1 if any prediction missed.

PRED holds the predictions as typed from README.md; every number and every substring in it must occur in README.md
(checked first, so the two cannot drift apart).
"""
import os
import re
import sys

RAW = os.path.dirname(os.path.abspath(__file__))
README = open(os.path.join(RAW, 'README.md')).read()

# name: (exit, [(check id, substring of that FAIL line), ...] in order, widest ours, widest theirs, smallest overlap, largest gap)
PLANTED = {
    'P1': (0, [], '3.000000e-01', '2.000000e-01', '1.000000e-02', '1.500000e-01'),
    'P2': (0, [], '2.000000e-01', '2.000000e-01', '0.000000e+00', '2.000000e-01'),
    'P3': (1, [('C4', ['l = 3'])], '2.000000e-01', '2.000000e-01', '-1.000000e-15', '2.000000e-01'),
    'P4': (1, [('C1', ['missing in ours: l = 3'])], '3.000000e-01', '2.000000e-01', '1.000000e-02', '1.500000e-01'),
    'P5': (1, [('C2', ['ours', 'l = 3'])], '3.000000e-01', '2.000000e-01', '1.000000e-02', '1.500000e-01'),
    'P6': (1, [('C3', ['ours', 'l = 3'])], '3.000000e-01', '2.000000e-01', '0.000000e+00', '1.500000e-01'),
}
CONTROLS = {
    'shift': (1, [('C4', ['l = 1500']), ('C5', ['l = 1500'])]),
    'drop': (1, [('C1', ['missing in ours: l = 777'])]),
    'swap': (1, [('C4', ['l = 2000']), ('C5', ['l = 2000'])]),
}
STATS = ['largest bracket width, ours:', 'largest bracket width, theirs:', 'smallest overlap:', 'largest midpoint gap:']


def load(name):
    base = os.path.join(RAW, 'step3', name)
    rc = int(open(base + '.rc').read())
    lines = open(base + '.log').read().splitlines()
    fails = [ln for ln in lines if ln.startswith('FAIL')]
    stats = {}
    for ln in lines:
        for s in STATS:
            if ln.startswith(s):
                stats[s] = ln[len(s):].split()[0]
    return rc, fails, stats


def fail_id(line):
    return re.match(r'FAIL\s+(\S+?):', line).group(1)


def judge(name, pred, fails, rc, stats):
    notes = []
    if rc != pred[0]:
        notes.append(f"exit {rc}, predicted {pred[0]}")
    got = [fail_id(f) for f in fails]
    want = [w[0] for w in pred[1]]
    if got != want:
        notes.append(f"FAIL checks {got}, predicted {want}")
    else:
        for f, (cid, subs) in zip(fails, pred[1]):
            notes += [f"{cid} line lacks '{sub}'" for sub in subs if sub not in f]
    if len(pred) > 2:
        for s, w in zip(STATS, pred[2:]):
            if stats.get(s) != w:
                notes.append(f"{s} {stats.get(s)}, predicted {w}")
    return notes


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else ''
    if which not in ('planted', 'controls'):
        print(__doc__)
        return 2
    table = PLANTED if which == 'planted' else CONTROLS
    for name, pred in table.items():
        vals = [w[0] for w in pred[1]] + [sub for w in pred[1] for sub in w[1]] + list(pred[2:])
        for v in vals:
            if v not in README:
                print(f"prediction text not in README.md: {name}: {v}")
                return 2
    out = [f"| case | exit | FAIL lines | verdict |", "|---|---|---|---|"]
    bad = 0
    for name, pred in table.items():
        rc, fails, stats = load(name if which == 'planted' else 'mutate_' + name)
        notes = judge(name, pred, fails, rc, stats)
        bad += bool(notes)
        out.append(f"| {name} | {rc} | {' '.join(fail_id(f) for f in fails) or 'none'} | "
                   + ("as predicted" if not notes else "MISSED: " + "; ".join(notes)) + " |")
    text = "\n".join(out)
    print(text)
    open(os.path.join(RAW, f'verdicts_{which}.md'), 'w').write(text + "\n")
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
