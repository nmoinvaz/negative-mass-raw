# I213-mac-review: the coordinator's review of #213 (rerun, independent check ind213)

Machine: macOS (the coordinator's Mac, Apple M5), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`: numpy 2.5.4,
scipy 1.18.1, numba 0.68.1), nice 10, at most 2 processes. Issue: https://github.com/nmoinvaz/negative-mass/issues/213.
Under review: branch `wip/i213-expanding-branch` at 94d89f7, raw `I213-dh610` at 6cba01a. Written 2026-11-27 before the first
run of `ind213.py` and before the rerun.

## Rerun

From a detached worktree `~/Source/negative-mass-r213` at 94d89f7, in `notes/wormhole_evolution`:
- `expansion.py analyze --raw=<I213-dh610>` over the runner's stored runs;
- one job of record again, D = 4, member tuned, h = 0.02, X = 200, into `rerun/`, compared with the runner's npz.

The expectation, written now: the analysis prints the lines of `expansion_output.txt` again (12 of 13 checks, CT failing)
apart from paths and timings; the rerun job's diagonal series equals the runner's to 1e-12 relative where p*_h agrees, and
its k, τ_s and H/W at r/a = 10, 25, 50 equal the printed values to their digits.

## ind213: the symmetric expanding branch by the coordinator's own code

The coordinator's double-null code of the review of #40 (`notes/wormhole_evolution/threshold_check.py` on main), copied and
extended: no event stop, and the diagonal series r, f and φ₊ recorded. It shares no code with `dn.py` or `expansion.py`.
Shared: the field equations and the family S of #40 (pulse centre 3, width 0.5), and the definitions below, taken from
#213's README.
- On the throat x⁺ = x⁻: τ = ∫e^{−f/2}dt, H = (dr/dτ)/r with dr/dt = √2 r₊, |ρ| = e^f φ₊² (the ghost's energy density for the
  purely radial gradient that the symmetry forces), r₊ and φ₊ from centred differences across the diagonal.
- "tuned" is A = p*_h + 1e-6 with ind213's own p*_h (bisection as in the review of #40); the other members are A = 0.01, 0.05, 0.2.
- The last e-fold of r: the diagonal points with r ≥ r_end/e. k = −1/(slope of 1/H against τ there), τ_s its zero.

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| K1 | D = 4, X = 200, members tuned, 0.01, 0.05, 0.2, at h = 0.02 and 0.01: k is within 1e-3 of 2, and \|ρ\|/H² at the last diagonal point is within 1e-3 of 4 |
| K2 | D = 4, tuned, at both h: H/W at the first diagonal point with r/a ≥ 10, 25, 50 is within 3e-3 relative of the runner's value at the same h in `expansion_output.txt` (1.231, 1.946, 2.752 at h = 0.02; 1.230, 1.946, 2.752 at h = 0.01) |
| K3 | D = 4, each member, at both h: τ_s is within 2e-3 relative of the runner's τ_s from the last e-fold at the same h (h = 0.02: tuned 17.89018, 0.01 10.05900, 0.05 8.43404, 0.2 6.16920; h = 0.01: 17.89022, 10.05589, 8.43337, 6.16898) |

Reported, not gated: D = 5 (h = 0.01/√2, X = 100, tuned and 0.05): k, \|ρ\|/H², τ_s; the exponent of r against τ_s − τ.

## Mutations (`--mutate=NAME`; each must make ind213 exit non-zero with exactly these criteria failing)

The targets are predicted from the code, not yet computed. A mutation that misses its targets is reported.

| mutation | change | targets |
|---|---|---|
| `coord-time` | τ replaced by t (no lapse) | K1, K2, K3 |
| `rho-factor` | \|ρ\| doubled | K1 |
| `tuned-offset` | tuned is p*_h + 1e-3 | K2, K3 |

## Amendments

## Runs (filled in as they are done)

| file | what |
|---|---|
