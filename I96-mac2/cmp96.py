#!/usr/bin/env python3
"""Compare the Mac's re-solve of sigma R = 8, m = 7/2 with the laptop's stored arrays (I96-win/eig)."""
import sys
import numpy as np
a, b = np.load(sys.argv[1]), np.load(sys.argv[2])
print('keys', sorted(a.files))
for k in a.files:
    x, y = a[k], b[k]
    if x.dtype.kind in 'fc' and x.size > 1:
        xs, ys = x[np.argsort(-np.abs(x), kind='stable')], y[np.argsort(-np.abs(y), kind='stable')]
        top = slice(0, 60)
        d = np.max(np.abs(np.abs(xs[top]) - np.abs(ys[top])) / np.abs(xs[0]))
        print(f'{k}: n = {x.size} / {y.size}, top 60 moduli differ by at most {d:.1e} of the leading modulus;'
              f' leading {xs[0]:.10f} / {ys[0]:.10f}')
    elif x.size == 1:
        print(f'{k}: {x} / {y}')
