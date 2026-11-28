# I325-dh610: G at D = 6, the throat drift speed against B = 0.01 … 0.15 (the D = 6 half of #273)

Machine dh610-fedora (Fedora, i7-12700, 20 threads shared with choptuik-large-d's runners, 62 GB), Python `~/Source/negative-mass-venv314/bin/python` (numba 0.68.1, numpy 2.5.4, scipy 1.18.1), one thread per
process, `nice -n 10`, at most 4 processes, every run a transient systemd user unit `nm-i325-*` writing log, err, time and rc here (`scripts/run1.sh`). Memory is reported, never a stop condition.
Issue https://github.com/nmoinvaz/negative-mass/issues/325 ("Measure how the D = 6 throat drift speed scales with B from 0.01 to 0.15"). Worktree `~/Source/negative-mass-i325`, branch
`wip/i325-drift-b6`, from `wip/i228-g-d6-third` (dee6425), #228's branch. Code, all unchanged and read-only here: `threshold.py`, `dn.py`, `checks.py`, `throat_locus.py`, `throat_drift.py`, `g_d6.py`,
`ellis_spectrum.py`; the new file is `notes/wormhole_evolution/drift_b6.py` (the analysis; it imports the others). Status words as in AGENTS.md: every number is *numerical evidence*. No sentence says a result is new.

sha256 of the unchanged code: threshold.py 8abeaacaeeb4a9da…, dn.py a3902d27fa294d71…, checks.py 3ded2bc07f28cd98…, throat_locus.py db40c30c3a981df4…, throat_drift.py 1d77958df7f48a94…,
g_d6.py 91402f3924cb4604…, ellis_spectrum.py e1275c0a1f5a7ad7….

This README is written in parts. **Part 1** (this one) is written before the pilot. **Part 2** (the criteria, the planted and null controls, the #272 prediction, the mutations with their computed effects) is
appended, dated, after the pilot and the development runs and before any run of record other than the pilot's; nothing declared in it is changed after the first run of record without a ruling over hc.

## The question

#228 measured the D = 6 throat drift of G (ghost pulse A tuned to p*ₕ plus a normal pulse B on the same ray) at B = 0.02, 0.04, 0.07, 0.1, 0.2. Its local exponent of ṙ against B falls with B: 2.6 (0.02 to 0.04),
2.7 (0.04 to 0.07), 2.2 (0.07 to 0.1), 1.1 (0.1 to 0.2), against |B|³ at D = 5 (#255); its fit ṙ(τ) = ṙ∞ + c e^{−κτ} does not converge for B ≥ 0.1 (κ → 0). This task adds B = 0.01, 0.014, 0.03, 0.15 at h = 0.0025
and two of them at h = 0.00125, so that the exponent over nine B has a window part and a resolution part, and tests #272's linear response against ṙ∞ at B = 0.02.

## Inputs, as #228's runner declared them (`C6` in `g_d6.py`; nothing here changes a constant of it)

| quantity | value |
|---|---|
| family, D | G of #40, D = 6 (n = 4), a = 1, 8πG = 1, pulses centre 3, width 0.5 on the ray x⁻ = 0; ghost pulse A = p*ₕ(B, h) ∓ δ, normal pulse B |
| h | hk = 1: 0.0025 for all B; hk = 2: 0.00125 for 0.03 and one other B (chosen after the pilot's timing, declared in part 2) |
| bisection | `g_d6.py drift bisect`: p*ₕ(B, h) to hi − lo ≤ 1e-12 by `throat_drift.job_bisect` from the bracket (0.3, 3) × (B/0.1)² p*ₕ(0.1, h), #228's; p*ₕ(0.1, h) from #40's merged record `I228-dh610/runs40` (read only) |
| pair | `g_d6.py drift stall`: A = p*ₕ ∓ 1e-10 (δ = 1e-10, #228's) kept whole; the pair's mean is the tuned member |
| local ṙ | dr_th/dτ by a linear fit over ±0.5 in τ (±0.25 and ±1 give the window part) at t = 8, 10, 12 (`g_d6.rdot_at`, the same as #228's) |
| fit | `throat_drift.fit_rdot` unchanged, masked at |odd| > 3e-4, read only where κ ≥ 0.05 and SE(ṙ∞) ≤ 10 % of |ṙ∞| (#228's `fit_ok`) |
| linear window | |odd| ≤ 3e-4 (#255's NO bar); a ṙ at a time beyond the window is reported with its time of leaving, not as a value |

## Pilot

B = 0.15, h = 0.0025 (the costliest bisection of the set, B = 0.2's hit the 2 h limit at h = 0.0025 in #228), `runs/bisect_B0.15_hk1`, stop at 2 h (`timeout 7200`). If it finishes (rc 0, hi − lo ≤ 1e-12) it is the run of
record for B = 0.15's bisection: it uses the declared bracket, tolerance and code, and no criterion depends on it. If it does not finish, its bracket is reported and, as in #228, p* is read from its points
(`g_d6.py stopped-pstar`) for the pair.

## Stops and limits

- Any single run: 2 h (`timeout 7200`), stopped and reported with its bracket. Logs are never overwritten; a rerun is a new directory (`*.partialN` for the dead one).
- Only my own units are stopped, by unit name (`systemctl --user stop nm-i325-…`). Nothing of choptuik-large-d's is touched.
- A dependency (a pair on its bisection) is waited for inside the run (`WAITFOR=`), not by a queue line.

# Part 2a: runs, criteria, the planted case and the #272 prediction (2026-11-28 about 04:36, dh610 clock; before any pair of record. The first draft of this heading said 04:40, written before the clock was read)

The pilot (04:29) and the three bisections at h = 0.00125 (B = 0.03, 0.01, 0.014, 04:33) started before this part was written. A bisection is judged by one criterion only, that it finishes (BIS), and no
number below depends on its p*ₕ; the pairs, which are the judged data, wait inside their run for the file `PART2B_DECLARED`, written when part 2b (the mutations' computed effects) is committed.

## What pilot and development showed (not runs of record)

1. The pilot's per-run cost at B = 0.15, h = 0.0025 is 12 to 20 s (so a bisection of about 45 runs is 10 to 20 min, not the 2 h of B = 0.2 at the same h in #228): B = 0.15 is not the costliest. The h = 0.00125
   bisections are about 3.3 times a h = 0.0025 one (#228: 3228 s, 3937 s at B = 0.04, 0.07).
2. #228's p*ₕ(B) has an additive h² part: p*ₕ(0.04) = 1.875e-3, 1.461e-3 at h = 0.0025, 0.00125 (extrapolated 1.324e-3). At B ≤ 0.02 the ghost pulse that cancels the unstable mode is mostly the one that
   cancels the scheme's own perturbation, so the resolution part of ṙ may grow as B falls. This is why the second h is put on the **smallest** B (0.01, 0.014) and not on B = 0.15, whose resolution part at 0.07 → 0.1 is
   −0.003 (#228).
3. `ellis_spectrum.py`'s time-domain code is a function of n (`evolve(n, h, tmax, S0f, W2guess)`), not of D = 5, 4 only; it was never run at n = 4. A development run (h = 0.01, 0.005 Richardson, Gaussian
   centre 3 width 0.5, `dev/lin_dev.log`) gives at D = 6 (n = 4) a **constant** throat speed, v/P = 1.2373, 1.2362, 1.2355, 1.2351, 1.2350 at t = 5 … 10, d ln v/dt = 1e-4; at n = 3 it reproduces #272's
   table (v/P = 0.28155 at t = 10, rate 0.0236) and ind272's (0.2815). Its unstable eigenvalue at n = 4 is W² = 4.686582 against #195's W² = 4.686621 (relative 8e-6).

## Runs of record

| B | h = 0.0025 (hk = 1) | h = 0.00125 (hk = 2) | source |
|---|---|---|---|
| 0.01, 0.014, 0.03 | bisection to 1e-12 and the pair p*ₕ ∓ 1e-10 | the same | this task |
| 0.15 | the same | extra, only if time is left | this task |
| 0.02 | #228's | extra: 0.00125 (so that 0.014 → 0.02 → 0.03 has resolution parts), only if time is left | #228's, read only |
| 0.04, 0.07, 0.1 | #228's | #228's | read only |
| 0.2 | #228's (p* from the stopped bisection) | none | read only |

Required by the issue: 0.01, 0.014, 0.03, 0.15 at h = 0.0025 and **two** of them at 0.00125: 0.03 and 0.01. 0.014 is added at 0.00125 so that the exponent 0.01 → 0.014, the one that tests the linear limit,
has its own resolution part. If t = 10 is outside the pair's linear window at B ≤ 0.014 (WIN10 below), a pair at δ = 1e-11 is added at that B and h = 0.0025 and reported as a **separate** row: its p* is known to 5e-13,
so its mean carries up to 5 % of its odd part (the primary pair's 0.5 %).

## Criteria (`drift_b6.py`; each can fail; a failure is a result, not repaired by changing the check)

Estimators are #228's, unchanged: local ṙ = dr_th/dτ by a linear fit over ±0.5 in τ on the pair's mean at t = 8, 10, 12 (±0.25 and ±1: the window part); `throat_drift.fit_rdot` masked at |odd| > 3e-4, read
only where κ ≥ 0.05 and SE(ṙ∞) ≤ 10 % of |ṙ∞|; exponents α of a ∝ B^α between neighbouring B at the same h; the resolution part of an exponent is α(h = 0.0025) − α(h = 0.00125) where both B have both h, and the
Richardson exponent (second order, assumed, as the observed order of p*ₕ at B ≠ 0.1 is 2.008, 2.007) is reported beside it.

| id | criterion | source |
|---|---|---|
| BIS[B,h] | the bisection ends with hi − lo ≤ 1e-12 and not stopped | `throat_drift.job_bisect` summary |
| JOB6[B,h] | the pair p*ₕ ∓ 1e-10 has fates (collapse, expansion) on #40's events | #228's JOB6 |
| WIN8[B,h] | |odd| ≤ 3e-4 on the whole fit window of ṙ(8) (τ ± 0.5): ṙ(8) is a value only inside it | new; the bar is #255's NO bar |
| WIN10[B,h], WIN12[B,h] | the same at t = 10, 12: **reported** with the time t_L at which the pair leaves the window, not gated (NO6 failed at B ≤ 0.07 in #228) | reported |
| PL1_6, PL2_6, PL3_6 | #228's planted static and moving throats through the locus code (bars 2e-4, 5e-4 on r_th, rdot) and planted ṙ(τ) = ṙ∞ + c e^{−κτ} through the same fit (local slope to 2e-4, ṙ∞ within 3 SE), unchanged | `g_d6.chk_planted6` |
| PLX | a planted family ṙ_h(B) = c B^α (1 + ε_h) with known α, known h² part ε_h and a known window part goes through the table code and returns α, the resolution part and the Richardson exponent to 1e-9 | new |
| LIN1 | the code that gives the prediction reproduces known answers: the unstable eigenvalue at n = 4 against #195's W² (`checks.W_EXACT[4]`) to 1e-4, and at n = 3 v/P(t = 10) against #272's 0.2815 to 3e-3 | planted |
| LIN2 | the prediction itself: at D = 6 the linear response is a constant speed, |d ln v/dt| ≤ 5e-3 over t ∈ [8, 12] (D = 5's is 0.024 at t = 10, D = 4's 0.245) | `ellis_spectrum.evolve(4, …)` |
| LIN3 | the shape in the linear limit: ρ(B) = ṙ(10)/ṙ(8) − 1, at the finest h at each B where t = 10 is inside the window, falls strictly over B = 0.04, 0.03, 0.02, 0.014, 0.01, and ρ(0.01) ≤ 0.05 (#228: 0.148, 0.104 at 0.04, 0.02) | prediction of LIN2 |
| LIN4 | the amplitude law in the linear limit: the Richardson exponent of ṙ(8) between B = 0.01 and 0.014 lies in [1.8, 2.3] (a speed ∝ P ∝ the pulses' second-order source ∝ B²) | prediction of LIN2 |

LIN3 and LIN4 are skipped, and said to be skipped, where the data they need (t = 10 inside the window; B = 0.014 at both h) are absent.

## The #272 prediction for ṙ∞ at B = 0.02, D = 6

**`ellis_spectrum.py` cannot give ṙ∞ at B = 0.02.** Its response is Y(t, 0) = P y(t) for data Y_t(0, l) = σ₀(l) with P = ∫ w Y₁ σ₀ dl, the momentum conjugate to the scale mode: it gives the shape y(t) and the speed per unit P,
not P. The pulses of G enter as a matter source of second order in B (the normal pulse) and first order in the ghost pulse A = p*ₕ(B) ∝ B², and the code has no source term. #272 says so (limits; E_net
is second order and "P cannot be got from E_net"), and its recommended task 1 (put the pulses' stress into Y_tt = DY + S) is not done; writing it here is new method code, which this task does not allow.
What the code gives at D = 6 and what the data can fail:

- v/P = 1.2350 at t = 10, constant to d ln v/dt = 1e-4 (a Jordan block of a normalizable zero mode at n = 4: Y₁ ∼ l^{−1} in the canonical variable; at n = 3 the same code gives the slowly falling t^{−0.2} speed). So
  ṙ∞ = 1.235 P and the transient of #228's fit (κ = 0.72 at B = 0.02, ṙ rising 10 % between t = 8 and 10) is **not** in the linear response: LIN3, LIN4.
- Against #228's 0.00173 at B = 0.02: the linear response needs P = 0.00173/1.235 = 1.40e-3 = 0.026 E_net (E_net = (B² − p*ₕ²) I₂ = 0.0545; D = 5's implied P is 0.049 E_net at B = 0.02, 0.24 E_net at B = 0.1
  in #272). The implied P/E_net at every B of the nine is reported (`P_impl`), not a prediction; if the linear response is the cause of ṙ, it is constant as B → 0.
- The B = 0.02 values of #228 (ṙ(8), ṙ(10) = 0.00154, 0.00170, ṙ∞ = 0.00173) were known when this was written; the blind tests are LIN3 and LIN4, at B = 0.01 and 0.014.

## Stops and limits (as part 1)

2 h per run, stopped and reported with its bracket; units named `nm-i325-*`, stopped by name only; memory is reported, never a stop condition. At most 4 processes.

# Part 2b: corrections, one amendment, the mutations and their computed effects (2026-11-28 05:44, dh610 clock; before any pair of record. The first draft said 05:50, an estimate; the push was at 05:44 and the flag file README_2B_DONE was created at 05:44:34)

No pair of record had started when this was written (the pairs wait for `README_2B_DONE`, created after this part is pushed). Development runs: `dev/analysis_dev1`, `dev/analysis_dev2` (the analysis on #228's frozen record
and the four finished bisections), `dev/mut_all_quick` (every mutation of `drift_b6.py` against the baseline), `dev/pair_B0.04_d1e-11_hk1` (one pair at δ = 1e-11, B = 0.04, h = 0.0025, from #228's bisection),
`dev/mut_odd_scale_devbase`, `dev/mut_dl_scale_devbase`, `dev/mut_tau_unit_full` (running).

## Corrections to part 2a (found by the runs; made before any pair)

1. Item 1 of "What pilot and development showed" is wrong. The pilot's first 17 runs cost 12 to 20 s, and the extrapolation to 10 to 20 min was not justified: later runs reach T = 25 to 45 and the bisection took
   **3848 s** (64 min, 40 runs). B = 0.15 is the costliest bisection at h = 0.0025, as the task said (4 times #228's B = 0.04, 965 s). The three bisections at h = 0.00125 took 3065, 3028, 3101 s (36, 33, 34 runs).
2. The extra "B = 0.15 at h = 0.00125" is dropped: 3.3 times 3848 s is above the 2 h stop. B = 0.02 at h = 0.00125 (about 1 h) stays an extra, only if the pairs are finished and time is left.
3. The resolution part of an exponent is **α(h = 0.00125) − α(h = 0.0025)**, #228's sign, not the opposite sign that part 2a wrote.

## Amendment (before any pair of record): LIN3 is read on pairs at δ = 1e-11

The development analysis of #228's record shows that at δ = 1e-10 the fit window of ṙ(10) (τ ± 0.5) is inside the linear window only for B ≥ 0.07 (t_L = 9.95, 10.18, 11.18, 13.26 at B = 0.02, 0.04, 0.07, 0.1), so LIN3, which needs ṙ(10) at
B = 0.04, 0.03, 0.02, 0.014, 0.01, cannot be read from the δ = 1e-10 pairs. Part 2a's contingency (a δ = 1e-11 pair where t = 10 is outside, at B ≤ 0.014) is replaced by:

- pairs at **δ = 1e-11, h = 0.0025, B = 0.01, 0.014, 0.02, 0.03, 0.04** (p*ₕ from the bisections of this task, #228's for B = 0.02, 0.04), 2 to 4 min each; LIN3 reads ρ from these only;
- **DLT[B]**: ṙ(8) of the δ = 1e-11 and the δ = 1e-10 pair agree within 2 % at each of the five B (the mean is the tuned member: p*ₕ is known to 5e-13, so the mean of the δ = 1e-11 pair carries up to 5 % of its odd part, that of
  δ = 1e-10 0.5 %). In development at B = 0.04 the two agree to 1.2e-5 (relative); a skipped DLT (no value inside the window) is not a pass;
- **JOB6d[B]**: the δ = 1e-11 pair has fates (collapse, expansion).

LIN4 is unchanged (δ = 1e-10, both h). The pairs run in the order of `scripts/dispatch.sh` (the long h = 0.00125 ones first), never more than 4 compute processes of mine.

## Checks of record

BIS (each bisection of this task), JOB6 and WIN8 (each δ = 1e-10 pair), JOB6d and DLT (each δ = 1e-11 pair), LIN1, LIN2, LIN3, LIN4, PLX, PLL, PL1_6, PL2_6, PL3_6. Failures expected from development:
JOB6 at B = 0.2 (#228's: the + side's event lies beyond t = 34; reported again, not repaired). Nothing else is expected to fail; LIN3 and LIN4 are tests of the prediction and may fail.

## Mutations and their computed effects (`drift_b6.py mutate --mutate=NAME`, each baseline against mutated analysis on development data; the verdicts that change)

| mutation | what it breaks | verdicts that change in development |
|---|---|---|
| `odd_scale` | the pair's odd part × 100 | WIN8 at B = 0.02, 0.04 (h = 0.0025, 0.00125), 0.07 (both h); DLT[B = 0.04] passes → skipped (dev base) |
| `bis_tol` | hi − lo × 1e3 in BIS | BIS at B = 0.15 (h = 0.0025), 0.01, 0.014, 0.03 (h = 0.00125) |
| `fate_swap` | the pair's fates reversed | JOB6 at the 7 of #228's 8 pairs that pass (B = 0.2 fails with and without it) |
| `dl_scale` | the δ = 1e-11 value of ṙ(8) × 1.05 | DLT[B = 0.04]: +1.2e-5 → +5.0e-2 (dev base with the dev pair) |
| `b_label` | B labelled √(0.1 B) | PLX, PLL |
| `res_swap` | the resolution part with the opposite sign | PLX |
| `rich_order` | Richardson with first-order weights (2 x₂ − x₁) | PLX, PLL |
| `lin_n3` | the linear response of n = 3 used for D = 6 | LIN1, LIN2 |
| `rho_swap` | ρ = ṙ(8)/ṙ(10) − 1 | PLL |
| `alpha_scale` | the Richardson exponent × 1.3 | PLL |
| `tau_unit` (#255's, through `g_d6.chk_planted6`) | τ in units of √2 t | PL3_6 (as #228 computed); its run through this script is `dev/mut_tau_unit_full`, appended when it finishes |

LIN3 and LIN4 have no data in development (B = 0.01, 0.014 are absent); their mutations act on the planted families (PLL) and on the data of record, where the effect will be read and reported, not declared. At the end each mutation is
run again on the frozen record (`runs/mut/`, `drift_b6.py mutate-all`) and the changed verdicts are compared with this table; a difference is reported.
