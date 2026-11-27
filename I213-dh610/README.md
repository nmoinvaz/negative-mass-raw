# I213-dh610: the Ellis threshold's expanding branch, followed past the linear mode (D = 4, 5)

Machine: dh610-fedora (Fedora 45, Linux 7.3.3, Intel i7-12700, 20 threads, 62 GB), shared with choptuik-large-d (load average 12 to 20 of 20 during the
development runs). At most 4 processes, one thread each, `nice -n 10`. Issue: https://github.com/nmoinvaz/negative-mass/issues/213.
Worktree `~/Source/negative-mass-i213`, branch `wip/i213-expanding-branch`, base main 3e15f46 (#39's code, unchanged). Python
`~/Source/negative-mass-venv314/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1, numba 0.68.1, sympy 1.14.0, mpmath 1.3.0). The evolution is #39's `dn.py`
(`dn.row_step`, the row sweep of `dn.evolve`) and its `checks.bisect_A`, `checks.fate_run`, `W_EXACT`. The driver is `notes/wormhole_evolution/expansion.py` at
**1b6b43d**, committed and pushed before this README and before any run of record.

**This README was written after the development runs `dev/dev_01` to `dev/dev_13` listed below and before the first run of record.** Everything under
"Declared" is the `CRIT` and `MUTATIONS` tables of `expansion.py` at 1b6b43d, in words. Nothing there is changed after a run of record has been seen. A
criterion that is not met is reported as not met. A control that fires on real data stops the work until the cause is known. Status words as in AGENTS.md:
every number below is *numerical evidence* unless marked *proved* or *checked symbolically*. No sentence here says a universe forms.

## Contents

```
I213-dh610/
├── README.md
├── scripts/            lane.sh (one lane of the queue of record), queue_*.txt (its job lines)
├── dev/                development runs (kept, none edited): dev_NN_*.py, dev_NN.log, mut/ (dev_11), mut13/ (dev_13), rec_trial/ (dev_12)
└── runs/               runs of record
    ├── D<D>_<member>_h<h>.npz        one streamed run: the diagonal series, the edge columns, the slice minima, the ray identity, the horizon contours
    ├── ctrl_D<D>_<name>_h<h>.json    the controls
    ├── frw_h<h>.npz                  the planted homogeneous ghost
    ├── analysis.log                  `expansion.py analyze` on the above (= notes/wormhole_evolution/expansion_output.txt)
    └── mut/<name>.log                the mutation runs (reduced size)
```

## Rulings received (coordinator's brief, over hc)

1. Work as the issue states, with #39's and #211's guidance first. Before any run of record declare the observer (two-sided symmetric pulses; the throat is
   both the diagonal and the minimum-r slice; a planted check that they agree), the definitions of rho, p and w on that locus with a planted check on a
   homogeneous ghost (w = +1), the criteria for "de Sitter-like", and the alternatives. Run the expanding branch of family S at D = 4 (D = 5 if cheap) as long as
   the grid allows, at two resolutions, recording max e^{-f}, the e-folds of r_th and the first excised cell. Report H(tau), w(tau), the anti-trapped region
   and the cosmological horizon, #211's slope test, the mass at each end against time and the flux through it, and the positive-energy control.
   Each check has a `--mutate=` whose targets are computed in a development run before they are declared.
2. Project rules: a failed check is a result; never loosen a criterion or a tolerance after seeing data; never move families, resolutions, observers,
   definitions or windows after a development run without asking; ask before replacing a declared planted case or control; code each criterion exactly as
   worded here; a control that is silent on its named target is a result; the classification is *numerical evidence*; no sentence says a universe forms or that
   the expanding region is a universe beyond the declared criteria; no novelty claim; keep every log, never overwrite one, number reruns.
3. Threads and memory: at most 4 processes, `nice -n 10`; any single run not finished in 2 h is stopped and reported; memory is reported only.
4. Files: `expansion.py`, `expansion_output.txt`, `expansion.md` under `notes/wormhole_evolution/`, and this folder. Close with a comment, remove `running`, leave
   the issue open.

## What the development runs showed before anything was declared (reported, none of it fixed)

1. **On the mirror-symmetric diagonal w is fixed by the symmetry.** The data of family S are mirror symmetric, phi(x+, x-) = -phi(x-, x+), r and f symmetric.
   On the diagonal phi = 0 for all time, so phi_u = 0, and phi_+ = -phi_-. With T_ab = eps (d_a phi d_b phi - g_ab (d phi)^2 / 2) and g_{+-} = -e^{-f}: T_{+-} = 0,
   rho = T_uu = e^f (T_++ + T_--)/2 = eps e^f phi_+^2, the radial pressure p_par = T_ll = rho, and the angular pressure p_perp = T^theta_theta = eps e^f phi_+ phi_- = -rho.
   So p_bar = (p_par + n p_perp)/(n+1) = (1-n) rho/(n+1) and **w_bar = (1-n)/(1+n) = -1/3 at D = 4, -1/2 at D = 5, for every run and every time** (*proved* by hand;
   dev_04 and dev_07: -0.33333333 to 3e-16). The brief's "w within a stated distance of -1" is therefore decided by the symmetry for this observer, not by the dynamics,
   whenever rho is not zero. It is kept as worded (a class that needs it is declared below) and the components w_par = +1 and w_perp = -1 are reported beside w_bar. This is
   reported to the coordinator in the started post, not worked around.
2. **The grid does not stop the run.** Symmetric expanding members run to t = 283 (X = 200) with no excised cell, no NaN, max e^{-f} = 1.0000 (at the corner) and
   min e^{-f} falling to 1e-7 (the cells shrink in proper time, they do not stretch). h = 0.08, 0.04, 0.02 agree on r to 2.7e-5 and H to 1.2e-4 at (0.04, 0.02)
   with ratio 4.0 per halving (dev_03). So the run length is set by the cost declared below, not by the grid.
3. **What the diagonal does** (dev_01, 02, 04, 09; observed, not interpreted at that point): the proper time along the diagonal saturates; 1/H is linear in tau
   over the last e-fold of r (H = k/(tau_s - tau), k = 2.0001 at D = 4 for A = tuned, 0.01, 0.05, 0.2 and both h; 3.96 at D = 5 at r/a ~ 50); |rho|/H^2 -> 4.0000 at D = 4
   (6.75 at D = 5); the Misner-Sharp mass on the diagonal is m = r^{n+1} H^2/2 to 1e-4. The anti-trapped region contains the diagonal from t ~ 3 to the end, no trapped
   cell forms, the left contour r_+ = 0 stays at x+ ~ 3 to 6, and the right contour r_- = 0 leaves the grid (x+ > X) at x- ~ 5 to 6.
4. **The masses at the edges are Bondi-like at fixed x- and grow with x-**: M(x+, x-) converges as x+ grows for each x- (dev_05) and rises with x- to 1e7 (X = 100) because the edge
   x+ = X enters the anti-trapped region; the flux identity holds to 1.5e-7 relative (dev_04). Which numbers the ends' masses should be quoted at is declared below.
5. **E0 does not set the fate for the phi-Gaussian family**: S(+0.05) and S(-0.05) both have E0 = -0.0121 (pulse energy at the edge, relative to the static wormhole's)
   and opposite fates (dev_12 ctrl); the normal-field pulse of the same shape has E0 = +0.0118. #39's F1 note about [SH02]'s sign rule concerned the derivative-form pulse.

## Development runs (kept, none edited; `dev/`)

| id | what | outcome |
|---|---|---|
| dev_01 | S at D = 4, h = 0.02, X = 30, A = 0, 0.01, 0.05, 0.2 | A = 0 collapses at t = 10.4 (p*_h = 4.75e-5 > 0); the three others expand to t = 42 with no excised cell, max e^{-f} = 1.0000; mirror asymmetry <= 4e-12; the node-level minimum of r on the slice is the diagonal (l = 0.0000) on every slice in the grid |
| dev_02 | reach: A = 0.05, h = 0.04, X = 200 and h = 0.02, X = 100 | t = 283, no excised cell, no NaN, e^{-f} down to 3e-7; tau(t = 280) = 8.14, r/t -> 0.71 |
| dev_03 | h = 0.08, 0.04, 0.02 at X = 200 | r agrees to 2.7e-5, H to 1.2e-4, tau to 2.7e-3 (0.04 vs 0.02); ratios 4.0 per halving |
| dev_04 | stored run, h = 0.04, X = 100: rho, p, w, m, edge masses, horizons, slice minima | w_bar = -1/3 and p_perp/rho = -1 to 3e-16; |rho|/H^2 -> 4.0000; m/(r^3 H^2/2) -> 1.0000; |l_min| <= 1e-9 on all full-length slices; r_ll > 0 throughout; edge mass 1e7, flux residual 1.6 (1.5e-7 relative); the anti-trapped region reaches the grid edge from t ~ 10 |
| dev_05 | rows of M(x+, x-), the contour r_- = 0 in columns, the ray identity diagonal to edge | M converges in x+ at fixed x-; r_- = 0 at x- = 2.7, 3.9, 4.55, 5.0, 5.4, 5.7 for x+ = 3, 8, 20, 40, 70, 100; ray identity 4e-4 (x- = 3) to 3e-7 (x- = 80) relative |
| dev_06 | the open FRW + homogeneous ghost, D = 4 (a^2 = cosh 2 eta, phi = sqrt6 atan tanh eta) against dn.py's three equations and two constraints | residuals 1e-30 (*checked symbolically*); rho = p_perp = p_par = -3/cosh^3 2eta, so w = +1; H = sinh 2eta / cosh^{3/2} 2eta |
| dev_07 | `expansion.stream` against `dn.evolve` (store) on three small grids, one with excision | diagonal series bit-identical; edge mass 3e-9 absolute on 1e4; flux residual, constraints, cell classes identical |
| dev_08 | the planted ghost through `stream`, h = 0.04, 0.02, 0.01 | orders 1.95 to 2.00 (r, f, phi, H, tau, rho, p); |w_bar - 1| = 2.5e-8, 1.6e-9, 1.0e-10; the observer passes the bounce |
| dev_09 | late diagonal of D = 4 (tuned, 0.01, 0.05, 0.2; h = 0.04, 0.02; X = 100) and D = 5 (tuned, 0.05; h = 0.0141, 0.00707; X = 60) | k = 2.0001, |rho|/H^2 = 4.0000, m/(r^3H^2/2) = 1.0000 for all four D = 4 members at both h; tau_s = 17.89, 10.06, 8.43, 6.17; D = 5: k = 3.96, |rho|/H^2 = 6.75; H/W at r/a = 10, 25, 50: 1.23, 1.95, 2.75 (tuned, D = 4) |
| dev_10 | the reduced suite (`expansion.py dev`) | 12 of 13 checks passed; OB0 failed because its window ran past the static solution's own departure (t ~ 9); its window was cut to t <= t_c = 4.0 (#39's P1), then it passed |
| dev_11 | the 15 mutations on the reduced suite, first version | targets read; the control rectangle was then cut from X = 20 to 12 (D = 5 cost), so dev_13 repeats all of them |
| dev_12 | the runs of record at full size, D = 4 (trial, not of record) | 13 of 13 checks pass; MB1 6.5e-8, MB3 1.3e-4, RES 3e-5; the flux residual falls by 4.6 and 2.9 per halving of h; controls collapse |
| dev_13 | the 15 mutations on the frozen code | the targets declared below; the fired sets are identical to dev_11's. The lane script wrote to `dev/mut1313/` (a doubled substitution in its path); the folder and the script were renamed to `mut13` after the run, no log was changed |

## Declared

**Units and the family.** a = 1, 8 pi G = 1, t = (x+ + x-)/sqrt2, l = (x+ - x-)/sqrt2, h the null step. Family S as #40: ghost field 0, Gaussian in phi, centre 3, width 0.5,
amplitude A on the ray x- = 0 mirrored onto x+ = 0 with the parity of the static field (odd), on the static Ellis wormhole (`dn.ellis_rays(..., symmetric=True)`).
"tuned" is A = p*_h + 1e-6, with p*_h bisected by `checks.bisect_A` (bracket +-0.01, to 1e-10, X = 20 at D = 4, 15 at D = 5, as #39's G1); the others are A = 0.01, 0.05, 0.2.
The expanding branch is A > p*_h.

**Observer.** The diagonal x+ = x-, the worldline fixed by the reflection (a geodesic by the symmetry), proper time tau with d tau = sqrt2 e^{-f/2} dx on the diagonal,
r_th = r there, H = d ln r_th/d tau. The throat in the sense of the brief is the diagonal and the minimum of r on the slices t = const: planted check **OB0** (the static
wormhole: |r_diag - 1| <= 1e-3 for t <= 4.0, and the node-level minimum of r on every full-length slice within one node of the diagonal, h = 0.02, X = 6), **OB1** (every run: the fields
at the nodes next to the diagonal are mirror symmetric, |r(j+1, j-1) - r(j-1, j+1)|/r, |f - f'|, |phi + phi'| <= 1e-9 through the run) and **OB2** (every run: the node-level minimum of r
on every full-length slice s <= N lies within one node of the diagonal, and r_ll > 0 on the diagonal through the run). Full-length means t <= X/sqrt2; a longer slice is cut by the rectangle.

**rho, p, w.** In the unit frame u = e^{f/2}(d_+ + d_-)/sqrt2, e = e^{f/2}(d_+ - d_-)/sqrt2 and the angular directions, with T_ab = eps (d_a phi d_b phi - g_ab (d phi)^2/2) per field:
rho = T_uu = e^f (T_++ + T_-- + 2T_{+-})/2, p_par = T_ee = e^f (T_++ + T_-- - 2T_{+-})/2, p_perp = T^theta_theta = e^f sum eps phi_+ phi_-, p_bar = (p_par + n p_perp)/(n+1),
**w = w_bar = p_bar/rho** (the isotropic average; it equals p/rho for an isotropic fluid, so a homogeneous ghost has w = +1). w_par = p_par/rho and w_perp = p_perp/rho are reported.
Planted check **W1**: the exact open FRW with a homogeneous ghost (dev_06) is run through the same `stream` code from characteristic data on two rays; at h = 0.04, 0.02, 0.01 the observer is
the comoving diagonal chi = 3 across the bounce (eta from -1 to 1.5): (r, f, phi), H(tau), tau, rho, p_perp, p_par converge at observed orders in [1.75, 2.25], and |w_bar - 1| <= 1e-6 at h = 0.01.
**W2** (every run): on the symmetric diagonal |p_perp/rho + 1|, |p_par/rho - 1|, |T_{+-}/rho|, |w_bar - (1-n)/(1+n)| <= 1e-9.

**Growth control SL0** (the tuned members, both h): the slope of ln|H| against tau over the points after the global minimum of |H| with |H|/W in [1e-3, 1e-2] equals W within 1 % (#39's G1 form, one side of p*_h).

**Criteria, evaluated on the last e-fold of r on the diagonal (CL).** In this order: **DS (de Sitter-like)** if max H/min H <= 1.2 and max |rho|/min |rho| <= 1.2 and |w_bar + 1| <= 0.2 at every point; **STIFF**
(a stiff ghost-dominated state) if |w_bar - 1| <= 0.2 at every point; **FT** if H rises by at least 1.2 and monotonically, 1/H is linear in tau (maximum residual <= 1 % of its mean) with
negative slope, and the intercept tau_s satisfies tau_end < tau_s <= 1.2 tau_end (r diverges at a finite proper time; k = -1/slope is H = k/(tau_s - tau)); **GROW** (H rises by at least 1.2 monotonically, not FT);
**OTHER**. Planted check **PL**: five synthetic series through the same `classify` and `slope_test`: de Sitter (H = W, rho constant, w = -1) must give DS and the slope test met; r = (tau_s - tau)^-2 with rho = -4H^2 and w = -1/3 must
give FT; a flat stiff fluid (a ~ tau^{1/3}, w = +1) STIFF; r = exp(tau^2/2) GROW; a ~ tau^{1/2} OTHER; the last four with the slope test not met.

**#211's slope test (SL, a verdict, not a check).** H/W at the first diagonal point with r/a >= 10, 25, 50 (those the run reaches); the slope W is kept if |H/W - 1| <= 0.10 at all of them. Reported beside it, as
[SH02]'s fit form: the least-squares exponent of ln(r/a - 1) against tau over 1e-2 <= r/a - 1 and r/a <= r_max, r_max = 1.5, 2, 3, 5, 10, 25 (1.1 a^-1 = 0.931 W at D = 4).

**The anti-trapped region and the horizons (AT, reported).** First anti-trapped diagonal cell (r_+ > 1e-2 and r_- > 1e-2) and whether every later live diagonal cell is; number of trapped cells; the contours r_+ = 0 and
r_- = 0 (x+, r) at fixed x-; where the right contour leaves the grid.

**Two resolutions (RES).** D = 4: h = 0.02, 0.01, X = 200, members tuned, 0.01, 0.05, 0.2; D = 5: h = 0.01/sqrt2, 0.005/sqrt2, X = 100, members tuned, 0.05. They agree if the class is the same, H at fixed r/a = 10, 25, 50
differs by <= 1 %, k and tau_s by <= 1 %, and ln r_max by <= 1e-3.

**Masses (MB).** M = r^{n-1}(1 + 2 e^f r_+ r_-)/2 at the nodes, as `dn.mass_nodes`. The mass at an end is M on the edge x+ = X (right end) and on x- = X (left end), as a function of x- (resp. x+); also on the columns x+ = X/2, X/4 for
the Bondi-like convergence in x+. **MB1:** M(j) - M(0) = int -(r^n/n) e^f r_+ sum eps phi_-^2 dx- (the C2 identity of #39 along the edge, the same along the columns and along the top edge): largest residual / largest change <= 1e-3.
**MB2:** the two ends have the same history, M(i, N) = M(N, i): relative difference <= 1e-6. **MB3 (the ray identity from the throat to the edge):** along the row x- = const from the diagonal cell to the last cell,
m_edge - m_diag = int -(r^n/n) e^f r_- sum eps phi_+^2 dx+ (cell centred), residual <= 1e-3 of (|I_pos| + |I_neg|) at x- = 3, 4, 6, 8, 12, 20, 40, 80. The values of M at the ends are quoted as M(x+ = X, x-) with X stated; no mass at spatial infinity is claimed.

**Control (CT).** The same Gaussian in a *normal* scalar (eps = +1), mirrored (even), A = 0.05, and the S ghost pulse of the other sign, A = -0.05, X = 12: both collapse (first trapped cell, r_+ and r_- both < -1e-2) at h and h/2,
the event times differing by <= 4 sqrt2 h, and the normal pulse has E0 > 0 (E0 = M at the edge start minus the static wormhole's 1/(2 r^{n-1}) there).

**Driver check ST.** `stream` reproduces `dn.evolve` (store) on S, D = 4, h = 0.04, X = 20 and on the normal-pulse collapse with excision: diagonal series, edge mass, flux residual, C_++, cell classes to 1e-9.

**Runs of record.** D = 4: h = 0.02, 0.01, X = 200 (t = 283; N = 10^4, 2x10^4), members tuned, 0.01, 0.05, 0.2. D = 5: h = 0.00707, 0.00354, X = 100 (t = 141), members tuned, 0.05. The planted ghost at three h; the controls at D = 4 and 5 at both h.
`stream` keeps the diagonal series, the nodes at the columns X/4, X/2, X, the last three rows, the node-level minimum of r on every slice, per row the anti-trapped cell counts and the two horizon contours, the ray identity, and the
constraints (reported, not gated: max |C_++|, |C_--| absolute and relative to their terms). The grid is not the stop; the stop is the declared X (cost: about 3 min at N = 2x10^4). A run not finished in 2 h of wall time is stopped and reported.

**Mutations** (`python3 expansion.py mutate --mutate=NAME`, the suite at reduced size: D = 4, X = 40, h = 0.04, 0.02, members tuned and 0.05, controls at X = 12; targets computed in dev_13 on the frozen code; each run of record fires exactly its list):

| mutation | what it breaks | fires exactly |
|---|---|---|
| `mirror_parity` | the mirrored pulse gets the even parity: the data are not mirror symmetric | MB1, MB2, MB3, OB1, OB2, RES, W2 |
| `w_sign` | p_perp with the wrong sign | W1, W2 |
| `time_unit` | tau scaled by sqrt2 (H by 1/sqrt2) | SL0, ST, W1 |
| `class_loose` | the classification tolerances widened to 1e3, 1e3, 10 | PL |
| `control_ghost` | the control pulse put in the ghost field instead of a normal one | CT |
| `flux_sign` | dn.py: the flux term of the mass identity with the wrong sign | MB1, MB3 |
| `mass_exponent` | dn.py: M with r^n instead of r^(n-1) | MB1, MB3 |
| `no_corrector` | dn.py: predictor-only update | MB1, MB3, RES, W1 |
| `ellis_charge` | dn.py: the data's charge 1.1 times too large | BUILD, CT, MB1, MB3, OB0 |
| `theta_coef` | dn.py: n for n-1 in the sphere term | BUILD, CT, MB1, MB2, OB0, OB1, OB2, RES, W1 |
| `scalar_coef` | dn.py: n-1 for n in the scalar equation | BUILD, MB1, MB2, OB0, OB1, OB2, RES, W1 |
| `ghost_sign` | dn.py: the sign of the scalar source in f | BUILD, MB1, MB2, OB0, OB1, OB2, RES, W1 |
| `data_constraint_sign` | dn.py: the sign of the constraint solve in the data | BUILD, CT, MB1, MB2, OB0, OB1, OB2, RES |
| `finder_sign` | dn.py: the sign test of the trapped cell finder | BUILD, CT |
| `constraint_sign` | dn.py: the sign of the constraint monitor | none (silent by design) |

Silent by design: `constraint_sign` changes only the reported constraint monitor; the dn.py kernel mutations other than those listed change the data or the evolution and are caught through BUILD (the bracket of p*_h no longer straddles).
BUILD means a run of the reduced suite could not be completed (for the mutations that break the evolution this is the bisection for p*_h).

## Queue of record and results

Filled after the runs of record (`runs/`, `scripts/`), in a later commit of this folder.
