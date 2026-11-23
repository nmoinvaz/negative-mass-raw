# I129-mac: coordinator's review of #129, the mean value test of arg D

Machine: the coordinator's Mac (Apple M5, macOS, Python 3.14.7, numpy and scipy of the repo's venv), one thread, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/129

| file | what |
|---|---|
| `rerun_collect.txt` | `harm_circles.py --collect` on a copy of `I129-win`'s caches (96ab665), from fb7d97a: exit 0; equal to the committed `harm_circles_output.txt` except one S12 entry, 5.075e-10 against 5.076e-10 |
| `rerun_mutate_nonholo.txt` | `--mutate=nonholo` on the cached S12 data of `c075_l2`: exit 1, D fails at all six rows, the controls pass |
| `resolve_c075_l2_S12_p2.txt`, `.time`, `resolve_harm_circles_c075_l2_S12.pkl` | a fresh S12 run of `c075_l2` point 2 (129 evaluations, 10.0 s each, 1298 s): ratios 7.86e-4 and 2.91e-3, both pass |
| `ind129.py`, `ind129_run1.txt`, `.err`, `ind129_run2.txt` | first independent check, of holomorphy of D (log\|D\| and a Cauchy-Riemann mode). Run 1 stopped on an assertion of its own (a branch error, fixed with the criteria unchanged); run 2 fails C1-C3 at every setting by the same factor, because \|D\| is phase-normalised by `PolarProblem.D`, so only arg D is the arg of an analytic function. Its premise was wrong; its failures stand as recorded, and its mutations were not run |
| `ind129b.py`, `ind129b_run1.txt` | second independent check, of arg D only (own DFT, and a two-radius estimate that removes the rho^4 term), criteria fixed before its run: C0-C3 pass; S12 at most 3.2e-3 of the limit; the Mac's D agrees with the laptop's to 3.3e-12 in arg; max \|arg(D_S8 / D_S12)\| = 6.8e-7 rad |
| `ind129b_mut_nonholo.txt`, `ind129b_mut_half.txt` | its mutations: each exits 1 on its targets |
