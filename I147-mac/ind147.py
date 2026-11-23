#!/usr/bin/env python3
"""ind147: the coordinator's bookkeeping check of #147's 16 new mutations (criteria N1-N6 in I147-mac/README.md).

Reads files and git only; imports nothing from zerilli_derivation*.py or its library.
"""
import argparse
import ast
import re
import subprocess
import sys
from datetime import datetime

ap = argparse.ArgumentParser()
ap.add_argument('--repo', required=True)
ap.add_argument('--raw', required=True)
ap.add_argument('--mac-main', required=True)
ap.add_argument('--mac-ctrl', required=True)
ap.add_argument('--mutate', default='')
args = ap.parse_args()
MUT = args.mutate
FAIL = []
BR = 'origin/wip/i147-zerilli-mutations'
NEW = ['ds_sign', 'gauge_odd', 'x_odd', 'x_gauge', 'odd_norm', 'odd_flow', 'same_m0', 'grr_trace', 'hexpr_sign', 'e4_drop',
       'e5a_det0', 'v_s2', 'back_coef', 'd3_s1', 'd4_l2', 'd5_ah0']


def check(name, ok, msg):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}", flush=True)
    if not ok:
        FAIL.append(name)


def git(repo, *a):
    return subprocess.run(['git', '-C', repo] + list(a), capture_output=True, text=True, check=True).stdout


def pairs_at(rev):
    tree = ast.parse(git(args.repo, 'show', f'{rev}:phase2/dg_proof/zerilli_derivation_controls.py'))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(isinstance(t_, ast.Name) and t_.id == 'PAIRS' for t_ in node.targets):
            return [(e.elts[0].value, e.elts[2].value, e.elts[3].value) for e in node.value.elts]
    raise SystemExit('no PAIRS')


# ---- N1: Mac controls lines
ctrl = open(args.mac_ctrl).read().splitlines()
rows = []
for ln in ctrl:
    m = re.match(r'^(OK  |MISS) (\S+)\s+target=(\S+)\s+exit=(\d+) \(want (\d+)\) first-FAIL=(\S+)', ln)
    if m:
        rows.append(dict(ok=m.group(1).strip() == 'OK', name=m.group(2), target=m.group(3), exit=int(m.group(4)),
                         want=int(m.group(5)), first=m.group(6)))
if MUT == 'miss2':                                        # miss2: one OK pair read as MISS
    rows[3]['ok'] = False
base = [ln for ln in ctrl if ln.startswith(('OK   baseline', 'MISS baseline'))]
okb = len(base) == 1 and base[0].startswith('OK') and 'PASS=32' in base[0] and 'FAIL=0' in base[0]
miss = [r for r in rows if not r['ok']]
ok1 = okb and len(rows) == 34 and sum(r['ok'] for r in rows) == 33 and len(miss) == 1 and miss[0]['name'] == 'fsign_bg' \
    and miss[0]['first'] == 'PL.O.3'
check('N1', ok1, f"baseline {base[0] if base else None!r}; {len(rows)} pair lines, {sum(r['ok'] for r in rows)} OK, MISS "
      f"{[(r['name'], r['first']) for r in miss]}")

# ---- N2: the driver's pairs against the pre-registration and #143's
now, old = pairs_at(BR), pairs_at('3400e74')
readme = git(args.raw, 'show', '5e9657b:I147-rpi5/README.md')
pre = []
for ln in readme.splitlines():
    c = [x.strip() for x in ln.strip().strip('|').split('|')]
    if len(c) == 8 and c[0].isdigit():
        pre.append((c[3].strip('`'), c[5], int(c[6])))
if MUT == 'retarget':                                     # retarget: one pre-registered target changed
    pre[4] = (pre[4][0], 'PL.O.2', pre[4][2])
ok2 = now[:18] == old and now[18:] == pre and [p[0] for p in pre] == NEW
check('N2', ok2, f"#143's 18 unchanged {now[:18] == old}; 16 new = pre-registered (name, target, exit) {now[18:] == pre}; "
      f"{len(pre)} rows in the README table")

# ---- N3: coverage and first FAIL of the new pairs
main = open(args.mac_main).read().splitlines()
ids = [ln.split()[1] for ln in main if ln.startswith('PASS ')]
plist = list(now)
rws = list(rows)
if MUT == 'drop_pair':                                    # drop_pair: one new pair removed
    plist = [p for p in plist if p[0] != 'v_s2']
    rws = [r for r in rws if r['name'] != 'v_s2']
targets = {p[1] for p in plist}
uncovered = [i for i in ids if i not in targets]
byname = {r['name']: r for r in rws}
offt = [n for n in NEW if n not in byname or byname[n]['first'] != byname[n]['target'] or byname[n]['exit'] != byname[n]['want']]
ok3 = len(ids) == 32 and not uncovered and not offt
check('N3', ok3, f"{len(ids)} PASS ids, uncovered {uncovered}; new pairs off target on the Mac {offt}")

# ---- N4: pre-registration before the code and the later raw commits
t = lambda repo, rev: datetime.fromisoformat(git(repo, 'show', '-s', '--format=%cI', rev).strip())
t_pre = t(args.raw, '5e9657b')
later = [ln.split()[0] for ln in git(args.raw, 'log', '--format=%h', '5e9657b..HEAD', '--', 'I147-rpi5').split()]
ok4 = t_pre < t(args.repo, '7a44d73') and all(t_pre < t(args.raw, h) for h in later)
check('N4', ok4, f"5e9657b at {t_pre.isoformat()}; code 7a44d73 at {t(args.repo, '7a44d73').isoformat()}; later raw commits {later}")

# ---- N5: the 16 names occur only as switches
src = git(args.repo, 'show', f'{BR}:phase2/dg_proof/zerilli_derivation.py')
lib = git(args.repo, 'show', f'{BR}:phase2/dg_proof/zerilli_derivation_lib.py')
if MUT == 'leak':                                         # leak: a bare use of a mutation name
    src += "\nfds = ds_sign\n"
tree = ast.parse(src)
allowed = set()
for node in ast.walk(tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'mut':
        allowed |= {id(a) for a in node.args}
    if isinstance(node, ast.Assign) and any(isinstance(t_, ast.Name) and t_.id == 'XFLIP' for t_ in node.targets):
        allowed |= {id(e.elts[0]) for e in node.value.values}
bad = [(n.value, n.lineno) for n in ast.walk(tree) if isinstance(n, ast.Constant) and n.value in NEW and id(n) not in allowed]
bad += [(n.id, n.lineno) for n in ast.walk(tree) if isinstance(n, ast.Name) and n.id in NEW]
xflip = re.search(r"XFLIP = \{[^}]*\}", src).group(0)
mut_def = re.search(r"def mut\(name\):\n\s+return name in _MUT", lib) is not None
fill = re.findall(r"_MUT\s*(?:\|=|=)\s*[^\n]+", lib)
ok5 = not bad and mut_def and len(fill) == 2 and "--mutate=" in lib
check('N5', ok5, f"bare uses {bad[:4]}; XFLIP {xflip!r}; mut = name in _MUT {mut_def}; _MUT assignments {fill}")

# ---- N6: unmutated output equals the committed one apart from timing lines
com = git(args.repo, 'show', f'{BR}:phase2/dg_proof/zerilli_derivation_output.txt').splitlines()
strip = lambda L: [ln for ln in L if not re.match(r'^# \[\s*[\d.]+ s\]', ln)]
ok6 = strip(com) == strip(main)
check('N6', ok6, f"{len(strip(main))} lines compared, equal {ok6}")

print('ALL PASS' if not FAIL else 'FAILED: ' + ', '.join(FAIL))
sys.exit(1 if FAIL else 0)
