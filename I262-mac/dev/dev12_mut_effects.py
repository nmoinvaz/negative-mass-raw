"""dev12: computed effects of the declared mutations (development; numbers go into the README before the runs of record)."""
import sys, time
sys.path.insert(0, ".")
import mpmath as mp
import cm_core as cm
K = cm.setup(60)
N = 90
g = cm.frobenius_s(K, 1, mp.mpf(1) / 2, 1 / (4 * K), N)
pts1 = [mp.mpf(s) * mp.mpf(x) for s in (1, -1) for x in ("0.01", "0.05", "0.1")]
print("N1 closed form vs Frobenius series (g1 = 1/(4K), g_k from the recursion to k = %d), max relative difference over rho = +-0.01, +-0.05, +-0.1" % N)
for mut in (None, "R2coef", "kscale", "xsign"):
    m = max(abs(cm.Yref_closed(K, r, mut) - cm.Y_frob_s(g, 0.5, r)[0]) / abs(cm.Y_frob_s(g, 0.5, r)[0]) for r in pts1)
    print("  mutation %-8s  max rel diff %s" % (mut, mp.nstr(m, 5)))
# slope mutants
beta = mp.pi / 4 - mp.mpf("0.9853152459183190904806585766012862060507")
Jab = -1j * mp.pi ** 2
s_true = -(mp.pi / 2) * beta
print("s = d(W/kappa)/dc =", mp.nstr(s_true, 20))
print("  mutation Jsign (B1 -> -B1):", mp.nstr(-s_true, 10))
beta0 = beta - mp.pi / 8
print("  mutation g1 (beta* in the g1 = 0 basis):", mp.nstr(-(mp.pi / 2) * beta0, 10))
kdot = mp.pi / 4 - 2 / mp.pi
print("  mutation kappa (forget d kappa/dc):", mp.nstr(s_true + kdot / (2 / mp.pi), 10))
