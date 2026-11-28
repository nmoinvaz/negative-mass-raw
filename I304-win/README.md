# I304-win: the D = 4 throat tail of family G at B = 0.01, 0.014, 0.03 (#291's ensembles at three more B)

Machine: surface-laptop-4 (Windows), runner `negative-mass-win-i304`, worktree `C:\Users\nathan\Source\negative-mass-i304` on
`wip/i304-tail-b` (scripts by the coordinator, commit 0fc1844), four lanes at below-normal priority, one thread each.
Issue: https://github.com/nmoinvaz/negative-mass/issues/304.

## Method (written by the coordinator 2026-11-28, before the runs of record)

- `notes/wormhole_evolution/throat_tail_b.py --B=B` sets #291's `throat_tail.py` to the amplitude B (its B0, TAG and bracket
  key) and calls its `main()` unchanged: the bisection `pstar` of p*ₕ to hi − lo ≤ 1e-14 from bracket k of #291's eight, then the
  pair p*ₕ ∓ 1e-12 (`member`, e = 12), D = 4, family G, h = 0.01 and 0.005.
- `throat_tail_b_jobs.py` runs the 48 groups of `jobs.txt` ("B H K") in four lanes. Layout as #291: `runs` (k = 0) or `runs_k<K>`,
  then `G_B<B>/h<H>/{pstar, logs, e12/{member, logs}}`. No log is overwritten; a restarted lane skips finished groups.
- Pilot on the coordinator's Mac (B = 0.01, h = 0.01, k = 0): bisection 37 s (43 runs, hi − lo = 9.1e-15, p*ₕ = 1.6439e-4, against
  5.872e-4 at B = 0.02, ratio 3.57), pair 28 s, both rc 0. Not part of the record.

## What the analysis will read (declared now; the analysis script is written before any run of record is read)

- Per B and h: the ensemble-mean speed v(t) = dr_th/dτ of the eight pairs on their common slices and rate × t = −t d ln|v|/dt at
  t = 10 and 15, with the ensemble's standard error (#291's estimator).
- The late constant: a fit v = A t^(−p) + c over t from 10 to the end of the clean window (#291's ens_tol rule), with c's error
  bar, against the B^3.16 prediction from #291's B = 0.02 (#273, #255): c(B) = 7.8e-6 (B/0.02)^3.16, that is 8.8e-7, 2.5e-6 and
  2.8e-5 at B = 0.01, 0.014, 0.03.
- Planted truth through the same estimator, first: v = t^(−3) plus each predicted c, with #291's measured noise. It must recover p to
  10 % and c to 25 %, or the analysis is stopped.
- Gating: every bisection ends with hi − lo ≤ 1e-14 and no stop; every pair collapses on the − side and expands on the + side.
  Reported: rate × t, c and p with their errors, per B and h.

## Launch (Windows)

Three lanes (choptuik-large-d's run of #1112 shares the laptop; never touch its processes). From PowerShell, detached through
WMI so that the session's terminal cannot end them:

    $q = Invoke-CimMethod Win32_Process -MethodName Create -Arguments @{CommandLine="conhost.exe --headless powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\nathan\Source\negative-mass-raw\I304-win\run_lanes.ps1"}
    Invoke-CimMethod Win32_Process -MethodName Create -Arguments @{CommandLine="conhost.exe --headless powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\nathan\Source\negative-mass-raw\I304-win\keepawake.ps1 -QueuePid $($q.ProcessId)"}

`keepawake.ps1` is #114's (I114-win): it holds SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED) until the queue's
process ends and changes no power setting. Progress: `queue.log`, `logs\lane<L>.log`; the end: `lanes_done`.

## Runner's part

Run the four lanes, post progress, push this folder. The coordinator writes and runs the analysis.
