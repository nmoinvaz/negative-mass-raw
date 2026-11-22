# I102-mac: coordinator's review of #102, the Type III set on D = 0

Machine: the coordinator's Mac (Apple M5, macOS, Python 3.14.7, sympy 1.14.0, mpmath 1.3.0), one thread, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/102

| file | what |
|---|---|
| `rerun_he_type3.txt`, `.time` | `python notes/warp/he_type3.py` from 3bfabb6: exit 0, 16 checks pass, 28 controls fire, 69.6 s, 168 MiB peak; stdout equals the committed `he_type3_output.txt` except the wall time |
| `rerun_mutate_cof-g2-drop.txt`, `.time` | `--mutate=cof-g2-drop` alone: exit 1, fails `cert_T0`, its frozen target |
| `ind102.py` | independent check, no code shared with `he_type3.py`, `review_he_surface_lib.py`, `he_surface.py` or `he_type.py` (criteria in its docstring, fixed before the first run) |
| `ind102_run1.txt` | its first and only run: C0 to C8 pass, 11 s, 78 MiB peak |
| `ind102_mut_*.txt` | its mutations `gamma`, `phi`, `Kdrop`, `sigma`: each exits 1 on its targets |
