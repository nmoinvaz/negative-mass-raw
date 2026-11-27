"""Design probe of #188 (development): is the R diagonal of numpy's QR (LAPACK zgeqrf) real for a complex matrix?"""
import numpy as np
rng = np.random.default_rng(1)
worst, neg = 0.0, 0
for _ in range(1000):
    Y = rng.normal(size=(6, 3)) + 1j * rng.normal(size=(6, 3))
    Q, R = np.linalg.qr(Y)
    d = np.diag(R)
    worst = max(worst, np.max(np.abs(d.imag) / np.abs(d)))
    neg += int(np.sum(d.real < 0))
print(f"1000 random complex 6x3 matrices: largest |Im d|/|d| of R's diagonal {worst:.2e}; negative real diagonal entries {neg} of 3000")
