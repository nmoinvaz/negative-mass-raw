# I188-mac: the Taylor crate over complex s for the polar box counts (negative-mass #188), design stage

Machine: mac, the coordinator's Mac (Apple M5, 10 cores, macOS), shared with other sessions; runner negative-mass-mac-i188
(Claude Code, account claude-me2). Issue: https://github.com/nmoinvaz/negative-mass/issues/188
Code: worktree `~/Source/negative-mass-i188`, branch `wip/i188-complex-s` from main 0d1d376; pushes
`git push origin HEAD:refs/heads/wip/i188-complex-s`. Library clone `~/Source/negative-mass-i188-libs/multishoot` (main f929163) for stage 3.
Python `~/Source/negative-mass/.venv/bin/python`. Stage 1 (this README so far): the design note `design.md` and the development runs
`dev_NN_*` it rests on (made with `devrun.sh`: stdout, stderr and exit code kept). No crate code has been written.

## Files (stage 1)

| file | what |
|---|---|
| `design.md` | the design note posted on the issue for review |
| `probe_scipy.py`, `dev_01`, `dev_07` | winding2's D at stored points of the box: fresh rtol 1e-8 and 1e-12, Hermitian Gram–Schmidt in place of LAPACK's QR, and the conjugate-free control. `dev_01`'s B12 column is wrong (the control's class attribute was shared with the Hermitian class, so it equals H12); `dev_07` reruns three points with the fixed control |
| `probe_rtol.py`, `dev_14` | the scipy path at rtol 1e-8 … 1e-13 at three points (`dev_08` was this probe started as a third process by mistake, stopped by its PID after 5 s: `notes_stopped.txt`) |
| `probe_count.py`, `dev_09` … `dev_13` | winding2's counter ported to read a cache: the stored result, then its four mutations |
| `probe_mut_effects.py`, `dev_15` | the size of `strip_off`, `conj_s`, `rs_shift` on the stored points |
| `probe_qr_diag.py`, `dev_16` | LAPACK's complex QR has a real R diagonal |
| `dev_02` … `dev_04` | the real crate (main 0d1d376, built here) at the box's \|s\|: star data, dd and f64 times |
| `cxbench/`, `dev_05`, `dev_06` | the cost of a complex multiply-add against a real one (`dev_05`'s f64 line was optimized away: 0.0 ns; `dev_06` uses `black_box`) |
