# I291-mac: the power-law tail of family G's throat speed at D = 4, B = 0.02: criteria, planted cases, mutations and development runs (#291)

Machine: the coordinator's Mac (Apple M5, 10 cores, macOS, shared and loaded), Python 3.14.7, numpy 2.5.4, scipy 1.18.1, numba 0.68.1, one thread per process (`NUMBA_NUM_THREADS=1`),
`nice -n 10`, at most 2 processes. Runner negative-mass-mac-i291 on the claude-me2 account. Issue https://github.com/nmoinvaz/negative-mass/issues/291 ("Measure the power-law tail of G's
throat speed at D = 4 in the nonlinear data"). Worktree `~/Source/negative-mass-i291`, branch `wip/i291-d4-tail`, from main b17db7a. Code (declared at 7415596): `notes/wormhole_evolution/throat_tail.py`, a thin
driver that imports #266's `settled_mass_b.py` (which imports #41's `settled_mass.py`, #253's `settled_mass_g.py`, #40's `threshold.py`, #225's `throat_locus.py` and #39's `dn.py`) and #255's
`throat_drift.py`, all unchanged. This README is written after the development runs (`dev/`) and before any run of record (`runs/`, `runs_k1` … `runs_k7`); the runs of record are the same
computations as the development runs (the evolution is deterministic) and are expected to reproduce them bit for bit (REPRO below). Status words as in AGENTS.md: every number is
*numerical evidence*. No sentence claims novelty.

## Question and plan

#272 (`ellis_spectrum.md`): in the *linear* response of the symmetric Ellis wormhole at D = 4 the throat's speed falls as t⁻³ (rate × t = 2.74, 2.89, 2.97 at t = 15, 20, 25), the shift
saturates, and #255's transient rate κ = 0.244 is the local exponent of that tail, not a mode. #267: at B = 0.1 the tail is masked by a drift (the speed tends to +1.26e-3). #255: the drift
speed scales as B^3.16, so at B = 0.02 it is about 6e-3 of B = 0.1's. This issue measures the speed v = dr_th/dτ of the tuned throat at B = 0.02 and asks whether it is a power law (log-log slope
within 20 % of −2.9) rather than an exponential (rate × t growing as t).

## What the development runs found (dev/, before this README)

| what | result |
|---|---|
| p*ₕ at B = 0.02 (member 0, bracket (−0.01, 0.01), hi − lo ≤ 1e-14) | 6.5839623e-4, 5.8719937e-4, 5.6939539e-4 at h = 0.02, 0.01, 0.005: second order (observed 2.00); 43 runs, 6 s, 25 s, 69 to 108 s |
| the pair p*ₕ ∓ 1e-12 | 13 to 38 s each; collapse on the − side, expansion on the + side in all 24 members; the odd part grows at 1.181 per unit t (the unstable mode's W = 1.182) and reaches 3e-4 of r_th at t = 20.06 to 20.09 |
| r_th − 1 and v (mean series) | r_th − 1 = +6.4e-4 at t = 6, zero near t = 9.4, −4.1e-4 at t = 14, −5.7e-4 at t = 18; v < 0 and \|v\| falls at every t from 8 on: no sign change and no relax-then-rise as at B = 0.1. The stall member: γ₁ = 0.0012 (t = 6) to 0.0019 (t ≥ 10), a nearly static throat |
| the speed (h = 0.005) | v = −1.776e-4, −1.141e-4, −7.70e-5, −5.47e-5, −4.67e-5, −4.02e-5, −3.50e-5 at t = 8, 10, 12, 14, 15, 16, 17 |
| rate × t = −d ln\|v\| / d ln τ (central difference ±0.5, clean part) | 1.71, 2.13, 2.19, 2.26, 2.29, 2.30 to 2.35 at t = 8, 10, 12, 14, 15, 16; the rate −d ln\|v\|/dt falls from 0.213 at t = 10 to 0.136 at t = 17, an exponential keeps 0.244. #272's linear response has 2.74 at t = 15 |
| second order in h | v at t = 10 and 12: observed order 1.96, 1.97; the speeds at h = 0.01 and 0.005 differ by 5e-4 to 9e-4 (relative) for t = 10 to 14 |
| **late contamination** | after t ≈ 16 the speed of a pair is contaminated by the roundoff floor of p*ₕ. A pair's mean is r_c + ε Q(t), Q = odd/δ ∝ e^{1.18 t}, ε the offset of p*ₕ from the threshold (1e-14 to 6e-14, different for every bisection and every pair). The pairs of one h differ from their mean by (v_k − v̄)/(λ odd_k/δ) = ε_k − ε̄, **constant in t to three digits** for t = 12 to 18 (−1.29, +0.47, −1.78, +0.07, +1.38, +1.17 e-14 for six members at h = 0.01). λ Q ε is 0.1 % of \|v\| at t = 16, 1 to 2 % at 17 to 18, 40 % to 70 % at t = 20, and 1 % of it changes the local exponent by 0.2 at t = 18. No choice of δ removes it (it is the offset, not the odd part): e = 10, 11 and 12 pairs of one bisection differ by 3e-14 and 6e-14 |
| ensemble (K = 8 per h) | spread of ε over the members 1.74e-14 (h = 0.01), 4.49e-14 (h = 0.005), pooled 3.41e-14; the standard error of the K-mean of v is 1.2e-4, 4.4e-4, 1.6e-3, 6e-3 of \|v\| at t = 15, 16, 17, 18 (h = 0.01) and 2.9e-4, 1.1e-3, 4.2e-3, 1.5e-2 (h = 0.005); window ends 18.90 (h = 0.01) and 18.20 (h = 0.005) |
| slope of the mean series (dev) | over [15, 16]: 2.306 (h = 0.005), 2.321 (h = 0.01); [15, 17]: 2.313, 2.349; [15, T_end = 18.2]: 2.304, 2.413. The bar \|p − 2.9\| ≤ 0.58 is p ≥ 2.32: **the slope sits on the bar's edge and the verdict follows the realization**. The single pairs at h = 0.005 give 1.94 to 2.67 over [15, 18.2] (std 0.23), at h = 0.01 2.25 to 2.50 (std 0.09) |
| rate × t spread (dev) | over [10, 16]: 9.9 % (h = 0.01), 9.4 % (h = 0.005) of the mean against 46.2 % for an exponential |
| tail plus constant (post hoc, v = −A τ^−p + b) | p = 1.90 to 2.13 and b = +3.3e-6 to +1.1e-5 over the starts t = 8, 10, 12 and the two h (not stable); #255's B^3.16 scaling predicts b = +7.8e-6; the constant is 7 % to 23 % of \|v\| at t = 15 |
| dev baseline of the checks | 1 gating check fails: S1 at h = 0.005 (\|p − 2.9\| = 0.596, bar 0.580); S1 at h = 0.01 passes (0.487), S2 passes at both h, S3 passes (4.6 %); planted PL1 97 %, PL2 100 %, PL3 100 %, PL4 100 %, PL5 92 % |

Development, in order: single pairs at e = 9 … 12 and h = 0.02, 0.01, 0.005 (`dev/runs`); the ensemble k = 1 … 7 at the three h (`dev/runs_k*`, `dev/jobs_dev*.txt`, `logs/dev0*`); the analysis
on the whole set (`dev/ana/dev_baseline.log`); the 13 mutations (`dev/mut/`). The planted development run first used the primary pair alone as the series of record and a spread test on
[15, T_end]: a planted t⁻³ speed passed that test in 46 % of the draws and its slope was within 0.15 in 78 % (the window is 2.5 long and its end is contaminated at 2 %). The estimator was
redesigned *before* the runs of record: the series of record is the ensemble mean, the shape test uses the clean window [10, 16], and the tolerance on the recovered slope is 0.25 (the S1 bar
is 0.58). No bar of S1, S2 or S3 was changed, and none is changed after the dev baseline above, which fails S1 at h = 0.005.

## Declared parameters (none is changed after a run of record without a ruling)

| quantity | value |
|---|---|
| dimension, family, units | D = 4 (n = 2), family G of #40 with B = 0.02 (`threshold.CRIT["G_B"]`, ghost pulse A on field 0 and normal pulse B on field 1, both on the + ray, centre 3, width 0.5); 8πG = 1, a = 1 the throat radius of the initial static wormhole; t = (x⁺ + x⁻)/√2, τ the locus's proper time (#225) |
| h | 0.01 and 0.005 (the issue's two, gating), 0.02 (post hoc, for the order in h); the h passed is the float of the literal |
| p*ₕ | `threshold.bisect` on `threshold.point` (X = 28, #40's), hi − lo ≤ 1e-14, p*ₕ = (lo + hi)/2, through #266's `pstar`. Member k uses the bracket BRACKETS[k]: (−0.01, 0.01) for member 0 (the run of record named by the task, #266's bracket of B = 0.025), seven others for the ensemble |
| the pair | A = p*ₕ ∓ 1e-12 through `throat_locus.sweep` (`dn.row_step` unchanged, triangle t ≤ 34), profile slices every 0.5 in t from 3, the member fitted on each (#266's `member` command with the exponent 12) |
| series | the pair's mean r_th(τ) on the slices both runs have (the unstable mode is odd in the pair: odd = (r₊ − r₋)/2). **The series of record is the mean over the K = 8 pairs** (r_th and τ averaged; the single pairs are reported and checked); v = dr_th/dτ by #255's `rdot_local` (local linear fit over ±0.5 in τ, every k/10-th slice), interpolated on a 0.05 grid in t |
| window | [15, T_end], T_end = min(25, the first t at which any member's \|odd\|/r_th ≥ 3e-4, the last speed sample, the first t ≥ 15 at which the standard error of the K-mean of v (sample std/√K) reaches 2 % of \|v\|). Common to the two h: the smaller T_end. Not informative if T_end − 15 < 2 |
| slope | p = −d ln\|v\| / d ln τ by the least-squares line through ln\|v\| against ln τ over the window (ln t is reported, τ = t − 0.01 at this B) |
| rate × t | −t d ln\|v\|/dt, from the quadratic fit of ln\|v\| against ln τ over a window, at its start, middle and end; spread = (max − min)/mean; an exponential's spread over the same three times is (t₃ − t₁)/t₂ (as #272's T7: 50 % over t = 15, 20, 25) |
| shape window | [10, min(16, T_end)] (inside the clean part of v: the standard error of the mean is below 2e-3 of \|v\| at t = 16) |
| drift | v keeps one sign and \|v\| falls monotonically on [12, T_end]; otherwise the drift dominates and S1, S2 are reported as not informative |

Readings of the issue that are mine, stated so the coordinator can overrule them:

- "to t = 25 or until the odd part reaches 3e-4": the odd part reaches 3e-4 at t = 20.1, but the roundoff offset contaminates v beyond t ≈ 17 to 18, well before that (above), so T_end also carries the
  ensemble's standard-error rule. t = 20 and 25 of the acceptance's "rate × t at t = 15, 20, 25" are not reachable; the three times are taken inside the window.
- "the log-log slope of |v| over t ∈ [15, 25]" is the slope over [15, T_end], with the window fixed by the rule above before the runs of record.
- The shape test (rate × t grows less than half as fast as an exponential's) is evaluated on [10, 16], where planted truth shows it separates a power law from an exponential and [15, T_end] does not
  (PL3, PL4, and the report line of the planted run).
- The ensemble mean as series of record is an addition; the task's pair (member 0) is reported in every table and its slope is in the ensemble's table.

## Checks, bars, and what gates

Gating: h = 0.01 and 0.005. Post hoc, gates nothing: h = 0.02 checks and the reports. A failed check is a result; nothing here is changed after a run of record.

| id | check | bar |
|---|---|---|
| BR-h | every bisection (K = 8) ends with hi − lo ≤ 1e-14 and no stop; the replayed bracket (`settled_mass_b.bracket_after`) equals lo and hi; the first end collapses and the second expands | 1e-14, equal |
| EVT-h | the pair p*ₕ ∓ 1e-12 collapses on the − side and expands on the + side, inside the triangle, in every member | all |
| RATE-h | the pair's odd part grows at the unstable mode's rate on t ∈ [10, 16] in every member | 1.10 to 1.25 (W = 1.182) |
| WIN | the common window is at least 2 long | 2.0 |
| DR-h | no drift before the window: v one sign and \|v\| falling on [12, T_end], both h | monotone |
| **S1-h** | **the issue's acceptance 1:** the log-log slope of \|v\| over [15, T_end], mean series, each h, within 20 % of −2.9 | \|p − 2.9\| ≤ 0.58 |
| **S2-h** | **the issue's acceptance 2:** rate × t at the start, middle and end of the shape window: spread at most half of an exponential's (46.2 % over [10, 16]) | 23.1 % |
| **S3** | **the issue's acceptance 3:** the two h agree on the slope | 10 % |
| ORD-p, ORD-v10, ORD-v12 | second order in h over 0.02, 0.01, 0.005: p*ₕ and v at t = 10, 12 (post hoc: needs h = 0.02) | observed order 1.8 to 2.2 |
| PL1, PL2 | planted: a speed ∝ τ⁻³ (PL1) and τ^−2.3 (PL2) with the measured noise of r_th (rms of r_th around its local quartic fits) and K = 8 pairs with offsets ε_k ~ N(0, σ²), σ the measured pooled spread of the stored ensemble, through the window rule and the slope, 200 draws: the recovered slope is within 0.25 of the truth in at least 90 % | 90 %, 0.25 |
| PL3 | planted τ⁻³: the shape test passes in at least 90 % of the draws | 90 % |
| PL4 | planted exponential (rate 0.244, the same amplitude at t = 15): the shape test and the slope test (S1's bar) both fail in at least 90 % (a negative control that must fire) | 90 % |
| PL5 | as PL1 with the offsets at 3σ | 90 %, 0.25 |
| REPRO | the stored runs of record equal the development runs bit for bit: `cmp` on `locus.npz` and `member.json` for every (h, k) (`scripts/repro.sh`; reported, not in the driver) | equal |

Reports with no bar (printed, gate nothing): the local exponent of the mean at t = 8 … 20 with its standard error; the three-point rate × t on [15, T_end] and the planted separation on that
window; the slope over windows [12 … 15, 16 … T_end] and with ln t; the slope of each single pair and its spread (the roundoff realization), the h difference (truncation) and the window spread
(fit choices), kept apart; the tail plus drift fit v = −A τ^−p + b for three starts; the stall member (r_th, γ₁) along t; #272's linear response beside the data.

## Mutations (each computed on the development set, `dev/mut/`, before it was declared)

`python3 throat_tail.py analyze --raw=<folder> --mutate=NAME` breaks one input and must fire exactly the declared set. **S1-h0.005 fails without any mutation (the dev baseline: 2.304, bar
2.32) and is therefore in every set where S1 is evaluated**; it is not in the sets of `odd_t2`, `ens_one`, `short_win` and `drift_add`, where the slope tests are not informative and are skipped.

| mutation | what it does | fires |
|---|---|---|
| `bisect_early` | the bracket of every bisection after 30 steps instead of the last | BR-h0.02, BR-h0.01, BR-h0.005, S1-h0.005 |
| `evt_swap` | the two sides of the pair exchanged in EVT | EVT-h0.02, EVT-h0.01, EVT-h0.005, S1-h0.005 |
| `odd_t2` | the odd part multiplied by e^{0.3 t} (wrong growth rate; the 3e-4 rule then ends the window at 17) | RATE ×3, WIN, PL1, PL2, PL4, PL5 |
| `one_side` | the + side's r_th instead of the pair's mean (the unstable mode kept) | S1-h0.01, S1-h0.005, S2-h0.01, S2-h0.005 |
| `ens_one` | the primary pair alone: no ensemble, the window rule sees no spread | DR-h0.005, PL1, PL2, PL4, PL5 |
| `short_win` | a window of at least 20 required | WIN, PL1, PL2, PL4, PL5 |
| `drift_add` | a constant speed +1e-4 added to the throat | DR-h0.01, DR-h0.005 |
| `rate_not_p` | the slope taken against τ (a rate) instead of ln τ | S1-h0.01, S1-h0.005, PL1, PL2, PL5 |
| `v_exp` | an exponential speed of rate 0.244 in place of the data's, same amplitude at t = 15 | S1 ×2, S2 ×2, ORD-v10, ORD-v12, PL1, PL2, PL4, PL5 |
| `s3_scale` | the slope at h = 0.005 × 1.25 in S3 | S3, S1-h0.005 |
| `order_h` | the h = 0.02 records replaced by the h = 0.01 ones | BR-h0.02, ORD-p, ORD-v10, ORD-v12, S1-h0.005 |
| `pl_exp` | the planted power law replaced by an exponential | PL1, PL2, PL3, PL5, S1-h0.005 |
| `pl_eps` | the planted offsets × 30 | PL1, PL2, PL4, PL5, S1-h0.005 |

Every check fires under at least one mutation: BR, EVT, RATE, WIN, DR, S1, S2, S3, ORD (three) and PL1 to PL5.

## Runs of record

`scripts/run_one.sh` (the bisection of p*ₕ, or the pair, for one (h, k)) and `scripts/run_jobs.sh` (two lanes, nice 10, `NUMBA_NUM_THREADS=1`, a log, an err and an rc for every stage, reruns
numbered, never overwritten). Order: `jobs_rec.txt`, 3 h × 8 members × (bisection, pair), h = 0.005 and 0.01 first. Detached with `nohup`. A run not finished in 2 h of wall time is stopped and
reported (the longest development run took 108 s). Then `python3 throat_tail.py analyze --raw=<this folder>` (about 2 min) and `scripts/run_muts.sh <this folder> <this folder>/mut LANE 2` (13
mutations, about 1 min each).

## Limits stated before the runs

- D = 4, B = 0.02, family G only; h = 0.01 and 0.005 (0.02 post hoc). The data end at the roundoff floor: the clean part of the speed is t ≤ 16 to 18; the issue's t = 20 and 25 are not reached.
- The offset ε is estimated from the ensemble's spread; its mean over the K members is not known (zero mean assumed). A common offset of all members would bias the late speed by λ Q ε̄ and is
  not separable from the data.
- The evolution is #39's, unchanged and not independently coded (the one-sided family needs the double-null code): the cross-checks are second order in h (ORD) and the linear response of #272.
- The planted cases test the slope, the shape test and the window rule with the measured noise, not the evolution.
- The drift decomposition and the member's γ₁ are post hoc.

## Changes made after this README

Report-only additions and one script fix; no check, bar, window, series or mutation changed (the criteria, the bars and the mutation sets are as committed at c324b74a, code 7415596):

- `report_offsets` in the driver (1c9ba81): the offsets ε_k − ε̄ of the eight pairs of each h at t = 12 … 18, and the dependence on δ of member 0's pair, printed in the output. Six extra pairs
  (member 0 at e = 11 and 10, the three h: `jobs_rec_C.txt`, `jobs_rec_D.txt`, `scripts/launch_I291_extra.sh`) were run for it. The development table above quotes six offsets from a K = 6 mean;
  the output has the K = 8 table.
- `scripts/repro.sh` first compared the `pstar/summary.json` files byte for byte and flagged the wall-clock `secs`; it now compares the json without `secs` (72 files, 0 different).
- The figure script `throat_tail_graph.py` and the note.
- During development the first launch of `scripts/run_muts.sh` stopped at once (the list was looked up after a `cd`); it was relaunched, nothing else.

## Results of record

Runs: `scripts/launch_I291.sh` at 23:39 on 2026-11-27: 48 jobs (3 h × 8 members × bisection and pair), all exit 0 in 9 min (bisection 4 to 5 s, 15 to 18 s, 53 to 63 s and pair 7 to 9 s, 10 to 11 s, 19 to 21 s at
h = 0.02, 0.01, 0.005); then the six extra pairs. REPRO: `scripts/repro.sh` → `logs/repro.log`: 72 files, 0 different from the development runs. `analyze_record.log` (= `throat_tail_output.txt` of the
note): 25 checks, 24 pass, **1 fails: S1 at h = 0.005** (slope −2.304, |p − 2.9| = 0.596 against 0.580). `mut/`: 13 of 13 mutations fire exactly their declared set.

| check | verdict | numbers |
|---|---|---|
| S1 slope over [15, 18.2] within 20 % of −2.9 | h = 0.01 met, h = 0.005 not met | −2.413, −2.304 (over [15, 16]: −2.321, −2.306) |
| S2 rate × t on [10, 16], spread against half an exponential's | met | 9.9 %, 9.4 % against 23.1 % |
| S3 the two h agree within 10 % | met | 4.6 % |
| DR no drift before the window | met | v < 0, \|v\| falls on [12, 18.2] |
| WIN | met | T_end = 18.20 (18.90 at h = 0.01, 18.20 at 0.005) |
| ORD (post hoc) | met | p*ₕ 2.00, v(10) 1.96, v(12) 1.97 |
| PL1, PL2, PL3, PL4, PL5 | met | 97 %, 100 %, 100 %, 100 %, 92 % against 90 % |
| BR, EVT, RATE, three h | met | 24 members each |

Figure: `throat_tail.svg` (from `throat_tail_graph.py` in the worktree).
