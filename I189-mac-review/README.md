# I189-mac-review: the coordinator's review of #189 (rerun of the crate switch, independent check ind189)

The runner's raw folder for #189 is `I189-mac` (it ran on this Mac), so the review uses this folder name.

Machine: macOS (the coordinator's Mac, Apple M5, arm64), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`:
mpmath 1.3.0), Rust 1.94.0, nice 10, at most 2 processes. Issue: https://github.com/nmoinvaz/negative-mass/issues/189.
Under review: multishoot pull request #70 (`feat/plane-stepper` at a880903), branch `wip/i189-plane-lib` at 6c40e02,
raw `I189-mac` at bb964b6. Written 2026-11-26 before the first run of `ind189.py`.

## Rerun of the crate switch

`rerun.sh`, from a detached worktree `~/Source/negative-mass-r189/nm` at 6c40e02, with the crate built there with
`cargo build --release --locked --features lib_plane`. It runs the rows for l = 2, 4 and 6 (with CAP6), then the default
mode, with a fresh `--jsonl-dir`. The feature-off reference is the coordinator's own rerun of #187
(`I187-mac-review/rerun_*.log`, built at 2a84083, which has no `lib_plane`). `compare_switch_review.py` compares them
row by row with timings and load removed. Expected from the runner's report: every D and q token equal, and the
CAP6b line's E2 and E3 values differ.

## ind189: the plane stepper on an Airy system no one has used

A planted case of the coordinator's choosing, through the pull request's `plane::Plane::advance`. A Rust harness
(`airy_plane/`, depending on the clone `~/Source/negative-mass-r189/multishoot` at a880903 by path) carries a k-plane
and prints its basis and `ln_vol`. `ind189.py` computes the exact plane and volume in mpmath at 90 digits and compares.

The system: y = Q (u, u′, v, v′) with u″ = x u and v″ = 4x v, Q = G(2,3; 7/25, 24/25) G(0,1; 8/17, 15/17)
G(1,3; 5/13, 12/13) G(0,2; 3/5, 4/5), a product of Givens rotations with rational cosines that couples the two blocks.
J(x) = Q (A + B x) Qᵀ is linear in x and dense. The fundamental matrices are built from Ai and Bi:
- for u: f = π(Bi′(0) Ai − Ai′(0) Bi) and g = π(Ai(0) Bi − Bi(0) Ai), which have Φ(0) = I;
- for v: f and g at c x with c = 4^{1/3}.

Growth rates are (2/3)x^{3/2} for the u block and (4/3)x^{3/2} for the v block, super-exponential, with two decaying
partners. The starting basis is Q·Bmat[:, :k], with Bmat = [[1, 0, ½, ¼], [½, 1, 0, −½], [¼, −½, 1, 0], [0, ¾, ½, 1]]
(exact binary entries, every column mixing both blocks). The exact plane at X is Q blockdiag(Φ_u, Φ_v) Bmat[:, :k],
and the exact ln_vol is ½ ln det(YᵀY) of it.

Lanes f64, dd, qd. The plan is order kt = 24, 40, 70 and tol = ε/10 with ε = the lane's `Real::EPS`, hmax 0.5,
kj = kt. The ends are X = 4 and 10; at X = 10 the u and v rates differ by e^21 and the extremes by e^84.

Shared with the object under test: nothing but the API (`Plane::new`, `advance`, `columns`, `ln_vol`) and multidouble's
lane types. New: the system, the basis, the exact solution, the comparison.

## Criteria (each coded as worded; each can fail)

In each lane and at each X, the plane error is the Frobenius norm of (I − U Uᵀ) Y_lib, where U is an orthonormal basis
of the exact plane and Y_lib the library's basis (a bound on the sine of the largest principal angle). The ln_vol error
is |ln_vol_lib − ln_vol_exact|. The bars are set now: plane ≤ 1e4·ε, ln_vol ≤ 1e4·ε·max(1, |ln_vol_exact|).

| id | criterion |
|---|---|
| Q1 | k = 1 (the dominant direction, the v block's Bi): the plane and ln_vol bars hold in f64, dd and qd at X = 4 and 10 |
| Q2 | k = 2 (the two growing solutions): the same |
| Q3 | k = 4, the Liouville identity: tr J = 0, so ln_vol_exact = ln \|det(Q·Bmat)\| at every X; the ln_vol bar holds in each lane at X = 4 and 10 |

A harness run that panics or exits non-zero fails its cell.

## Mutations (`--mutate=NAME`; each must make ind189 exit non-zero with exactly these criteria failing)

| mutation | change | targets |
|---|---|---|
| `wrong-scale` | the reference uses v″ = 4(1 + 1e-9) x v | Q1, Q2 (Q3's determinant is 1 whatever the scale) |
| `scaleonly` | the harness, built with multishoot's `mutate` feature, sets `PlaneControl::ScaleOnly` (no orthogonalization between steps) | Q2, Q3 (k = 1 has nothing to orthogonalize) |

## Runs (filled in as they are done)

| file | what |
|---|---|
| `ind189_run1.txt` | run 1: **crashed** before any verdict, on a formatting bug in ind189 (an mpf passed to a float format). Fixed in place: the bar is formed as a float. No criterion or bar changed |
| `ind189_run2.txt` | run 2: exit 1. **Q1 and Q2 pass** in every cell (the worst case is qd's plane error at 1.6e-64 against 1.5e-60). **Q3 fails at X = 10 in dd and qd**, with the same ln_vol error, 4.5e-18, in both lanes; f64 at X = 10 and every lane at X = 4 pass. The cause is the coordinator's reference, not the library: at X = 10, Φ's entries reach e^±42, so ½ ln det(YᵀY) for k = 4 cancels about 73 digits of the 90 the reference carries, leaving about 17. The reference's own self-check (\|ln_vol_exact − ln\|det(Q·Bmat)\|\| < 1e-80) fails at both cells too. Q3 stays failed as run 2 reports it |
| `ind189_run3.txt` | run 3, with A1: **exit 0, 3 of 3.** Q1 (k = 1): plane errors up to 1.5e-16, 1.1e-32 and 1.6e-64, ln_vol errors up to 1.8e-14, 5.0e-31 and 2.7e-63 (f64, dd, qd). Q2 (k = 2): plane errors up to 2.9e-16, 3.0e-32 and 3.9e-65, ln_vol errors up to 6.2e-15, 1.2e-30 and 5.0e-63. Q3 (k = 4, Liouville): 1.8e-14, 3.6e-30, 9.4e-63 at X = 10. Each is at least 1e3 below its bar. 22 to 31 steps to X = 10 |
| `ind189_run3_mut_*.txt` | `wrong-scale` fails exactly Q1 and Q2. `scaleonly` fails exactly Q2 and Q3. Q2 fails at X = 10 in every lane (plane 1.3e-8, 4.4e-24, 1.5e-56) and passes at X = 4. Q3 fails at X = 4 in f64 (9.2e-10) and at X = 10 in every lane (ln_vol off by 67, 6.1, 3.5e-30). Q1 passes, as declared |
| `rerun_*.log`, `compare_switch_review.py`, `compare_switch_review_1.txt`, `_2.txt` | the feature-on reruns (load 5 to 9.5). In `rerun_rows_l2` **RX was SKIPPED**: the review worktree sits one level deeper, so the driver's default raw path (`../../../negative-mass-raw`) did not exist. That was the harness's defect, so l = 2 was rerun with `--raw` given (`rerun_rows_l2_2`). Against the coordinator's feature-off reruns of #187: **every row and header line is identical** at l = 2, 4 and 6, with the same exit codes and the same verdicts on every CHECK line. The CHECK lines differ in 0 of 83, 1 of 51 (a time), 3 of 139 (CAP6b's E2 and E3: 9.60e-9 on against 6.90e-9 off) and 20 of 1445 tokens (the default mode: P0–P2's planted errors at roundoff, L1's f64-lane D in its last digits, V3's error bars). The default mode gives 22 passed, 0 failed, 1 skipped (TS) of 23, 1147 s |

## Amendments

**A1, 2026-11-26, after run 2.** The reference's working precision is raised from 90 to 200 digits (`mp.mp.dps`), so the
k = 4 determinant keeps more than 120 digits after its cancellation. No criterion, bar, lane, plan or point changes. Run
3 is the run with the corrected reference; the mutations are run with it.
