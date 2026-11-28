# I228-dh610: family G at D = 6, third resolution h = 0.00125: #40's job, the locus (#225) and the drift (#255)

Machine dh610-fedora (Fedora, i7-12700, 20 threads shared with choptuik-large-d, 62 GB), Python `~/Source/negative-mass-venv314/bin/python`, numba, one thread per process, `nice -n 10`, at most 4
processes, every run a transient systemd user unit `nm-i228-*` writing log, err, time and rc here. Memory is reported, never a stop condition.
Issue https://github.com/nmoinvaz/negative-mass/issues/228 ("Run the one-sided threshold family G at D = 6 at its third resolution"), with #225's task 4 and #255's task 4 added. Worktree
`~/Source/negative-mass-i228`, branch `wip/i228-g-d6-third`, from main at b17db7a. Code: `threshold.py`, `dn.py`, `checks.py`, `throat_locus.py`, `throat_drift.py` unchanged (sha256 below);
the new file is `notes/wormhole_evolution/g_d6.py`, a thin driver (it changes no constant of those files except `threshold.CRIT["not_run"]`, below). Status words as in AGENTS.md: every number is
*numerical evidence*. No sentence says a result is new.

This README is written before the job of record starts. Part 2 (the checks and mutations of the driver, the D = 6 windows of the locus and drift analyses) is appended, dated, after the development runs and before any
analysis of record; nothing declared here is changed after the first run of record without a ruling over hc.

sha256 of the unchanged code: threshold.py 8abeaacaeeb4a9da…, dn.py a3902d27fa294d71…, checks.py 3ded2bc07f28cd98…, throat_locus.py db40c30c3a981df4…, throat_drift.py 1d77958df7f48a94….

## The question

#40 ran G (ghost pulse A tuned to p*ₕ plus a fixed normal pulse B = 0.1 on the same ray) at D = 6 at h = 0.005 and 0.0025 only: p*ₕ = 1.26577e-02, 1.10880e-02, ratio 1.1416; the order is not computed
(`threshold.md`). #246 bisected the third h with `threshold.bisect` unchanged: p*ₕ = 0.01069693394962485 (hi − lo 5.7e-15, 44 runs, 2569 s; raw `I246-dh610/runs/pstar_D6_G_k2.json`).
This task runs the job at h = 0.00125, reads G on the throat locus at the two finest h (#225) and measures the drift speed and its B dependence at D = 6 (#255).

## Declared inputs

| quantity | value |
|---|---|
| family, D | G of #40 (`threshold.family('G', A)`), D = 6 (n = 4), a = 1, 8πG = 1, pulses at centre 3, width 0.5 on the ray x⁻ = 0; B = 0.1 |
| h | 0.005, 0.0025, 0.00125, exactly `threshold.CRIT["H"][4]` (the third is `--h=0.00125`, the same float) |
| rectangle X | 28.0 (N = 22400 at h = 0.00125), #40's |
| bisection | bracket (0.005, 0.03), tolerance hi − lo ≤ 1e-14 (#40's `bisect_tol`) |
| series | p*ₕ ∓ 10^−e, e = 3, 3.5, …, 12 (38 points), primary window [1e-11, 1e-3], 15 fits (`threshold.fit_set` unchanged) |
| p*ₕ of #246 | 0.01069693394962485 (lo + hi)/2, to compare, not to use in the job |
| W (D = 6) | #195's, `checks.W_EXACT[4]`, 1/W = 0.461924 |

## Commands

All from `notes/wormhole_evolution` of the worktree, `NUMBA_NUM_THREADS=OMP_NUM_THREADS=1`, through `scripts/lane.sh` (a queue, `queue*.txt`, one line per run; units `nm-i228-<lane>`).

1. **The job of record** (`runs/D6_G_h0.00125`):
   `python3 threshold.py job --D=6 --family=G --h=0.00125 --out=RAW/runs/D6_G_h0.00125` with a 5 h limit (the waiver), as #40's `lane.sh` ran the other two but **without** `--cons --stall`. The bisection and the series are
   unchanged. The two flags store the whole grid up to the event: 8.2 GB peak at h = 0.0025 (`I40-dh610/runs/D6_G_h0.0025/job.time`), so about 33 GB at h/2 on a machine shared with other runners. They are run after the job as
   `python3 g_d6.py tail --D=6 --family=G --h=0.00125 --out=RAW/runs/D6_G_h0.00125` (the same `threshold.constraint_runs` and `threshold.stall_runs` on the job's own `lo`, `hi`, p*ₕ, writing the same `constraints.json` and
   `stall.json`), so that a failure there cannot lose the bisection and the series. This is the one change from "as #40 ran the other two".
2. **The merged record** `runs40/`: relative symbolic links to the 26 jobs and `g6` of `I40-dh610/runs` and to `runs/D6_G_h0.00125`. It is the `--raw` of #40's analysis and the `RAW40` of #225's and #255's code (set by `g_d6.py`).
3. **#40's analysis**: `python3 g_d6.py threshold-analyze --raw=RAW/runs40` = `threshold.main()` of `analyze` with `threshold.CRIT["not_run"] = {}`. `threshold.py analyze` itself skips G at D = 6, h = 0.00125 by its
   declaration `not_run={(4, "G"): 2}` ("the third is about 4 h, accepted"), prints "two h only" and gates nothing for a third h, so it cannot be used as it stands; the file is read-only here. Every other line of the output is
   `threshold.py analyze`'s; the output is compared with `threshold_output.txt` on main line by line (the two differ in the D = 6 G rows, the tally and the timing only). Proposed one-line change for the coordinator: delete `not_run` from `CRIT`.
4. **The locus** (#225's `throat_locus.py series`/`stall`, D = 6, hk = 1 and 2 = h 0.0025 and 0.00125; the series split in 4 parts per h as #225 ran it): p*ₕ and the control points from the merged record, so at hk = 2 from the job of
   record, after its bisection. `python3 g_d6.py locus series|stall --D=6 --hk=K --out=…` = `throat_locus.main()` with `RAW40` set.
5. **The drift** (#255's `throat_drift.py bisect|stall`, D = 6): the pair p*ₕ ∓ 1e-10 kept whole at B = 0.1 (p*ₕ from the job of record) and at B = 0.04, 0.2 (declared set of #255), with p*ₕ(B, h) by bisection of #40's events
   to 1e-12 from the declared bracket (0.3, 3) × (B/0.1)² p*ₕ(0.1, h) (#255's); h = 0.0025 first, h = 0.00125 as far as the time budget allows; B = 0.02, 0.07 (#255's post hoc extras) only if time is left.
   The fit of ṙ(τ) = ṙ∞ + c e^{−κτ} and the exponents are `throat_drift.fit_rdot` and `expo` unchanged; the windows at D = 6 are declared in part 2 from development runs at h = 0.005.

## Acceptance (the task's; each can fail)

| id | criterion | source of the check |
|---|---|---|
| BR | the job at h = 0.00125 finishes (`status` done) with the bisection to hi − lo ≤ 1e-14 and no run static through X | `threshold.analyze` BR |
| FM | every series point with e ≤ 11 lands on its own side of p*ₕ and ends in an event | FM |
| P246 | p*ₕ of the job agrees with #246's to 1e-14 (the difference is reported if not) | new, `g_d6.py` |
| PS | p*ₕ's Richardson order over the three h lies in [1.75, 2.25] (the order found is reported otherwise) | `threshold.analyze` PS with `not_run = {}` |
| RA | the primary diagonal slopes at the two finest h agree within 0.5 % | `threshold.analyze` RA |
| SL | 1/W inside the fit spread of the slopes: reported (G is expected not to satisfy it: +115 % at the two coarser h), not an acceptance criterion | SL |
| LRA | the locus τ slopes at the two finest h agree within 0.5 % (#225's RA, `CRIT["RA"]`) | `throat_locus.analyze_series` RA |
| LJOB, LCTL, LFA, LED | #225's JOB, CTL, FA, ED at D = 6 as at D = 4, 5 (all points present; #40's events and times reproduced bit for bit; same fates on #40's and the locus's events; alternative levels inside the spread) | `analyze_series` |
| CMP | the pair rate 1/λ against r_th(t)/W along the locus at D = 6, reported as #225's CMP1–3 with their 2 % bar (windows in part 2); RA of the member's r_th, DR (the drift of the radius) | `member_report` |
| DRIFT | the drift speed ṙ∞ at the finest h and its B exponent, each with its error stated (the fit's SE for ṙ∞; the spread of the exponent over the two finest h and over the fit window) | `throat_drift.fit_rdot`, `expo` |

A failed check is a result, not repaired by changing the check. Nothing is loosened after seeing data.

## Stops and limits

- The job at h = 0.00125: 5 h (`timeout 18000`), the waiver. Any other single run: 2 h (`timeout 7200`), stopped and reported if not finished.
- Logs are never overwritten; a rerun is a new directory (`*.partialN` for the dead one).
- Nothing stops or kills a process over memory; a memory watcher only reports.
- Only my own units are stopped, by unit name (`systemctl --user stop nm-i228-…`).

# Part 2: declared after the development runs, before any analysis of record

Written 2026-11-28 about 01:40 (dh610 clock; pushed in the commit "README part 2"). At that time the job of record had finished (rc 0, 6854 s), the locus series, stall pair and B = 0.1 pair at h = 0.0025 were done, and the series at h = 0.00125 and the other
pairs were running; none of those was analysed. The development runs are `dev/` (h = 0.005 only, plus the two-h base `dev/combo01` made from them and the runs at h = 0.0025 for the RA mutations):
`dev/series`, `dev/stall` (locus series and stall pair), `dev/bisect` (B = 0.02, 0.04, 0.07, 0.2), `dev/stall_drift` (pairs at δ = 1e-10, and 1e-12 at B = 0.1), `dev/analysis/analyze_dev1.log` (the first analysis),
`dev/tail_h0.005` and `dev/tail_control_h0.005` (the tail control), `dev/analyze40_orig` (#40's analysis on #40's raw), `dev/mut/`, `dev/mut_*` (mutations).

## What the development runs showed

1. **The locus levels of #225 do not mark a lifetime at D = 6.** On the collapse side the locus's r_min reaches 0.5 only for e ≤ 4 (3 of 19 points at h = 0.005, 2 at 0.0025): the sweep runs to the end of the triangle t ≤ 34 without a
   crossing, because #40's trapped cell forms at r about 1.7 and the minimum leaves the slice. For e ≥ 10 both sides cross the expansion level r_min = 2 at the same τ = 15.8 (the throat radius grows through 2 at the tuned
   stall's own time). #225's FA and ED fail at D = 6 on that account (14 of 34 points off; alternative levels 0.805 against 0.554). They stay in the analysis as they are and are reported as failed; the expansion side alone
   is added as SLx and LRAx.
2. **#255's fit does not converge at B = 0.1.** ṙ(τ) falls slowly (0.094, 0.087, 0.079 at t = 8, 10, 12) and does not approach a constant: `fit_rdot` gives κ → 0 and ṙ∞ = −101 ± 5e4. The model-free
   local ṙ is therefore the primary drift speed; the fit is read only where it converges (κ ≥ 0.05 and SE ≤ 10 % of |ṙ∞|). At B = 0.04 it converges (ṙ∞ = 0.0110 ± 7e-5, κ = 0.46).
3. **Planted evolutions at n = 4.** #255's planted static throat and moving throats, with its h = 0.02, 0.01, 0.005, miss its bars at n = 4 (3.6e-4 against 2e-4, 1.1e-3 against 5e-4; second order, 1.99). The planted checks
   PL1_6, PL2_6 are run at D = 6's own h = 0.005, 0.0025, 0.00125; the bars are #255's, unchanged.
4. **NO6 fails at B = 0.04 with δ = 1e-10** (max |odd| 1.2e-2 against 3e-4, as #255's NO at D = 5, B = 0.04 by 13 %): the unstable mode grows faster at the smaller radius. The fit masks the points above 3e-4 as in #255. Reported, not repaired.
5. **CMP1 at #40's stall time fails** at h = 0.005 (−3.3 %, bar 2 %): the pulse has just left at t = 6. CMP3 holds over t = 7 to 11 (−0.9 % to +1.5 %). #40's two stall times at D = 6 differ (6.24 expansion, 11.9 collapse);
   t = 6 is the earlier, since the pair rate is a linear-regime quantity and the pair at 1e-9 is not linear at t = 12 (|odd| 7e-4).
6. **The split of the job's tail is exact.** `g_d6.py tail` on #40's own D = 6, G, h = 0.005 bracket writes `constraints.json` and `stall.json` identical byte for byte to #40's (cmp), 2.2 GB peak (so about 35 GB at h = 0.00125).
   `threshold.py analyze` on #40's raw reproduces `threshold_output.txt` line for line, apart from the header and the timing (111 checks, 100 pass).

## Declared settings (`C6` in `g_d6.py`; the D = 6 entries added to #225's and #255's dictionaries by `declare()`)

| item | value |
|---|---|
| h of the locus and drift records | hk = 1, 2 = 0.0025, 0.00125 (hk = 0 is development) |
| locus series, bracket ends | #225's, unchanged (`throat_locus.job_series`, TCAP 34, TCAP_BR 44, 4 parts) |
| CMP1, CMP2 | at t = 6.0, bar 2 % (#225's) |
| CMP3 window | t in [7, 11], bar 2 %: the slices where the pair at 1e-9 is linear (\|odd\| ≤ 3e-4) |
| DR | the throat radius over t = 7 to 11: a drifting scale if it grows by ≥ 5 % (#225's D = 5 bar) |
| LRAx | the expansion-side locus τ slopes at the two finest h agree within 0.5 % (#225's RA bar) |
| drift pair | A = p*ₕ ∓ 1e-10 kept whole (#255's), B = 0.04, 0.1, 0.2 and the extras 0.02, 0.07 as far as time allows; p*ₕ(B ≠ 0.1) by `throat_drift.job_bisect` to 1e-12 from #255's bracket |
| primary drift speed | the local ṙ = dr_th/dτ at t = 8, 10, 12 (linear fit over ±0.5 in τ of the pair's mean; ±0.25 and ±1 give the window part of the error); ṙ(t = 8, 10, 12) and r_th − 1 there |
| B exponents | α of a ∝ B^α between neighbouring B at the same h, for p*ₕ, r_th − 1, local ṙ (error: the window part and the difference between the two finest h) and for ṙ∞ where both fits converge (error: the SE of the two fits propagated) |
| NO6 | max \|odd\| ≤ 3e-4 for t in [6.5, 12] (#255's window and bar); a fail is reported |
| PL1_6, PL2_6, PL3_6 | #255's bars at n = 4 and D = 6's h; PL3_6 adds a slow case (ṙ∞ 0.05, κ 0.15) and the local-slope recovery at t = 8, 10, 12 to 2e-4, ṙ∞ within 3 SE |
| P246 | \|p*ₕ(job) − p*ₕ(#246)\| ≤ 1e-14 at hk = 0, 1, 2 (hk = 0, 1 are #246's copies of #40's) |
| CTLN | every amplitude of the locus series and brackets is a point of the job's own record (CTL would pass vacuously on an empty overlap) |
| JOB6 | the pair has fates (collapse, expansion) on #40's events |

Failures expected from the development runs and kept as results: FA and ED (item 1), CMP1 (item 5), NO6 at B = 0.04 (item 4); #40's SL at G (1/W outside the spread at every h).

## Mutations of the new and the reused checks (effect computed on the development data, `dev/mut*`; each fires exactly the listed checks, a verdict that changes)

| mutation | what it breaks | checks it changes |
|---|---|---|
| `p246_off` | #246's p*ₕ shifted by 1e-12 | P246 |
| `ctl_shift` | the amplitudes shifted by one relative 1e-15 before the lookup | CTLN |
| `odd_scale6` | the pair's odd part × 10 | NO6 |
| `ra_scale6` | the finer h's expansion-side slope × 1.01 | LRAx |
| `tau_unit` (#255's) | τ in units of √2 t | PL3_6 |
| `rth_diag` (#255's) | the diagonal's radius instead of the locus's | JOB6, NO6, PL2_6 as computed in development (superseded: PL2_6 only, see Part 3) |
| `pstar_off` (#225's) | p*ₕ shifted by 1e-9 in the fits | CMP2, CTL |
| `locus_diag` (#225's) | the diagonal's radius in the member table | CMP2, CMP3 |
| `drop_bracket` (#225's) | the bracket ends not read | JOB |
| `ra_scale` (#225's) | the finer h's slope × 1.01 | RA |
| `odd_off`, `ed_t` (#255's, #225's) | not declared: `odd_off` changes no check at D = 6; `ed_t` acts on ED, which fails anyway | (none; ED) |

At the end, each declared mutation is run again on the stored record (`runs/mut/mutate_*.log`, baseline and mutated analysis, `scripts/final_mut.sh`) and the changed verdicts are compared with this table.

Correction written 2026-11-28 03:25: the last sentence of the first draft of this part said that #40's own mutations (`time_unit`, `pstar_off`, `bisect_loose`, `pstar_h1`) would be repeated through the wrapped analysis
of the merged record. They were run (`runs/mut/threshold_*.log`) and are not interpretable there: the record already fails SL, BR, ED, so `fired` is not a change of verdict, and #40's declared targets come from dedicated
runs at D = 4 (G6 needs a mutated growth control, `bisect_loose` acts in the job's bisection). They are kept as logs and not claimed. What stands for the wrapper is the line-for-line identity of its output with
`threshold_output.txt` outside the D = 6 G rows, the tally and the timing (`dev/analysis/threshold_analyze_prelim.log`, `runs/analysis/threshold_analyze_record1.log`).

# Part 3: results (2026-11-28 04:10)

Everything is in `notes/wormhole_evolution/g_d6.md` of branch `wip/i228-g-d6-third` (the numbers come from `runs/analysis/g_d6_analyze_record2.log` and `runs/analysis/threshold_analyze_record1.log`). Short form:

- Job `runs/D6_G_h0.00125` (rc 0, 6854 s): bisection 44 runs, hi − lo 5.68e-15, `lo`/`hi` bit for bit #246's; p*ₕ order 2.005; diagonal slopes 0.990046, 0.994756, 0.996251. Tail `runs/tail_D6_G_h0.00125` (rc 0, 903 s, 32.1 GB peak).
- Locus: FA, ED fail at D = 6 (collapse side has no r_min = 0.5 event for e ≥ 4.5; both sides cross 2 at τ = 15.75); RA 7.06e-4, LRAx 1.29e-3; CMP3 met (−0.8 … +1.5 %), CMP1 not met (−3.1 %).
- Drift: local ṙ(8, 10, 12) at B = 0.1 is 0.0938, 0.0872, 0.0790; #255's fit converges for B ≤ 0.07 only; exponents in the note.
- Analyses of record: `runs/analysis/g_d6_analyze_record1.log` (before the post hoc report `PHB` was added) and `record2.log` (the same checks, with `PHB`); record 2 is quoted.

## What went wrong, in order

1. `lane.sh`'s WAIT is per lane: two pair runs (`runs/pair_B0.07_d1e-10_hk1`, `…_hk2`, rc 1) were taken by another lane before their bisections existed. Reruns: `…_hk1_run2`, `…_hk2_run2` with `scripts/waitrun.sh`. The failed logs stay.
2. `runs/bisect_B0.2_hk1` hit its 2 h limit (rc 124, 36 runs, bracket 7.0e-12); its p* is read from the points (`runs/bisect/D6_B0.2_h0.0025/pstar_stopped.json`, `g_d6.py stopped-pstar`) for the pair `runs/pair_B0.2_d1e-10_hk1`.
3. The development effect of `rth_diag` (JOB6, NO6, PL2_6) was an artifact of the data growing between baseline and mutated analysis; on the frozen record only PL2_6 changes.
4. Part 2's time (02:00) was written at about 01:40 (corrected in place).
5. `runs/mut/threshold_*.log` (#40's mutations through the wrapped analysis of the merged record) are not interpretable and not claimed.
