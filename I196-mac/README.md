# I196-mac: where scipy's polar D(γ) drifts from #186's crate as γ grows (l = 5, γ = 1000, 2000, 3000)

Machine: mac, the coordinator's Mac (Apple M5, 10 cores, macOS, shared with other sessions); runner negative-mass-mac-i196
(Claude Code, Sonnet 5.5, account claude-me2). Issue: https://github.com/nmoinvaz/negative-mass/issues/196
Code: worktree `~/Source/negative-mass-i196`, branch `wip/i196-polar-drift` (from main fca41a4); pushes
`git push origin HEAD:refs/heads/wip/i196-polar-drift`. Script `phase2/nonradial/taylor_drift.py`, crate additions
`taylor_polar/src/main.rs` (command `starsteps`) and `rows.rs` (variant `phio24`).
Written before the first run of record (`run_*`); the development runs `dev_NN_*` (made with `devrun.sh`, which keeps stdout,
stderr and exit code) sit beside it. Amendments are numbered and dated at the end. A number below that came from a development
run names it.

## The question

#187's CAP5c is not met: at (l, γ) = (5, 6000) the crate's φ_cut D differs from #114's scipy value by 4.7e-8 (bar 1e-8). #187 read the
growth of the gap with γ (8e-13 up to γ = 10, 2e-10 at 300, 3e-9 at 1000, 5e-8 at the top γ) as "not a static input". **That
step does not follow.** D is a normalized determinant of two nearly parallel 3-planes (|D| ≈ 0.2 γ⁻³, so 1/|D| grows as γ³); an input
error that is the same at every γ has an effect on D that need not be. The candidates are therefore all open:

| H | candidate | what it predicts |
|---|---|---|
| H1 | truncation of scipy's DOP853 (rtol, atol 1e-14) | the gap falls as rtol falls; scipy's integrator on a smooth planted system with a known answer errs by about the gap |
| H2 | the star and M_ext as inputs (scipy's `solve_bvp` star, tol 1e-9, against the crate's) | the crate's star in `PolarProblem` moves D by more than the realization noise and removes the gap |
| H3 | rounding noise in J (f64 arithmetic), amplified by D's conditioning | planted noise of 1 ulp per entry of J moves D by about the realization noise, in proportion to its size |
| H4 | the kinks of `solve_bvp`'s cubic interpolant make the integrator's error erratic | the realization noise falls when the star is smooth (the crate's) |

## What is built

- **`CrateStar`** (`taylor_drift.py`): the crate's star as data. The new crate command `starsteps` dumps the 163 Taylor steps (order
  30, coefficients of (P, u, m, Z) = (φ0², φ0′/φ0, m, α⁻²) about each step's x0, 20 digits, to r = 62; `crate_star_steps.jsonl`, central
  data P_c = 3.8668247305203969e-4 and Z_c = 0.98111972688634190 from `taylor_polar star`, rs = 1e-8, nothing from scipy). A class with
  `bg(r)`, `w`, `eps`, `r0`, `R` replaces `solve_star`'s object in `PolarProblem`. It sums each step's series in f64.
- **`DriftProblem`** (`taylor_drift.py`): `PolarProblem` with five knobs, all off by default (then the code path is `PolarProblem`'s, bit
  for bit, check IDENT): `atol`, `extra_chunks` (the chunk count of `_integrate_plane` plus n: the same problem on another chunk grid),
  `vac_scalar` (the exterior scalar plane integrates in vacuum at every r, as the crate does; see below), `mext` (M_ext replaced) and
  `noise_ulp`, `noise_seed` (every entry of every J the integrator evaluates is multiplied by 1 + noise_ulp · 2⁻⁵³ · ξ, ξ standard
  normal, numpy `default_rng(seed)`). `D` is `PolarProblem.D` with the same operations; it keeps the two planes to print the sines of the
  principal angles between them (|D| is their product).
- **`planted`**: scipy's `_integrate_plane`, unchanged, on #186's planted system y′ = A y (`taylor_polar.planted_A`, A = blockdiag
  [[0, 1], [g², 0]] + C, growth e^{γ r}, D ≈ γ⁻³ like the real one), L = 24.1, the decaying plane from L + 30/γ; the reference is the
  invariant subspaces at 90 digits in mpmath (`converged_plane`), which shares no code with the integrator. J is exact here (a constant
  matrix of dyadic entries), so this isolates the chunked DOP853 and the QR from the evaluation of J.
- **`crate`**: the crate's reference D, taken from `taylor_polar.get_rows` (the `rows` command of #187): double-double order 30,
  tol 1.2e-30 (`base`, `phi`); order 24 at tol 1e-22 (`o24`, and the new `phio24`, which is `phi` at order 24); Taylor tol 1e-12 (`tol`,
  base only); f64; quad-double at γ = 1000.
- **What differs between the two paths besides the integrator** (read in `polar.rs` and `polar_solver.py`, not assumed): scipy's
  `scalar_plane` integrates the exterior scalar plane from R_s = r_m + 40/γ down to r_m with `jf = _Jvac if r > st.R else J`, and
  st.R = 60, so it uses the *star's* J there. The crate uses vacuum J (Schwarzschild of M_ext) throughout (`VacSource`). With the exact
  star the two agree to ε φ0² (about 1e-24); with scipy's star they differ by the star's error in α, a and u. The plant `sci_vac`
  integrates in vacuum with scipy's star. Everything else (the symbolic J, the r_m rule, the flat start data, the Riccati start, the
  Moncrief map, the scalar start) is shared.

## What a gap is, and the reference

**gap = |D_scipy / D_crate − 1|**, D_crate the crate's double-double D (base: r_m = 24.10980364018201; φ_cut: r_m = 34.20514015700785,
the `phi_cut 1e-12 (larger r_m)` variant of `convergence.py`; both r_m equal to the last bit on scipy's and the crate's star, #187's RM,
check RMX). "The crate's r_m" is therefore the same number as scipy's, and substituting it changes nothing; it is tested rather than
planted. The reference's own accuracy (check REF): dd against order 24 at tol 1e-22 and, at γ = 1000, quad-double, bar 1e-20; the dev
values are 1.5e-26 … 4.5e-24 (`dev_26`). Its lane differences, printed and not gated: f64 against dd 5.5e-11 … 2.8e-9 over the six
cells (`dev_22`), Taylor tol 1e-12 against dd 1.7e-14 (1000), 9e-16 (2000), 9e-18 (3000) in base.
**A gap is one realization.** It is one evaluation on one chunk grid; the null control below measures how much D moves when only the
chunk grid changes.

## The runs

Cost, measured (`dev_02`, `dev_03`, `dev_05`): (5, 1000), base, rtol 1e-10, 132 to 137 s per evaluation at load 2.6 to 2.8, one thread,
nice 10; the crate's star in place of scipy's costs the same. Scaling with γ (chunks ∝ γ) and r_m (34.2 against 24.1, about ×1.4) and
with rtol (about ×2.3 from 1e-10 to 1e-13) gives about 6 h of one thread for the core grid, 3 h on two processes. The earlier estimate
of 4 to 6 h stands for the whole task.

Two processes at nice 10, detached (`nohup`), `run_A.sh` and `run_B.sh` through `runrec.sh` (log, err with `/usr/bin/time -l`, rc);
one JSON line per case in `jsonl/scipy_*.jsonl`, resumable; each case stops after 7200 s and is recorded `stopped`.

**Core grid (all must finish; check COMPLETE counts 55 cases)**, l = 5, variants base and φ_cut, γ = 1000, 2000, 3000:

| name | what | cases |
|---|---|---|
| P0 | scipy's star, rtol 1e-10, 1e-11, 1e-12, 1e-13 (the issue's first part) | 24 |
| P1 | the crate's star and its M_ext in `PolarProblem`, rtol 1e-10 and 1e-13 (the issue's planted input) | 12 |
| N0 | P0 at rtol 1e-10 with one extra chunk: the null control, η = \|D(N0)/D(P0) − 1\| | 6 |
| N1 | P1 at rtol 1e-10 with one extra chunk | 6 |
| NOISE | scipy's star, base, rtol 1e-10, noise 1 ulp seeds 1, 2, 3 and 0.1 ulp seeds 1, 2 at γ = 1000; 1 ulp seeds 1, 2 at γ = 3000 | 7 |
| PLN | the planted system through scipy's integrator, γ = 1000, 2000, 3000, rtol 1e-10 and 1e-13 (file `planted.jsonl`, not in COMPLETE) | 6 |

**Extras** (run after the core in this order, reported whatever they show, not gating; one stopped by me before it ends is reported as
not run): X_N0R13 (N0 at rtol 1e-13: γ = 1000 both variants, 3000 base), X_P2 (`sci_vac`, rtol 1e-10, γ = 1000, 3000), X_ATOL (atol
1e-17 at rtol 1e-13, γ = 1000 both, 3000 base), X_P3 (`int_crate`: the crate's star in the interior with scipy's M_ext, and `ext_crate`:
scipy's star with the crate's M_ext, at (3000, base)), X_P1R (P1 at rtol 1e-11 and 1e-12, which completes the issue's second grid).

## Declared criteria and decision rules (before the first run of record)

All thresholds are constants in `taylor_drift.py` (`CRIT`); none is changed after a run. A criterion that fails on real data is reported
as not met.

1. **The rtol curve**, per cell (γ, variant): ρ = gap(rtol 1e-13) / gap(rtol 1e-10) in P0. Label *truncation* if ρ ≤ 0.1, *floor* if
   ρ ≥ 0.5, else *mixed*.
2. **The planted input moves D** in a cell iff |D_P1/D_P0 − 1| > max(3 η, 1e-12) at rtol 1e-10, η from N0. **It moves the gap** by the
   factor gap_P1/gap_P0 at the same rtol, labelled *removes* (≤ 0.1), *none* (≥ 0.5), *partly*.
3. **The planted system** (PLN) *accounts* for the gap in a cell if its error is ≥ 0.3 of the gap at the same (γ, rtol 1e-10), *not* if ≤ 0.03.
4. **Planted noise** (NOISE): scatter = rms over the seeds of |D/D_P0 − 1|. It *accounts* for the null scatter η if the scatter at 1 ulp is
   ≥ 0.3 η at both γ and the scatter at 0.1 ulp is ≤ 0.5 of that at 1 ulp (γ = 1000); *not* if ≤ 0.03 η at both.
5. **Hypotheses**, from the above, in `verdicts`:
   - H1 *supported* if all six rtol curves are *truncation*; *ruled out* if PLN is *not* in all six cells and at least four curves are not *truncation*.
   - H2 *supported* if the plant moves D in all six cells and the gap at rtol 1e-13 is *removed* in all six; *ruled out* if it moves D in at most one.
   - H3 *supported* if planted noise *accounts* (rule 4); *ruled out* if *not*.
   - H4 *supported* if η(N1)/η(N0) ≤ 0.1 in at least 5 of 6 cells; *ruled out* if ≥ 0.5 in at least 5 of 6.
   - Otherwise *undecided*. **A cause is named only if exactly one hypothesis is supported and the other three are ruled out**; otherwise
     "not established", with the four statuses. A named cause carries the status word *numerical evidence* (not *proved* or *certified*).

## Checks and their controls (`python taylor_drift.py check --dir=jsonl --steps=...`; `--mutate=NAME`)

Every check has a mutation; its effect on what the check reads was computed in a development run before it is declared here.

| check | what it must show | bar | mutation | effect, development run |
|---|---|---|---|---|
| IDENT | `DriftProblem` with no knob equals `PolarProblem` bitwise at (2, 10); atol, one extra chunk, 1 ulp of noise each move D; the same noise seed twice gives the same D | equality | `ident_atol`: the no-knob run built with atol 1e-6 | D differs by 1.2e-8, FAIL (`dev_14`); unmutated PASS (`dev_23`: atol 1e-6 moves D 1.2e-8, a chunk 6.9e-12, noise 7.5e-12) |
| CS | the dumped star in f64 equals `starcheck` (dd) at 12 radii, 4 functions | 1e-14 | `cs_order`: the series cut at order 8 | 4.5e-6 at r = 30, FAIL (`dev_15`); unmutated 1.9e-16 (`dev_08`) |
| RMX | `PolarProblem`'s r_m on scipy's and on the crate's star equals `taylor_polar.R_M`, both variants, to the last bit | equality | `rm_cut`: φ_cut 1e-11 on the crate's φ variant | r_m 30.82 against 34.21, FAIL (`dev_16`); unmutated PASS (`dev_08`) |
| REP | this Mac's scipy D at (5, 1000) (base rtol 1e-10, base rtol 1e-12, φ_cut) against the win laptop's stored D (`I4-win`) | 1e-8 | `rep_variant`: base compared with the stored φ_cut D | 1.0, FAIL (`dev_25`); unmutated 5.6e-10 on the base cell (`dev_24`) |
| REF | the crate's dd D against order 24 and (γ = 1000) quad-double, six cells | 1e-20 | `ref_tol`: the base reference replaced by the Taylor tol 1e-12 row | 1.7e-14, FAIL (`dev_27`); unmutated 4.5e-24 (`dev_26`) |
| CLS | the three classifiers and the naming rule give the declared labels on synthetic tables | labels | `cls_swap`: two labels swapped | FAIL (`dev_29`); unmutated PASS (`dev_28`) |
| PLN0 | scipy's integrator on the planted system at γ = 10, 100 against mpmath (the harness itself) | 1e-6 | `pln_sign`: the reference's sign flipped | 2.0, FAIL (`dev_20`); unmutated 1.1e-14 (`dev_19`) |
| COMPLETE | the 55 core cases are present and finished | all | `drop_cell` | 54 of 55, FAIL (`dev_32`); unmutated PASS (`dev_31`, on a synthetic complete set) |

REP's bar is loose by design: two machines, one code. The one pair it has seen (`dev_24`) differs by 5.6e-10, larger than the gap that
motivates the task (3.4e-10 on this Mac, 9.0e-10 on the win laptop, at (5, 1000)).

## What the development runs showed, and what they changed

- `dev_02`, `dev_03`, `dev_05` (one (5, 1000) base case each, rtol 1e-10; crate dd D = −1.9301859625832848e-10):

  | case | D | gap |
  |---|---|---|
  | scipy's star, this Mac | −1.9301859632455635e-10 | +3.4e-10 |
  | scipy's star, one extra chunk | −1.9301859619273796e-10 | −3.4e-10 |
  | crate's star and M_ext | −1.9301859624594586e-10 | −6.4e-11 |
  | scipy's star, win laptop (`I4-win`, stored) | −1.930185964326392e-10 | +9.0e-10 |

  Moving the chunk grid by one chunk moves D by 6.8e-10, twice the gap; the two machines differ by 5.6e-10. **At (5, 1000) the gap
  is realization noise of this size**, and one planted input (4.1e-10) cannot be told from it without a null control. This is why
  N0, N1 and the noise runs are in the core grid. M_ext: scipy's −0.014580496641517959, the crate's −0.014580496640979936 (5.4e-13 apart);
  α(r_m)/√(1 − 2M/r_m) − 1: −1.7e-13 (scipy's star), 2e-16 (the crate's). The star is a good one at r_m.
- `dev_21`: scipy's integrator on the planted system errs by 1.8e-13 to 2.3e-13 at rtol 1e-10 and 4.5e-14 to 1.4e-13 at rtol 1e-13
  (γ = 1000, 2000, 3000; D = 4.3e-9, 5.4e-10, 1.6e-10), three orders below the real gap.
- `dev_22`: the crate's f64 lane against dd, 5.5e-11 … 2.8e-9: the same size as scipy's noise, on the same exact tables; f64 roundoff
  amplified by D's conditioning is a candidate (H3) to be tested with planted noise, not to be assumed.
- The loops `dev_09` to `dev_13` failed (rc 2) because zsh does not split `$m` in `set -- $m`; they are kept, `dev_14` to `dev_18` are the
  same controls through `dev_ctl_loop.sh` (bash).
- The `starsteps` command and the `phio24` variant are crate additions that these runs needed; no other crate code was changed.

## Amendments

- **A1 (2026-11-27, before the first run of record).** `dev_07` (the crate's quad-double rows at γ = 1000) was stopped by me after 9 min, by the PIDs of its
  script, its python and its rust child, to free a thread; `dev_07_note.txt` says so, and it has no `.rc`. `run_B.sh` redoes it as a run of record
  (`crate --qd --qd-gammas=1000`, γ = 1000 only) together with the dd, order 24 and f64 reference rows, ahead of its scipy cases. `taylor_drift.py` got the
  `--qd-gammas` flag for this (commit 2cc3857, after the one the README names, ec7b99a); nothing else changed. The runs of record started at 09:08 (A: `run_01`, B: `run_02`).

- **A2 (2026-11-27 09:55, before any NOISE, NOISEROW, X_ATOL or P1 run; P0 at rtol 1e-10 has 5 of 6 cases and N0 has 3 of 6, which I have read).** Three changes,
  none of which moves a threshold of the rules above.
  1. **The amplitude of planted noise is measured, and the declared knob does not match it.** `taylor_drift.py jround` (`dev_33`) evaluates the generated
     `J_and_h` in f64 at the inputs the integrator gives it (scipy's star, l = 5, 40 radii in [0.5, 34.2], γ = 1000 and 3000) against the same source at 60 digits
     (`taylor_polar.mp_J`). The relative error of an entry is 2651 ulp rms (max 57481 ulp, at r = 32.5, entry (3, 5)), because small entries of a row inherit the
     rounding of its large terms; relative to the largest entry of its row it is 1.05 ulp rms (γ = 1000) and 0.93 (γ = 3000), max 11.4 and 6.0. The knob `noise_ulp`
     (1 ulp of each entry) therefore plants far less than the generated J's rounding for the small entries. New knob `noise_row`: every nonzero entry gets the
     absolute noise `noise_row` · 2⁻⁵³ · ξ · (largest entry of its row), ξ standard normal. New core group **NOISEROW**, 7 cases: noise_row 1.0 with seeds 1, 2, 3 and 0.1 with
     seeds 1, 2 at (1000, base); 1.0 with seeds 1, 2 at (3000, base); rtol 1e-10. **The verdict on H3 (rule 4) is taken from NOISEROW** with the same thresholds
     (0.3, 0.03, linear 0.5); the 7 NOISE cases stay in the core grid and are reported beside them. COMPLETE counts 62 cases (`dev_35` pass, `dev_36` `drop_cell` fails,
     61 of 62). IDENT also requires the new knob to move D and to repeat with its seed (`dev_34`: 1 ulp of the row maximum moves D by 3.4e-12 at (2, 10), a chunk by 6.9e-12,
     1 ulp per entry by 7.5e-12).
  2. **A fifth hypothesis, H5**: scipy's absolute tolerance atol = 1e-14 sets the plane error. The gaps correspond to plane errors (gap × smallest sine of the
     principal angles) of 1.7e-14 to 2.7e-13, the size of atol. Rule: the gap at (atol 1e-17, rtol 1e-13) against the gap at (atol 1e-14, rtol 1e-13) in X_ATOL's three cells
     (1000 base, 1000 φ_cut, 3000 base) is *removes* (≤ 0.1) in all three: *supported*; *none* (≥ 0.5) in all three: *ruled out*; otherwise *undecided*. The naming rule
     now counts five hypotheses.
  3. **The order of the rest of process B changes** (`run_B2.sh`, started by `watch_swap.sh` when N1 has 6 cases, replacing `run_B.sh` by PID: it freezes it, stops its
     child and it): N0 and N1 as before, then NOISEROW, NOISE, P1 (rtol 1e-10, 1e-13), then X_ATOL, X_N0R13, X_P2, X_P1R (rtol 1e-12). X_ATOL moves ahead of the other
     extras for H5. Resumable files, so no case is run twice. `run_A.sh` still lists X_ATOL after P0; it will find those cases done.
  Also `planted` records the principal angles of the planes it produces (in the file from the start) and takes `--noise-ulp`; the planted system's plane errors are
     err × smallest sine = 3e-16 … 6e-17 (`planted.jsonl`), 100 to 1000 times below the real problem's.

- **A3 (2026-11-27 11:35, before any NOISE, NOISEROW, CJ, CJE, CJN, X_ATOL or P1 datum; P0 at rtol 1e-10 and N0, N1 are complete and read, and P0 at rtol 1e-13 has 3 of 6 cases).**
  What happened first. The row-scaled noise at amplitude 1 made the integrator thrash: the first NOISEROW case ran 22 min without finishing against 2.3 min for an unperturbed one;
  I stopped `run_B2.sh` and its python by PID (no record was written) and piloted the cost (`dev_38`, `pilot_noise_speed.py`, mid-star, 300 chunks, γ = 1000, rtol 1e-10):
  9.5 steps per chunk unperturbed, 9.5 with 1 ulp per entry, **560 with 1 ulp of the row maximum** (65 times the work), 10.8 with 0.01 ulp. The generated J's own rounding is 1.05 ulp of
  the row maximum rms (`dev_33`) and does not thrash, so independent planted noise at that amplitude is not a faithful emulation of it. Then the better handle: **the crate's J tables
  in the scipy path.** `crate`'s `jtable` command (new) dumps the table of J = J0 + s² J1 (464 steps, 24 entries, Taylor coefficients 0..29 about each step's start, double-double
  rounded to 20 digits; `crate_jtable_l5.jsonl`, 19.7 MB, regenerated by `taylor_drift.py j-table`); `CrateJ` sums them in f64 and `DriftProblem(jtab=...)` uses them in place of
  `J_and_h` (the interior and the exterior scalar plane's J; the vacuum J beyond r = 60 is not replaced). Plant **`crate_j`** = the crate's star, M_ext and J tables. New check **CJ**: against
  `J_and_h` at 60 digits on the exact star (12 radii, γ = 1000, 3000, 576 entries) the table's per-entry error is rms 1.12 ulp, max 4.5 ulp (bars 10 and 100; `dev_40`), the generated J in
  f64 on its own inputs rms 3.1e7 ulp, max 5.2e8 ulp (12 radii from r = 0.002; `dev_33` has 2651 rms over r ≥ 0.5); mutation `cj_shift` (the series summed from the step's end): rms 1.8e15 ulp,
  FAIL (`dev_41`). **The table also makes a case 10 times cheaper**: (5, 1000, base, rtol 1e-10) takes 11 to 14 s against 136 s (`dev_42`). That allows realization ensembles. Changes, all declared here
  before any datum of the groups they concern:
  1. **NOISE and NOISEROW leave the core** (not run, extras X_NOISE if time permits): the per-entry noise on `J_and_h` is cheap and the row noise is unfaithful, and CJN below replaces both.
  2. **CJE** (core, 72 cases): plant `crate_j`, the cells (1000, base), (1000, φ_cut), (3000, base), the settings (rtol, atol) = (1e-10, 1e-14), (1e-13, 1e-14), (1e-13, 1e-17), and 8 realizations each
     (extra chunks 0 … 7). Per cell and setting: mean and standard deviation (ddof 1) of the signed gap, and t = mean / (std / √8).
  3. **CJN** (core, 20 cases): plant `crate_j`, (1000, base), rtol 1e-10, atol 1e-14: planted noise 1, 10, 100 ulp per entry and 0.01, 0.1 ulp of the row maximum, seeds 1 … 4 (each case stops after 900 s;
     a stopped case is reported as such and makes COMPLETE fail): the dose-response of the scatter to planted rounding, against CJE's 8 realizations at no noise.
  4. **P1 in the core is rtol 1e-10 only** (6 cases); P1 at rtol 1e-13 is the extra X_P1_13. H2's rule is read on the gap at rtol 1e-10 (it said 1e-13). The thresholds are unchanged.
  5. **H1, H5 and H3 are re-based** on the exact-J system; thresholds as before (0.1, 0.5). H1: std(rtol 1e-13, atol 1e-14) / std(rtol 1e-10, atol 1e-14) over CJE's realizations, per cell:
     *supported* if ≤ 0.1 in all three cells, *ruled out* if ≥ 0.5 in all three. H5: std(rtol 1e-13, atol 1e-17) / std(rtol 1e-13, atol 1e-14), same thresholds. H3 (rounding in the
     generated J_and_h): η_J / η_1, with η_J = |D(extra chunk 1)/D(0) − 1| on `crate_j` and η_1 the same on the crate's star with `J_and_h` (N1), in the three cells: *supported* if ≤ 0.1 in all
     three, *ruled out* if ≥ 0.5 in all three (η_1 is read: 6.8e-10 → 1.0e-9 at (1000, base); η_J at that cell in `dev_42` is 3.3e-10, ratio 0.33: that dev value is not a datum of record). H2 and H4 as declared.
     P0 and the issue's tables are reported as the issue asks, with their ensembles, and are not the basis of H1 or H5 any more (J_and_h's rounding and the star's interpolation noise them).
  6. **Order**: `run_B3.sh` replaces `run_B2.sh` (CJE, CJN, P1 at rtol 1e-10, then the extras X_ATOL, X_P1_13, X_N0R13, X_P2, X_P3). A is unchanged (P0 first).
  COMPLETE counts 134 core cases (P0 24, P1 6, N0 6, N1 6, CJE 72, CJN 20; `dev_43` pass, `dev_44` `drop_cell` fails 133 of 134). A script change during the runs: `--extra-chunks` takes a list.
  The estimate is revised to about 6.5 h in total (the issue's P0 grid alone is 3.6 h on a thread, the load on the Mac is 4 to 15).

- **A4 (2026-11-27 12:10, before any `crate_j_vac` datum; CJE has 65 of 72 cases and I have read its first 8 cells and settings).** CJE (exact J, 8 realizations) shows at (3000, base), rtol 1e-13: mean signed gap
  −1.33e-9 (t = −8.2), and −1.66e-9 (t = −5.6, 5 of 8 realizations) with atol 1e-17: a systematic offset of scipy's path against the crate, beyond the scatter, and not moved by atol. At γ = 1000 the means are
  within 1.5 σ/√8 of zero. A difference of construction I had noted in "What is built" is the candidate: **H6**, the exterior scalar plane. PolarProblem integrates it from R_s = r_m + 40/γ to r_m
  through the star's J (r < 60), which keeps the scalar–metric couplings proportional to φ0 (about 1e-9 at r_m for φ_cut 1e-9, 1e-12 for φ_cut 1e-12); the crate integrates it in exact vacuum (couplings zero).
  Plant `crate_j_vac` = `crate_j` with `vac_scalar` (the crate's treatment, scipy's integrator). New core group **CJV** (24 cases): rtol 1e-13, atol 1e-14, 8 realizations at (3000, base), (1000, base), (1000, φ_cut).
  Rule: at (3000, base), mean_vac = mean signed gap of CJV, mean_novac that of CJE (rtol 1e-13, atol 1e-14): **H6 supported if |mean_vac| ≤ 0.3 |mean_novac|; ruled out if ≥ 0.7; else undecided.**
  COMPLETE counts 158. `run_V.sh` runs it with `run_A.sh`'s python paused (SIGSTOP by PID, resumed after) so that two processes run at a time.

- **A5 (2026-11-27 12:25, before any `crate_j_r13`, `crate_j_q13` or `crate_j_q12` datum; CJV has 13 of 24 cases and its (3000, base) cell is complete and read).**
  **CJV result (read):** the 8 realizations at (3000, base), rtol 1e-13, with the exterior scalar plane in vacuum equal CJE's to the printed two digits (mean −1.34e-9 against −1.33e-9):
  the scalar-plane treatment does not make the offset (H6 will come out *ruled out*, ratio 1.0). **What else is common to all realizations**: the exterior Zerilli column. `PolarProblem.zerilli_q`
  hard-codes `solve_ivp(..., rtol=1e-11, atol=1e-14)` and ignores `self.rtol`, so the issue's rtol sweep never touches it. The stored full-precision q_ext (`I4-win`, base variant) differs from
  the crate's by 6e-14 relative at γ = 1000 and 3.6e-14 at 6000 (read from the files; not a run of this issue). With D = Π sin θ_i and sin θ_min = 1.6e-5 at (3000, base), an error of
  5e-14 in the exterior column can move D by order 5e-14 / 1.6e-5 = 3e-9. **H7**: the offset comes from the Riccati integration of q at rtol 1e-11. Knobs (`DriftProblem`): `riccati_rtol`,
  `riccati_atol` (a line-for-line copy of `zerilli_q` with the tolerances as parameters; default is `PolarProblem`'s, bit for bit: IDENT, `dev_*_check_IDENT_A5`, which also needs q planted 1e-9 off to move D
  by 5e-10 and the Riccati at rtol 1e-5 to move it by 6.4e-7 at (2, 10)) and `q_eps` (q multiplied by 1 + q_eps). Plants `crate_j_r13` (Riccati rtol 1e-13, atol 1e-16), `crate_j_q13`, `crate_j_q12`
  (q planted 1e-13 and 1e-12 too large). New core groups **CJR** (24 cases: `crate_j_r13`, rtol 1e-13, atol 1e-14, 8 realizations at (3000, base), (1000, base), (1000, φ_cut)) and **CJQ** (4 cases: the planted q errors at
  (1000, base) and (3000, base), rtol 1e-10, extra chunks 0, which differ from CJE's case with the same chunk grid only by q, so the change of D is free of realization noise: the sensitivity of D to q).
  Rule for H7: at (3000, base), mean_r13 = mean signed gap of CJR, mean_1e11 = that of CJE (rtol 1e-13, atol 1e-14): **H7 supported if |mean_r13| ≤ 0.3 |mean_1e11|; ruled out if ≥ 0.7; else undecided.**
  COMPLETE counts 186. Order: `run_R.sh` runs as soon as CJV ends, with `run_A.sh`'s python still paused; A resumes after it. The P0 layer rtol 1e-12 will be run from the second slot when `run_B3.sh` has finished P1
  (`run_P12.sh`), `run_A.sh` continues with 1e-13 and 1e-11; whichever is not finished at 14:30 is reported as not run.

- **A6 (2026-11-27 12:55, before any `planes_*.jsonl` datum of record; the dev run `dev_47` of the planes is read).**
  What I read first. CJQ (`jsonl/scipy_CJQ.jsonl`): D's sensitivity to a planted relative error of q is (ΔD/D)/(Δq/q) = −1.46 and −0.24 at γ = 1000, 0 and −0.43 at γ = 3000, so q's known error
  (6e-14) moves D by at most 1e-13, and the Riccati's tolerance (H7) cannot make a bias of 1e-9. CJN per-entry noise (12 cases, 11 to 16 s each): the scatter of D is 3e-10 at 1 ulp (as at no noise), about 1e-9
  at 10 ulp, 1e-8 at 100 ulp. CJN row-maximum noise at 0.01 ulp took 500 to 580 s a case against 13 s (thrash, as in `dev_38`; 3 of 4 cases done; the case at 0.1 ulp would hit the 900 s cap four times).
  **Planes** (`taylor_drift.py planes`, new; the crate's `rows` command got `planes=1`, new): scipy's two orthonormal 3-planes at r_m against the crate's double-double ones, as the sine of the largest principal angle.
  `dev_47` at (3000, base), crate_j, rtol 1e-13, atol 1e-14, extra chunks 0 … 3: **interior plane ε_Y = 2.4e-14, 7.8e-15, 2.7e-14, 2.0e-14; exterior plane ε_Z = 2.2e-16 in all four, its metric direction 0 (to the last bit)
  and its scalar plane 2.5e-16 … 3.5e-16.** The whole error of D sits in the interior plane: ε_Y / sin θ_min (1.6e-5) = 1.5e-9 … 1.7e-9, the size of the bias.
  Changes, declared before any planes datum of record:
  1. **Dropped from the core**: CJR (24 cases, not run; a stopped `run_R.sh` has 1 case, kept) and the row-maximum noise of CJN (8 cases; 3 done, kept; extras X_CJN_ROW, X_CJR). I stopped `run_B3.sh` and `run_R.sh` by PID (frozen, children stopped,
     then killed) at 12:50. COMPLETE counts 154: P0 24, P1 6, N0 6, N1 6, CJE 72, CJN 12 (per entry), CJV 24, CJQ 4.
  2. **H7 is re-based** on CJQ (it was on CJR): sens = max over the two planted q errors of |ΔD/D| / (Δq/q) at (3000, base); t = sens × 6e-14 / |bias|, bias = |mean signed gap| of CJE at (3000, base), rtol 1e-13, atol 1e-14.
     *Supported* if t ≥ 0.3; *ruled out* if t ≤ 0.03; else *undecided*. (CJQ is read: t = 0.43 × 6e-14 / 1.3e-9 = 2e-5.)
  3. **H8, roundoff accumulation of the interior plane's renormalizations.** The interior plane is renormalized every 2/γ (12 000 times at (1000, base)). Knob `chunk_factor` (interior only): 1/4, 1/2, 1 (as PolarProblem), 2, 4, 8 times as many.
     Plants `crate_j_cf025`, `_cf05`, `crate_j`, `_cf2`, `_cf4`, `_cf8`; (1000, base), rtol 1e-13, atol 1e-14, extra chunks 0 … 3, `planes_CF.jsonl` (24 cases). Per factor the median ε_Y over the four.
     **H8 supported if median(8×) / median(1×) ≥ 2.0 and median(1/4×) / median(1×) ≤ 0.7; ruled out if the three medians (1/4×, 1×, 8×) lie within a factor 1.3 of each other; else undecided.**
  4. Also planes at (3000, base) (extra chunks 0 … 3, `planes_3000.jsonl`) and (1000, φ_cut) (`planes_1000phi.jsonl`). The planes files are not in COMPLETE.
  5. Order: `run_F.sh` (the planes) and `run_B4.sh` (P1 at rtol 1e-10, then P0 at rtol 1e-12, then X_ATOL and X_P1_13) in the two slots; `run_A.sh`'s python resumes (SIGCONT) when `run_F.sh` ends. Whatever of P0 is not finished at 14:30 is reported
     as not run. Total estimate about 7 h.

- **A7 (2026-11-27 13:55, a time box, before the data of the cells it concerns).** The load on the Mac (4 to 5 from other users, 15 at times) made the P0 cells about twice as slow as planned
  (`(1000, base, rtol 1e-12)` took 551 s against 240 s; `(2000, phi, rtol 1e-13)` 6572 s with 55 min paused by me). P0 as declared (24 cells) cannot finish in the 6 to 7 h the task has. Rule:
  the cells (3000, phi, 1e-13), (3000, base and phi, 1e-11) and (3000, base and phi, 1e-12) are **not run** (5 cells, reported as such, and COMPLETE fails on them); the cells (1000 and 2000, base and phi, 1e-11)
  run in `run_A2.sh`; `run_A.sh` and `run_B4.sh` are stopped by PID after their (3000, base, 1e-13) and (2000, phi, 1e-12) cases (the bash scripts were killed at 13:50 so that they start nothing more; `watch_timebox.sh`
  stops their pythons). Planned beyond A6: the extras X_ATOL and X_P1_13 are not run. The timestamps of A2 to A6 above are the planned ones; the machine's clock was 9 to 16 minutes earlier at each (A2 09:46, A3 11:25,
  A4 12:06, A5 12:20, A6 12:39).
  **A7 amendment, 14:02 (clock): the case (3000, base, rtol 1e-13) was stopped by its own alarm** (status `stopped`, 7200 s of wall: it ran from about 11:59, 55 min of which `run_A.sh`'s python was paused by me for the
  `crate_j_vac` and plane runs; the stop condition counts wall time). It is not rerun. `run_A.sh`'s python was killed by PID at 14:02 while it ran (3000, phi, 1e-13), which is therefore not run either; `watch_timebox.sh` was killed
  (its first condition could not fire). `run_A2.sh` (P0 at 1e-11, γ = 1000 and 2000) runs in that slot; `run_B4.sh`'s python continues with the rtol 1e-12 layer and is stopped by me by PID at 15:00 whatever it has finished
  (the (3000, base, 1e-12) case is the last it may reach). Not run, so: P0 at (3000, base, 1e-13), (3000, phi, 1e-13), (3000, both, 1e-11), (3000, phi, 1e-12) and (3000, base, 1e-12) unless it finishes: 5 to 6 of 24.
  **Time box applied, 14:50 (clock).** `run_A2.sh` and `run_B4.sh`'s pythons were killed by PID (34210, 73881) with 17 of 24 P0 cells finished; the cells running at that moment, (2000, phi, 1e-11) and (3000, base, 1e-12), have no record.
  P0 finished: rtol 1e-10 all six; 1e-11: (1000, base), (1000, phi), (2000, base); 1e-12: (1000, base), (1000, phi), (2000, base), (2000, phi); 1e-13: (1000, base), (1000, phi), (2000, base), (2000, phi).
  **Not run (7 of 24):** (2000, phi, 1e-11), (3000, base, 1e-11), (3000, phi, 1e-11), (3000, base, 1e-12), (3000, phi, 1e-12), (3000, base, 1e-13) (stopped by its alarm, record kept), (3000, phi, 1e-13). COMPLETE therefore fails by design of the time box.
  The checks and their controls then run as `run_C1.sh` and `run_C2.sh` (two processes), the output file is assembled by `assemble_output.py`.

## Runs of record and result (assembled 2026-11-27 15:10)

Result in one paragraph: see `phase2/nonradial/taylor_drift.md` (the note) and `taylor_drift_output.txt` (assembled from the logs below by `assemble_output.py`). The checks: 8 pass, COMPLETE fails (7 of the 24 P0 cells not run, A7);
each control fires on its target (`run_11` … `run_15`, `run_18` … `run_21`; on real data `drop_cell` moves COMPLETE from 147 to 146 of 154, its pass-to-fail effect is the synthetic set of `dev_43`, `dev_44`).
The check table of the README's first version lacks CJ (A3: the crate's J tables in f64 against the generated J at 60 digits, rms 1.12 ulp, max 4.5 ulp, bars 10 and 100; control `cj_shift`, `dev_41`, `run_21`).

| run | what | exit |
|---|---|---|
| `run_01` | A: P0 rtol 1e-10, 1e-13; stopped by me (bash killed 13:50, python killed 14:02) | killed |
| `run_02` | B: crate reference, planted system, N0, N1; replaced by `run_03` after N1 (A2) | killed |
| `run_03` | B2: stopped at its first NOISEROW case (thrash, A3) | killed |
| `run_04` | B3: CJE, CJN (row noise stopped), replaced by `run_08` (A6) | killed |
| `run_05` | CJV | 0 |
| `run_06` | R: CJQ, 1 case of CJR, stopped (A6) | killed |
| `run_07` | F: planes | 0 |
| `run_08` | B4: P1, P0 at 1e-12; python killed 14:49 (A7) | killed |
| `run_09` | A2: P0 at 1e-11; python killed 14:49 (A7) | killed |
| `run_10` | the checks | 1 (COMPLETE) |
| `run_11` … `run_15`, `run_18` … `run_21` | the controls | 1 each, as expected |
| `run_16`, `run_22` | the report (`run_22` adds the γ² section) | 0 |
| `run_17` | `jround` | 0 |

Files: `jsonl/` (every case, one JSON line each; the crate's reference rows `rows_l5_*.jsonl`; the planes and the planted system), `crate_star_steps.jsonl`, `crate_jtable_l5.jsonl.gz` (19.7 MB uncompressed, regenerated by
`taylor_drift.py j-table`), `dev_*` (development runs; `dev_09` … `dev_13` failed on zsh's word splitting, `dev_07` was stopped by me).
