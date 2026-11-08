# Environment and warning records of I7-win2

Read-only records collected on 2026-11-08 while the last three runs were going. Nothing was changed for them.

## 1. Thread variables in each job's own environment

`OPENBLAS_NUM_THREADS`, `OMP_NUM_THREADS` and `MKL_NUM_THREADS` were 1 for every attempt. This comes from the code that
launched each one, not from reading the environment of an exited process.

| attempt | launched by | the three variables = 1 |
|---|---|---|
| the 13 queue jobs (control, scans, windings, convergence, and the first runs of scan_085_l2, conv_085_l2, conv_085_l3) | `queue.py`, in the `env` it passes to `subprocess.run` | yes |
| diag_085_l2 | `Start-Process` from a PowerShell where the three were set to 1 first | yes |
| conv_085_l2 retry | `retries.py` `conv()`, in its `env` | yes |
| scan_085_l2 retry, pool of 2 | `retry_scan_085_l2.py` `main()`, in its `env`; the pool workers inherit it | yes |
| conv_085_l3 rerun, conv_085_l2 third run | `retry_conv_085_l3.py`, `retries.py` `conv()` | yes |

Check on the effect: in the venv, with the three variables set to 1, both OpenBLAS copies below report 1 thread; without
them, 20. Only `OPENBLAS_NUM_THREADS` matters, because the wheels carry OpenBLAS (no MKL) built with native threads
(no OpenMP).

## 2. BLAS and LAPACK of the venv (`negative-mass-venv`, Python 3.12.8)

numpy 2.5.4 and scipy 1.18.1 each bundle their own OpenBLAS, two different copies loaded into one process.

| | numpy 2.5.4 | scipy 1.18.1 |
|---|---|---|
| DLL | `numpy.libs\libscipy_openblas64_-ed4f167a...dll` (19.6 MB) | `scipy.libs\libscipy_openblas-197ee2fc...dll` (19.3 MB) |
| OpenBLAS | 0.3.34.106.0 | 0.3.31.dev |
| integers | 64-bit (`USE64BITINT`) | 32-bit |
| configuration | `DYNAMIC_ARCH NO_AFFINITY Haswell MAX_THREADS=24` | `DYNAMIC_ARCH NO_AFFINITY SkylakeX MAX_THREADS=24` (build target) |
| core type chosen at run time | Haswell | Haswell |
| threading | native threads (`openblas_get_parallel` = 1) | native threads |
| default threads here | 20 | 20 |

Machine: Intel Core Ultra 7 265K, 20 cores, 20 threads (no AVX-512, hence the Haswell kernels). numpy's SIMD baseline
X86_V2, found X86_V3. BIOS and microcode versions were not checked. `numpy.show_config()` output (BLAS/LAPACK section):
`blas` and `lapack` are both `scipy-openblas` 0.3.34.106.0, detected by pkgconfig, configuration string as in the table.

## 3. Overflow and invalid-value warnings in each log

The warnings are `polar_solver.py:106: RuntimeWarning: overflow encountered in multiply`
(`return r * (s * s + V(r) - q * q) / f`, the exterior Riccati equation for q = psi'/psi) and, right after it,
`rk.py:684-685: RuntimeWarning: invalid value encountered in dot`. Python prints a warning once per location per process,
so a count is the number of processes that overflowed, not the number of overflow events. "During gamma = X" means the
warning appeared after the previous row had printed, while X was being evaluated.

| log, attempt | overflow warning | where | outcome |
|---|---|---|---|
| control | none | | completed |
| wind_070_l2, wind_070_l3, wind_085_l2, wind_085_l3 | none | | completed |
| scan_085_l3 (pilot) | yes, 2 (the two pool workers) | during the scan | completed, clean |
| scan_070_l2 | yes, 1 | during the scan | completed, clean |
| scan_070_l3 | yes, 2 | during the scan | completed, clean |
| conv_070_l2 | yes, 1 | during gamma = 300 | completed, clean |
| conv_070_l3 | yes, 1 | during gamma = 40 | completed, clean |
| diag_085_l2 (serial, 100 points) | yes, 1 | during grid point 94 (g = 158.67) | completed, clean |
| scan_085_l2, queue run | yes, 1 | during the scan, before the hang | worker crash, hang |
| conv_085_l2, first run | **none** | | crashed during gamma = 40, before any warning |
| conv_085_l2, retry | yes, 1 | during gamma = 137 | crashed during gamma = 300 |
| conv_085_l3, first run | yes, 1 | during gamma = 300 | crashed during gamma = 1000 |

So the clean 0.70 runs, the diagnostic and the pilot overflow too, and one crash (conv_085_l2, first run) had no overflow
warning before it. The warning does not separate the crashing runs from the clean ones. No `np.seterr` or other change
was made.
