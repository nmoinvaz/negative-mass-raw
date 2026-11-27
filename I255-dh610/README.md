# I255-dh610: what drifts the throat radius of family G at D = 5 (B = 0.04, 0.1, 0.2), and the expanding member A = 0.05 at X = 160

Machine: dh610-fedora (Fedora 45, 20 threads, shared with choptuik-large-d, load average 18 of 20 at the start). At most 4 processes, one thread each, `nice -n 10`.
Issue: https://github.com/nmoinvaz/negative-mass/issues/255 (it serves #42; follow-ups 3 and 5 of #225). Worktree `~/Source/negative-mass-i255`, branch
`wip/i255-g-drift`, base main 5ffd461. Python `~/Source/negative-mass-venv314/bin/python`. Status words as in AGENTS.md: every number below is *numerical
evidence* unless marked. No sentence here says a result is new.

This file is written in stages and says at each stage what had been run. Nothing in a stage is changed after a later stage has seen data.

## Stage 1: the prediction (written after the development runs dev_01 to dev_05 on #225's stored B = 0.1 data, before any run with B != 0.1 and before any new code)

What the development runs read (`dev/`, all from #225's `I225-dh610/runs/stall`, the pairs p*_h -/+ 1e-9, family G, B = 0.1):

- `dev_01`: the throat radius of the pair's mean, r_th(t) = 1.0105 (t = 4), 1.0502 (5), 1.0589 (6), 1.0714 (7), 1.0879 (8), 1.1078 (9), 1.1293 (10), 1.1522 (11), 1.1759 (12), 1.2000 (13)
  at D = 5, h = 0.00354; at D = 4 it falls from 1.0241 (t = 5) to 1.0029 (t = 13). The two sides of the pair differ (the unstable mode) by at most 7e-4 up to t = 12.
- `dev_02`: on the locus the ghost energy density is the equilibrium one of a static throat of that radius, rho_g = -n(n-1)/(2 r_th^2), to 4e-4 at t = 13 (ratio 1.0131 at t = 6
  falling to 1.0004). The normal field's energy density on the locus is 1e-7 or less from t = 11 (it has left). The charge flux per unit t through the locus is constant at D = 4
  (1.381 to 1.397 over t = 6 to 13) and rises from 2.46 to 3.40 at D = 5, as sqrt(n(n-1)) N_th r_th^(n-1) with N_th = dtau/dt on the locus.
- `dev_03`: the Misner-Sharp mass at fixed areal radius is constant in t from t = 12 at D = 4 and drifts at D = 5 (at R = 2 by +0.016 per unit t on the + side and +0.019 on the - side between t = 8 and 14).
- `dev_04`: the radial velocity of the throat, dr_th/dtau (local linear fit over +-0.5 in tau), fitted over t in [6.5, 12] by
  `rdot(tau) = rdot_inf + c exp(-kappa (tau - tau_0))`: D = 5, h = 0.00177: rdot_inf = +0.02602 +- 4e-5, kappa = 0.481 +- 0.004, rms residual 8.8e-5 over 107 points;
  D = 4, h = 0.005: rdot_inf = +0.0013 +- 2e-5, kappa = 0.244. So at D = 5 the throat radius is not relaxing to a static value: its velocity approaches a constant (H = d ln r_th/dtau
  is constant at 0.021 from t = 10 to 13). The pulse integrals on the initial ray, I_2 = integral of r^n (dg/ds)^2 ds = 10.081 (D = 4), 38.730 (D = 5), with g the unit Gaussian
  (centre 3, width 0.5, r from the static wormhole), and I_1 = integral of r^n dg/ds ds = -3.760, -19.945.

**Power counting (the structural claim).** The normal field is a test field at first order in B: it enters the metric and the ghost field only through its stress, which is B^2.
The ghost pulse A enters at first order, and the unstable mode's amplitude is alpha A + beta B^2 + O(A^2, A B^2, B^4), so the tuned amplitude is A* = p*_h(B) = kappa B^2 + O(B^4).
The cross term of the ghost pulse's energy with the background vanishes (the integral of dg/ds is zero), so the ghost pulse's energy is -A*^2 I_2, fourth order in B, and the net
energy the pulses leave is E_net(B) = (B^2 - A*^2) I_2. Every effect of the tuned data on the throat is therefore second order in B, with the same time dependence:

    r_th(tau; B) - 1 = B^2 g(tau) + O(B^4),   p*_h(B) = kappa B^2 + O(B^4),   rdot_th(tau; B) = B^2 g'(tau) + O(B^4).

The alternative, first order in B, gives exponent 1 in all three. At B = 0.1 the throat radius is already 0.2 above 1 at t = 13, so the O(B^4) terms are of relative size
about R(B) = r_th - 1 itself (3 % at B = 0.04, 20 % at 0.1, order 1 at 0.2). That is why the gates below are exponents, with bands that exclude exponent 1 and allow the
nonlinearity, and why B = 0.2 is a reported measurement of the nonlinearity, not a pass/fail test of the scaling.

**Predicted values** (from B = 0.1 and the scaling; D = 5; the reference values are #225's pairs at the same h, the exponent is the claim):

| quantity | B = 0.04 | B = 0.1 | B = 0.2 (linear extrapolation, reported only) |
|---|---|---|---|
| p*_h / p*_h(0.1) | 0.16 | 1 | 4 |
| r_th(tau) - 1 relative to B = 0.1 | 0.16 | 1 | 4 |
| rdot_inf (velocity the throat radius approaches) | 0.0042 | 0.0260 | 0.104 |
| transient rate kappa | 0.48, B independent | 0.481 | 0.48 |
| E_net = (B^2 - A*^2) I_2 | 0.0619 | 0.383 | 1.48 |

**What is not predicted.** The mechanism: why the velocity of the throat radius approaches a constant at D = 5 and (to 0.0013, a factor 20 smaller) at D = 4. The candidates read in
`dev_02` and `dev_03` are (i) a flux of the normal field through the locus (ruled out as the driver after t = 8: its energy density there is 1e-7), (ii) the unstable mode (ruled
out: the odd part of the pair is at most 7e-4 up to t = 12), (iii) a resolution effect (ruled out for B = 0.1: three h agree to second order), (iv) the constraint plateau of #226
(roundoff of 1e-11 against a drift of 0.02), (v) the observer (the minimum of r on a slice; planted moving throats of #225 recover r_th = 1). Not ruled out: a generalized zero mode
of the static family (a throat radius with a constant velocity, a Jordan block of the linearization), a slowly decaying tail of the ghost field in the region 2 < r < 8 (the mass at
R = 6 to 8 on the + side changes by 0.01 to 0.02 between t = 8 and 14 at D = 5), and a drift of the lapse relative to the far region. The note will say which of these the B scan
and the h scan bear on, and call the cause "not established" unless a check can fail on it.

## Stage 2: the criteria (written after the development runs dev_06 to dev_12 and the mutation runs in `dev/mut`, before the first run of record)

Everything here is the `CRIT` and `MUTATIONS` tables of `notes/wormhole_evolution/throat_drift.py` at the commit named in "Code" below, in words. The driver imports `dn.py`, `checks.py`,
`threshold.py`, `expansion.py` and `throat_locus.py` unchanged. A criterion that is not met is reported as not met; no bar, family, resolution, window or bound is moved after a run of
record has been seen. A control that fires on real data stops the work until the cause is known.

**Development runs (kept, none edited; `dev/`):** dev_01 to dev_05 the reads of #225's stored B = 0.1 pairs (above); dev_06, dev_07 the control pair and #40's 8 points rerun through the
new code (bit for bit, below); dev_08, dev_11 the development suite (stored pairs as the B family with a planted exponent, planted evolutions, expansions from #225's X = 100 files);
dev_09, dev_10 the control bisection at D = 4 (run 1 stopped at a bracket of 4.7e-12 because the triangle covered t <= 30, too short for a run within 5e-12 of p*_h at D = 4; the
cap was made to grow with the bracket (`bis_tcap` + ln(1/(hi - lo))/W, x 1.4 on a retry), run 2 reached 5.9e-13); `dev/mut_run1` the first mutation runs (12 mutations, before CT4 and
the cap), `dev/mut` the final ones. No run with B != 0.1 was made. The brackets for B = 0.04 and 0.2 are the declared ones below, not scanned.

**Code.** `notes/wormhole_evolution/throat_drift.py` at **6f060f4** (branch `wip/i255-g-drift`), committed and pushed before this stage was committed and before any run of record. The first
`bis_loose` mutation run (`dev/mut/mut_bis_loose.log`) also changed CT1 and CT2, only because its mutated control directory held no CT1/CT2 files; with them copied in
(`mut_bis_loose_r1.log`) it changes CT4 alone. The development suite (dev_11): 22 of 23 checks pass, KX2 fails by construction (#225's X = 100 runs are GROW at 1.2024).

**The runs of record.** All use `dn.row_step` row by row on a triangle (`throat_locus.sweep`), nothing stored but the locus series and the profile of every slice t = 2, 3, ...
The rectangle runs of the expanding member stream the same way (two rows of the grid and the locus's per-slice bookkeeping are kept, O(X/h) numbers: 22 627 nodes at h = 0.00707 and
45 255 at h = 0.00354 for X = 160; the grid of N^2 = 5e8 and 2e9 cells is never held).

| item | declaration |
|---|---|
| D = 5, family G, B | 0.04, 0.1, 0.2 (ghost amplitude A tuned, normal amplitude B, both Gaussian in phi, centre 3, width 0.5, on the ray x- = 0; eps = (-1, +1)) |
| D = 5, h | 0.00707107, 0.00353553, 0.00176777 (`threshold.CRIT['H'][3]`, exact floats; the gates use the two finest) |
| p*_h | B = 0.1: #40's (`I40-dh610`, same floats). B = 0.04, 0.2: bisection of #40's events (collapse = first row with a trapped cell, expansion = first diagonal anti-trapped cell with r >= 2) to hi - lo <= 1e-12; bracket (0.3, 3) x (B/0.1)^2 p*_h(0.1, h); an end without its fate is moved by a factor 2, at most 4 times, and reported |
| the pair | A = p*_h -/+ 1e-10 (B = 0.1 too, rerun), kept whole to the first events on #40's and the locus's levels (r_min = 0.5, 2); the tuned series is the pair's mean on the slices both have |
| D = 4 (reported, not gated) | B = 0.04, 0.1, 0.2 at h = 0.02, 0.01, the same procedure; B = 0.1 from #40 |
| the expanding member | D = 5, family G (B = 0.1), ghost amplitude A = 0.05, rectangle X = 160 (t to 226), h = 0.00707107, 0.00353553; #213's classes and k on the locus's proper time (`throat_locus.expansion_summary`) |
| planted | PL1 static throat of radius 1.2 (D = 5, h = 0.02, 0.01, 0.005, t in 0.8 to 2.7); PL2 static throat moving with v = 0.13, -0.3; PL3 synthetic rdot series; PL5 #213's five class series; PX planted B families |
| fit window | rdot(tau) = rdot_inf + c exp(-kappa (tau - tau_0)) over t in [6.5, 12] where the pair's odd part (r_+ - r_-)/2 is at most 3e-4; rdot is the slope of a local linear fit of r_th over +-0.5 in tau |
| times | r_th - 1 compared at t = 8, 10, 12 |

**Checks (each can fail), with bars:**

| id | check | bar |
|---|---|---|
| PS | exponent of p*_h(B) between B = 0.04 and 0.1 at the two finest h | in [1.8, 2.4] (first order gives 1) |
| PR | exponent of r_th(t) - 1 between B = 0.04 and 0.1 at t = 8, 10, 12 at the two finest h | in [1.8, 2.4] |
| PV | exponent of rdot_inf between B = 0.04 and 0.1 at the two finest h; kappa(0.04)/kappa(0.1) | [1.8, 2.4]; [0.75, 1.25] |
| CV | r_th(10) - 1 over the three h, each B: observed order; the two finest differ | in [1.7, 2.3]; by at most 1 % |
| NO | the pair's odd part in the fit window, each (B, h) | at most 3e-4 |
| QS | on the locus |rho_g / rho_eq - 1|, rho_eq = -n(n-1)/(2 r_th^2), t in [8, 12], each (B, h) | at most 5e-3 |
| JOB | the pair has fates (collapse, expansion) on #40's events and the locus's levels; the bisection finished to 1e-12 without "static through X" | exact |
| CT1 | 8 of #40's recorded points of G (B = 0.1, h = 0.00707) rerun through `make_data_B`: fate, event cell, T | bit for bit |
| CT2 | the pair at B = 0.1, delta = 1e-9, h = 0.00707 rerun: r, l, f, tau, v against #225's stored | 1e-12 |
| CT3 | the X = 160 locus series against #225's X = 100 on every slice inside both rectangles | 1e-12 |
| CT4 | the bisection of this work at B = 0.1 (D = 4, h = 0.02) against #40's p*_h | 2e-12 |
| DL | the tuned mean at delta = 1e-9 (#225) and 1e-10 at B = 0.1, t in [7, 11] | 1e-5 |
| RV | rdot_inf of the B = 0.1 tuned series at the finest h against dev_04's 0.02602 | 5 % |
| PL1 | the planted static throat of radius 1.2: r_th and rdot = 0, second order | 2e-4, 5e-4; orders in [1.75, 2.25] |
| PL2 | the planted moving throat: r_th = 1 and rdot = 0 | 5e-4, 1e-3 |
| PL3 | the synthetic rdot series through the same fit: rdot_inf, kappa | 1e-5, 0.5 % |
| PL5 | #213's five planted class series | exact classes |
| PX | planted B families from #225's pairs, exponents 2 (gates PS, PR, PV pass), 1 and 3 (all three fail) | exact |
| KX2 | the expanding member, both h: class FT with tau_s / tau_end <= 1.2 (#213's bound) | exact |
| RES2 | the two h: same class, H at r/a = 10, 25, 50, k and tau_s | 1 % |

B = 0.2 is reported (exponents between 0.1 and 0.2, the nonlinearity), not gated, except by JOB, NO, QS and CV. The energy table (E_net = (B^2 - A*^2) I_2 against rdot_inf), the Misner-Sharp
mass at R = 2, 3, 4 on both sides, the lapse N_th, the charge flux q_t and the whole D = 4 table are reported. The mechanism is named only with the status word it earns.

**Mutations** (`--mutate=NAME`; each target is the set of checks whose verdict changes against the unmutated development suite, computed in `dev/mut` before this was written):

| mutation | what it breaks | targets |
|---|---|---|
| b_label | B labelled sqrt(0.1 B) | PR, PS, PV, PX1, PX2 |
| pstar_swap | p*_h of B = 0.04 and 0.2 exchanged | PS, PX2 |
| r_not_r1 | r instead of r - 1 in the exponent | PR, PX2 |
| rdot_swap | the rdot fits of B = 0.04 and 0.2 exchanged | PV, PX2 |
| cv_swap | the h in the wrong order | CV |
| rho_nolapse | e^f dropped from the stress on the locus | QS |
| rth_diag | the diagonal's radius instead of the locus's | CV, PL2, QS, RV |
| tau_unit | tau in units of sqrt2 t | PL3, RV |
| odd_off | one side of the pair instead of the mean | DL |
| pstar_off | run level: p*_h shifted by 3e-9 in the control pair | CT2 |
| bis_loose | run level: the control bisection stopped at 1e-9 | CT4 (computed in `dev/mut`) |
| ts_bound | the bound on tau_s / tau_end relaxed to 1.32 | KX2 (flips to pass in the development suite, whose expansions are #225's X = 100 runs: GROW) |
| ts_scale | the coarse run's tau_s scaled by 1.02 | RES2 |

**Planted truth before real data.** PL1 and PL2 run the same locus code on exact static throats (known r_th, known zero rate), PX runs the three gates on families of known exponent, PL3 the fit on a known
rdot(tau); all passed in the development suite (dev_11) before any run of record: PL1 4.6e-5 and 7.3e-5 (bars 2e-4, 5e-4) with orders 1.99; PL2 1.2e-4, 2.2e-4; PL3 8.1e-8.

**Jobs and cost.** `scripts/make_queue.py` writes `runs/queue.txt` (longest first); `scripts/lane.sh` runs it in four lanes, one thread each, `nice -n 10`, `timeout 7200` per job,
logs `runs/logs/job_<name>.{log,time,rc,lane}` never overwritten (a rerun gets a number). Measured in development: one D = 5 run to the event costs 14 s (h = 0.00707) and 45 s (h = 0.00354); the
finest h about 3 to 5 min, so a bisection at h = 0.00177 is about 1 to 1.5 h, inside the 2 h stop. The X = 160 runs: #225's X = 100 took 97 s and 414 s, so about 4 min and 18 min.
Memory is reported (`/usr/bin/time -v`), not a stop condition.

## Stage 3: rulings and changes during the runs of record (written while the runs were going; nothing in Stage 1 or 2 changed)

- **Rulings (coordinator, over hc).** Q1: no waiver of the 2 h stop for B = 0.2 at h = 0.00177; the job ends at its `timeout 7200` and is reported as stopped with what finished
  (`bisect/D5_B0.2_h0.00176777/points.jsonl`), and B = 0.2 is reported at the two h that finished. Q2: yes to a **post-hoc supplementary scan**, D = 5, B = 0.02 and 0.07 at
  h = 0.00707 and 0.00354, the same `bisect_stall` procedure, output in `runs/extra/`, run after the declared runs, gating no criterion; PR and PV stay as declared.
- **What the declared runs showed on the way** (the first `analyze` over the finished jobs, `runs/analysis_partial1.log`, which stopped on a report-only bug in the mass table):
  NO fails at B = 0.04 (max |odd| 3.4e-4 against 3e-4 at the end of the window; the fit mask drops the points above 3e-4); QS fails at B = 0.2, h = 0.00707 (1.0e-2 against 5e-3); JOB fails at
  B = 0.2: the + side run (A = p*_h + 1e-10) does not reach #40's expansion event inside the triangle (t <= 34; near threshold at B = 0.2 the expansion event is at t = 52 to 56 on the
  diagonal) and the locus's r_min = 2 level is crossed on both sides (the throat radius exceeds 2 during the stall), so the locus fates are (+1, +1). Not changed; reported.
- **Code after 6f060f4.** Report-only additions and the bug fix of the mass table go in a later commit (named in the note); no check, bar, window or mutation changes.

## Stage 4: results (after the runs of record, the analysis in `runs/analysis_record2.log` = `notes/wormhole_evolution/throat_drift_output.txt`, driver at a44d066)

Jobs (`runs/logs/job_*.{log,time,rc,lane}`, `runs/logs/lanes.log`): 18 declared jobs, all rc = 0 except `bs_D5_B0.2_hk2` (rc = 124, the 2 h timeout: 33 runs, bracket not finished; its points are
`runs/bisect/D5_B0.2_h0.00176777/points.jsonl`; no waiver, coordinator's ruling Q1); the 4 post-hoc extras (`*_extra`, `runs/extra/`) rc = 0. Longest finished job 57 min (`bs_D5_B0.2_hk1`), the X = 160
expansions 4 min and 31 min, peak memory 306 MB (`/usr/bin/time -v`), load average 12 to 23 of 20 (four lanes, nice 10).

| result | value |
|---|---|
| checks | 37 of 48 pass; fail: PR, PV, NO (B = 0.04, three h), QS (B = 0.2, two h), JOB (B = 0.2, three h), CV (B = 0.2) |
| PS | p*_h exponent between B = 0.04 and 0.1: 2.044 (h = 0.00354), 2.107 (0.00177): met |
| PR | r_th - 1 exponent: 2.610, 2.769, 2.857 (t = 8, 10, 12; h = 0.00354); 2.602, 2.761, 2.851 (0.00177): not met |
| PV | rdot_inf exponent 3.163, 3.162; kappa ratio 1.026, 1.033: not met (exponent) |
| rdot_inf (h = 0.00177) | B = 0.04: +0.00144 +- 6e-6; B = 0.1: +0.02602 +- 4e-5 (D = 4: B = 0.1 +0.00133, B = 0.04 0.0000 +- 4e-6) |
| expanding member (D = 5, A = 0.05, X = 160) | FT at both h, k = 3.9957, tau_s / tau_end = 1.1759, 1.1760 (KX2 and RES2 met; X = 100: GROW, 1.2024) |
| mutations on the record | `runs/mut/summary.txt`: every declared target fires except where the check already fails in the unmutated record (PR, PV) and `ts_bound` (KX2 passes under both bounds) |

Contents of `runs/`: `bisect/D<D>_B<B>_h<h>/{summary.json,points.jsonl}` (every bisection run: amplitude, fate, T), `stall/stall_D<D>_B<B>_h<h>_d1e-10_side{-1,1}.npz` (the pairs), `expand/G_D5_0.05_h<h>.npz`,
`ctl/` (CT1, CT2, CT4), `extra/` (the post-hoc scan, same layout), `mut/` (mutation runs on the record), `analysis_partial1.log` (the first analysis, which stopped on a report-only bug), `analysis_record1.log`
(before the energy table), `analysis_record2.log` (of record), `queue.txt` (empty: every line was taken), `logs/`.

**Discrepancies reported, not repaired:** PR and PV not met; NO at B = 0.04 by 13 %; QS at B = 0.2; JOB at B = 0.2 (triangle cap t <= 34 inherited from #225 is shorter than the + side's expansion event at t = 38 to 56
and the locus's r_min = 2 level is crossed on both sides while the throat radius exceeds 2); B = 0.2 at h = 0.00177 not finished. The prediction in Stage 1 was right about the threshold (p*_h ~ B^2) and wrong about the radius and its speed.
