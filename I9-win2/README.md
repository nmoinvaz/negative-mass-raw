# I9-win2: #9's lost radial FD cells, the low-ω root tables on denser grids, and the strong-field turning point

Machine: win2 (Windows desktop, Intel Core Ultra 7 265K, 20 cores, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/9

## Machine state

BIOS 3.40 (2026-09-17), microcode 0x122, last boot 2026-11-08 15:40:29 local, RAM 4800 MT/s (a 6400 kit, no XMP/EXPO
profile applied), `D:` is ReFS. Same as in [I55-win2](../I55-win2/README.md), whose Python 3.14 run had no crash.

## Code and environment

Code: `D:\negative-mass` on main at 325b23e, run from `phase2/radial`. The task writes no code.

Python: `D:\negative-mass-venv314\Scripts\python.exe`, Python 3.14.10, numpy 2.5.4, scipy 1.18.1. Every job runs with
`-X faulthandler -u`, `OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1`, Normal priority, no affinity. Two
queues of one process each, so 2 processes in all. choptuik-large-d's #204 load test shares the machine.

## What runs

Queue A, `queue.ps1 -Queue A`, jobs in sequence:

| job | command |
|---|---|
| fd | `fd_check.py` |
| complex | `complex_check.py` |
| strong | `strongfield.py 1 0.280,0.279,...,0.262` (19 targets, step 0.001) |

then `strongfield_eps+1.json` is copied here.

Queue B, `queue.ps1 -Queue B`, jobs in sequence, with `N` = 0.3,1,3,6,9.2,15,25,35,40,42,42.6:

| job | command |
|---|---|
| pilot | `lowscan.py 1 42.6 160 160` |
| low_p16, low_p80, low_p160 | `lowscan.py 1 N 16 16`, `... 80 80`, `... 160 160` |
| low_m16, low_m80, low_m160 | `lowscan.py -1 0.3,1,12 16 16`, `... 80 80`, `... 160 160` |

The pilot is a gate. The queue goes on only if it exits 0 within 30 min with `sigma2=['4.03972e-05', '1.80151e-03',
'4.70273e-03']`, the Mac's row (I9-mac at ccde4b8, 7 min 52 s). Otherwise queue B ends at once with `HOLD` in its log
and waits for the coordinator, and `launch.cmd B <job>` resumes it at a job. A crashed job is not retried, its queue
goes on.

## Checks (after the queues, from `phase2/radial`, each with `--selftest`)

`cmp_lowscan.py low_p.txt low_p16.log`, `low_p80.log` against `low_p160.log`, `low_m80.log` against `low_m160.log`,
`strong_refine.py strongfield_eps+1.json`, the new `fd` and `complex` cells against `fd_check_output.txt` and
`complex_check_output.txt`, `strong` rows 0.28 and 0.27 against `strong_p.txt`, `low_m16` against RESULTS.md §4 and
`low_recheck_m.txt`, and the Application Error and WHEA-Logger events. Outputs are saved here as `<check>.log`.

## Files

- `launch.cmd`: starts `queue.ps1` for A and B (`queue_A.log`, `queue_B.log`, with exit codes and wall times) and
  `memwatch.ps1` for each (`memwatch_A.log`, `memwatch_B.log`, a reporter of the queue's cpu and memory, the I7-win2
  script, it never stops or kills a process), all detached.
- `<job>.log`: the job's stdout and stderr.
