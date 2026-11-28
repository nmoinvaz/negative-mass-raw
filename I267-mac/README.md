# I267-mac: family G's settled mass against the static member at departure, delta from 1e-3 to 1e-12 (D = 4, B = 0.1): #41's chain, #225's member, #266's relation as the prediction

Machine: the coordinator's Mac (Apple M5, 10 cores, macOS, shared and heavily loaded), Python 3.14.7, numpy 2.5.4, scipy 1.18.1, numba 0.68.1, one thread per process (`NUMBA_NUM_THREADS=1`),
`nice -n 10`, at most 2 processes. Runner negative-mass-mac-i267 on the claude-me2 account. Issue https://github.com/nmoinvaz/negative-mass/issues/267 ("Test whether family G's settled mass
follows the static member at departure as δ → 0"). Worktree `~/Source/negative-mass-i267`, branch `wip/i267-mass-vs-member`, from #266's head c24b3a1. Code:
`notes/wormhole_evolution/settled_mass_member.py`, a thin driver that imports #266's `settled_mass_b.py` (which imports #41's `settled_mass.py`, #253's `settled_mass_g.py`, #40's
`threshold.py`, #225's `throat_locus.py` and #39's `dn.py`) and #255's `throat_drift.py`, all unchanged. This README is written after the development runs (`dev/`) and before any run of record
(`runs/`); nothing above the line "Changes made after this README" is changed after the first run of record. Status words as in AGENTS.md: every mass and every member parameter here is
*numerical evidence*. No sentence claims novelty.

## Question and plan

#253: G's settled mass at D = 4, B = 0.1 rises by 2e-4 to 6e-4 per decade of δ below 1e-6 (0.23498 a at 1e-6, 0.23555 a at 1e-8, 0.23762 a at 1e-12), with no limit visible. #225: the near-critical
state is the static member r_th = 1.0028 a, γ₁ = 0.048, and its throat radius drifts slowly. #266: along B, at δ = 1e-8, M/r_th − M(B = 0) = 0.2027 γ₁ + 0.853 γ₁² to 6e-6 over four B (member read where
the unstable mode has grown to 1e-3 of r_th). If the settled mass follows the member at departure, then the member that G leaves after a longer stall (smaller δ) should predict the mass at that δ by
#266's relation. This issue measures the member (γ₁, r_th) at departure for each δ, at two h, and tests that prediction. It also measures the drift of r_th along the stall at D = 4 and sets it beside
#255's D = 5 drift.

## Declared parameters (the chain is #41's, unchanged; none of this is changed after a development run without a ruling)

| quantity | value |
|---|---|
| dimension, family, units | D = 4 (n = 2), family G of #40 with B = 0.1 (`threshold.CRIT["G_B"]`, ghost pulse A on field 0 and normal pulse B on field 1, both on the + ray, centre 3, width 0.5); 8πG = 1, a = 1 the throat radius of the initial static wormhole; t = (x⁺ + x⁻)/√2 |
| h | 0.01 and 0.005 (the issue's two), and 0.02 (post hoc, for the order in h); the h passed is the float of the literal |
| p*ₕ | bisected for each h: `threshold.bisect` on `threshold.point` (X = 28, #40's), hi − lo ≤ 1e-14, p*ₕ = (lo + hi)/2, bracket (0.005, 0.03) = #266's. The development runs read #266's p*ₕ; the runs of record bisect again, and P266 compares them (the same code on the same machine: expected equal) |
| δ, e | A = p*ₕ − δ, δ = 10^−e. **Gating (the issue's six): e = 7, 8, 9, 10, 11, 12.** Supplementary (the rest of #253's scan to 1e-3, gate nothing): e = 3, 4, 5, 6. 1e-2 and 1e-1 of #253's scan are not run |
| chain | #41's, through #253's `run_real_g`: F₁ = 1.5, K = 20, W₁ = 2.4, r_cut = 0.05, trap tol 1e-2, dxp = 12, dm = 3, limit e^{−f} ≤ F_max = 1 572 864 on the horizon; first trapped cell of #40's `point` at p*ₕ − δ; the expansion side p*ₕ + δ must expand |
| settled mass | plateau mean of M_AH over the last 1.0 of x⁺ (`settled_mass_g.summary_g`, key `plat1`), as #253 and #266; M = r_AH/2 |
| member pair | the pair A = p*ₕ ∓ δ through `throat_locus.sweep` (`dn.row_step` unchanged, triangle t ≤ 34, profile slices every 0.5 in t from 3, #266's `member` command with the exponent e) |
| departure | #266's: t_dep(ε) is the first t ≥ 6 at which the unstable mode's part \|r_min(p*ₕ + δ) − r_min(p*ₕ − δ)\|/2 reaches ε of the tuned (mean) throat radius; primary **ε = 1e-3**, alternative ε = 1e-2 |
| member at departure | #266's `member_at`: #225's `slice_masses` and `fit_asym` on the pair's **mean** profile, r_th the mean of the two locus minima, s_th and r_th linearly interpolated in t between the two slices that bracket t_dep, γ₁ = s_th/√(1 − s_th²) |
| the prediction | #266's relation `M/r_th − M₀ = a γ₁ + b γ₁²`, fitted by least squares through the four B = 0.025, 0.05, 0.1, 0.125 of #266's stored runs **at the same h** (member read at ε = 1e-3; M₀ = B = 0's plateau, 0.223086 at h = 0.005): (a, b) = (0.2027, 0.853) at h = 0.005, (0.2029, 0.850) at 0.01. Predicted: M(δ) = r_th(δ) [M₀ + a γ₁(δ) + b γ₁(δ)²], with the member of this scan at departure |
| the drift | #255's estimator (`throat_drift.fit_rdot`, `rdot_local`): dr_th/dτ = ṙ∞ + c e^{−κ(τ−τ₀)} over t in [6.5, 12] where \|odd\| ≤ 3e-4, on the pair's mean (r_th, τ of the locus), τ the locus's proper time. Compared with #255's D = 4 fit (B = 0.1, h = 0.01, pair 1e-10: ṙ∞ = +0.00133, κ = 0.244) and D = 5 (ṙ∞ = +0.02602), read from `throat_drift_output.txt` |

Readings of the issue that are mine, stated so the coordinator can overrule them:

- "six δ": e = 7 to 12, because the member is read where its mode has grown to ε = 1e-3, and for δ ≥ 1e-6 that is before t = 9.6, while the pulses are still leaving (dev: the fit residual of M(r) at departure is 3e-4 at 1e-6,
  9e-3 at 1e-5, and t_dep reaches its floor t = 6 at 1e-3, 1e-4). The four larger δ of the scan are run and reported, and gate nothing. **δ = 1e-12 is gating although the development runs show it at the roundoff floor**: the
  pair's odd part there differs from the linear value by 1 % to 3 %, the departure time between the two h by 0.05, and HST fails by 1.6 to 1.1 times its bar there (dev: below).
- "to 1e-4 relative": relative difference of γ₁ and of r_th between h = 0.01 and 0.005 at each δ.
- "one smooth function to the scan's precision": the six (γ₁, r_th, M) of the scan lie on a one-parameter curve in the (γ₁, r_th) plane, along which any smooth M(δ) is a smooth function of the member. SMOOTH
  tests that and is weak by construction. The test that can fail is the cross-family one, PRED: the function of #266 (found along B) must also describe the scan. The bar is the one of #266's REL, 6e-5, about
  twice the h-difference plus the roundoff-realization scatter of the plateau at the finest pair (1e-5 + 7e-6, #253).
- "the drift's rate": dr_th/dτ of the pair's mean, #255's estimator and window; at D = 4 it is extended to the pair 1e-12 (t to 20.5), which gives the late speed on a longer stall than #255's window.

## What the development runs found (dev/, before this README)

| run | what | result |
|---|---|---|
| dev01 | the pair p*ₕ ∓ 10^−e through #266's `member`, e = 8, 10, 12, h = 0.01 | 31, 44, 50 s; t_dep(1e-3) = 13.615, 17.623, 21.664 (2.00 and 2.02 per decade; ln 10 over the mode's rate 1.15 = 2.00); both events inside the triangle t ≤ 34 |
| dev (jobs) | chain and pair at e = 3 … 12, h = 0.02, 0.01, 0.005 with #266's p*ₕ (30 jobs, all rc 0) | chain 4 to 8 s, whole job (chain and pair) 10 s (h = 0.02) to 81 s (h = 0.005); fates collapse/expansion at every δ, 1e-12 included (T 23.96 / 29.59 at h = 0.01); every run ends at e^{−f} = 1.56e6 to 1.57e6 |
| the member against t | pair-mean rows (t, r_th, γ₁) | identical for every δ before departure to ≤ 3e-6 (TRAJ); r_th(t) falls from 1.024 (t = 5) to 1.00287 (t = 13.5), then **rises** at a speed that tends to +1.1e-3 per unit t (1.0087 at t = 21.7); γ₁(t) falls from 0.04857 (t = 11) to 0.04757 (t = 24), slope −7.6e-5 per unit t |
| the unstable mode | \|odd\|(t)/δ at t = 10 | 1585.4 to 1585.6 for e = 7 … 9 and 1585.45 to 1584.1 at e = 10 (spread 1e-4 at h = 0.01, 9e-4 at 0.005); at e = 11 it differs from that by ≤ 1.7e-3; **at e = 12 by 1.1 % (h = 0.02), 2.7 % (0.01), 3.1 % (0.005)**: the roundoff realization of the evolution is ~3e-14 in the effective amplitude, the size of p*ₕ's own floor |
| member at departure, two h | relative differences h = 0.01 against 0.005 | γ₁ ≤ 3.3e-5 and r_th ≤ 2e-6 for e = 7 … 11; **e = 12: 1.6e-4 and 1.1e-4** (t_dep 21.664 against 21.613) |
| plateau, two h | \|plat(0.01) − plat(0.005)\| | 6.2e-6 to 9.7e-6 for e = 3 … 11, **4.5e-5 at e = 12** (#253: 4.1e-5) |
| order in h | three h, windows of RC6 | second order (1.89 to 2.21) for e ≤ 8; out of the band 1.5 to 2.5 for e ≥ 9 (2.3 to 3.0 at 1e-9, 1.6 to 2.0 at 1e-10, 0.6 to 1.4 at 1e-11, −2.9 at 1e-12): the h-differences there are of the size of the roundoff scatter |
| the prediction | M − predicted by #266's relation (h = 0.005) | e = 7: −5.2e-4, e = 8: +5e-7, e = 9: +3.5e-4, 10: +5.9e-4, 11: +7.6e-4, 12: +8.9e-4 (the same at h = 0.01 to 1e-5): 10 to 15 times the bar 6e-5. The part of dM (e = 8 → 12, +2.07e-3) the relation assigns: +1.35e-3 through r_th, −1.7e-4 through γ₁ |
| the drift | #255's fit on the pair 1e-10, h = 0.01 and 0.005 | ṙ∞ = +0.00133 ± 1.9e-5, κ = 0.244, r_th − 1 = +0.00949, +0.00498, +0.00316 at t = 8, 10, 12: #255's numbers to all printed digits. Pair 1e-12: the fit on [6.5, 12] extrapolates to the measured slope over t = 14 to 20 within 6.8e-5; the fit on [6.5, 20.5] gives ṙ∞ = +0.00126 ± 3.3e-6 (h = 0.005; +0.00127 ± 3.6e-6 at 0.01), κ = 0.246 to 0.247 |
| post hoc, seen in dev | (not checks) | the part of dM not carried by r_th, dM − (M/r_th) dr_th, falls by 0.65 per decade (0.649, 0.653, 0.669, 0.650); e^{−κ Δτ} with #255's κ = 0.244 is 0.62. With a third parameter, the speed ṙ_th at departure, y = M/r_th − M₀ = a γ₁ + b γ₁² + c ṙ_th fits the four B and five δ to 4.3e-5 (leave-one-out ≤ 6.6e-5), against 8.4e-4 without it. Reported in the output as post hoc descriptions, with no bar |

Development (first launches that failed on a slip are in `dev/aborted/`): the first analysis was pointed at a folder without `runs/` (`ana_dev1.log`); the second stopped on `settled_mass_g.I253` (it is `settled_mass_b.I253`); LIN and TRAJ
were first written with bars and row lookups that the development data showed mis-specified (LIN over e = 8 … 12 at 2e-3, TRAJ with an exact match on t); both were corrected before this README (LIN split into LIN and LIN2, TRAJ takes the nearest slice).

## Checks, bars, and what gates

Gating: the six δ (e = 7 … 12) at h = 0.01 and 0.005. Post hoc, gates nothing (`-ph` in the output): e = 3 … 6 and h = 0.02. A failed check is reported as not met; nothing here is changed after a run of record.

| id | check | bar |
|---|---|---|
| CFG | `settled_mass.CRIT` equal #41's declared chain; X = 28; `threshold.CRIT["G_B"]` = 0.1 at import | equal |
| RUNS | every (δ, h) has its chain and member output and every h its p*ₕ | all |
| PMEM, PDEP, PREL | #266's planted cases through this driver (exact static members as profile slices through the extraction; a planted growing pair through the departure time; a planted relation through the leave-one-out) | γ₁ ≤ 1e-5, r_th ≤ 1e-6, m± ≤ 1e-4; 2e-5; 6e-5 |
| PTD | planted δ scan: odd part Q₀ δ e^{λt}, a member trajectory of the measured size, rows every 0.5 in t from the exact static member, through `member_at`: t_dep, r_th, γ₁ at the six δ against the known values | t_dep 2e-5, γ₁ 1e-5, r_th 5e-5 (observed 7e-6, 4e-10, 1.0e-5) |
| PPOS, PNEG | the planted relation M = r_th(M₀ + aγ₁ + bγ₁²) through the prediction test passes; with an extra 3e-4 per decade of δ it must fire | 6e-5 |
| PDR | planted ṙ = ṙ∞ + c e^{−κτ} (0.0013, 0.244) through the drift fit on [6.5, 12] and on [6.5, 20.5], and its extrapolation | ṙ∞ 1e-5, extrapolation 1e-5 |
| BR | bracket ends are collapse and expansion, the replayed bisection equals lo and hi, hi − lo ≤ 1e-14, h as its float repr | 1e-14 |
| P266 | this machine's p*ₕ equals #266's G (B = 0.1) | 1e-13 |
| EVT | the chain's first trapped cell equals the pair's collapse-side one; fates −1, +1 at p*ₕ ∓ δ | equal |
| RC5, RC4, RC8 | every run ends at the declared limit (F_end in [0.5, 1) F_max, horizon ≥ Nc/8 from the edges); first law with both fields to F = 20; M_AH settled (plateau change ≤ 1e-4, flux ≤ 1e-5) | 0.5 F_max; 2e-2; 1e-4, 1e-5 |
| RH | \|plat(0.01) − plat(0.005)\| at each δ | 5e-5 |
| RC6-ph | second order in h over three h, three windows (post hoc: needs h = 0.02) | observed order 1.5 to 2.5 (fails in dev for e ≥ 9; reported) |
| R266 | δ = 1e-8 reproduces #266's G (B = 0.1): the plateau, γ₁, r_th at departure | 1e-6 |
| R253 | every δ's plateau reproduces #253's scan (rpi5, #40's p*ₕ) at h = 0.01, 0.005 | 1e-4 |
| TG | the lifetime T at p*ₕ ∓ δ gains 1.8 to 2.5 per decade on both sides, e = 7 … 12 | [1.8, 2.5] |
| TDEP | t_dep(1e-3) gains 1.9 to 2.1 per decade, e = 7 … 12 | [1.9, 2.1] |
| LIN | \|odd\|(t)/δ at t = 10, 11 agrees for δ = 1e-8, 1e-9, 1e-10 (the mode is linear and the same) | relative spread 2e-3 |
| LIN2 | the same at δ = 1e-11 and 1e-12 differs from it by at most the roundoff realization | 5e-2 |
| TRAJ | the member's r_th(t), γ₁(t) at t = 11, 12, 13 is the same for every δ whose odd part there is below 3e-4 | r_th 2e-5, γ₁ 1e-5 |
| FITQ | the fit of M(r) on the two sides at departure has rms ≤ 1e-4 | 1e-4 |
| HST | **the issue's acceptance 1:** γ₁ and r_th at departure at h = 0.01 and 0.005 agree for each of the six δ | 1e-4 relative (fails at e = 12 in dev) |
| SMOOTH | **weak:** the six (γ₁, r_th, M) satisfy M = c₀ + p γ₁ + q r_th (any smooth M(δ) does) | 6e-5 |
| PRED | **the issue's acceptance 2, the declared prediction:** M(δ) = r_th [M₀ + a γ₁ + b γ₁²] from #266's four B at the same h, for each of the six δ at h = 0.01 and 0.005 | 6e-5 (fails in dev: up to 9e-4) |
| DR255 | #255's D = 4 fit is reproduced (pair 1e-10, h = 0.01 and 0.005): ṙ∞, κ, r_th − 1 at t = 8, 10, 12 | 2e-5, 0.01, 1e-5 |
| DREXT | **the issue's acceptance 3 (the drift):** the model fitted on [6.5, 12] predicts the measured dr_th/dτ over t = 14 to 20 (pair 1e-12); the fit on [6.5, 20.5] gives ṙ∞ within 2e-4 of it | 1e-4, 2e-4 |

Reports with no bar (printed, gate nothing, labelled post hoc where they were suggested by the data): the member at ε = 1e-2 and on the collapse side alone; the prediction without the r_th scaling and with the member read at ε = 1e-2; the decomposition of dM into the
parts assigned to r_th and γ₁; the scan's own fit dM = p dγ₁ + q dr_th and its condition number; the part of dM not carried by r_th; the three-parameter relation; dr_th/dτ along the stall and the D = 5/D = 4 ratio.

The checks that fail in the development set (HST at e = 12, PRED, and the post hoc RC6-ph, FITQ-ph, HST-ph, PRED-ph) are in every mutation's fired set. Each mutation's set was computed on the development set (`dev/mut/`, with the final code) before being declared:

| mutation | what it does | fires (beyond the six that fail without a mutation: HST, PRED, FITQ-ph, HST-ph, PRED-ph, RC6-ph) |
|---|---|---|
| `asym_sign` | #225's `fit_asym` with the sides swapped | PMEM, PPOS, PTD |
| `bisect_early` | the bracket of the bisection after 30 steps instead of the last | BR, BR-ph |
| `crit_dm` | dm = 2.0 in the chain constants | CFG |
| `delta_off` | the reference run at δ × 0.1 (e = 9) against the pair at e = 8 | EVT, R253, R266, RH, SMOOTH, TG |
| `dep_eps` | ε × 10 in the departure time (#266's) | PDEP, PPOS, PTD |
| `drext_win` | the drift model fitted on [10.5, 12] instead of [6.5, 12] | DREXT |
| `drift_win` | the drift window [8, 12] instead of [6.5, 12] | DR255 |
| `eps_h` | ε × 100 at the finest h only (#266's) | FITQ, SMOOTH |
| `family_B` | B = 0.11 in the chain at the reference run (e = 8, h = 0.01): the chain refuses | LIN, LIN2, R253, R266, RH, RUNS, SMOOTH, TDEP, TG |
| `fitq_scale` | the fit residual × 10 | FITQ |
| `flux_sign` | the horizon flux with the wrong sign | RC4, RC4-ph |
| `h_plat` | the plateau at h = 0.02 in place of 0.005 in RH | RH, RH-ph |
| `lin_scale` | |odd| of e = 10 × 2 | LIN, LIN-ph, LIN2, LIN2-ph |
| `lin_scale12` | |odd| of e = 12 × 1.2 | LIN2, LIN2-ph |
| `mass_exponent` | M = r^n/2 in place of r^(n−1)/2 in the chain at the reference run | R253, R266, RC4, RH, SMOOTH |
| `no_settle` | every series cut 3.0 short in x⁺ | R253, R253-ph, R266, R266-ph, RC5, RC5-ph, RC8, RC8-ph |
| `pneg_off` | the planted extra dependence removed (the negative control must fire) | PNEG |
| `ppos_off` | the planted M offset by 1e-4 | PPOS |
| `pstar_h_swap` | #266's p*ₕ of the next h in P266 | P266, P266-ph |
| `ptd_lambda` | the planted truth with λ × 1.05 | PPOS, PTD |
| `rdot_nolapse` | τ = t (the lapse dropped) | DR255, PDR |
| `rel_perm` | #266's planted M rolled by one in PREL | PREL |
| `short_limit` | K = 12 at the reference run: the chain stops at e^{−f} = 6144 | R253, R266, RC5, RC8, RH, SMOOTH |
| `smooth_swap` | M of e = 10 and e = 11 exchanged in SMOOTH | SMOOTH |
| `tau_unit` | τ in units of √2 t | DR255, PDR |
| `tdep_e9` | ε × 10 at e = 9 only | SMOOTH, TDEP, TDEP-ph |
| `tg_flat` | the lifetimes at e and e − 1 taken equal | TG, TG-ph |
| `traj_shift` | the row of e = 9 read 0.5 later in t | TRAJ, TRAJ-ph |

## Runs of record

`scripts/run_one.sh` (the bisection of p*ₕ for an h, or the chain and the pair for an (h, e)) and `scripts/run_jobs.sh` (two lanes, nice 10, `NUMBA_NUM_THREADS=1`, a log, an err and an rc for every stage, reruns numbered, never overwritten).
Order: `jobs_pstar.txt` (h = 0.02, 0.01, 0.005: the three bisections, then P266), then `jobs_rec.txt` (e = 12 … 3 at h = 0.005, 0.01, 0.02: 30 jobs). Both detached with `nohup`. A job not finished in 2 h of wall time is stopped and reported (the longest development job took 81 s).
`python3 settled_mass_member.py analyze --raw=<this folder>` (about 1 min), then `scripts/run_muts.sh <this folder> <this folder>/mut LANE 2` (28 mutations, about 15 min on two lanes), each compared with the set above. The figure (`plot_settled_mass_member.py`, written after the runs) uses `/arriba:graph-data`'s `data_graphs.py`.

## Limits stated before the runs

- D = 4, B = 0.1 and δ ≤ 1e-7 for the gating δ; h = 0.01, 0.005 (0.02 post hoc). p*ₕ is bisected on this machine and equals #266's (P266).
- The member is read at ε = 1e-3 (mine); #266 found the relation depends on that reading at the 1e-4 level, so it matters less than the 1e-3 to 1e-4 differences measured here.
- At δ ≤ 1e-11 the pair is at the roundoff floor of the evolution (LIN2); the quantities read there are good to the realization scatter, not to the truncation error.
- The chain is #41's, unchanged; the roundoff-realization scatter of the plateau is #253's (6.6e-6 at h = 0.005, 2.5e-5 at 0.01), not remeasured.
- The planted cases test the extraction, the departure time, the prediction test and the drift fit, not the evolution; the chain's planted truths stay #41's.

## Changes made after this README

None. (The criteria, bars and mutation sets above are as committed at d534bf03, before any run of record.)

## Results of record (after the runs)

- Runs: `jobs_pstar.txt` (3 bisections, rc 0, p*ₕ equal to #266's bit for bit) and `jobs_rec.txt` (30 jobs, rc 0), 20:13 to 20:19, two lanes; logs in `runs/G_B0.1/h<h>/{logs,e<e>/logs}` and `logs/`.
- `analyze_record.log` (`python3 settled_mass_member.py analyze --raw=<this folder>`, code 09d549f): 48 checks, 29 gating, 19 post hoc; **two gating checks fail, HST (δ = 1e-12 only) and PRED**, and four post hoc (RC6-ph, FITQ-ph, HST-ph, PRED-ph): the same verdicts as the development set.
- `mut/`: 28 mutated analyses of the records, **28 of 28 fire exactly their declared set** (MATCH); `logs/mut_lane*.log` truncate the summary line at 300 characters, the MATCH is in each `mut/<name>.log`.
- `settled_mass_member.svg` (`plot_settled_mass_member.py`, vendored `data_graphs.py` equal to the graph-data skill's): M(δ) with the prediction, the residual, and r_th(t) along the stall.
- Note, output and code: `notes/wormhole_evolution/settled_mass_member.{md,py}`, `settled_mass_member_output.txt` on branch `wip/i267-mass-vs-member`.
