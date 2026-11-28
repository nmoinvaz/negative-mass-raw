# I185-mac: the conical ODE N = 0 at η = 0 without a leading-power hypothesis, and the crossing of F² = η² + 1 at #167's three a3->0 points

Machine: the coordinator's Mac (Apple M5, macOS, shared, loaded), at most 2 processes, `nice -n 10`.
Issue: https://github.com/nmoinvaz/negative-mass/issues/185 (depends on #167; related #207, #203).
Code: negative-mass branch `wip/i185-conical-eta0`, worktree `~/Source/negative-mass-i185`, `notes/warp/conical_eta0.py` at cecf0b8. It imports
`det_classify` unchanged and calls #167's crate binary (`conical_global walk`, `scan`) unchanged, built with `cargo build --release -j 2` from the worktree
(multishoot 5.0.0, multisolver 0.3.0, multidouble 6.1.0 as in `conical_global/Cargo.toml` at origin/main); the series cache is copied from `~/Source/negative-mass-i216`.
Python: `~/Source/negative-mass/.venv/bin/python` (sympy 1.14, mpmath 1.3, numpy, scipy).

## Issues read before the work

`gh search issues` on "conical eta", "a3->0", "kappa curve", "locate_lib": #203 (open: classifies #183's 126 κ-curve ends and continues the log ends across
F² = η² + 1 by a C¹ rule, so it uses this issue's decision), #207 (closed: `locate_lib`; 10 of 126 ends read as complex pairs at Im ~ 1.5e-11), #183, #191 (the locator),
#309. #167's closing text (`notes/warp/conical_global.md` §2, §5) is the source. choptuik-large-d #782 is a Domb–Sykes test of a square-root point against a pole for another
equation; its method is not used, its code is not run.

## What the script does (status words: AGENTS.md)

With t = ln η, P = ηF′ = F_t, Q = η²F″ + ηF′ = F_tt, s = η²: η⁴N = N₀ + sN₂ + s²N₄ exactly (`reduction`). The autonomous part factors, N₀ = −2AB,
A = F(P − Q) − P² = −η²(FF″ + F′²), B = (F² − 1)Q² + 2FP²Q + 2FP³ + 2P⁴. A = 0 is F² = a + bη (branch I); B = 0 is branch II.

| check | what | status of what it shows |
|---|---|---|
| `reduction` | the identity, the factorization, no odd powers of η | **checked symbolically** |
| `planted` | the dominant-balance code on six planted equations with known local solutions | the code's test |
| `table` | the code on N: exponents and coefficients of every balance, for F → f (f generic, 0, ±1), F → ∞, P → p₀ ≠ 0, F ~ ln T | **checked symbolically** (Newton polygon of the exponential-logarithmic ansätze) |
| `ift_row1` | a real C¹ solution with F′(0) = g ≠ 0, F(0) = f ∉ {0, ±1} has F″ → −g²/f and is the analytic family | **proved** (by hand, the leading coefficients **checked symbolically**) |
| `floor15` | #167's 15 FLOOR flows continued below η = 10⁻⁶ along branch II to its fold | **numerical evidence** |
| `iia_exists` | branch II orbits with P → 0, F − f ~ 2(1 − f²)/(f \|ln η\|) | **numerical evidence** |
| `kappa_symbolic` | the desingularized flow at κ = F² − η² − 1 = 0, its 1:1 resonance, the scaled normal form and its exact solution | **checked symbolically** |
| `kappa_cross` | the three a3->0 ends of #167 at 50 digits: the solution crosses κ = 0 | **numerical evidence** |
| `kappa_retrace` | the physical ODE integrated back from the crossing to the crate's state at η* + 10⁻⁴ | **numerical evidence** (independent integration, shared N) |

The dominant-balance code (in the script) takes a polynomial E(F, P, Q; s), a regime and the weights of the monomials; it returns the faces of the Newton polygon (exponents where two or
more monomials tie), the truncated equation on the face and its solutions, in exact rationals. Regimes: `exp` (F = f + c e^{pt}, powers of T = −t allowed: weight degree + 2e/p), `alg`
(F = f + cT^{−γ}), `const` (P → p₀ ≠ 0, F ~ p₀t, admissible iff Q ~ T^{−θ} with θ ≥ 1), `iter` (P = aT^{−m}, F ~ T^{1−m} or ln T), `big` (F = ce^{−pt} large).

**Planted cases** (each equation has an exact local solution; the code must return its exponent and coefficient, and the exact solution is substituted symbolically):

| id | equation | exact solution | code must return |
|---|---|---|---|
| PL1 | Q = 0 (ηF″ + F′ = 0) | F = a + p₀ ln η | P → p₀ with p₀ free |
| PL2 | Q² − 2P³ = 0 | F = f₀ + 2/(t₀ − t), a non-power approach | γ = 1, c = 2 |
| PL3 | Q − P² = 0 | F = −ln(t₀ − t), an iterated logarithm | m = 1, a = 1 |
| PL4 | Q − P + 9.25F = 0 | F = e^{t/2} cos 3t | indicial roots ½ ± 3i (no real p) |
| PL5 | Q − P + F/4 = 0 | F = e^{t/2}(1 + 2t) | indicial root ½ of multiplicity 2 (a log factor) |
| PL6 | F(P − Q) − P² = 0 | F² = a + bη | p = 1 at f ≠ 0; p = ½ at f = 0 |

## Development (before this file)

Probe scripts are in `dev/probes/` (their outputs were printed in the session and not saved; the numbers below are read again by the logged dev runs). `dev/dev_01_checks.log` to
`dev/dev_09_retrace-root.log` are the logged dev runs at cecf0b8 (rc in the `.rc` files).

What the probes found, which fixed the thresholds below:
- The crate's FLOOR flows are on branch II with Q < 0: at the floor B(F, P, Q) = 0 to 4.7e-13 relative. The first continuation used the cubic's nearest root and jumped across F = 0; the
  continuation of record follows B = 0 (closed-form root) to its fold. Two earlier root choices (nearest root of the full cubic, with and without the s-terms) were discarded.
- At the three κ-curve points the desingularized flow (η, F, F′)′ = (a₃, F′a₃, w), w the root of w³ + a₂w² + a₁a₃w + a₀a₃² = 0 (monic, regular at a₃ = 0), crosses κ = 0 at η = η* + 3.62e-9
  (1.5, 3000), +9.76e-9 (±2, ±3000), with F″ finite (−5607.75, ∓4547.85), not at an end. The first attempt integrated for τ fixed at 10 and ran past 50 digits at the (±2) points
  (κ below 1e-50): the run now stops at |κ| < 1e-28. For F < 0 the flow runs in −τ. The first prediction of y_∞ interpolated κ_z in the 1-unit samples (factor 2.1 off); it uses every step.
- The continuation below the crossing on the tracked root passes a fold of the cubic in w at d ≈ 5e-9 (Y = y/√κ reaches 2√(a₁α)/β); the tracker changes root there at (2, 3000). Only the
  retrace (upward, no fold) is a check; the downward values are printed as information.

## Criteria (declared here; none is loosened after the record run)

| check | passes iff |
|---|---|
| `reduction` | N₀ + 2AB, N₂ − (F²P²Q² + 4FP⁴Q − 2FQ³ + 4P⁶ − 3P²Q²), N₄ − P²(P⁴ − Q²) are 0 as polynomials, the odd powers of η vanish, A = −η²(FF″ + F′²) |
| `planted` | all six rows of the table above equal the planted truth and the exact solutions satisfy the equations (sympy residual 0) |
| `table` | f generic: face (3, s⁰), g(p) = 2f(f² − 1)p⁵(p − 1), roots {1, 0⁵}; alg γ = 1, c = 2(1 − f²)/f. f = 0: roots {½, 0⁵}; alg γ = ½, c = ±3/2. f = ±1: tie σ = 1 (p = 2), c = ±2/5, σ > 1 face roots {1, −½, 0⁴}, no alg balance. P → p₀: no admissible tie (θ ≥ 1), dominant face carries P⁴. iter: no tie. big: g(p) roots {2/5, −½, 0⁴}. All exact |
| `ift_row1` | a₃(0) = a₂(0) = 0, a₁(0) = 2g²f(f² − 1), a₀(0) = 2g⁴(f² − 1), x₀ = −g²/f, and a₃F″² + a₂F″ + a₁ = 2f(f² − 1)(ηF″ + g)² at orders η², η, 1 (exact) |
| `floor15` | all 15 flows reach the fold of B at t_fold ∈ (−1000, −14); B = 0 at the floor to < 1e-9; the neglected s-terms < 1e-9 of the leading terms along each path; P^{−1/2} follows P₀^{−1/2} + (√κ/2)(t − t₀) to < 1% ten e-folds below the floor for the 4 points with \|P₀\| < 5e-4; the mirror (F → −F) agrees to 1e-9 |
| `iia_exists` | at three starts (F, P) at t = −13.8 on the Q > 0 root, walked to t = −4e5: P T²κ/4, the slope of P^{−1/2} over √κ/2 and c from F against 2(1 − f²)/f are each within 1% of 1 |
| `kappa_symbolic` | the 11 identities of the check hold exactly: a₃ = 2Fη²κ; a₂ on κ = 0; the zero g_e = η/(2F); κ′ = −η; β = ∂a₂/∂g = 2Fη³; λ_κ = −β (equal eigenvalues); a₁(E) = η⁶(η² + 2)/(4F³); the scaled cubic; dY/dτ = ½√(β²Y² + 4a₁α); the sinh solution; y_∞ = c√κ_z with c = η√(η² + 2)/(2√2 F²) |
| `kappa_cross` | at each of (1.5, 3000), (2, 3000), (−2, −3000): \|κ\| < 1e-26 reached; sgn(F)·(F′ − η/(2F)) > 0; \|y_∞\|/\|c√κ_z\| − 1 < 2e-3; step 0.02/β against 0.01/β agree to 1e-7 in (η, F′, F″); \|η_κ − x*_ref\| < 1e-8 (x*_ref: the crate's refined estimate at R ≤ 1e-8); N/scale at the end < 1e-30; \|F″\| < 1e5; (2, 3000) and (−2, −3000) mirror to 1e-12 |
| `kappa_retrace` | at (1.5, 3000) and (2, 3000), 50 digits, the retrace reaches η* + 10⁻⁴ with (F, F′, F″) within 1e-7 relative of the crate's state at both step sizes (1% and 0.5% of the distance) and the two differ by < 1e-9 |

A check that raises counts as a failure. A failed check is a result.

## Mutations (`--mutate=NAME`; effect computed in the dev runs)

| name | change | target | effect in the dev run |
|---|---|---|---|
| `red-factor` | B with 3FP³ in place of 2FP³ | `reduction` | residual of N₀ + 2AB is not 0 |
| `bal-weight` | weight of Q is γ + 1 in place of γ + 2 | `planted` | PL2: no tie at a positive γ, the code returns nothing |
| `n-c33` | `conical_N(c33=3)` | `table`, `kappa_symbolic` | table: g(p) = fp³(p − 1)(3f²p² − 2f²p + f² − 2p²) with extra roots (f² ∓ √2 f√(1 − f²))/(3f² − 2), no alg tie, no tie at f = ±1; `kappa_symbolic`: a₃ = 2Fη²κ is false |
| `ift-sq` | perfect square 3f(f² − 1) in place of 2f(f² − 1) | `ift_row1` | the quadratic part differs |
| `floor-sign` | continuation on the Q > 0 root | `floor15` | not every flow reaches the fold (range to −9000), law deviation 0.28 |
| `iia-sign` | Q < 0 root for the P → 0 orbits | `iia_exists` | P T²κ/4 = −5.7, −1.0, −61; P^{−1/2} is not defined |
| `cross-root` | the flow follows the root −a₀a₃/a₁ | `kappa_cross` | η_κ − η* = 1.1e-5, F′ − η/(2F) = −0.186, no zero crossing of y, N/scale 0.24 |
| `retrace-root` | the retrace takes the root −a₀/a₁ | `kappa_retrace` | F, F′, F″ differ from the crate's state by 1.0 |

## Run of record

`scripts/run_record.sh` runs `conical_eta0.py` (nine checks, then the eight controls, each on its target checks only) detached with nohup; logs `record/run_01.{log,err,rc}`, the controls' logs in
`record/`. A run not finished in 2 h wall time is stopped by its PID and reported. Nothing stops a process on its memory use.

## What I expect (a prior, not a criterion)

All nine checks pass and all eight controls fire. The a3->0 ends are complex pairs of the Taylor series at distance < 1e-8 from the real axis, not log ends: the flow crosses κ = 0
analytically, with F′ above η/(2F) by y_∞ ~ 2e-5 to 4e-5. The 15 FLOOR flows end at a fold of branch II at η_fold between e^{−299} and 8e-8, and F′ ≈ p₀/η is a transient of branch II.
