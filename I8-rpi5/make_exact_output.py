#!/usr/bin/env python3
"""Builds phase2/nonradial/verify_polar_exact_output.txt from the logs of run_exact_all.sh (order of that script)."""
import re, os
RAW = os.path.expanduser('~/Source/negative-mass-raw/I8-rpi5')
OUT = os.path.expanduser('~/Source/negative-mass-i8/phase2/nonradial/verify_polar_exact_output.txt')
runs = [('points', 0), ('mutate_coef', 1), ('mutate_bg_alpha', 1), ('mutate_bg_a', 1), ('mutate_bg_phi0', 1), ('mutate_bg_u', 1), ('mutate_eq', 1),
        ('points_af', 0), ('sensitivity', 0), ('selftest', 0), ('symbolic', 0), ('symbolic_mutate_coef', 1),
        ('symbolic_mutate_bg_alpha', 1), ('symbolic_mutate_bg_a', 1), ('symbolic_mutate_bg_phi0', 1),
        ('symbolic_mutate_bg_u', 1), ('symbolic_mutate_eq', 1), ('crosscheck', 0), ('frac_free_r', 0), ('frac_free_r_s', 0), ('frac_free_r_alpha_a', 0)]
times = open(RAW + '/exact_all.time').read()
commit = re.search(r'commit (\w+)', times).group(1)
wall = {m.group(1): int(m.group(2)) for m in re.finditer(r'^(\S+) exit \d+ wall (\d+) s', times, re.M)}
rows, body = [], []
for name, want in runs:
    log = open(f'{RAW}/verify_polar_exact_{name}.log').read().splitlines()
    cmd = log[0].lstrip('# ').strip()
    rc = int(open(f'{RAW}/done/exact_{name}.rc').read())
    res = [l for l in log if l.startswith(('RESULT', 'MUTATION ')) and ':' in l or l.startswith('RESULT')]
    verdict = res[-1] if res else '(no verdict line)'
    rows.append((name, rc, want, verdict))
    body.append(f'\n$ {cmd}\n' + '\n'.join(log[1:]) + f'\nexit {rc}  (wall {wall[name]} s)')
head = f'''verify_polar_exact.py, unmodified at commit {commit} (branch wip/i8-polar-exact), run from phase2/nonradial on rpi5-ubuntu,
Python 3.14.10, sympy 1.14.0. Raw logs, timings and exit codes: negative-mass-raw, folder I8-rpi5. Every run is
nice -n 10 python -I verify_polar_exact.py ... with OMP_NUM_THREADS=1, one process at a time.
Exit code 0: all checks of the run pass. Exit code 1: a check fails. A run with --mutate must exit 1, since the mutation must be
detected; its "expected" exit code below is 1.

| run | exit | expected | last verdict line of the run |
|---|---|---|---|
'''
head += '\n'.join(f'| {n} | {rc} | {w} | {v[:150]} |' for n, rc, w, v in rows)
head += '\n\nAll exit codes as expected: ' + ('yes' if all(rc == w for _, rc, w, _ in rows) else 'NO') + '\n'
open(OUT, 'w').write(head + '\n'.join(body) + '\n')
print(head)
