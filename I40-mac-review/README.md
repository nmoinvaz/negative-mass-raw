# I40-mac-review: the coordinator's review of #40 (rerun, independent check ind40)

Machine: macOS (the coordinator's Mac, Apple M5, arm64), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`: numpy
2.5.4, scipy 1.18.1, numba 0.68.1), nice 10, at most 2 processes. Issue: https://github.com/nmoinvaz/negative-mass/issues/40
(and #150). Under review: branch `wip/i40-ellis-threshold` at 2e97643 (`threshold.py` 13a1301), raw `I40-dh610` at 99423f6.
Written 2026-11-27 before the first run of `ind40.py` and before the rerun.

## Rerun

`rerun.sh`, from a detached worktree `~/Source/negative-mass-r40` at 2e97643, in `notes/wormhole_evolution`, two lanes:
- `threshold.py job` with the runner's flags (`--cons --stall`, and `--ed` at the middle h) for 13 of the 26 jobs: D = 4 S, O
  and G at all three h; D = 5 S at h = 0.00707107 and 0.00353553; D = 6 S at h = 0.005 and 0.0025. Output in `rerun/<job>/`.
- `threshold.py analyze --raw=<the runner's runs>`, the analysis of record over the runner's own 26 jobs.
- `threshold.py analyze --raw=rerun --only=4S,4O,4G`, the analysis of the rerun D = 4 jobs.

The expectation, written now:
- the analysis of record prints the same lines as `threshold_output.txt`, apart from the header, paths and timings;
- in each rerun job, p*_h = (lo + hi)/2 equals the runner's within 1e-11, and every series point with e ≤ 9 has the
  runner's fate and event cell (j, i). numba's floating point on arm64 and x86 may differ in the last digits, which can
  move points below the roundoff floor (|p − p*_h| ≈ 1e-11);
- the rerun D = 4 analysis gives the runner's verdicts for those 9 jobs.

## ind40

ind40 shares none of the machinery under test. Shared: the field equations (derived again by the coordinator's own
brute-force Ricci tensor in ind39), the family S as `threshold.py` defines it, and W from #195's crate.
- **Data.** The S member with amplitude p: the static Ellis wormhole (a = 1, ghost φ, q = √(n(n−1))) plus the ghost pulse
  p(g − g(0)), g = exp(−((s − 3)/0.5)²), on the ray x⁻ = 0, mirrored onto x⁺ = 0 with odd parity. Gauge f = 0 on both
  rays, and the corner is the throat (r = 1, r_s = 0). On the ray the coordinator's own code integrates the background
  (r_ss = (n−1)/(2r^{2n−1}), φ_s = q/(√2 rⁿ)) together with the constraint r_ss = (φ_s²/n) r (scipy DOP853, rtol 1e-13).
- **Evolution.** The coordinator's own second-order diamond scheme in numba: Z_N = Z_E + Z_W − Z_S + h² F(centre), the
  centre values the four-corner average, derivatives the two-edge differences, three corrector passes. By the symmetry of S
  (r and f even, φ odd under x⁺ ↔ x⁻) only the half x⁺ ≥ x⁻ is marched, row by row in x⁻; the diagonal x⁺ = x⁻ is the
  throat. A cell with r < 0.05, e^{−f} > 1e8 or a non-finite value ends its row there.
- **Events, on the diagonal only.** Collapse: r_d first falls to 0.5; expansion: r_d first reaches 2. T = t =
  (x⁺ + x⁻)/√2 at the crossing, interpolated linearly between diagonal nodes. The proper time τ = ∫e^{−f/2}dt along the
  diagonal is reported beside it. These events differ from #40's (the first trapped row, or an anti-trapped diagonal cell
  with r ≥ 2).
- **Bisection and series.** Bracket [−0.01, 0.01], bisected until hi − lo ≤ 1e-14. Series p = p*_h ∓ 10^{−e}, e = 4, 4.5,
  …, 10 (13 per side). Primary fit window |p − p*_h| ∈ [1e-9, 1e-4], 11 points per side: T = c_side + s ln(1/|p − p*_h|),
  one intercept per side and a common slope, by the closed-form within-side normal equations (no lstsq). Points at
  e = 9.5 and 10 are recorded, not fitted. Slopes over [1e-9, 1e-5] and per side are reported.
- **Grids** as #40's S: D = 4, h = 0.02, 0.01, 0.005, X = 28; D = 5, h = 0.01/√2, 0.005/√2, 0.0025/√2, X = 18; D = 6,
  h = 0.005, 0.0025, 0.00125, X = 15. 1/W from #195's crate: W²a² = 1.39705243433350684, 2.98495893035176025,
  4.68662054311946479.

## Criteria (each coded as worded; each can fail)

"rel" means |a/b − 1|.

| id | criterion |
|---|---|
| K0 | Planted: an oracle with fate sign(p − p₀) and T = c_side + s₀ ln(1/|p − p₀|), p₀ = 3.7e-6, s₀ = 0.8, c = (1.0, 3.0), no noise, through ind40's own bisection, series and fit, gives p₀ to 1e-13 and s₀ to rel 1e-9 |
| K1 | Refit of record: for each of the runner's 26 jobs, ind40's fit of its `points.jsonl` (phase `series`, fate equal to the side, \|p − p*_h\| ∈ [1e-11, 1e-3], p*_h = (lo + hi)/2 from `summary.json`) gives the primary slope that `threshold_output.txt` prints, to its 6 printed decimals (difference ≤ 1e-6) |
| K2 | Independent evolution: at each D, the slope at each of the two finest h is within rel 1% of 1/W, and the two agree within rel 0.5% (#39's and #40's bars). Every fitted point ends in an event on its own side |
| K3 | The sharper bar #40 reports for D = 4 and 5: at the finest h, ind40's slope is within rel 2e-3 of 1/W |
| K4 | Cross-code: at each D, ind40's slope at the finest h and #40's S slope at its finest h, both fitted by ind40 over [1e-9, 1e-4], agree within rel 3e-3 (the event definitions differ) |

Reported, not gated: p*_h at three h and its order; the slope in τ; the slopes over [1e-9, 1e-5] and per side; the
D = 6 slope against 1/W; the floor points.

## Mutations (`--mutate=NAME`; each must make ind40 exit non-zero with exactly these criteria failing)

The targets are predicted from the code, not yet computed. A mutation that misses its targets is reported. The two
evolution mutations run at D = 4 only, with `--only=K2,K3,K4 --D=4`.

| mutation | change | targets |
|---|---|---|
| `oracle-slope` | K0 compares with 0.81 in place of s₀ | K0 |
| `fit-pstar` | K1's p*_h shifted by 1e-9 | K1 |
| `time-unit` | ind40's T divided by √2 (x⁻ units) | K2, K3, K4 |
| `sphere-coef` | the sphere term (n − 1) → n in ind40's r₊₋ | K2, K3, K4 |

## Amendments

**A1, 2026-11-27, after the rerun.** `rerun.sh` passed h for the two D = 5 jobs as 0.00707107 and 0.00353553, rounded
to 6 figures, where the runner passed 0.0070710678118654745 and 0.0035355339059327372 (its `job.log`). Their p*_h then
differ from the runner's by +1.8e-10 and −1.6e-10, which is p*_h ∝ h² at the rounded h (+6.2e-7 and −2.2e-6 relative).
The error is the review's, and those logs are kept as `rerun_1/D5_*`. `rerun_2_d5.sh` reruns the two jobs with the
runner's strings. A first attempt passed repr(0.01/√2), one ulp from the runner's double, and was stopped and kept as
`rerun_2_stopped_1ulp/`.

## Runs (filled in as they are done)

| file | what |
|---|---|
| `rerun.sh`, `rerun_1/` | the 13 jobs, all rc 0, 1 to 4 min each |
| `rerun_analyze_record.log` | the analysis of record over the runner's 26 jobs: **100 of 111, the same 11 failures**, every line equal to `threshold_output.txt` except one printed relative difference (1.52e-12 against 1.51e-12, a difference of two equal slopes) and the timing |
| `compare_rerun.py`, `rerun_compare.txt` | rerun 1 against the runner: the 11 D = 4 and D = 6 jobs meet the expectation (p*_h within 7.3e-14 at D = 4 and 2.9e-12 at D = 6; every point with e ≤ 9 has the runner's fate and cell). The two D = 5 jobs do not (A1) |
| `rerun_2_d5.sh`, `rerun_2/`, `rerun_2_compare.txt` | rerun 2 of the D = 5 jobs: p*_h within 1.1e-12 and 1.1e-13, every point with e ≤ 9 equal. **The expectation is met by all 13 jobs.** Points with e ≥ 9.5 to 10 differ between the machines in 10 of the 13 jobs |
| `rerun_analyze_rerun.log` | the analysis of rerun 1 (`--only=4S,4O,4G,5S,6S`): the D = 4 verdicts equal the runner's. Slopes move by up to 1.4e-4 (D = 4 S, h = 0.005: 0.846642 against 0.846522), from the points below 1e-10 that differ between machines. The D = 5 jobs are reported missing, because their rounded h does not match the declared h (A1) |
| `ind40_run1.txt`, `ind40_run1_points/` | run 1: **exit 0, 5 of 5.** K0: p₀ to 2.0e-15, s₀ to 8.8e-14. K1: the 26 printed slopes reproduced to 5.0e-7. K2: slope against 1/W at the three h: D = 4 −3.3e-5, −6.9e-6, −2.6e-6; D = 5 −4.9e-4, −1.35e-4, −2.5e-5; D = 6 −6.3e-3, −1.56e-3, −4.7e-4, falling by about 4 per halving at D = 5 and 6. K3: D = 4 −2.6e-6, D = 5 −2.5e-5. K4: against #40's points over the same window: +3.7e-6, +4.3e-6, −1.4e-4. #40's own D = 6 S points at h = 0.00125 give 0.461770 (−3.3e-4) over [1e-9, 1e-4], against 0.459628 (−5.0e-3) over its primary [1e-11, 1e-3]. p*_h has order 2.000, 2.001, 2.007 and lies within 2e-4 relative of #40's. The slope in τ agrees with the slope in t to 1e-5 |
| `ind40_run1_mut_*.txt` | `oracle-slope` fails exactly K0, `fit-pstar` exactly K1, `time-unit` exactly K2, K3, K4 (slope 0.598243 = 1/(√2W) to 4e-6). **`sphere-coef` does not fire cleanly**: with n in place of n − 1 the bracket [−0.01, 0.01] no longer straddles (p = 0.01 collapses), and ind40 stops with an exception before any criterion is evaluated, as #40's six JOB mutations do |
