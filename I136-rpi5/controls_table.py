#!/usr/bin/env python3
"""Reads mutate_<NAME>.log and done/mutate_<NAME>.rc and prints the control table against the targets frozen in README.md."""
import re, sys
T = {  # frozen before the first run (README.md, "Controls")
    'sigma': ['points:le', 'points:rodal'],
    'drop-P-term': ['frame', 'small_z:le', 'small_z:rodal', 'tail:le', 'tail:rodal', 'points:le'],
    'exp-ulp': ['exp'],
    'frame-typo': ['frame'],
    'tail-zt': ['tail:le', 'tail:rodal'],
    'small-z-range': ['small_z:le', 'small_z:rodal'],
    'drop-leaf': ['cover:le'],
    'krawczyk-shift': ['planted', 'points:le'],
    'w-range': ['points:le', 'points:rodal'],
    'spurious-on-P-root': ['spurious:le', 'spurious:rodal'],
    'planted-double': ['planted'],
}
print('| control | exit | checks run | targets fired | other checks that fired | seconds |')
print('|---|---|---|---|---|---|')
allok = True
for n, tg in T.items():
    log = open('mutate_%s.log' % n).read()
    rc = int(open('done/mutate_%s.rc' % n).read())
    run = re.findall(r'^check (\S+)', log, re.M)
    failed = re.findall(r"^check (\S+)\n(?:.*\n)*?  -> FAIL", log, re.M)
    failed = [m.group(1) for m in re.finditer(r'^check (\S+)$((?:\n(?!check ).*)*)', log, re.M) if '-> FAIL' in m.group(2)]
    fired = [t for t in tg if t in failed]
    other = [f for f in failed if f not in tg]
    sec = open('mutate_%s.time' % n).read().split('\n')[-2].split()[0]
    ok = rc != 0 and len(fired) == len(tg)
    allok &= ok
    print('| `%s` | %d | %d | %d of %d%s | %s | %s |' % (n, rc, len(run), len(fired), len(tg), '' if ok else ' MISSED', ', '.join('`%s`' % o for o in other) or '-', sec))
sys.exit(0 if allok else 1)
