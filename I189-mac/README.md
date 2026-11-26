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

(none yet)
