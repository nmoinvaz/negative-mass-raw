# I96-dh610: tanh spectrum of T₁ at σR = 16, the 11 sectors at P = 340, N = 320

Machine: dh610-fedora (Fedora, 20 cores, 62 GB, shared with choptuik-large-d). Issue:
https://github.com/nmoinvaz/negative-mass/issues/96

Started by the coordinator on 2026-11-22. The σR = 16 sectors need about 27.6 GiB each (P = 340), more than the laptop
(surface-laptop-4, I96-win) can hold beside its other work; Nathan approved dh610 for them. The radial size P = 340 is
attempt 2 of the σR = 16 `conv` check, running on the laptop (I96-win, `conv-s16-p340-n320.log`). These sectors count
only if that check passes; if it fails they are rerun at the size that passes.

Code: negative-mass `wip/i96-thin` (c5fd40d), from the worktree root, one thread, nice 10:

    python notes/warp/tanh_spectrum.py --part=vc,planted,shift,tanh --sigmas=16 --p=16:340 --npan=320 --procs=1 --raw=<this folder>/eig

- `sectors-s16-p340.log` and `.exit`: the run's output and exit code.
- `eig/`: the eigenvalue files per sector.
- `memwatch.log`: the run's RSS and the machine's MemAvailable once a minute (report only; nothing is stopped over memory).
