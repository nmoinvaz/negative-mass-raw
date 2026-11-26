# I187-mac-review: the coordinator's review of #187 (rerun, independent check ind187)

The runner's raw folder for #187 is `I187-mac` (it ran on this Mac), so the review uses this folder name.

Machine: macOS (the coordinator's Mac, Apple M5, arm64), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`: numpy,
scipy 1.18.1), Rust 1.94.0, nice 10, at most 2 processes. Issue: https://github.com/nmoinvaz/negative-mass/issues/187.
Under review: branch `wip/i187-taylor-rows` at 2a84083, raw `I187-mac` at 89bc112. Written 2026-11-26 before the first
run of `ind187.py`.

## Rerun

`rerun.sh A` and `rerun.sh B` from a detached worktree `~/Source/negative-mass-r187` at 2a84083, the crate built there
(`cargo build --release -j 2`), with a fresh `--jsonl-dir` (this folder's `jsonl/`), so no line is read back from the
runner's cache. Lane A: run_02 (l = 2), run_04 (l = 4), run_05 (l = 5 with CAP5, CAP5s), then run_03 (l = 3 rows, no
check). Lane B: run_06 (l = 6 with CAP6), then run_18 (the default mode). Each is compared with the runner's log of the
same run.

## ind187.py: the stored rows by rounding, l = 3 out of sample, CAP5c recomputed

The runner compared tokens as strings, formatting the crate's values in `convergence.py`'s format. ind187 does not
format: it parses each stored token as a decimal, and asks whether the crate's full-precision value (the dd string of
the rerun's jsonl) lies within half a unit of the token's last printed digit. It computes the spread and the signs from
the crate's variants itself.

Shared with the object under test: the crate's values (the rerun's jsonl) are the object; the stored files
`convergence_l{2,4,5,6}_output.txt`, scipy's `polar_solver.PolarProblem` with `background.solve_star(0.7603, -1)`, and
#114's `I114-win/convergence_l5_w0.7603.partial.csv` are the references. New in ind187: the parsing, the rounding test,
the spread and signs, the choice of the l = 3 points, and the recomputation of CAP5c.

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| K1 | For every row of `convergence_l{2,4,5,6}_output.txt`: the crate's base D (`D_base`, `%.6e`), φ_cut D (`D(r_m~34)`, `%.3e`), base q_int and q_ext (`%.6e`), and the spread (`%.1e`, computed by ind187 as (max − min)/\|mean\| over the variants whose name has no `phi_cut`, and over `background R=90` and `r0 = 3e-3` alone in the two capped rows, whose note says "over 4 variants") each lie within half a unit of the stored token's last digit, times (1 + 1e-9); the token `signs` is `[np.float64(-1.0)]` and every crate D of the row's variants is negative; each header r_m (`%.2f`) holds the crate's r_m of that variant within 0.005 |
| K2 | Out of sample, l = 3 (no stored file, and no scipy comparison by the runner or by ind186): at γ = 0.3 and 40, the crate's base D and φ_cut D, and its base q_int and q_ext, against scipy's (`PolarProblem(st, 3)` and `PolarProblem(st, 3, phi_cut=1e-12)`, q as `convergence.py`'s `task('q')`) within 1e-7 relative, signs equal |
| K3 | CAP5c recomputed: at (l, γ) = (5, 6000), \|D_crate/D_scipy − 1\| for base, rtol (the crate's tol variant against #114's `rtol 1e-12`), φ_cut, R = 90 and r0, from the rerun's jsonl and #114's csv, rounded to two significant digits, equal the closing comment's 5.4e-9, 3.1e-9, 4.7e-8, 8.0e-10, 4.2e-9; and the largest exceeds 1e-8 (CAP5c not met, as reported) |

## Mutations (`--mutate=NAME`; each must make ind187 exit non-zero with exactly these criteria failing)

| mutation | change | targets |
|---|---|---|
| `k1-ulp` | each crate base D is moved by one unit of the stored token's last digit before K1's test | K1 |
| `k2-l` | scipy is evaluated at l = 4 in place of 3 | K2 |
| `k3-pair` | K3 pairs the crate's φ_cut D with scipy's base D | K3 |

## Runs (filled in as they are done)

| file | what |
|---|---|
| `rerun_*.log`, `.err`, `.rc`, `compare_rerun.py`, `compare_rerun_1.txt` | the six reruns (run_02 to run_06, run_18), load 2.7 to 5.1: **each identical to the runner's log line for line once timings and load are removed, with the same exit code** (run_05 exits 1 on CAP5c and CAP5s, as the runner's did). The default mode: 22 passed, 0 failed, 1 skipped (TS) of 23, 854 s |
| `ind187.py`, `ind187_run1.txt` | run 1: exit 0, 3 of 3. **K1**: 41 rows, 266 tokens, every one within half a unit of its last digit. The closest is `D(r_m~34)` at l = 4, γ = 1, at 0.994 of half a unit (3e-8 absolute from the boundary, against crate–scipy agreement near 1e-14 at γ ≤ 10). **K2** (l = 3, first comparison with scipy): γ = 0.3, D 1.6e-13, D34 2.5e-14, q_int 8.6e-14, q_ext 1.2e-14; γ = 40, D 6.6e-12, D34 2.5e-11, q_int 1.0e-11, q_ext about 3e-11. **K3**: base 5.44e-9, tol 3.11e-9, φ_cut 4.70e-8, R = 90 7.98e-10, r0 4.16e-9, each the reported value at two digits; CAP5c not met, as reported |
| `ind187_run1_mut_*.txt` | `k1-ulp` fails exactly K1, `k2-l` exactly K2, `k3-pair` exactly K3 |
