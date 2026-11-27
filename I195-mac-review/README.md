# I195-mac-review: the coordinator's review of #195 (rerun, independent check ind195)

Machine: macOS (the coordinator's Mac, Apple M5, arm64), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`:
sympy 1.14.0, mpmath 1.3.0), Rust 1.94.0, nice 10, at most 2 processes. Issue:
https://github.com/nmoinvaz/negative-mass/issues/195. Under review: branch `wip/i195-w2-largeD` at 514ac42, raw
`I195-dh610` at e70f58a. Written 2026-11-26 before the first run of `ind195.py`.

## Rerun

`rerun.sh A`, `B`, then `C`, from a detached worktree `~/Source/negative-mass-r195` at 514ac42, with the crate built
there (`cargo build --release --locked -j 2`). The commands are those of I195-dh610's `.env` files, with paths mapped
to this Mac (`cmds.txt`):
- the planted runs (run_01 in f64, dd, qd and od);
- the qd W² of growth.csv's D (run_02) and of the D list (run_03);
- the od W² of the D list (run_04 p0–p2);
- then the driver (run_08) on these logs.

The crate's values are compared with dh610's as strings. They should agree bit for bit, since multidouble's results
do not depend on the machine.

## ind195.py

Four parts, sharing with #195 only the equation E2 of `master.py` and, for K3 and K4, the crate's W² values (the
object under test).
- **K1**: the coordinator's own transformation of E2 into ℓ = s ln r, w = dY/d ln r, checked in sympy against the A and
  B of the raw README's "Method".
- **K2**: an independent W² at D = 50 and 1000, in Python and mpmath at 50 digits, by a different matching:
  - the throat series summed at ℓ₀ = ½ (not 1), integrated outward to ℓ_m = 3;
  - the far side started at ℓ_∞ = 180 on the decaying eigenvector of the frozen coefficients (not the vector (1, 1)),
    integrated inward to ℓ_m;
  - M(Ω) = Y_out w_in − w_out Y_in at ℓ_m, solved by the secant method;
  - Taylor steps of order 60 with fixed steps (0.25 up to ℓ = 3, 0.5 beyond) and jets of e^{2εℓ} and e^{−ℓ} formed
    exactly.
- **K3**: Ω₁ and Ω₂ from the crate's qd W² of the D list (the rerun's run_03), by a different estimator: Neville
  extrapolation to ε = 0 through the N largest D, N = 16, 20 and 24 (#195 used least squares in cells).
- **K4**: PSLQ on K3's Ω₂.

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| K1 | A = (1 + εΩ)e^{2εℓ} − (½ + ε)F − ½e^{−ℓ} and B = (½ + 2ε)F + ½e^{−ℓ} (F = 1 − e^{−ℓ}, ε = 1/(2(D − 3))) follow from E2 with r′² = 1 − r^{−2(n−1)}, r r″ = (n − 1) r^{2−2n}: sympy residual 0 |
| K2 | At D = 50 and 1000, \|W²_ind − W²_crate\| ≤ 1e-35·W²_crate, with W²_crate the qd value of the rerun's run_02 |
| K3 | With g = W² − 2(D − 3) + 4 ln 2: Neville on g/ε gives Ω₁ within 1e-30 of 2π²/3 + 8 ln²2 at each N. Neville on (g/ε − Ω₁)/ε, with Ω₁ the closed form, gives Ω₂ within 1e-20 of 80ζ(3) − (8/3)π² ln 2 − (32/3) ln³2 at each N. The spread of Ω₂ over N is ≤ 1e-20 |
| K4 | mpmath `pslq([Ω₂, ζ(3), π² ln 2, ln³2], tol=1e-18, maxcoeff=1000)`, with K3's Ω₂ at N = 20, returns a multiple of (3, −240, 8, 32). With ζ(3) replaced by ζ(3) + 1e-12 it returns no relation |

## Mutations (`--mutate=NAME`; each must make ind195 exit non-zero with exactly these criteria failing)

| mutation | change | targets |
|---|---|---|
| `k1-B` | K1's expected B uses (½ + ε)F in place of (½ + 2ε)F | K1 |
| `k2-eps` | K2's own code uses ε(1 + 1e-8) | K2 |
| `k3-omega1` | K3 subtracts Ω₁ + 1e-20 in place of Ω₁ | K3, K4 |

## Runs (filled in as they are done)

| file | what |
|---|---|
| `rerun_run_*.log`, `.err`, `.rc`, `.env` | the rerun of every run of record. **The od values are bit-identical** to dh610's (68 RESULT lines). **The qd values are not**: 4 of the 64 qd W² of the D list differ, by 3e-64 to 3e-63 relative, and a few planted fields (S4M, S5) and Newton traces differ. The cause is the step planner's f64 `powf` (flow.rs:161) and the ℓ_∞ rule's f64 `exp` (flow.rs:191), which differ by an ulp between macOS's libm and glibc, so step sizes differ. The coordinator's expectation of bit identity, written above, is not met. Every difference is at qd roundoff, far below every bar. The driver rerun (`rerun_run_08_driver_final.log`) exits 1 with the same verdicts, fit and PSLQ numbers. It differs from dh610's run_08 in 17 of 181 lines: the code line, the planted table's last digits, the qd/od digit counts at D = 70, 162, 527 and 1572, and timings |
| `ind195.py`, `ind195_run1.txt` | run 1: **exit 0, 4 of 4.** K1 residual 0. K2: the independent W² agrees with the crate to 5.6e-51 (D = 50) and 4.2e-40 (D = 1000), in 6 secant steps and 35–38 s each. K3: Ω₁ within 2.5e-44 … 4.1e-43 of 2π²/3 + 8 ln²2; Ω₂ = 74.3693867279333175953846702958 within 9.8e-41 … 9.7e-40 of 80ζ(3) − (8/3)π² ln 2 − (32/3) ln³2 at N = 16, 20, 24 (spread 8.7e-40). K4: PSLQ returns (3, −240, 8, 32), and none for the perturbed basis |
| `ind195_run1_mut_*.txt` | `k1-B` fails exactly K1, `k2-eps` exactly K2, `k3-omega1` exactly K3 and K4 |
