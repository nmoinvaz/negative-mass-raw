# I41-mac-review: the coordinator's review of #41 (rerun, independent check ind41)

Machine: macOS (the coordinator's Mac), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`: numpy 2.5.4, scipy 1.18.1,
numba 0.68.1), nice 10, at most 2 processes. Issue: https://github.com/nmoinvaz/negative-mass/issues/41. Under review: branch
`wip/i41-threshold-masses` at dd4cad9, raw `I41-rpi5` at 9d6082b. Written 2026-11-27 before the first run of `ind41.py` and
before the rerun.

## Rerun

From a detached worktree at dd4cad9, in `notes/wormhole_evolution`: `settled_mass.py analyze` over the runner's stored jobs,
and one job of record (δ = 1e-6, h = 0.01). The expectation: 13 of 13 checks, the output's lines again apart from paths and
timings, and the job's M_AH(x⁺) equal to the runner's to 1e-9.

## ind41: the apparent horizon of family S by the coordinator's own code

The half-domain double-null march of the reviews of #40 and #213 (`threshold_check.py`'s scheme), with no event stop. On
each row x⁻ = const it records the right apparent horizon, the first r₊ = 0 crossing to the right of a trapped cell, with
r and f interpolated linearly to it; M_AH = r_AH/2. It shares no code with `dn.py` or `settled_mass.py`.
- Family S at D = 4 (#40), on the collapse side at p*ₕ − 1e-6, with ind41's own p*ₕ (X = 28, bisection to 1e-14).
- A uniform grid, h = 0.005 and 0.0025, X = 12, with no zoom. It therefore reads the horizon only while its x⁻ moves by many
  cells: up to e^{−f} ≈ 12, x⁺ − x⁺_f ≈ 3. The settled value (x⁺ − x⁺_f ≥ 7) is not reached.
- Comparison is at fixed e^{−f} on the horizon. The gauge is the same (f = 0 on both rays, the same data), so the
  formation times of the two codes need no alignment.

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| K1 | At e^{−f} = 1.335, 1.936, 4.074, 11.96 on the horizon (the runner's rows x⁺ − x⁺_f = 1.5, 2.0, 2.5, 3.0 at δ = 1e-6, h = 0.0025), ind41's M_AH equals the runner's 0.43732, 0.37800, 0.30314, 0.24998 within 1e-3 at h = 0.0025, and h = 0.005 agrees with h = 0.0025 within 1e-3 |
| K2 | At e^{−f} = 11.96, the horizon's x⁻ equals the runner's 9.39779 within 5e-3 |

Reported, not gated: M_AH at e^{−f} = 36.23 (runner 0.22930) if the horizon spans at least two rows there.

## Mutations

| mutation | change | targets |
|---|---|---|
| `M-factor` | M = r_AH in place of r_AH/2 | K1 |
| `side` | p*ₕ + 1e-6 (the expansion side: no trapped cell) | K1, K2 |

## Amendments

**A1, 2026-11-27, after run 1.**
- **K1 is not met as worded.** Against the runner, h = 0.0025 is within 5.7e-5, 2.8e-5, 1.4e-5 and 2.8e-4 at the four
  points. But at e^{−f} = 11.96, h = 0.005 differs from h = 0.0025 by 2.1e-3 (bar 1e-3): the uniform grid at h = 0.005
  no longer resolves the horizon there, as the README foresaw for e^{−f} ≈ 12.
- **K1b** adds the same bars for the pair h = 0.0025 and 0.00125, with h = 0.00125 compared with the runner. K1 stays
  NOT MET.

## Runs (filled in as they are done)

| file | what |
|---|---|
| `rerun.sh`, `rerun_analyze.log`, `rerun_analyze_diff.txt` | `analyze` over the runner's stored runs: **13 checks, 0 failed**, every line of `settled_mass_output.txt`'s analyze section again apart from the timing |
| `rerun_job/`, `rerun_job_compare.txt` | the job h = 0.01, δ = 1e-6 again, with the runner's p*ₕ files. M_AH(x⁺) agrees to 8e-10 at a quarter of the run, 4.6e-9 at half and 3.7e-7 at three quarters. At the end, deep in the zoom (e^{−f} ≈ 1.5e6), it agrees to 1.6e-5 (0.223109 against 0.223125). **The expectation of 1e-9 is not met past mid-run.** The same code on another machine reproduces the settled value to about 2e-5, larger than the finest-h difference the note quotes (2.4e-6) |
| `ind41_run1.txt` | run 1: **K1 not met as worded** (A1). Against the runner at h = 0.0025: −5.7e-5, −2.8e-5, +1.4e-5, +2.8e-4; h = 0.005 differs from 0.0025 by 2.1e-3 at e^{−f} = 11.96. K2 passes: x⁻ 9.39768 against 9.39779 |
| `ind41_run2_K1b.txt` | run 2 (A1): **exit 0, K1b and K2 pass.** h = 0.00125 against the runner: −5.7e-5, −2.8e-5, +9.2e-6, +1.2e-4; h = 0.00125 against 0.0025 within 1.6e-4 at all four points; x⁻ 9.39775 (−4.2e-5). The settled value (e^{−f} ≥ 1e5) is beyond a uniform grid, as foreseen |
| `ind41_run2_mut_*.txt` | `M-factor` fails exactly K1; `side` (the expansion side, no trapped cell) fails exactly K1 and K2 |
