# I189-mac: a k-plane stepper with re-orthonormalization between Taylor steps, for multishoot

Machine: mac, the coordinator's Mac (nathans-macbook-air-m5-3: Apple M5, 10 cores, 32 GB, macOS), shared with other sessions; runner
negative-mass-mac-i189 (Claude Code, Sonnet 5.5, account claude-me2). Issue: https://github.com/nmoinvaz/negative-mass/issues/189
Code: worktree `~/Source/negative-mass-i189`, branch `wip/i189-plane-lib` (from `wip/i187-taylor-rows` 2a84083, #187's head); pushes:
`git push origin HEAD:refs/heads/wip/i189-plane-lib`. Library clone `~/Source/negative-mass-i189-libs/multishoot` (main c0915f0, 4.2.0),
feature branch `feat/plane-stepper`. Rust 1.94.0 (aarch64-apple-darwin); multishoot builds against crates.io's multidouble 5.1.0 and
multisolver 0.2.2 only.
Written before the first run of record. `dev_NN_*` are development runs (made with `devrun.sh`: stdout, stderr and exit code kept);
`run_NN_*` are the runs of record. Amendments are numbered and dated at the end; a number below that came from a development run says so.

## What is built

A module `multishoot::plane` (the engine knows nothing of any one problem):

- `plane::Real`, the scalar trait: `zero, one, from_f64, to_f64, recip, sqrt, ln` and the unit roundoff `EPS`, implemented for `f64`, `DD`, `QD`
  and `OD`. It is not `Precision::Scalar`: that trait has no division, square root or logarithm, and `f64` is no `Precision`; `DD`, `QD`, `OD`
  are `Precision<Native>`'s scalars for `Double`, `Quad`, `Octo`.
- `plane::JetSource<T>`: `pattern()` (the nonzero entries (i, j) of J) and `jets(x0, kj, &mut Jets<T>)` (coefficients 0..kj of every entry about x0).
  `Jets<T>` holds one `Entry { i, j, n, c }` per pattern entry. The caller supplies the jets; the library holds no problem.
- `plane::Plane<T>`: `new(n, k, columns)` takes a basis of the initial plane (column-major, any full-rank), orthonormalizes it by classical
  Gram–Schmidt with one reorthogonalization (positive diagonal) and records ln of the diagonal as the initial Gram term;
  `advance(&src, xa, xb, &plan, kj)` carries it from xa to xb (either direction) by Taylor steps, orthonormalizing after every step and adding
  Σ ln R_ii; `columns()`, `ln_vol()` (= ln of the volume of the plane as carried from the supplied basis: initial Gram term plus every step's
  Σ ln R_ii); `Stats { steps, hmin, hmax }`.
- The step is multishoot's planner rule (`taylor::Plan`, `kth_root`): the largest h with e_(kt−1) h^(kt−1) ≤ tol and e_kt h^kt ≤ tol, capped at
  `hmax`, e_k = max |c_k| over the plane's entries. `taylor::step_size` is split so that its rule is a function of the two norms
  (`step_from_norms`), which the plane uses; `step_size` gives the same bits as before (its tests are unchanged). **Where multishoot's
  types did not fit** (to be stated in the PR): `Work`/`Fl` hold 8 B-lane fields on collocation points (`Equations`), `Jet<N>` is a series in
  eight SIMD lanes, and `Precision::Scalar` lacks the operations above; the plane's coefficients are scalars of one lane, so it has its own
  scalar trait and entry jets and shares `Plan`, `kth_root` and the step rule.
- Controls (feature `mutate`, `control::PlaneControl`, set with `Plane::set_control`): see below.

## Planted cases (in multishoot's `tests/plane.rs`; the reference of each is a closed form that shares no code with the stepper)

Common: Taylor tol = 100 ε_lane, kt = `Plan::optimal_kt(tol)`, kj = kt, hmax = 1, xa = 0. The plane's error is the Frobenius norm of
(I − Π) Y_c, Π the projector onto the exact plane, formed in the lane from the exact basis (sin of the largest principal angle ≤ this).
The log-volume error is |ln_vol − reference|. The bars are written once, as 1e4 ε_lane for the plane and 1e4 ε_lane max(1, |reference|) for
the log-volume, ε f64 1.1102230246251565e-16, dd 1.232595164407831e-32, qd 1.504632769052528e-64, od 2.3e-128 (the crate's `Num::EPS`).

| case | system | exact | xb |
|---|---|---|---|
| **P1** | n = 4, J = P diag(24, 8, −8, −24) P⁻¹, P = L U with L = [[1,0,0,0],[1,1,0,0],[0,1,1,0],[1,0,1,1]], U = [[1,1,0,1],[0,1,1,0],[0,0,1,1],[0,0,0,1]] (det P = 1, cond₂ P = 96, J an exact integer matrix); k = 2, initial plane P[:, :2] (not orthonormal; Gram matrix [[3,4],[4,7]], det 5) | plane = span P[:, :2] for all x; ln_vol = (24 + 8) x + ½ ln 5 (constant 0.804718956217050187300379666613093819762800677134…, from mpmath) | 12 |
| **P2** | n = 4, J(x) = Q′Qᵀ + Q Λ Qᵀ, Q(x) = H Rot₁₂(θ₁(x)) Rot₂₃(θ₂(x)), H = ½[[1,1,1,1],[1,−1,1,−1],[1,1,−1,−1],[1,−1,−1,1]], Rot by cos θ = (1 − u²)/(1 + u²), sin θ = 2u/(1 + u²), u₁ = x/2, u₂ = x/4, Λ = diag(20, 4, −8, −20); k = 2, initial plane Q(0)[:, :2] M with M = [[3,1],[1,1]] (det 2) | Φ(x) = Q(x) e^{Λx}: plane = span Q(x)[:, :2]; ln_vol = (20 + 4) x + ln 2 | 12 |
| **P3** | n = 4, k = n, J(x) = P diag(24, 8, −8, −24) P⁻¹ + x A₁ + x² A₂ (integer A₁, A₂ in the test; tr A₁ = 3, tr A₂ = −2, tr(P diag P⁻¹) = 0), initial plane U (columns, det 1, not orthonormal) | Liouville: ln_vol = ∫₀ˣ tr J = 3 x²/2 − 2 x³/3 (no plane to compare: k = n) | 4 |
| **P1o** | P1 in octo-double, a smoke test of the `OD` lane (bars 1e4 · 2.3e-128) | as P1 | 12 |

Each of P1, P2, P3 in f64, dd and qd (bars: plane 1.11e-12, 1.23e-28, 1.50e-60; log-volume P1 4.3e-10, 4.7e-26, 5.8e-58, P2 3.2e-10, 3.6e-26,
4.3e-58, P3 2.1e-11, 2.3e-27, 2.8e-59, from the formula, computed in the test). Pass criteria are written in each test's doc comment before its first run. Passing
needs, in addition: the returned columns orthonormal to 1e2 ε_lane (‖YᵀY − I‖_max), and the step count and hmin/hmax printed (the
stepper itself panics on a diagonal entry that is not positive and finite). P3 has no plane check (k = n: the plane is everything); its
initial basis U has det U = +1, so the volume carries no sign.

Timing is not a criterion here.

## Controls

Declared by name before any run; **their targets (which check each must fail, in which lane) are declared after a development run of each
and written in an amendment** (the coordinator's rule: compute what a control does first).

In the library (`mutate`, `PlaneControl`):

| name | what it breaks | expected to fail |
|---|---|---|
| `LowSum(m)` | the Taylor sum cut at order m = 8 while the step assumes kt | P1, P2, P3, every lane |
| `RecipDD` | 1/k formed in double-double and widened | P1, P2, P3 in qd only (a no-op in f64 and dd) |
| `EndOnly` | no orthonormalization between steps, one at the end of `advance` | P1, P2, P3 where the in-plane spread (λ₁ − λ_k) x exceeds ln(1/ε): P1 and P2 192 and 192, f64, dd, qd |
| `NoGram` | the initial Gram term left out of `ln_vol` | P1, P2 (P3's Gram term is 0) |
| `LogDrop` | the last column's ln R_kk left out of every step's term | P1, P2, P3 |
| `SkipQr(i)` | no orthonormalization after step i (and its R's term carried into the next one's) | **to be computed in a development run, step 3; if silent, reported and the coordinator names the control that replaces it** |

In the test (a wrong input, no hook): `J_gamma` (P1 with γ₂ scaled by 1 + 1e-6), `J_noQdot` (P2 with the Q′Qᵀ term dropped from J),
`J_trace` (P3 with tr A₁ off by 1), `wrong_plane` (P1's check against span P[:, 1:3]).

## Crate switch (`phase2/nonradial/taylor_polar/`, feature `lib_plane`)

- The crate's `plane::integrate` and `gram_schmidt` call the library behind the feature; `Cargo.toml` carries `[patch.crates-io] multishoot =
  { git = "https://github.com/nmoinvaz/multishoot", rev = "<PR branch commit>" }` next to the multidouble patch, no absolute path.
  With the feature off the crate's own `plane.rs` runs, #186's and #187's paths unchanged.
- **X1** the crate builds with the feature on and off on this Mac (and `Cargo.toml` has no absolute path: `rg '/Users' Cargo.toml` empty).
- **X2** `python taylor_polar.py` (default mode, 23 checks) with the feature on: 22 passed, 0 failed, 1 skipped (TS), exit 0; the same off
  (it passed before, #187's run_18).
- **X3** `python taylor_polar.py --rows` for l = 2, 3, 4, 5, 6 and the capped rows: every token of the output (as strings) is the same with the
  feature on and off, and the same as the stored `convergence_l{2,4,5,6}_output.txt` tokens where #187 matched them (327 tokens).
- **X4** `taylor_polar d` at l = 2, γ = 1, 40, in f64, dd and qd, and at l = 4, γ = 300 in dd: D printed in full with the feature on and off, and the
  number of leading digits that agree reported (information; the step points differ by an ulp where `kth_root` and `powf` differ, so D
  need not agree in every digit); the gate is X3.
- **X5** the comparison itself can fail: the same comparison script run on an on-output against an off-output of a run with `mutate=jsign`
  (one J sign flipped) must report a mismatch and exit 1.
- Timing with the feature on and off at l = 6, γ = 1000 (dd, f64), reported with machine, load and thread count.

## Runs

One process at a time, nice 10, at most 2 threads (`RAYON_NUM_THREADS=2`, `cargo build -j 2`, `cargo test --release -j 2 -- --test-threads=2`),
runs over a few minutes detached with the PID recorded; any run not finished in 1 h of wall time is stopped by its PID and reported. Memory
is reported only (`/usr/bin/time -l`). Backends on this Mac: the default build (aarch64 NEON) and `--features portable`, whose test output
is compared bitwise; the `+avx2,+fma` build cannot run here and is not run.

## Amendments

**A1 (2026-11-26, after dev_02 to dev_12). Code at multishoot `feat/plane-stepper` b8bae85. Control targets declared; one control renamed.**

First run of P1, P2, P3 (dev_02, bars as written above, not changed): every cell passes, 1e2 to 1e4 below its bar. Plane error, ln_vol error
(bar), steps: P1 f64 8.4e-16, 4.5e-13 (4.3e-10), 154; dd 1.5e-31, 6.3e-30 (4.7e-26), 96; qd 5.3e-64, 1.8e-61 (5.8e-58), 58; P1o od 1.5e-129,
2.0e-127 (8.9e-122), 34; P2 f64 1.1e-16, 5.7e-14 (3.2e-10), 126; dd 2.1e-32, 0 (3.6e-26; the computed dd log-volume equals the reference's
parts exactly: the accumulator's resolution at 288.7 is 3.5e-30, coarser than the terms' noise), 79; qd 6.6e-65, 6.7e-63 (4.3e-58), 48; P3
f64 1.4e-14 (2.1e-11), 116; dd 1.3e-29 (2.3e-27), 74; qd 6.5e-61 (2.8e-59), 47. The wrong inputs `J_gamma`, `wrong_plane` (now `OtherPlane` in
the code), `ref_no_gram`, `J_noQdot`, `J_trace` fire in f64, dd and qd (plane error 0.76 for `wrong_plane`, ln_vol errors 9.6e-5, 0.80, 0.69,
8.0e-2, 8.0).

**Declared targets** (dev_03 table, dev_10 to dev_12):

| control | fails (case × lane) | silent, by design |
|---|---|---|
| `LowSum(8)` | P1, P2, P3 × f64, dd, qd (ln_vol error 2e-2 to 16) | |
| `ScaleOnly` (renamed from `EndOnly`, see below) | P1, P2, P3 × f64, dd, qd (ln_vol errors 40 to 510; P3 in f64 the stepper refuses: the columns became dependent, a panic, counted as failed) | |
| `LogDrop` | P1, P2, P3 × f64, dd, qd (ln_vol errors 48 to 129) | |
| `NoGram` | P1, P2 × f64, dd, qd (0.80 and 0.69) | P3 (its starting basis has volume 1: error 1e-14 as without the control) |
| `RecipDD` | P1, P2, P3 × qd (ln_vol 4e-31, 3e-31, 7e-30 against bars of 1e-58) | f64, dd (the widened reciprocals are the lane's own: identical bits) |
| `SkipQr(i, m)` | **not declared: see below** | |

`EndOnly` became `ScaleOnly`: with no orthogonalization and no rescaling, the columns grow like e^(24 x), the planner's absolute tolerance
shrinks the steps with them and the f64 run of P1 took 10 114 309 steps (dev_09, 69 s of a test run). The control now scales each column to unit
length after every step (adding ln of its length to the log-volume) and orthonormalizes once at the end; same exact result, same step grid as
the baseline, and the loss is what the orthogonalization prevented (dev_10 to dev_12).

**`SkipQr`, the issue's control "skip one orthonormalization".** `SkipQr(i, 1)` after step i (dev_03; i = first, middle, second to last):

- silent on P1 and P2 in f64, dd and qd and on P3 in f64 and dd: ln_vol errors stay at the baseline's (P1 f64 1e-13 to 4.5e-13, baseline 4.5e-13;
  P2 qd 1e-62 against 6.7e-63; plane errors unchanged);
- on P3 in dd the error is 2.2e-27 at i = 0 against the bar 2.3e-27 (silent by 7%), 3.4e-28 and 4.8e-29 at the others; **on P3 in qd it
  fires**, 7.8e-58, 1.5e-58 and 2.6e-58 against 2.8e-59 (baseline 6.5e-61). That is not the growth spread: the step's spread (γ₁ − γ₄) h is 2.7
  to 6.7 there against ln(1/ε) = 147. The error is independent of the Taylor tolerance (dev_04: tol 1000 ε down to ε, qd 4.3e-58, 7.8e-58, 1.6e-58,
  4.6e-58; dd 6.6e-28, 2.2e-27, 1.1e-27, 1.7e-27), so it is rounding, not truncation: it is the loss of the full 4-column determinant's last
  digits to the condition number of the unnormalized product (P is non-normal, cond₂ P = 96), about 30 to 1000 times the baseline's roundoff.
- The per-step spreads (largest step times the gap) against ln(1/ε): P1 (γ₁ − γ₂ = 16, γ₁ − γ₃ = 32) 1.2 / 2.5 (f64), 2.0 / 4.0 (dd), 3.3 / 6.6
  (qd); P2 (16, 28) 1.5 / 2.7, 2.4 / 4.3, 4.0 / 7.0; P3 (γ₁ − γ₄ = 48) 3.0, 4.5, 6.7; ln(1/ε) is 36.7, 73.5, 147.0. One step's spread is
  5 to 30 times too small, as the coordinator expected.
- Skipping a run of m consecutive orthonormalizations (dev_05, from a quarter of the way; spread S = gap × mean step × m): the loss grows smoothly
  with S, not at S = ln(1/ε). ln_vol error against the bar: P1 f64 4e-11 at S = 12.5 (silent), 9.7e-10 at 18.7 (fires), 1.3e-8 at 25;
  dd 9e-28 at S = 10 (silent), 1.1e-24 at 20 (fires); qd 2.7e-56 at S = 17 (fires); P3 fires from m = 5 in every lane. P2 stayed silent
  from a quarter of the way up to S = 46 (f64) and 40 (qd) but fires from step 0 (dev_07: f64 3.6e-11 at S = 30, 1.5e-7 at 46, 7.3e-6 at 61,
  0.74 at 152). Which steps are skipped matters on P2, because the rotation slows (θ′ = 2/(2 (1 + x²/4))).
- Candidates in place of `SkipQr(i, 1)` (the coordinator chooses; none is declared): (a) `ScaleOnly` (above; fires on all 9 cells); (b)
  `SkipQr(i, m)` with m set per lane so that S ≥ about ln(1/ε)/2 (from dev_05: fires on P1 and P3 everywhere, on P2 only from the start); (c) a planted
  case in which one planner step's spread exceeds ln(1/ε), which needs a gap of about twice the largest rate at a high order (a decaying plane
  column, whose Taylor sum then cancels) and is not built.

**A2 (2026-11-26, the coordinator's ruling on step 3).** The control that stands for the issue's "skip one orthonormalization fails on a planted case"
is `ScaleOnly` (declared in A1; fixed, the same in every lane, added after the development run by this ruling). `SkipQr(i, m)` with m per lane is
not declared (choosing m after seeing the errors is tuning) and the planted case (c) is not built. `SkipQr(i, 1)` is recorded as a result, as it
is, in A1 above and in the PR: silent on P1 and P2 in every lane and on P3 in f64 and dd (dd at 93% of the bar at the first step), and past the bar
on P3 in qd by condition-number roundoff (cond₂ P = 96), not by the growth spread. In the closing table the issue's line is therefore met as worded
on one cell only (P3, qd), for a reason other than its intent; the `ScaleOnly` line follows it. The `SkipQr(i, m)` runs stay as development logs
(dev_05, dev_07). multishoot's test `skip_one_{f64,dd,qd}` prints the skip-one outcomes (a result, nothing asserted; dev_13). Library head
4a54bd0 (`plane: record the skip-one orthonormalization as a result`, `tests: keep the plane test's case alias with its only user`).
The planner difference and #186's comment (it says classical Gram–Schmidt; its loop is modified Gram–Schmidt applied twice) are reported in the note, and
#186's `plane.rs` comment is left as it is for the coordinator to correct on main.
