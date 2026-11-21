# I123-rpi5: logs and caches of #123's counts of the zeros of Z(r_m; s), D's poles, in the boxes n3_l2 and n3_l3 across Re s = 0

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/123

## Code and environment

Code: worktree `~/Source/negative-mass-i123` on branch `wip/i123-axis`, `phase2/nonradial/zerilli_zeros.py` (the new option
`--axis`) and `collect_i121.py`, run from `phase2/nonradial`. The commit of the code that ran is in the closing comment.

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

Files are added below as the runs make them.
