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
