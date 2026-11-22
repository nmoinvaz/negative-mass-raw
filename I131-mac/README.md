# I131-mac: coordinator's review of #131 (rerun and independent check of he_surface.py's D equality)

Machine: the coordinator's MacBook Air M5. Issue: https://github.com/nmoinvaz/negative-mass/issues/131

- `rerun.txt`: stdout of `python notes/warp/he_surface.py` from `wip/i131-dexact` at a54b86b (Python 3.14.7, nice 10),
  exit 0: 14 checks pass and all 18 controls fire. It equals the committed `he_surface_output.txt` apart from the Python
  version and the run time. `rerun.time`: 61.39 s wall, 128745472 bytes (123 MiB) maximum resident.
- `mut_nsimplify-back.txt`: `--mutate=nsimplify-back`, exit 1, only `axis` fails, at the #72 point.
- `ind131.py`: runs he_surface.main() (checks only) with he_type.he_type_exact wrapped to change only the returned D
  (D + 1e-80 where D != 0, then where D = 0). Criteria in its docstring, fixed before the first run.
  - `ind131_run1.txt`: PASS. Unchanged D: 14 checks pass. D + 1e-80 at the 24 nonzero D: `axis` fails. At the 340 D = 0:
    `axis`, `locus_points`, `null_points` and `outside_description` fail, the four checks that call `classify`.
  - `ind131_mut_identity.txt`: the wrappers return D unchanged, exit 1 (C2, C3, C4 fail).
