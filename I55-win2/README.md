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

Python: `D:\negative-mass-venv\Scripts\python.exe`, Python 3.12.8, numpy 2.5.4, scipy 1.18.1, sympy 1.14.0, mpmath 1.3.0.
This is the venv #7 ran in (its `pyvenv.cfg` records creation as `C:\Users\nathan\Source\negative-mass-venv`, which
does not exist on win2 now), so the task's `C:\...` path is replaced by this one. The two OpenBLAS DLLs in `numpy.libs`
and `scipy.libs` date from 2026-11-07 22:05, while the `scipy` and `sympy` folders have modification times of
2026-11-08 15:36–15:37 (before the last boot), which fits Nathan's note that the project was moved to `D:\` that day.
The package versions match #7's.

Drive: `D:` is Nathan's dev drive (ReFS, 220 GB; `fsutil devdrv query` needs elevation, so Dev Drive status is Nathan's
word). #7 ran from `C:` (NTFS). The code, the venv and the output all sit on `D:` now, so this rerun differs from #7 in
the BIOS and microcode and also in the file system. A clean run cannot be credited to the update alone.

`OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1`, Normal priority, no affinity. One queue, at most 2 processes
(the convergence job is 1, the scan uses a pool of 2).

## What runs

| job | command | log |
|---|---|---|
| conv_085_l3 | `python -X faulthandler -u convergence.py 3 0.85` | `conv_085_l3.log` |
| scan_085_l2 | `set TAG=_n100`, then `python -X faulthandler -u scan_growing.py -1 0.85 2 100 1e-3 300` | `scan_085_l2.log` |

A crashed job is not retried, the queue goes on. At the end `scan_eps-1_w0.85_l2_n100.csv` is copied here.

## Files

- `launch.cmd`: starts `queue.ps1` (the queue, with exit codes in `queue.log`) and `memwatch.ps1` (a reporter of the
  queue's cpu and memory into `memwatch.log`, the I7-win2 script, it never stops or kills a process), both detached.
- `queue.log`, `memwatch.log`, `conv_085_l3.log`, `scan_085_l2.log`, the CSV: the run.
- `cmp_conv.log`, `cmp_scan.log`, `events.txt`: the checks, run from `../I7-mac` (ff50e96) after the queue ends.
