# I130-mac: coordinator's review of #130 (rerun and independent exact check)

Machine: the coordinator's MacBook Air M5. Issue: https://github.com/nmoinvaz/negative-mass/issues/130

- `rerun.txt`: stdout of `python notes/warp/weitzenbock_conf.py` from `wip/i130-rot` at fdc208f (Python 3.14.7,
  sympy 1.14.0, nice 10, one thread). 61 checks pass and all 35 controls fire, which the script maps to exit 0. It
  equals the committed `weitzenbock_conf_output.txt` apart from the Python version and the timing line.
  `rerun.time`: `/usr/bin/time -l`, 877.76 s wall, 185237504 bytes (177 MiB) maximum resident.
- `mut_rot-dalpha.txt`: `--mutate=rot-dalpha` alone, exit 1, 8 checks fail (`planted_omega_rot`, `omega_rot_conv`
  and the six identities with alpha not constant).
- `ind130.py`: an independent check of item 6's identity on diag(A^2, B^2, C^2) in the frame rotated about z, with
  alpha = 2 atan t for a random polynomial t, so c and s are rational and both sides are exact at rational points.
  omega' comes from the Koszul formula of the frame commutators. It shares no code with `weitzenbock_conf.py` or
  `conventions.py`; R, mu and J are retyped from I99-mac/ind99.py. Its criteria are in its docstring, fixed before
  the first run.
  - `ind130_run1.txt`: PASS at 7 points (flat with K = 0, diagonal with K = 0, general), 82 s.
  - `ind130_mut_{Jsign,sign,frozen}.txt`: each exits 1 on its required criteria.
