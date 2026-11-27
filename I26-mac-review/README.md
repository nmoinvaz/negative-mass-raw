# I26-mac-review: the coordinator's review of #26 (rerun, independent check ind26)

Machine: macOS (the coordinator's Mac, Apple M5, arm64), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`:
mpmath 1.3.0 with the python backend, sympy 1.14.0), nice 10, at most 2 processes. Issue:
https://github.com/nmoinvaz/negative-mass/issues/26. Under review: branch `wip/i26-omega2` at 5b53626, raw `I26-dh610`
at ef60780. dh610 ran Python 3.14.10 with the same mpmath (python backend) and sympy. Written 2026-11-27 before the
first run of `ind26.py` and before the rerun.

## Rerun

`rerun.sh`, from a detached worktree `~/Source/negative-mass-r26` at 5b53626, in `notes/wormhole_largeD`. It runs the
five runs of record of `I26-dh610` (their `.env` files) in two chains of one process each:
- chain A: `order4.py n4b`;
- chain B: `order4.py sym closed reduce`, `order4.py n4bg`,
  `order4.py evals remainder --w2raw=<I26-dh610/inputs_w2_growthD.txt>`, then `order4.py lc2`.

mpmath and sympy are pure Python here and on dh610, at the same versions. The expectation, written now: every PASS and
FAIL line has the same verdict and the same printed numbers as dh610's logs, except timings.

## ind26: an independent derivation and evaluation of the hierarchy

`order4.py`'s methods A and B share the table of c_m and h_k (one sympy expansion, its check E0, from its own form of the
exact system). ind26 derives the order equations again from a different starting point, then integrates them by a
third method. It shares with #26 only mpmath, sympy, and the matching conditions of README.md: Y(0) = 1, L_k analytic at
R = 1, and G_k = 0.

- **The starting point.** The ℓ-system of #195, Y_l = εw and F w_l = AY + Bw. Here l = s ln r = ln R, F = 1 − 1/R,
  A = (1 + εΩ)e^{2εl} − (½ + ε)F − ½e^{−l} and B = (½ + 2ε)F + ½e^{−l}. The coordinator's ind195 K1 derived this system
  from E2 of `master.py` in sympy, with residual 0.
- **K1, the order equations.** Substitute w = e^{εl}L(R) (so w is r·L). Then (R − 1)L_R − L/2 = A e^{−εl} Y +
  (B − ½ − εF)L. Expand in ε to order 4 with Ω = Σ Ω_i ε^i. Compare the coefficients with `order4.py`'s `hk`, `cc` and
  `Fsum` (imported, the object under test).
- **K2, a third evaluation.** A Taylor integrator in v = √l, written for this review. Each step carries jets of order 40
  about v₀ for E = e^{v²}, 1/R, s = √(E − 1) and the hierarchy:
  - Y_k = ∫ 2v F_{k−1} dv;
  - h_k from K1's own coefficients;
  - C_k = ∫ (h_k − h_k(1)) 2vE s^{−3} dv, integrated **from the throat outward**. At v₀ = 0 the factors v² are divided
    out exactly.
  - L_k = −2h_k(1) + s C_k.

  The truncation is at V = 17 (the tail is about e^{−V²/2}). The step is 0.25 for v < 3 and 1/(2v₀) beyond, and the
  working precision is 70 digits. This differs from method B, which uses Chebyshev panels, integrates the tail from the
  right and uses spectral integration matrices. G_k = C_k(V) is affine in Ω_{k−2}: two runs at Ω_{k−2} = 0 and 1 give
  the root, Ω₀ from G₂, then Ω₁ from G₃, then Ω₂ from G₄. Ω_{k−1} is set to 0 while order k is solved, since it cancels
  in G_k.
- **K3, the derivation's statements.** These are checked against K2's numbers, not against `order4.py`, plus one
  quadrature.

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| K1 | For k = 0 … 4, the ε^k coefficient of the L equation and of Y_l = εw, from the ℓ-system, equals `order4.py`'s (R − 1)L_k′ − L_k/2 = h_k and dY_k/dl = F_{k−1}, with its `hk`, `cc` and `Fsum`: sympy residual 0 |
| K2 | K2's Ω₀ is within 1e-35 of −4 ln 2. Its Ω₁ is within 1e-33 of 2π²/3 + 8 ln²2. Its Ω₂ is within 1e-30 of 80ζ(3) − (8/3)π² ln 2 − (32/3) ln³2, and within 1e-30 of #26's A70 value, as printed in `order4_output.txt` |
| K3 | (a) K2's slopes dG_k/dΩ_{k−2} at k = 2, 3, 4 are −4π, to 1e-30 relative. (b) K2's G₃ at Ω₁ = 0 equals (4π/3)(−3Ω₀² − 12Ω₀ ln 2 + 24 ln²2 + 2π²), and its G₄ at Ω₂ = 0 equals π(320ζ(3) − (128/3) ln³2 − (32/3)π² ln 2), each to 1e-30 relative (`omega2.md` steps 6 and 7, Ω₀ and Ω₁ K2's own). (c) ∫₀^{π/2} tan θ Cl₂(π − 2θ) dθ = π³/12 to 1e-40, by mpmath tanh-sinh at 60 digits with `clsin(2, ·)` (the step-3 Clausen integral) |

## Mutations (`--mutate=NAME`; each must make ind26 exit non-zero with exactly these criteria failing)

The targets below are predicted from the code, not yet computed. A mutation that misses its targets is reported.

| mutation | change | targets |
|---|---|---|
| `k1-B` | the ℓ-system's B uses (½ + ε)F in place of (½ + 2ε)F, in K1 and K2 alike (this removes the F L_{k−1} term) | K1, K2, K3 |
| `short-V` | K2 truncates at V = 9 (tail about e^{−40}) | K2, K3 |
| `clausen` | K3 (c) compares with π³/12·(1 + 1e-35) | K3 |

## Runs (filled in as they are done)

| file | what |
|---|---|
| `rerun_run_0*.*` | the five reruns: **every line equals dh610's except the timings**, with the same exit codes (1, 1, 0, 0, 0 for runs 01 to 05). N3 (25.8 digits) and N4b (22.0) fail as written, as on dh610. The coordinator's expectation, written above, is met |
| `ind26.py`, `ind26_run1.txt` | run 1: **exit 0, 3 of 3.** K1: the ℓ-system's ε-expansion gives `order4.py`'s h_k and dY_k/dl for k = 0 … 4, sympy residual 0. K2: 304 Taylor steps to V = 17, 9 to 18 s per order. Ω₀ − (−4 ln 2) = 7.2e-45, Ω₁ − (2π²/3 + 8 ln²2) = 1.6e-44, Ω₂ − (80ζ(3) − (8/3)π² ln 2 − (32/3) ln³2) = 4.1e-40, and the same against A70. K3: the slopes are −4π to 1.3e-47 at k = 2, 3, 4. G₃(Ω₁ = 0) = 130.98380956625540135485702452 matches the derived form to 3.4e-45, and G₄(Ω₂ = 0) = 934.5532759858143274892985 to 5.5e-42. The Clausen integral is π³/12 to the working precision (difference 0 at 60 digits) |
| `ind26_run1_mut_*.txt` | `k1-B` fails exactly K1, K2 and K3 (K1's residuals are the missing F L_{k−1} terms). `short-V` fails exactly K2 and K3 (Ω₂ off by 8.6e-11). `clausen` fails exactly K3 (2.6e-35) |
