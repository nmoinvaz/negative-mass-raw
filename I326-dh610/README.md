# I326-dh610: G at D = 6, B = 0.2 and 0.15, p*ₕ to 1e-12 and the pair p*ₕ ∓ 1e-10 on a triangle that reaches t = 70

Machine dh610-fedora (Fedora, i7-12700, 20 threads shared with choptuik-large-d's runners, 62 GB), Python `~/Source/negative-mass-venv314/bin/python` (numba 0.68.1, numpy 2.5.4, scipy 1.18.1), one thread per
process, `nice -n 10` (`-p Nice=10`), at most 4 processes, every run a transient systemd user unit `nm-i326-*` writing log, err, time and rc here (`scripts/run1.sh`). Memory is reported, never a stop condition.
Issue https://github.com/nmoinvaz/negative-mass/issues/326 ("Bisect G at D = 6, B = 0.2 to 1e-12 with a longer triangle"), with the coordinator's comment that adds B = 0.15. Worktree `~/Source/negative-mass-i326`,
branch `wip/i326-b02-long` (from `wip/i325-drift-b6`, #325's, on #228's). Status words as in AGENTS.md: every number is *numerical evidence*. No sentence says a result is new.

Code, unchanged and read-only: `threshold.py`, `dn.py`, `checks.py`, `throat_locus.py`, `throat_drift.py`, `g_d6.py`, `drift_b6.py` (sha256 as in I325-dh610's README: 8abeaacaeeb4a9da…, a3902d27fa294d71…, 3ded2bc07f28cd98…,
db40c30c3a981df4…, 1d77958df7f48a94…, 91402f3924cb4604…; `drift_b6.py` cc79395657bac1df…). The new file is `notes/wormhole_evolution/drift_b6_long.py` (the driver and, later, the analysis).

This README is written in parts. **Part 1** (this one) is written at the start, after the code was read and before the pilot finished. **Part 2** (the mutations with their computed effects, and anything the pilot changes) is appended, dated, before the
pairs of record; the pairs wait inside their run for the file `PART2_DECLARED`. Nothing declared here is changed after the first run of record without a ruling over hc.

## The question

#228 stopped its bisection of G at D = 6, B = 0.2, h = 0.0025 at its 2 h limit after 36 runs (bracket 6.97e-12 against 1e-12; the 38 points are in `I228-dh610/runs/bisect/D6_B0.2_h0.0025/points.jsonl`, T up to 57.9), and its pair at p*ₕ ∓ 1e-10
(p* from the stopped points) failed JOB6: the + side's event of #40 lies beyond the triangle t ≤ 34 (fates (−1, 0)). #325 found the same at B = 0.15 (fates (−1, 0)); its bisection at B = 0.15 finished (40 runs, 3848 s, hi − lo = 9.8e-13, T up to 49.8).
This task finishes B = 0.2's bisection and runs the pair of both B on a triangle to t = 70.

## Inputs (nothing here changes a constant of #228's `C6` or #255's `CRIT`)

| quantity | value |
|---|---|
| family, D | G of #40, D = 6 (n = 4), a = 1, 8πG = 1, pulses centre 3, width 0.5 on the ray x⁻ = 0; ghost pulse A = p*ₕ(B, h) ∓ δ, normal pulse B |
| B, h | B = 0.2 and 0.15, h = 0.0025 (hk = 1); h = 0.00125 only if its cost fits the limits (below) |
| bisection | `throat_drift.job_bisect` from the declared bracket (0.3, 3) × (B/0.1)² p*ₕ(0.1, h) to hi − lo ≤ 1e-12; p*ₕ(0.1, h) from #40's merged record `I228-dh610/runs40` (read only) |
| pair | `throat_drift.job_stall`: A = p*ₕ ∓ 1e-10 kept whole, with `throat_locus.TCAP` = X = 70 (the triangle reaches t = 70, the profile slices are t = 2, 3, … 67) |
| local ṙ | dr_th/dτ by a linear fit over ±0.5 in τ at t = 8, 10, 12 (`g_d6.rdot_at`, #228's), on the pair's mean |

## How the triangle is chosen (the X of each run is logged as `X = …`)

The fate of an amplitude, and the cell and time of #40's event, do not depend on the triangle if the event lies inside it. A run that finds no event in its triangle (fate 0) costs the whole triangle and is repeated at 1.4 times the reach. The cost of a run
that finds its event at row j in a triangle of size s_max is s_max·j − j²/2 cells (about 1.7 µs per cell on this machine under its load): an oversized triangle is paid for, so X is set per run.

- **Bisection of B = 0.2.** `drift_b6_long.py bisect --resume=<#228's points.jsonl>`: the same `job_bisect` from the same declared bracket; an amplitude that #228's 38 stored points already ran is returned from them (marked `memo`, not run), and the new amplitudes are run
  with X = 2.5 ln(2/(hi − lo)) + 6 (63 … 72 over the last three halvings), never below the job's own cap, repeated at 1.4 X on fate 0. #228's cost for the 36 runs (6748 s from its log) is added to the new cost for BIS. A fresh bisection from the declared bracket would repeat
  the stored path (the same amplitudes in the same order); the checks RP below test that it does.
- **Bisection of B = 0.15.** Done by #325 (`I325-dh610/runs/bisect/D6_B0.15_h0.0025/summary.json`: 40 runs, 3848 s, hi − lo = 9.8e-13, not stopped; read only): its p*ₕ = 0.03412239114915812 is the one of the pair, and RP re-runs its two ends.
- **Pairs.** X = 70 for both sides (the pilot below gives T of the + side at δ = 1e-10 at B = 0.2).

## Limits

- 3 h for each bisection at h = 0.0025 (BIS), 2 h for any other single run (`timeout 7200`); stopped and reported with the bracket, and the issue left open.
- A bisection at h = 0.00125 is a single run over 2 h (B = 0.15 at h = 0.0025 took 3848 s; at h = 0.00125 about 3.3 times that): not run; its cost is reported from one run at h = 0.00125 (HC below).
- Only my own units are stopped, by unit name (`systemctl --user stop nm-i326-…`). Nothing of choptuik-large-d's is touched. Logs are never overwritten; a rerun is a new directory (`*.partialN` for the dead one).
- A dependency (a pair on its bisection or on README part 2) is waited for inside the run (`WAITFOR=`), not by a queue line.

## Criteria (each can fail; written before any run of record; the numbers of record are in `runs/` and the analysis is `drift_b6_long.py analyze`)

| id | what | pass if |
|---|---|---|
| BIS[B] | the bisection of record finished | hi − lo ≤ 1e-12, `stopped` and `error` empty, total cost (B = 0.2: #228's 6748 s + this task's wall; B = 0.15: #325's 3848 s) ≤ 10800 s |
| RP[B] | control: `fate` runs of stored points at X = T_stored + 2 (B = 0.2: the two ends of #228's final bracket and the points at 5.9e-11 and 2.4e-11 from p*; B = 0.15: the two ends of its final bracket) reproduce fate, T and cell | bit for bit |
| JOB6L[B] | the pair at p*ₕ ∓ 1e-10, X = 70 (JOB6 of #228 on the longer triangle) | fates (−1, +1) of #40's events, and both events inside the triangle (T < X) |
| RDOT[B] | ṙ(8), ṙ(10), ṙ(12) of the new pair against the stored ones (#228's pair at B = 0.2 from its stopped p*, #325's at B = 0.15) | within 1e-6 |
| NO6L[B] | the pair's mean is the tuned member: max \|odd\| over t ∈ [6.5, 12] | ≤ 3e-4 (#228's NO6) |
| HC | the local ṙ at t = 8, 10, 12 at h = 0.00125 against h = 0.0025 for one B | within 1e-4; **not run unless a bisection at h = 0.00125 fits the limits**; otherwise the cost of one run at h = 0.00125 is reported |

A check that fails is a result; no criterion, bar or tolerance is moved after the data are seen.

## Mutations (`drift_b6_long.py analyze --mutate=NAME`; the effect of each is computed on a development run and recorded in part 2 before the pairs of record)

`bis_tol` (tolerance 1e-14 for BIS), `rp_shift` (RP compares each control with the neighbouring stored point), `fate_swap` (the two fates exchanged, JOB6L), `rdot_off` (the new ṙ shifted by 2e-6, RDOT), `odd_scale` (|odd| × 1e4, NO6L).

## Pilot

B = 0.2, h = 0.0025, A = p* + 1e-10 with p* = 0.07681202535369897 (#228's stopped midpoint), X = 70: one fate run (`runs/pilot_B0.2_hk1_plus1e-10`). It sizes the pair and prices the triangle; it is not a criterion.

# Part 2: the mutations and their computed effects (2026-11-28 08:22, dh610 clock; before any pair of record)

The pilot (08:17), the continuation of B = 0.2's bisection (08:19) and the controls RP (08:20) started before this part was written; none of them depends on a mutation, and the criteria they are judged by are those of part 1. The pairs wait inside
their run for the file `PART2_DECLARED`, written when this part is committed.

**The development case** (`drift_b6_long.py analyze --dev`; logs `dev/dev_baseline.log`, `dev/dev_mut_<name>.log`): #228's pair at B = 0.1, h = 0.0025 (fates (−1, +1), the X = 34 triangle) stands for the pair of record and for the stored pair, #325's bisection at B = 0.15 for the
bisection, and its two end points for the controls. The five checks pass on it, so each mutation shows whether it can make its check fail. The baseline: BIS hi − lo 9.8e-13, RP 2 of 2 equal, JOB6L fates (−1, +1) with T = 18.4, 25.2 < X = 34, RDOT differences 0 (the same pair twice), NO6L max |odd| 6.98e-5.

| mutation | what it does | verdicts changed against the baseline on the development case | declared |
|---|---|---|---|
| `bis_tol` | BIS's tolerance 1e-12 → 1e-14 | BIS (hi − lo 9.8e-13 > 1e-14) | BIS |
| `rp_shift` | each control compared with the neighbouring stored point | RP (0 of 2 equal) | RP |
| `fate_swap` | the pair's two fates exchanged | JOB6L (fates (+1, −1)) | JOB6L |
| `rdot_off` | the new ṙ shifted by 2e-6 | RDOT (+2.0e-6 at t = 8, 10, 12 against the bar 1e-6) | RDOT |
| `odd_scale` | |odd| × 1e4 | NO6L (max |odd| 6.98e-1 against 3e-4) | NO6L |

Each fires exactly its declared check and no other. The development case does not test RDOT's agreement itself (the pairs are the same), only that the check can fail; the real RDOT compares two different runs. The mutations are re-run on the frozen record at the end
(`runs/mut/`).

## What the pilot and the first bisection runs settle (not criteria)

(filled in below as the runs finish)
