# I5-rpi5: polar-mode counts the l = 2, 3 scans did not cover (strip 0 < Re s < 0.1, |Im s| > 2.5, real-γ refinement)

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, 4 cores, 8 GB, aarch64, shared with choptuik-large-d).
Issue: https://github.com/nmoinvaz/negative-mass/issues/5
Code: negative-mass checkout `~/Source/negative-mass-i5`, branch `wip/i5-polar-count`, scripts in `phase2/nonradial/`.

Star: phantom, ω = 0.7603, M = −0.014580, l = 2 and 3. Python 3.14.10, numpy 2.5.4, scipy 1.18.1, sympy 1.14.0
(`~/Source/negative-mass-venv314`), `nice -n 10`, `OMP_NUM_THREADS=1`, at most two processes.

Contents are added as the runs finish. Each file's first line names the command that wrote it.
