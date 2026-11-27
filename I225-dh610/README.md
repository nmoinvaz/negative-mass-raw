# I225-dh610: the one-sided threshold family G's lifetime along the throat locus (D = 4, 5), the static member at the stall, and the expanding side on the locus

Machine: dh610-fedora (Fedora 45, Linux 7.3.3, Intel i7-12700, 20 threads, 62 GB), shared with choptuik-large-d (load average 14 to 21 of 20 during the
development runs). At most 4 processes, one thread each, `nice -n 10`. Issue: https://github.com/nmoinvaz/negative-mass/issues/225 (it serves #42).
Worktree `~/Source/negative-mass-i225`, branch `wip/i225-throat-locus`, base main 76f7178 (`dn.py`, `checks.py`, `threshold.py`, `expansion.py`, `ellis_efold.py` unchanged, imported
read-only). Python `~/Source/negative-mass-venv314/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1, numba 0.68.1). The evolution is #39's `dn.row_step`, unchanged, called row by row
on a triangle of the grid; the driver is `notes/wormhole_evolution/throat_locus.py` at **9a3079d**, committed and pushed before this README and before any run of record.

**This README was written after the development runs `dev/dev_01` to `dev/dev_12` and the mutation runs `dev/mut/` listed below and before the first run of record.** Everything under
"Declared" is the `CRIT` and `MUTATIONS` tables of `throat_locus.py` at 9a3079d, in words. Nothing there is changed after a run of record has been seen. A criterion that is not
met is reported as not met. A control that fires on real data stops the work until the cause is known. Status words as in AGENTS.md: every number below is *numerical evidence*
unless marked *proved* or *checked symbolically*. No sentence here says a result is new.

## Contents

```
I225-dh610/
├── README.md
├── scripts/            make_queue.py (writes runs/queue.txt), lane.sh (one lane of the queue), devlane.sh, mutlane.sh
├── dev/                development runs (kept, none edited): dev_NN_*.py, logs, mut/ (the mutation runs that computed the targets), _stopped_run0_* (see below)
└── runs/               runs of record
    ├── queue.txt                        the queue as written (lines are removed as lanes take them)
    ├── series/D<D>_G_h<h>/              points_<i>of<m>.jsonl: one record per run (the amplitude, #40's event and time, the locus's level crossings in t and tau)
    ├── stall/stall_D<D>_h<h>_side<s>.npz   the two runs p*_h -/+ 1e-9 kept whole: the locus series and the profiles of every slice t = 2, 3, ...
    ├── expand/<family>_D<D>_<member>_h<h>.npz   the expanding runs (rectangle): the locus series and the diagonal series
    ├── planted/ps_D<D>_hk<k>_v<v>.json  the planted lifetime series
    ├── logs/job_<name>.{log,time,rc,lane}, lanes.log
    └── analysis.log                     `throat_locus.py analyze` on the above (= notes/wormhole_evolution/throat_locus_output.txt)
```

## Rulings received (coordinator's brief and replies, over hc)

1. **The work**, as the issue and the brief state: the minimum of r on each slice t = const (the locus), its position l(t), drift dl/dt and proper time tau; the collapse and expansion events read on the
   locus; the lifetime slope in tau against ln(1/|p - p*_h|) of #40's family G (ghost pulse A tuned, normal pulse B = 0.1 on the same ray, eps = (-1, +1)) at D = 4 and 5 at two h; planted: a static
   wormhole whose throat moves with a known velocity in the grid's coordinates (x+ and x- rescaled by lam and 1/lam), recovering the velocity and the unboosted e-fold; control: #40's diagonal slope
   (0.898 at D = 4, h = 0.01); the member at the stall (throat radius, asymmetry by the two end masses, the normal field's charge) and the comparison of its e-folding time (#151's T(gamma_1), or what applies
   with a normal charge) with the locus slope, reported whether or not they agree; the expanding side (#213's addition): the classes, H/W at r/a = 10, 25, 50 and k on the locus.
2. **Project rules over the runner rules**: the issue stays open (the coordinator reviews and closes); a failed check is a result, never loosen a criterion or a tolerance after seeing data, never move
   families, resolutions, windows or definitions after a development run without asking; ask before replacing a declared planted case or control; each check has a `--mutate=` whose targets are computed in a
   development run before they are declared; status words as in AGENTS.md (slopes and members are *numerical evidence*); no sentence claims novelty; keep every log, never overwrite one, number reruns.
3. **An error of the brief, recorded here and in the note** (found in the development runs, reported to the coordinator, who confirmed it): the brief reads #40's stall table as "dl/dt = +0.58 at D = 4, +0.25 at D = 5".
   In `threshold.md` the table's columns are the locus's position l = (x+ - x-)/sqrt2 and then its drift dl/dt: +0.584 and +0.0735 (D = 4), +0.254 and +0.127 (D = 5); the raw `I40-dh610/runs/D4_G_h0.01/stall.json`
   has `l` = 0.5842, `v` = 0.0735. So +0.58 and +0.25 are positions. **The coordinator's ruling: keep the planted drifts chosen here (v = 0.1, 0.5 and 0.13).**
4. **The coordinator's ruling on the declarations**: they should test the D = 4 result (the locus slope matches the stall member's T(gamma_1) r_th) and the D = 5 drifting scale; declare them before the runs of record
   (checks CMP1 to CMP3 and DR below).
5. **#41's note on #225** (optional, "do it only if it fits, otherwise say so in the closing comment"): run #41's settled-mass chain (`settled_mass.py`, on main only, not in this worktree) for family G, M_AH(t) second
   order at three h, planted cases unchanged, against 0.2231 a. Decision: **not run in this issue.** The chain is on main only (this worktree is at 76f7178, before #41's merge), it needs p*_h of G on its own machine at each h, its own planted and control checks
   and a declaration of its own, and the files this task may write do not include a driver for it. It is recommended as a separate task (closing comment); the D = 4 member found here (gamma_1 = 0.048, r_th = 1.003, no normal charge)
   is the expectation to test: a settled mass different from S's 0.2231 a would then not come from the static member.
6. Threads and memory: at most 4 processes, `nice -n 10`, long runs as `systemd-run --user` units `nm-i225-*`; any single run not finished in 2 h is stopped and reported (`timeout 7200` in `lane.sh`);
   memory is reported only.
7. Files: `notes/wormhole_evolution/throat_locus.py`, `throat_locus_output.txt`, `throat_locus.md`, and this folder. Close with a comment, remove `running`, leave the issue open.

## What the development runs showed before anything was declared (reported, none of it fixed)

1. **The diagonal is the wrong observer for G, and a drift of 0.1 is enough.** At D = 4, h = 0.02 the same runs give #40's diagonal slope 0.898291 (bit for bit, all 40 points) and the locus's proper-time slope
   0.8501 +- 0.0007 (+0.5 % over 1/W = 0.846045; the coordinate-time slope on the locus is 0.871, +3.0 %, the rest is the lapse e^{-f/2} = 0.976 at the locus). The planted case says why: family S
   in coordinates in which its static throat drifts at v = 0.1 reads 0.9122 (+7.8 %) on #40's diagonal events and 0.84605 (+8e-6) on the locus (dev_11); v = 0.5: 1.018 (+20 %) and 0.84579 (-3.1e-4).
2. **At D = 4 the stall is a member of the static family.** On p*_h -/+ 1e-9 (dev_09), t = 10 to 16: r_th = 1.0050 to 1.0021, s_th = r_th N'/N = +0.048 (gamma_1 = 0.048), the normal field's charge
   ratio |q_n^2/q_g^2| below 1e-5, the drift 0.074 to 0.082 and the lapse f = 0.05; the growth rate of the unstable mode from the difference of the two runs is 1.1799 (1/lambda = 0.8475); GGS09a's
   T(0.048) r_th = 0.8472 (ratio 1.0004). The brief's remark that G's static end state may carry a normal charge is not what is seen at D = 4: the charge is zero to 1e-5 and the pulse's normal field has gone.
3. **At D = 5 the throat has no plateau.** r_th on the locus rises from 1.05 (t = 5) to 1.21 (t = 14) at h = 0.00707, s_th = 0.12 to 0.17, and the pair rate follows the symmetric member's W/r_th(t) to
   2 % (1/lambda against r_th/W: 0.981, 0.992, 0.995, 0.995, 0.996, 0.997, 0.998, 1.003 at t = 6, 7, ..., 13). The locus slope of the series is therefore an average of r_th(tau)/W over the departures:
   +21 % over 1/W at h = 0.00707 against #40's diagonal +38 %, and the local slope (per half decade of |p - p*_h|) rises from 0.63 to 0.78 as p -> p*_h (dev_04).
4. **The expanding side.** S (A = 0.05, D = 4, h = 0.02, X = 100) through the locus code: class FT, k = 2.0002, tau_s = 8.434, H/W = 1.280, 2.023, 2.861 at r/a = 10, 25, 50, the numbers of #213 (D4_A0.05_h0.02: k = 2.00004,
   tau_s = 8.43404, 1.2803, 2.0234, 2.8613). G (A = 0.05, same grid): class FT, k = 1.9998, tau_s = 9.514, H/W = 1.230, 1.946, 2.753 (dev_10); at h = 0.04, A = 0.0549, X = 100 the locus drifts at v = 0.021 and is 2.1 from the diagonal at t = 100 (dev_06).
5. **My errors, kept.** (a) The first D = 5 development series (dev_04, first run) used h rounded to six figures, which moves p*_h by 1e-9 (p*_h is proportional to h^2); the comparison with #40's recorded points
   showed it (the review of #40 made the same slip); its log was overwritten by the rerun (the rule's slip: the rerun's log is `dev_04_series_D5_h0.00707_exact_h.log`). h now comes from `threshold.CRIT["H"]` and
   `pstar_raw40` asserts it equals #40's summary. (b) The first reduced suite (dev_12 run 1) stopped on a missing import and on three bugs of the check code; it is kept as `dev_12_mini_run1_bugs.log`. (c) The four
   development units were stopped once (`dev/_stopped_run0_*`, partial logs kept) to add the checks CMP3 and DR that the coordinator's ruling asked for.
6. **Bracket ends need a longer triangle.** The two bracket ends of #40's bisection (p*_h -/+ 6e-15) have T = 28.4 and 34.9 at D = 4, h = 0.02, beyond the triangle of the series (t <= 34); they run on t <= 44.
7. **Planted v = 0.5 needs the locus's fate.** #40's diagonal event never fires at a drift of 0.5 (the diagonal is far from the throat); the planted bisection uses the locus's levels.


## Development runs (kept, none edited; `dev/`)

Scripts are `dev_NN_*.py`; logs `dev_NN_*_rK.log` (K = the run's number, with `.rc` and `.time`); runs stopped once for a code addition are `*_stopped_run0.*`.

| id | what | outcome |
|---|---|---|
| dev_01 | the streamed sweep (`throat_locus.sweep`, rectangle) against `dn.evolve` and `dn.throat_min` on a stored G run (D = 4, h = 0.04) | `scaled_rays` at lam = 1 equals `dn.ellis_rays` bit for bit; same slices, r_min differs by 2e-16, l by 0; same events, same diagonal |
| dev_02 | the triangle against the rectangle and against `dn.evolve(stop=True)`, G at A = 0.014 (collapse) and 0.016 (expansion), D = 4, h = 0.02 | bit-identical locus series and events inside the triangle |
| dev_03 | the near-critical locus of G, D = 4, h = 0.01, p*_h -/+ 1e-8 | r_min(t) 1.024 (t = 5) to 1.003 (t = 12): relaxation, not a plateau; l(t) smooth, v = 0.06 to 0.083, lapse f = 0.05 |
| dev_04 | G's series at the locus, D = 4, h = 0.02; D = 5, h = 0.00707 (first with h rounded: **my error**, see below; then the exact h) | D = 4: #40's diagonal slope 0.898291 reproduced; locus tau 0.84954 +- 0.00025 (+0.41 %), t 0.8709 (+2.9 %); D = 5: diagonal 0.79895 reproduced (+38 %), locus tau 0.70167 +- 0.0052 (+21 %), the local slope rises with e |
| dev_05 | the pair rate: lambda(tau) = d ln|r_min(p*+d) - r_min(p*-d)|/d tau, d = 1e-9, D = 4 (h = 0.01) and D = 5 (h = 0.00707) | D = 4: 1.1799 at t = 13, W = 1.18197; D = 5: 1.66 (t = 6) falling to 1.44 (t = 13) with r_th rising 1.059 to 1.197: lambda = W/r_th(t) within 0.5 % |
| dev_06 | the expanding locus of G (A = 0.0549) at h = 0.04 to t = 138 | the locus stays interior, v = 0.0214, H rises to 3.76 at r/a = 66 |
| dev_07 | the static ODE members (`static_member`) against GGS09a's closed form, D = 4, gamma_1 = 0 to 2; the fit of s_th from M(r) | m+ to 2e-8 (all gamma_1), m- to 8e-7 (gamma_1 = 0.3), 9e-6 (0.5), 1e-3 (1) and 1.1 (2: the extrapolation in 1/r is not converged on the negative-mass side; the check uses gamma_1 <= 0.5); fit recovers s_th to 1e-9 |
| dev_08 | planted static throats: pair-rescaled (v = 0.1, 0.5, -0.3) and gauge F, D = 4 (h = 0.04, 0.02, 0.01) and D = 5 (0.02, 0.01, 0.005) | all errors second order; at the finest h l <= 3.3e-5, r <= 1.2e-4, f <= 3.5e-4, tau <= 1.0e-4, v <= 5e-5 (boost); gauge v 2.1e-4 (the smoothing window's bias, h-independent). The first run (`dev_08_planted_static_run1.py`) used t up to 5 at D = 5: the static solution departs from truncation there (#39's t_c = 2.7) |
| dev_09 | the stall pair and the member table, D = 4 (h = 0.02) and D = 5 (h = 0.00707) | D = 4: gamma_1 = 0.048 (t = 10 to 16), r_th 1.0028, q ratio below 1e-5, 1/lambda / member 1.0004; D = 5: s_th 0.12 to 0.17, 1/lambda / (r_th/W) 0.981 to 1.003 over t = 6 to 13 |
| dev_10 | the expanding branch on the locus, S and G (A = 0.05), D = 4, h = 0.02, X = 100 | S: class FT, k = 2.0002, tau_s 8.434, H/W 1.280, 2.023, 2.861 (= #213's); G: FT, k = 1.9998, tau_s 9.514, H/W 1.230, 1.946, 2.753 |
| dev_11 | the planted lifetime series (family S, pair-rescaled): D = 4, h = 0.02, v = 0, 0.1, 0.5; D = 5, h = 0.00707, v = 0.13 | locus tau slope relative to 1/W: +1.9e-5, +8.4e-6, -3.1e-4; D = 5: -4.4e-4. The diagonal (#40's events): +7.1e-4, +7.8 %, +20 %; D = 5: +11.5 %. At v = 0.5 `threshold.bisect` on #40's fate stops (the diagonal event does not fire); the locus's fate is used |
| dev_12 | the reduced suite end to end | run 1 stopped on a missing import and three bugs (kept: `dev_12_mini_run1_bugs.log`); run 2: all checks pass (the checks CMP3 and DR were added later, at the coordinator's ruling) |
| dev/rec | the development record: D = 4, series at h = 0.02, 0.01, stall pairs, G expansions (tuned, 0.05) at X = 100 and h = 0.02, 0.01, S control at X = 200, planted series v = 0.1 | run 1 of its analysis: CTL[h = 0.01] failed (8 of 40 points): `points40` had read #40's `ed:` points into the series dict; fixed in code and the analysis reads #40's points itself; final analysis 26 of 26 pass (`analysis_baseline.log`; run 1 and run 2 kept) |
| dev/mut, dev/rec/mut | the mutation runs: 15 on the reduced suite, 20 on the development record | targets below; the first set of mini runs (before the final code edits, `dev/mut_run1_before_final_code`) is kept; the final ones are `dev/mut` |

## Declared

### Definitions

- **Slices and locus.** t = (x+ + x-)/sqrt2 on the anti-diagonals i + j = s of the nodes. On each slice the locus is the minimum of r with a parabolic refinement of the three nodes around the
  smallest, exactly `dn.throat_min`'s (the streamed sweep reproduces `dn.throat_min` and `dn.evolve` to roundoff: dev_01, dev_02); a slice is skipped if it has a dead node or the minimum is at its ends.
  Position l = (x+ - x-)/sqrt2 of the refined minimum; drift v = dl/dt by the local linear fit of l(t) over +- 0.5 in t; the lapse f at the refined minimum (parabolic in the three nodes).
  **Proper time** along the locus: d tau = e^{-f/2} sqrt(1 - v^2) dt (trapezoid on the slices), starting from tau = t_0 e^{-f_0/2} sqrt(1 - v_0^2) at the first valid slice.
  H = d ln r_min/d tau by centred differences on the slices.
- **Events.** #40's own events (first row with a trapped cell, r+ and r- below -1e-2; first row with an anti-trapped diagonal cell with r >= 2), evaluated in the same sweep, keep the fate of every point
  (fate = collapse below p*_h, expansion above) and give the control. **The locus's events** are level crossings of r_min on the locus: collapse r_min = 0.5 (primary), expansion r_min = 2 (primary),
  by linear interpolation between the two slices that bracket the level; alternatives r_min = 0.75 (collapse) and 3 (expansion). The lifetime T of a point is the proper time tau at the primary crossing of its own side.
- **Domain.** The triangle i + j <= s_max, s_max = sqrt2 T_cap/h, T_cap = 34 (the two bracket ends 44): every slice up to t = T_cap is full length and contains the locus for any |v| < 1. The expanding runs use
  the whole rectangle (X as #213: 200 at D = 4, 100 at D = 5), the locus is tracked on the truncated slices too and the series ends where it reaches the edge.
- **Fits.** `threshold.fit_set` unchanged: T = c_side + s ln(1/|p - p*_h|), common slope, one constant per side, primary window [1e-11, 1e-3] on the 19 values e = 3, 3.5, ..., 12 (both sides), four more windows,
  joint, collapse side alone and expansion side alone; the spread is the envelope of s +- 2 OLS SE over the 15 fits. p*_h is #40's (the raw I40-dh610 summary, lo and hi averaged), so the amplitudes
  p*_h -/+ 10^-e are the same floats as #40's and the same runs are repeated; its bracket ends are rerun as well.

### Runs of record

| what | runs |
|---|---|
| series of G (`series`) | D = 4, h = 0.02, 0.01, 0.005 and D = 5, h = 0.00707107, 0.00353553, 0.00176777 (#40's three h, the exact floats of `threshold.CRIT["H"]`); 38 series points + 2 bracket ends each, all from the same p*_h |
| stall pair (`stall`) | the same six (D, h): p*_h -/+ 1e-9 kept whole, the locus series and the profile of every slice t = 2, 3, ..., 30 (all nodes: r, f, phi, r+, r-, phi+, phi-) |
| expanding branch (`expand`) | G on the locus: D = 4, X = 200, h = 0.02, 0.01, members tuned (p*_h + 1e-6, p*_h from #40's raw), A = 0.05, 0.2; D = 5, X = 100, h = 0.00707107, 0.00353553, members tuned, A = 0.05; control: S, D = 4, h = 0.02, A = 0.05, X = 200 |
| planted lifetime series (`planted`) | family S in the pair-rescaled coordinates, h = 0.02 (D = 4) and 0.00707107 (D = 5): v = 0, 0.1, 0.5 (D = 4) and v = 0.13 (D = 5); p*_h by bisection of the locus's fate to 1e-13 |
| planted static throats (inside `analyze`) | PB, PG, PM, PO, PL |

Cost estimates (one thread each, load about 18 of 20): the six series jobs 155 CPU-min (D = 5, h = 0.00177: 110, in four parts), the stall pairs 20, the expanding runs 60, the planted series 40; 4 lanes, about 1.5 to 2 h wall.

### Checks (each can fail; the id is the check's id in `throat_locus_output.txt`)

| id | what | bar |
|---|---|---|
| JOB | every series point and both bracket ends of each of the six jobs present and ended at #40's event | all |
| CTL | **control**: the same amplitudes through the locus code give #40's event, cell, fate and time bit for bit; #40's diagonal slope of that job is reproduced | zero mismatches; slope within 1e-6 of threshold.md's 0.898291, 0.898043, 0.899089 (D = 4) and 0.798948, 0.800044, 0.800277 (D = 5) |
| FA | every series point with e <= 11 has one fate on #40's events, on the locus's levels and on its own side of p*_h | zero off |
| ED | the slope does not depend on the level: the alternative levels (0.75, 3) give a slope inside the primary fit spread | inside |
| RA | **the locus tau slope at the two finest h of each D agrees** | within 0.5 % |
| PB | **planted static wormhole in the pair-rescaled coordinates, drift v = 0.1, 0.5, -0.3**, D = 4 (h = 0.04, 0.02, 0.01, t in [0.8, 4]) and D = 5 (h = 0.02, 0.01, 0.005, t in [0.8, 2.7], the static solution departs from truncation after #39's t_c): the locus's l, r_min - 1, f, tau, v against the exact (v = (1 - lam^2)/(1 + lam^2), tau = t sqrt(1 - v^2), r = 1, f = 0) | at the finest h: l 2e-4, r 5e-4, f 1e-3, tau 5e-4, v 1e-3; orders of l, r, f, tau, v over the three h in [1.75, 2.25] |
| PG | **planted static wormhole in another double-null gauge** (x~+ = F(x+), F = x (1 - c (1 - e^{-x/b})), c = 0.15, b = 3: f = -ln F' != 0, drifting throat, exact l, f, tau by a root find) | the same bars; orders of l, r, f (tau and v carry the drift window's smoothing floor, found in dev_08) |
| PS | **planted lifetime series**: S in the pair-rescaled coordinates through bisection, series and fit: the locus tau slope is 1/W (the unboosted e-fold); the diagonal slope is reported beside it | \|slope W - 1\| <= 1e-3 in each of the four cases |
| PM | member machinery: the static ODE members reproduce GGS09a's closed form (gamma_1 = 0.3, 0.5: r_th, s_th, m+, m-), the fit recovers s_th from M(r) on both sides (D = 4, 5), and an evolved static wormhole (D = 4, h = 0.01, v = 0.1, t = 5) gives M = 1/(2r) and s_th = 0 | masses 1e-5, s_th 1e-6, evolved \|s_th\| 0.02, M 2e-3 |
| PO | the locus-frame rho, p_par and w on planted fields (one null stream, a two-sided state) at v = 0, 0.3, -0.5, n = 2, 3 | 1e-12 |
| PL | #213's five planted series through the classification used on the locus | all five |
| CMP1 | **the member at #40's stall time** (t = 12 at D = 4, t = 6 at D = 5, the nearest profile slice): its e-fold (D = 4: GGS09a's T(gamma_1) r_th at the gamma_1 fitted from M(r) on the two sides; D = 5: r_th/W of the symmetric member, T(gamma_1) is not available at D = 5) against 1/lambda of the pair rate | within 2 % |
| CMP2 | the same member e-fold against the locus tau slope of the series (primary window) | within 2 % |
| CMP3 | **the member follows the drifting throat**: at every profile slice in t = [7, 15] (D = 4) and [7, 13] (D = 5) the pair rate is the member's | within 2 % |
| DR | **the throat radius of the locus**: a plateau at D = 4 (t = 10 to 15), a drifting scale at D = 5 (t = 7 to 13) | \|change\| <= 1 % (D = 4); growth >= 5 % (D = 5) |
| KX | G on the locus (all expanding runs): class FT and k within 1 % of the symmetric throat's (#213: 2.0000 at D = 4, 3.9875 at D = 5) | all |
| RES | two resolutions of every expanding member: same class, H at r/a = 10, 25, 50 within 1 %, k and tau_s within 1 % | all |
| XC | **control**: S (A = 0.05, D = 4, h = 0.02, X = 200) through the locus code against #213's stored diagonal run | same class, k within 1e-3, tau_s within 1e-4 relative, H/W within 1e-3 |

Reported, not gated: the table of the member at every profile slice (r_th, v, f, M(r) on both sides at 1.25 to 4 r_th, s_th and its rms, the normal/ghost charge ratio, the pair rate); the locus's t slope and
the diagonal slope beside the tau slope; H/W at r/a = 10, 25, 50, |rho|/H^2, w_bar and the locus's drift on the expanding runs; the diagonal observer of #213 on the same expanding runs; the slope test of #211.
The comparison of the series' tau slope with the member is *numerical evidence* either way (CMP2 can fail).

### Mutations (computed in the development runs `dev/mut` (reduced suite, `mutate`) and `dev/rec/mut` (the development record, `analyze --raw=dev/rec --mutate=`) before being declared)

| mutation | what it breaks | must fire exactly: reduced suite | must fire exactly: stored record |
|---|---|---|---|
| `time_unit` | tau scaled by sqrt2 | CMP1, CMP2, CMP3, PB, PG, PS | PB, PG |
| `tau_diag` | tau of the diagonal (v = 0) instead of the locus's | PB, PG, PS | PB, PG |
| `tau_nolapse` | the lapse e^{-f/2} dropped from d tau | CMP1, CMP2, CMP3, KX, PG, RES | PG |
| `rho_diag` | rho in the grid's frame, not the locus's | PO | PO |
| `w_sign` | p_perp with the wrong sign | KX, PO | KX, PO, XC |
| `asym_sign` | the asymmetry fit with the two sides swapped | PM | PM |
| `pstar_off` | p*_h shifted by 1e-9 in the fits | CMP2, PS | CMP2, CTL, PS |
| `class_loose` | the classification's tolerances widened (expansion.py's own mutation) | KX, PL | KX, PL |
| `theta_coef` | dn.py: the sphere term's coefficient | BUILD, CMP1, CTL, FA, KX, PB, PG, PM, RES | PB, PG, PM |
| `scalar_coef` | dn.py: the scalar equation's coefficient | BUILD, CMP1, CTL, FA, KX, PB, PG, PM, RES | PB, PG, PM |
| `ghost_sign` | dn.py: the ghost's sign in f | BUILD, CMP1, CTL, FA, KX, PB, PG, PM, RES | PB, PG, PM |
| `no_corrector` | dn.py: predictor-only update | CMP1, CMP2, CMP3, CTL, FA, PB, PG, PS, RES | PB, PG |
| `data_constraint_sign` | dn.py: the sign of the constraint solve of the data | BUILD, CMP1, CTL, FA, KX, PB, PM, RES | PB, PM |
| `ellis_charge` | dn.py: the data's charge 1.1 times too large | BUILD, CMP1, CMP2, CMP3, CTL, ED, FA, PB, PM | PB, PM |
| `finder_sign` | dn.py: the sign of the trapped test | CTL, FA | nothing |
| `drop_bracket` | the bracket ends are not read | not run (record only) | JOB |
| `ed_t` | the alternative level read in t instead of tau | not run (record only) | ED |
| `ra_scale` | the finer h's slope scaled by 1.01 | not run (record only) | RA |
| `xc_tau` | the control's tau_s scaled by 1.01 | not run (record only) | XC |
| `locus_diag` | the diagonal's radius in the member table instead of the locus's | not run (record only) | CMP1, CMP2, CMP3, DR |

`finder_sign` is silent on a stored record by design (it acts on the events of a run, which a record does not rerun). The reduced suite is `throat_locus.py mutate` (D = 4: the planted checks, the G series at h = 0.02 for four e, the stall pair, the
expanding branch of S and G at X = 40, the planted lifetime series at h = 0.02); the development record is D = 4 only (series at h = 0.02, 0.01, stall pairs, G expansions at X = 100 and h = 0.02, 0.01, the S control at X = 200, one planted series).
The runs of record repeat the stored-record mutations on the runs of record (`runs/mut/`) and the reduced suite is repeated at the end (`runs/mut_mini/`).

### What is not declared as a criterion

- The comparison of the series' slope with 1/W (reported, no bar: the issue asks for the member's e-fold, not for 1/W), the locus's drift speed, the table of the member, the expanding runs' H/W and |rho|/H^2.
- The settled mass of G (see ruling 5).

### Commands (from `notes/wormhole_evolution/` of the worktree, `$PY = ~/Source/negative-mass-venv314/bin/python`)

```
$PY throat_locus.py series  --D=4 --hk=0 --part=0/1 --out=DIR     one job of the series (hk indexes threshold.CRIT["H"][D-2]); `stall`, `expand --member= --X= --family=`, `planted --v=` likewise
$PY throat_locus.py analyze --raw=RAW/runs [--mutate=NAME]           every check and table from the stored runs; exit 1 if a check fails
$PY throat_locus.py mutate  --mutate=NAME                             the reduced suite with one input broken
```

The queue is `scripts/make_queue.py` (31 jobs, longest first), taken by four lanes `scripts/lane.sh` (one thread each, `nice -n 10`, `timeout 7200`), started as `systemd-run --user --unit=nm-i225-laneN`.
Estimate after step 1 (revised from 6 to 9 h): the runs of record about 1.5 to 2 h wall on four lanes, the analysis and note about 1 h; about 4 to 5 h in all.

## Results (appended after the runs of record; the declarations above are unchanged)

Runs of record: 31 jobs from `runs/queue.txt` on four lanes (`scripts/lane.sh`, units `nm-i225-lane1` to `lane4`), 09:07 to 10:11 (2026-11-27), all exit 0, the longest 44 min (series D = 5, h = 0.00177, part 2 of 4), peak memory 274 MB,
none near the 2 h stop (`runs/logs/job_*.time`, `lanes.log`). Driver `throat_locus.py` at 9a3079d (the code as declared; no code change after the first run of record). `runs/analysis.log` is
`throat_locus.py analyze --raw=runs` (exit 1; = `notes/wormhole_evolution/throat_locus_output.txt`): **55 of 59 checks pass; CMP2 at D = 5 (h = 0.00707, 0.00354, 0.00177) and KX fail, reported as results, none moved.**

- CMP2 (D = 5): the series' locus tau slope 0.7017 / 0.7022 / 0.7022 against the member's e-fold at #40's stall time (t = 6), r_th/W = 0.6127 / 0.6129 / 0.6130: +14.5 % (bar 2 %). CMP1 (the pair rate against that member): −1.9 % (inside 2 %); CMP3
  (t = 7 to 13): −0.0051 to +0.0033; DR: +11.7 %.
- KX: D = 5, A = 0.05 is class GROW, not FT, at both h (tau_s/tau_end = 9.126/7.590 = 1.2025 against the declared bound 1.2 of `expansion.classify`'s FT test; k = 3.9883 against 3.9875, 1/H linear to 2e-4). All the other members: FT, k within 1e-3 of the symmetric throat's.
- The mutation runs of record: `runs/mut/` (20, `analyze --raw=runs --mutate=`) and `runs/mut_mini/` (15, the reduced suite): the declared set fires in every run; on the record CMP2 and KX fire beside it in every run because they fail without a mutation; the reduced suite
  fires exactly the declared sets.
- Discrepancies with the brief and with the repository's text: the brief's "dl/dt = +0.58, +0.25" (positions, coordinator confirmed); `threshold.md`'s "lifetime read by an observer off the throat … not separated" is now separated (the note proposes the wording); the brief's remark that G's end state may
  carry a normal charge is not seen at D = 4 (<= 1e-5) and is below 1e-3 at D = 5 after t = 8.
