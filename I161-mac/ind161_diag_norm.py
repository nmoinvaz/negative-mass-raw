#!/usr/bin/env python3
"""Diagnostic for ind161 run 1's Q4 failure (normalization 1.6e-8 against 1e-10). Not a criterion: the largest
|2 e^(2 sigma) pd qd - 1| along the geodesic through s = 0 and s = 0.3, for dt = 0.01, 0.005, 0.0025, 0.00125."""
import sys
src = open('ind161.py').read()
start = src.index('W = (1, 3, 1, 1)')
end = src.index('xg, wg = ')
ns = {'__name__': 'diag', 'MUT': ''}
exec('import math\n' + src[start:end], ns)
for s in (0.0, 0.3):
    row = []
    for dt in (0.01, 0.005, 0.0025, 0.00125):
        _, _, _, mn = ns['geodesic'](s, dt)
        row.append(mn)
    ratios = [row[i] / row[i + 1] for i in range(3)]
    print(f"s = {s}: max normalization error {['%.2e' % v for v in row]}; ratios {['%.1f' % r for r in ratios]}")
