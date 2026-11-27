"""dev07: formal series at rho = +infinity of the Y equation at c = -1, W = kappa: Y = e^{eps kappa x} Phi, Phi = rho * sum c_n rho^{-n}, eps = +-1.
Is the series convergent (an element of C(rho, R, arctan rho))? coefficient growth of c_n."""
import sys
sys.path.insert(0, ".")
import mpmath as mp
from cm_core import s_mul, s_inv, s_add, s_scale, s_der
mp.mp.dps = 60
K = 2 / mp.pi
n = int(sys.argv[1]) if len(sys.argv) > 1 else 120
M = n + 8
# A(s), s = 1/rho
A = [mp.mpf(0)] * M
A[0] = mp.mpf(1)
# A = 1 + K/s - K s^{-1} (1+s^2) sum (-1)^m s^{2m}/(2m+1)  -> series, the 1/s terms cancel
S = [mp.mpf(0)] * (M + 2)
for m in range(0, (M + 2) // 2):
    S[2 * m] = mp.mpf((-1) ** m) / (2 * m + 1)
# (1+s^2) S: coefficient list
P1 = [S[i] + (S[i - 2] if i >= 2 else 0) for i in range(M + 2)]
# A = 1 + K/s - K/s * P1(s) = 1 - K * (P1(s) - 1)/s
for i in range(M):
    A[i] = (1 if i == 0 else 0) - K * (P1[i + 1] - (1 if i + 1 == 0 else 0))
A[0] = mp.mpf(1) - K * (P1[1])
# P1[0] = 1, so (P1 - 1)/s starts at P1[1]; fix indices:
A = [mp.mpf(0)] * M
A[0] = mp.mpf(1)
for i in range(M):
    A[i] += -K * P1[i + 1]
print("A series:", [mp.nstr(x, 8) for x in A[:6]], " expected 1, -2K/3 =", mp.nstr(-2 * K / 3, 8))
Ap = [-(i - 0) * 0 for i in range(M)]   # A'(rho) = -s^2 dA/ds
dA = s_der(A)
Ap = [mp.mpf(0), mp.mpf(0)] + [-x for x in dA][:M - 2]
iA = s_inv(A, M)
AA = s_mul(Ap, iA, M)                                   # A'/A
iR2 = s_mul([mp.mpf(0), mp.mpf(0), mp.mpf(1)], s_inv([mp.mpf(1), mp.mpf(0), mp.mpf(1)], M), M)   # s^2/(1+s^2)
iR4 = s_mul(iR2, iR2, M)
sser = [mp.mpf(0), mp.mpf(1)] + [mp.mpf(0)] * (M - 2)
for eps in (+1, -1):
    Pe = [eps * 2 * K * iA[i] + AA[i] - (2 if i == 1 else 0) for i in range(M)]       # 2 eps K/A - P,  P = 2 s - A'/A
    P = [(2 if i == 1 else 0) - AA[i] for i in range(M)]
    dinvA = [-x for x in s_mul(Ap, s_mul(iA, iA, M), M)]                             # (1/A)'
    PA = s_mul(P, iA, M)
    Q0 = [iR4[i] for i in range(M)]
    t1 = s_mul(s_mul(AA, sser, M), iR2, M)
    t2 = s_scale(s_mul(iA, iR2, M), 2, M)
    Q0 = [Q0[i] - t1[i] - t2[i] for i in range(M)]
    Qe = [eps * K * dinvA[i] - eps * K * PA[i] - Q0[i] for i in range(M)]
    # unknowns phi_k, k = -1..n; store phi[k + 1]
    phi = {-1: mp.mpf(1)}
    pi_ = Pe; q_ = Qe
    assert abs(pi_[0] - 2 * eps * K) < 1e-40 and abs(q_[0]) < 1e-40 and abs(q_[1] + 2 * eps * K) < 1e-40, (pi_[0], q_[0], q_[1])
    for m in range(1, n + 1):
        # coefficient of s^m: phi_{m-2}(m-2)(m-1) - sum_j pi_j (m-1-j) phi_{m-1-j} + sum_j q_j phi_{m-j} = 0 ; unknown phi_{m-1}
        tot = mp.mpf(0)
        if (m - 2) in phi:
            tot += phi[m - 2] * (m - 2) * (m - 1)
        for j in range(1, m + 2):
            k = m - 1 - j
            if k in phi:
                tot -= pi_[j] * k * phi[k]
        for j in range(2, m + 2):
            k = m - j
            if k in phi:
                tot += q_[j] * phi[k]
        phi[m - 1] = tot / (2 * eps * K * m)
    print("eps =", eps, " c_n = phi_{n-1} (n = 0..):", [mp.nstr(phi[k], 6) for k in range(-1, 8)])
    rat = [abs(phi[k + 1] / phi[k]) for k in range(1, n - 1) if phi[k] != 0]
    for k in (10, 20, 40, 60, 80, 100, n - 3):
        if k < len(rat):
            print("   |phi_{k+1}/phi_k| at k =", k, mp.nstr(rat[k - 1], 8), "  ratio/k =", mp.nstr(rat[k - 1] / k, 6))
