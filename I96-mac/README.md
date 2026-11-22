# I96-mac: coordinator's box probes of #96 step 6 at σR = 8

Machine: the coordinator's MacBook Air M5 (32 GB). Issue: https://github.com/nmoinvaz/negative-mass/issues/96

`frank_loss.py --part=krylov --sigmas=8 --vs=0.5` from `wip/i96-thin` at c5fd40d, one thread, nice 10, at the spacing
dx = 2L/N = 1/32 (4 points across the wall of width 1/8):

- `box-s8-L1-N64.log`: L = 1, N = 64, reproducing the laptop's probe in I96-win (same numbers).
- `box-s8-L2-N128.log`: L = 2, N = 128 (run by `probe.sh` with the L = 1 one).
- `box-s8-L2.5-N160.log`: L = 2.5, N = 160, the same command with `--Ns=160 --L=2.5`.

Each log ends with the exit status and, from `/usr/bin/time -l`, the wall time and maximum resident set size.
