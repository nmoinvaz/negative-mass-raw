# I123-rpi5: logs and caches of #123's counts of the zeros of Z(r_m; s), D's poles, in the boxes n3_l2 and n3_l3 across Re s = 0

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/123

## Code and environment

Code: worktree `~/Source/negative-mass-i123` on branch `wip/i123-axis`, `phase2/nonradial/zerilli_zeros.py` (the new option
`--axis`, commit c4206eb, which every job here ran) and `collect_i121.py` (ce624b9), run from `phase2/nonradial`.

Python: `~/Source/negative-mass-venv314/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1). Every run is `nice -n 10` with
`OMP_NUM_THREADS=1` and `OPENBLAS_NUM_THREADS=1` (the script is single-threaded), detached with `setsid nohup`. At most two
processes at a time, and a second one starts only while the 15-minute load average is below 4. Memory is reported, never a
stop condition.

## Method

`--axis` integrates y = (Z, f Z') exp(s r*), which has no k in its equation, from the Jost solution Z = exp(-s r*) u,
u = sum a_n r^-n, at the fixed R_z of the box, and counts the phase of y1(r_m) = exp(s r_m*) Z(r_m; s). The start is
holomorphic in the box (the a_n have poles at s = 0 only). The path is the ray r = r_m - i p, not the real axis, because for
Re s < 0 the other solution grows inward by exp(-2 Re s (R_z* - r_m*)) on the real axis and the integration there is
unstable and slow (`explore_realr_vs_ray.out`). `zerilli_zeros.py`'s docstring has the details.

## Plan

1. Controls on the n3 boxes and on a flat-space box that holds a zero: `n3_l2_flat`, `n3_l3_flat` (count 0), `ax_flatzero`
   (count +1, the root of the reverse Bessel polynomial) and its reversed contour `ax_flatzero_rev` (must fail `flat`),
   `n3_l2_mprincipal` and `n3_l3_mprincipal` (`--mutate=principal`, must fail `holo`).
2. Pilot: `n3_l2` (planted zero at -0.0005 + 0.12i, `--guard=all`), alone. Stop condition: over 2 h.
3. The other jobs: `n3_l3`, the planted zero on the right of the axis (`*_pr`, 0.00005 + 0.12i) and `--zfac=2` (`*_z2`) for each box.
4. `python collect_i121.py <this folder> > i121_zeros_output.txt`, then each `--mutate=` into a log here (each must exit 1).

## Files

- `jobs.txt`: the 37 lines `job|arguments` of `python collect_i121.py --jobs`, byte for byte. #121's 25 (the first lines) were
  not rerun; the 12 of this task are `n3_l2`, `n3_l2_pr`, `n3_l2_z2`, `n3_l3`, `n3_l3_pr`, `n3_l3_z2` (boxes), `n3_l2_flat`,
  `n3_l3_flat`, `n3_l2_mprincipal`, `n3_l3_mprincipal`, `ax_flatzero` and `ax_flatzero_rev` (controls). `pilot.txt`,
  `boxes.txt` and `controls.txt` list the jobs of each stage.
- `<job>.log`, `done/<job>.rc`: the output and exit code of each job. `queue.log` has the start and end of each job and
  the load at each second start. The 25 logs of #121 (`p7603_l2.log` ... `mut_lshift.log`) are copies of
  `I121-win`'s, with their sha256 in `sources.sha256`, so that `collect_i121.py` can read the whole table here.
- `cache/`: `zerilli_zeros_cache_<tag>.pkl`, the y1(r_m) values at the contour points. `n3_l2` and `n3_l2_pr` (and `n3_l3`,
  `n3_l3_pr`) share one, and so do `ax_flatzero` and `ax_flatzero_rev`, so the second job of each pair shows 0 s.
- `launch_I123.sh LISTFILE`: the load-gated queue worker of `I126-rpi5` (one process starts at once, a second only while the
  15-minute load is below 4), reading `jobs.txt`; `memwatch.sh`: reports only; `memwatch.log`.
- `collect_mutate_{box,control,axis,oneside,zfac}.log`: `collect_i121.py <this folder> --mutate=<name>`, each exit 1.
- `explore/`: scratch scripts and outputs from before the option existed (`exp1.py`: Jost series and real-axis Radau;
  `exp2.py`, `exp3.py`: the same on the ray). `exp1_l2_z1.out` is the real-axis run, stopped by me with its PID after two
  points (the second took 229 s for three solves); `exp3_l2.out` is the ray at five points.
- `cross_continue_i123.py`, `run_cross.sh`, `run_cross_chain.sh`, `cross_n3_l2.log`, `cross_n3_l3.log`,
  `cross_n3_l2_flat.log`, `cross_n3_l2_shift.log`: the independent check of q at Re s < 0. It reads the `q at the ...
  points` lines of an `--axis` log and compares them with the real-axis solution of #121's form (Re s > 0 only)
  continued across the axis by a Taylor series fitted on a circle in Re s > 0. It shares only the potential, r_m and
  Mext with `--axis`. `--flat` runs it on a flat log (planted truth: the continuation must give the exact flat value),
  `--mutate=shift` evaluates the series 10^-4 off (must fail). `*_first_missed_axis_point.log` are the first runs, whose
  line parser missed the point on the axis; kept.
- `column_scan_i123.py`, `run_scan.sh`, `column_scan_l2.log`, `column_scan_l3.log`: q against `zerilli_q` along the two
  vertical edges of n3 (reported, not a criterion).
