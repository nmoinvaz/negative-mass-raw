# I55-win2: #7's two crashing ω = 0.85 jobs rerun on win2 after its BIOS update

Machine: win2 (Windows desktop, Intel Core Ultra 7 265K, 20 cores, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/55

## Machine state before the run

| | before the update (#7) | now |
|---|---|---|
| BIOS (`Win32_BIOS`) | 1.38 (2024-09-08) | 3.40 (2026-09-17) |
| microcode (`HKLM:\HARDWARE\DESCRIPTION\System\CentralProcessor\0`, `Update Revision`) | 0x110 | 0x122 |
| last boot | | 2026-11-08 15:40:29 (local) |

## Code and environment

Code: `D:\negative-mass` on main at bf0094a (includes #7's script fixes, 5bd77a1), run from `phase2/nonradial`.

Python: `D:\negative-mass-venv314\Scripts\python.exe`, Python 3.14.10, numpy 2.5.4, scipy 1.18.1, sympy 1.14.0,
mpmath 1.3.0 (numpy's OpenBLAS 0.3.34.106.0, `USE64BITINT DYNAMIC_ARCH NO_AFFINITY Haswell`). Its `pyvenv.cfg` records
creation as `C:\Users\nathan\Source\negative-mass-venv314`, which does not exist on win2 now (the project moved to `D:\`
on 2026-11-08). Nathan decided on 2026-11-08 that every Python job on win2 runs on 3.14.

Drive: `D:` is Nathan's dev drive (ReFS, 220 GB; `fsutil devdrv query` needs elevation, so Dev Drive status is Nathan's
word). #7 ran from `C:` (NTFS). The code, the venv and the output all sit on `D:` now, so this rerun differs from #7 in
the BIOS and microcode, in the file system, and in the Python version (#7 ran on 3.12.8). A clean run cannot be
credited to the update alone.

## First launch on Python 3.12.8 (stopped, not a crash)

The queue first ran on `D:\negative-mass-venv` (Python 3.12.8, numpy 2.5.4, scipy 1.18.1, sympy 1.14.0, mpmath 1.3.0,
the versions of #7's venv, relocated from `C:`). It started 2026-11-08 23:48:38Z and was stopped at 23:55:36Z by
negative-mass-win2 on the coordinator's instruction, because of Nathan's decision above. `conv_085_l3` was unfinished,
with 8 of its 10 γ rows printed (γ = 0.001 to 137) and no error. Stopped: the queue's powershell, its `cmd` and
python processes, and `memwatch.ps1`; no other process. Kept as `conv_085_l3_py312_stopped.log`,
`queue_py312_stopped.log` and `memwatch_py312_stopped.log`. No exit code exists for it, and its rows are not part of
the acceptance checks.

`OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1`, Normal priority, no affinity. One queue, at most 2 processes
(the convergence job is 1, the scan uses a pool of 2).

## What runs

| job | command | log |
|---|---|---|
| conv_085_l3 | `python -X faulthandler -u convergence.py 3 0.85` | `conv_085_l3.log` |
| scan_085_l2 | `set TAG=_n100`, then `python -X faulthandler -u scan_growing.py -1 0.85 2 100 1e-3 300` | `scan_085_l2.log` |

A crashed job is not retried, the queue goes on. At the end `scan_eps-1_w0.85_l2_n100.csv` is copied here.

## Result

The Python 3.14.10 queue ran 2026-11-08 23:56:30Z to 2026-11-09 00:36:02Z (`queue.log`). Both jobs exited 0 (`conv_085_l3`
31 min 46 s, `scan_085_l2` 7 min 46 s). `cmp_conv.log`: all 15 rows identical to `I7-mac/conv_085_l3.log`, self-test
FIRED. `cmp_scan.log`: 100 points, largest relative difference 0 against `I7-win2/diag_085_l2.jsonl` (tolerance 1e-8),
self-test FIRED. `events.txt`: no `Application Error` and no WHEA-Logger events since 15:48 local. The process tree
peaked at 331 MB working set and 370 MB private (`memwatch.log`), at most 2 cores.

## Files

- `launch.cmd`: starts `queue.ps1` (the queue, with exit codes in `queue.log`) and `memwatch.ps1` (a reporter of the
  queue's cpu and memory into `memwatch.log`, the I7-win2 script, it never stops or kills a process), both detached.
- `queue.log`, `memwatch.log`, `conv_085_l3.log`, `scan_085_l2.log`, the CSV: the run on Python 3.14.
- `*_py312_stopped.log`: the stopped first launch on Python 3.12.8. `ram.txt`: the RAM speed (4800 MT/s).
- `cmp_conv.log`, `cmp_scan.log`, `events.txt`: the checks, run from `../I7-mac` (ff50e96) after the queue ends.
