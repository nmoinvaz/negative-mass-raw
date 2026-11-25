# I161-rpi5: logs of notes/warp/planar_closure.py (closure for planar shifts that cross |u| = 1 or do not travel)

Machine rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process, one thread, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/161. Branch `wip/i161-planar-closure`, worktree
`~/Source/negative-mass-i161` (main 46ed4dc). Python `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0,
mpmath 1.3.0, numpy). Written 2026-11-24, before the first run of record. Stop condition: a single run not finished after
1 h of wall time is stopped and reported. Memory is reported, never a stop condition.

## Question

Planar shifts b(t, x) have D = det R3 = 0 and R = K g2 + 0 with K = -a_x, a = b_t - b b_x. #80 (`det_classify.md` section 2)
proved: closure holds iff g2 = -2 exp(2 H(p) J(q)) dp dq, and for traveling shifts u(xi) with |u| != 1 on the whole line
(Theorem T) closure fails unless flat. Left open: (Q1) which closure-passing g2 (K != 0 somewhere) have a
Painleve-Gullstrand chart -dt^2 + (dx + b dt)^2 with b -> constant as |x| -> infinity at every t; (Q2) what Theta' = 0
requires at a crossing of |u| = 1, and whether a superluminal planar bubble that crosses twice is excluded.

## What was explored before this README (not of record)

One scratch script in the scratchpad (not kept in the repository, no run of record), and hand derivations. They gave:

1. Hand: with C[b] = box ln|K| - 2K (box = the 2D d'Alembertian), closure iff C[b] = 0 on {K != 0}; for a static u this is
   exactly Theta'. For static u, any maximal interval I of {|u| != 1} is mapped by s' = 2/(1 - u^2) onto the whole line
   (s monotone, |s| -> infinity at both ends), while Phi = K (1 - u^2) tends to 0 at both ends (K bounded at a horizon,
   K -> 0 at infinity), which Phi = C e^{alpha s} cannot do unless C = 0. So K = 0 on every such interval (Theorem T').
2. Hand: for a time-dependent shift a PG chart is the Gaussian normal chart of a spacelike curve S0 (t = proper time from
   S0, x = arclength + c(t)); Jacobi: A_tt = K A, b_x = -A_t/A, L'' = integral of K dx over the slice.
3. Scratch numerics: H = h S(p), J = j S(q), S a smooth step on [0, 1], h = j = 3/2 (smootherstep, C^2), S0 = {p + q = -2};
   normal geodesics integrated by RK4 (dt = 0.002) in sigma = H J. They gave A >= 1 for all s and times to 10, A = 1 for
   |s| > 0.7 beyond what is transported, b_x = 0 outside |s| < 0.7, and L'(t) = -b_+(t) increasing to 4.5000 = 2 h j for
   t >= 6. So the construction of item 2 gives a localized b with unequal limits (b_- = 0, b_+ -> -2 Delta H Delta J).

Everything below was fixed after this exploration and is not changed after the first run of record, except by a dated
amendment written before the run it concerns. Thresholds below were chosen from error estimates, not tuned on data.

## Notation and imports

PG metric g = -dt^2 + (dx + b dt)^2, n = d_t - b d_x, a = b_t - b b_x, K = -a_x. Null form g = -2 e^{2 sigma} dp dq,
sigma(p, q) = H(p) J(q). Static u(xi): b = u(x), Theta = (1 - u^2) K'/K - 2 u u', Phi = K (1 - u^2), s' = 2/(1 - u^2).
Imported (trusted, as in #80): `phantom_source.ricci`; `two_scalars.closure`, `two_scalars.dform`. Not imported:
`det_classify` (it reads `--mutate` at import). Formulas of #80 (Theta, null criterion) are retyped. Output of this script
is stdout only; each run is logged in this folder, reruns are numbered.

## Checks (each is a `check(name, ok, detail)`; the script exits 1 if any fails)

**C1 `crit_null`.** (i) For undefined sigma(p, q): `ricci` of -2 e^{2 sigma} dp dq has R = K g with K = 2 sigma_pq e^{-2 sigma};
box f = -2 e^{-2 sigma} f_pq; and d_p d_q ln|R_pq| = -(e^{2 sigma}/2) (box ln|K| - 2 K), all exact. (ii) For the six planted
sigma of #80 (passes sin(p) e^{q/2}/3, p q + p^2 q, (p + q)^2/5; failures p^2 q/2 + p q^2/2, e^{p q}, p^3 q^2/6 + p q), the
4D null metric has R = a a - b b exactly, `two_scalars.closure` returns ok exactly for the three passes, and
C = box ln|K| - 2 K computed by the covariant formula in the null chart vanishes exactly for the three passes and for none
of the failures. Pass iff all six agree with the expectation.

**C2 `crit_pg`.** (i) For undefined b(t, x): `ricci` of the PG metric has R = K g with K = -(b_tx - b b_xx - b_x^2). (ii) For
undefined static u: C[u] = Theta' exactly, with box computed in PG coordinates from g^{-1} = -n n + d_x d_x. (iii) For undefined
static u, the obstruction of `two_scalars.closure` on the 4D PG metric is d omega_{t xi} = Theta'/2 (as #80). (iv) Planted
failures, Theorem T's case: the subluminal traveling bubbles u1 = (1/2)(1 - 1/(1 + xi^2)^2) (#80's planted failure),
u2 = 1/(2 (1 + xi^2)), u3 = 1/(3 (1 + xi^2)^2) have K != 0 and C[u] != 0 at xi in {1/3, 1, 3/2, 2, 5/2} (15 exact
points). (v) Planted pass, a formal local solution: u0 = 1/3, u1 = 1/2, u2 = 1/5, u3 = 2/7 at xi = 0, Taylor coefficients
c4..c8 solved in order so that C[u] = O(xi^5); verified exactly. The same jets with c6 + 1/7 give a coefficient of xi^2
in C[u] that is nonzero. Pass iff (i)-(v) all hold.

**C3 `horizon`.** (i) At a point with |u| = 1 and K != 0, Theta = -2 u u' exactly, and a closure interval through it has
alpha = -u u'(xi0); near a simple crossing u = 1 + u1 eta + ..., a solution of (1 - u^2) K' = (2 alpha + 2 u u') K has
K ~ |eta|^gamma with gamma = -(alpha + u1)/u1 (exact leading-order substitution). (ii) For u_s = 3/(1 + xi^2) (limits 0,
|u_s| = 1 at xi = +-sqrt 2, u_s > 1 between): u_s u_s' at the two horizons has opposite signs, so no single alpha serves
both. (iii) For u_s on each of its three components of {|u| != 1}, and for u2 of C2 on its one component: s' has one sign;
the exact residue or limit of s' at each end gives s -> +infinity at one end and -infinity at the other; Phi = K (1 - u^2)
-> 0 at both ends (exact limits); K != 0 at an exact interior point. So Phi = C e^{alpha s} with C != 0 is impossible on
each component. Pass iff (i)-(iii) hold. (The theorem itself is by hand.)

**C4 `jacobi`.** (i) For undefined A(t, s): `ricci` of -dt^2 + A^2 ds^2 has R = (A_tt/A) g. (ii) For undefined X(t, s) with
X_s = A, x = X, b = -X_t: the metric equals the PG form; with d_x = (1/X_s) d_s, n = d_t|_s (chain rule), b_x = -A_t/A,
n(b_x) - b_x^2 = -A_tt/A, a = n(b) = -X_tt, -a_x = A_tt/A. (iii) L = integral of A ds has L'' = integral of K dx over the slice,
and integral of K dx = a_- - a_+ if a -> a_+-. Pass iff (i)-(iii) hold.

**C5 `exterior`.** (i) For undefined H, J: R_pq = -2 H' J', K e^{2 sigma} = 2 H' J'; Christoffels of -2 e^{2 sigma} dp dq are
Gamma^p_pp = 2 sigma_p, Gamma^q_qq = 2 sigma_q and no others. (ii) Along a normal geodesic family p(tau, s), q(tau, s) with
2 e^{2 sigma} p_tau q_tau = 1 and orthogonality p_s q_tau + p_tau q_s = 0: A = e^{sigma} sqrt(-2 p_s q_s) = p_s/p_tau and
A_tau tau = K A, derived from the geodesic equations only (jets substituted). If this derivation is not completed it is
dropped and the note does not claim it. (iii) With H = h S, J = j S, S(x) = f(x)/(f(x) + f(1 - x)), f(x) = e^{-1/x} (x > 0), f = 0
(x <= 0): S = 0 for x <= 0, S = 1 for x >= 1, S' >= 0, integral of S' = 1, hence integral of K dA = 2 integral H' J' dp dq =
2 h j exactly, with dA = e^{2 sigma} dp dq. Pass iff (i), (iii) hold and (ii) holds or was dropped.

**C6 `limits_necessary`.** (i) For b = eps b1(t, x), C[b] = (-d_t^2 + d_x^2) ln|K1| + O(eps), K1 = -b1_tx, exactly (series in
eps with undefined b1). (ii) With p = t - x, q = t + x and K1 = F(p) G(q): the integral over x of K1 at fixed t equals
(F * G)(2t) (exact change of variables). (iii) For F = G = u(1 - u)(1 - 2u) on [0, 1] (sign-changing, compact support),
F * G is a polynomial on [0, 1] and on [1, 2] that is not identically zero (exact). The theorem (compact F, G with
F * G = 0 forces F = 0 or G = 0, by Paley-Wiener, by hand) is not tested. Pass iff (i)-(iii) hold.

**E1 `E_norm`, E2 `E_focus`, E3 `E_ext`, E4 `E_hol`, E5 `E_geo`** (numerical evidence, numpy, RK4 dt = 0.002, t in [0, 10],
s on 601 points in [-6, 6], h = j = 3/2, H = h S(p), J = j S(q) as in C5 (iii), S0 = {p + q = -2}, geodesic start
(p, q) = (-1 - s/sqrt2, -1 + s/sqrt2), velocity (1/sqrt2, 1/sqrt2); state p, q, p', q', A, A' with p'' = -2 sigma_p p'^2,
q'' = -2 sigma_q q'^2, A'' = K A, K = 2 H' J' e^{-2 H J}):
- E1: |2 e^{2 sigma} p' q' - 1| <= 1e-8 at every stored time (every 1 unit) and s.
- E2: A >= 1 - 1e-12 for every s and stored time; and max_s A(10, s) >= 2.
- E3: |A - 1| <= 1e-12 for s in {-6, -5, -4, -3, 3, 4, 5, 6} at every stored time (the geodesics with q_0 > 1 or p_0 > 1 never
  meet the support of K).
- E4: with L'(t) = integral of A_tau ds over the grid (trapezoid), |L'(10) - 2 h j| <= 1e-5; L' nondecreasing up to 1e-12;
  b(t, s) = -integral from -6 to s of A_tau ds' lies in [-2 h j - 1e-9, 1e-9] at every stored time.
- E5: A from the ODE equals A_geo = e^{sigma} sqrt(-2 p_s q_s) from central differences (spacing 1e-4) of neighboring
  geodesics at s in {-0.6, -0.2, 0.1, 0.4, 0.65} and tau in {2, 3, 5, 8}: relative difference <= 1e-5.

## Controls (`--mutate=NAME`; target in advance; each must exit non-zero with the target check failing)

| name | change | target |
|---|---|---|
| `crit-factor` | expects d_p d_q ln\|R_pq\| = -e^{2 sigma} C | C1 |
| `crit-deform` | adds p q^2/10 to sigma of the planted passes | C1 |
| `crit-static-g` | g^{xx} = 1 + u^2 in box | C2 |
| `crit-plant-jet` | the planted pass jets get c6 + 1/7 | C2 |
| `hor-orient` | s' = 2/(1 + u^2) | C3 |
| `hor-alpha` | alpha = +u u'(xi0) | C3 |
| `jacobi-sign` | K = -A_tt/A | C4 |
| `jacobi-theta` | b_x = +A_t/A | C4 |
| `ext-hol` | expects integral of K dA = h j | C5 |
| `ext-null` | Gamma^p_pp = sigma_p | C5 |
| `lin-order` | K1 = -b1_tt | C6 |
| `conv-zero` | G = 0 in the convolution | C6 |
| `E-norm` | initial velocity (1, 1) | E1 |
| `E-kneg` | A'' = -K A | E2 |
| `E-ext` | support of J' is [0, 2] | E3 |
| `E-hol` | expects L'(10) = h j | E4 |
| `E-geo` | finite-difference spacing 0.5 | E5 |

Extras (other checks failing under a control) are reported, not hidden. A control that crashes or hangs before its target
runs is reported as silent.

## Logs

`run_*` logs are stdout of the script; `ctl_*` logs one control each. Failed, stopped and silent runs are kept and numbered.

## Amendments

**A1 (2026-11-24, before any run of record).** Dev run `dev_pg_horizon.run1.log` (checks C2 and C3 together) was stopped by
hand after 13 min (CPU 10:47, no progress output, 670 MB resident): C3 called `sp.limit` on an expression with a symbolic
exponent and hung. That is a code defect, not a result; the leading-order coefficient (1 - u^2) gamma/eta - (2 alpha +
2 u u') is now written by hand, and residues come from `pole_residue`. The log is kept. Before the stop the same run
printed the C2 results: (i), (ii), (iii), (v) true, and (iv) false: u1 and u2 pass at all 5 points, u3 = 1/(3(1+xi^2)^2) has
K = 4(9 xi^2 - 1)/(9(1+xi^2)^6) = 0 at xi = 1/3, one of the five points. `dev_horizon.run1.log` is the C3 rerun (passes) and
`dev_crit_null.run1.log` is a failure of C1 caused by a helper that compared a matrix with 0 (code defect, fixed in run2).

**A2 (coordinator ruling A, 2026-11-24, before any run of record).** C2 (iv) stays exactly as written and stays FAILED
(u3 at xi = 1/3, where K = 0): the wording did not exclude zeros of K, where Phi = 0 and Theta is undefined. The run of
record exits 1 because of it. Bookkeeping only, no criterion changed: C2 is reported as three checks, `crit_pg` ((i), (ii),
(iii), (v)), `crit_pg_iv` ((iv) as written; no control, its target fails at baseline) and `crit_pg_ivb` (A3). The controls
`crit-static-g` and `crit-plant-jet` keep the target `crit_pg`.

**A3 (new check C2 (iv-b), `crit_pg_ivb`, written before its first run).** Same profiles u1, u2, u3 as (iv). The fixed list
ell = [1/5, 1/3, 1/2, 2/3, 1, 3/2, 2, 5/2, 3, 4] is scanned in order; a point is taken only if K(xi) != 0 is verified exactly
(the exact rational value of K is nonzero); the first 5 taken are the test points; fewer than 5 available means the check
fails. Pass iff C[u](xi) != 0 (exact) at all 15 taken points. Control `ivb-flat`: u1 is replaced by the constant 1/3, so
K = (u u')' = 0 at every point of ell, no point is taken, and the check fails (computed from K = 0, not run).

**A4 (new control, written before its first run).** C5 (ii), the derivation of A_tau tau = K A from the geodesic equations, was
not touched by `ext-hol` or `ext-null`. Control `ext-geo` changes the geodesic equation used there to p'' = -sigma_p p'^2
(coefficient 1 in place of 2, in the rule for p' and in the derived p_tau_tau_s). Target: `exterior`.

**A5 (diagnosis of the failure of E4 `E_hol`, written after the dev run `dev_E.run1.log` and the scratch study
`diag_E_hol.run1.log`; no criterion changed).** E_hol as worded fails: L'(10) = 4.5 + 4.79e-6 passes the first test
(tolerance 1e-5), and b_min = -4.5000048 fails b >= -2 h j - 1e-9. Cause: quadrature in s (the trapezoid sum over the 601
geodesics, spacing 0.02), not the time step and not a true violation. L'(10) - 4.5 against the spacing of the s grid
(dt = 0.002 unless stated): 0.02: +4.793e-6; 0.01: +8.047e-9; 0.005: -5.214e-12; 0.0025: -5.963e-12; 0.005 with dt = 0.001:
+4.334e-13. The excess falls faster than any power of the spacing, as for a C-infinity integrand of compact support, and
the remainder, 5e-12, is the RK4 time-step error (it changes with dt, not with the grid). Domain truncation and ends are
not the cause: the domain [-3, 3] gives the same values as [-6, 6]; A' = 0 exactly for |s| > 0.64 at t = 10 (and the
geodesics with |s| > 2 sqrt 2 never meet the support of K). The true value is L'(10) = 2 h j = 4.5, the total
curvature of C5 (iii) (also the boost rapidity between the far geodesics). E_hol stays FAILED as worded; the failed
dev log is kept.

**A6 (proposed check E_hol_b, `E_hol_b`; NOT to be run before the coordinator accepts its error control).** Same geodesics as
E1-E5 on s in [-3, 3] (the integrand is exactly 0 beyond 2 sqrt 2). L'(t) = integral of A' over s by composite
Gauss-Legendre, 120 panels of width 0.05, order 10 (1200 nodes), RK4 dt = 0.001, at the stored times t = 0, 1, .., 10.
Error estimate e_q = |L'(10) with 240 panels - L'(10) with 120 panels|, e_t = |L'(10) with dt = 0.0005 - L'(10) with
dt = 0.001|, both printed. Pass iff e_q <= 1e-11, e_t <= 1e-11, |L'(10) - 2 h j| <= 1e-5 (the README's own tolerance),
L' nondecreasing over the stored times to 1e-12, and b at the panel boundaries (b = minus the cumulative integral of A')
in [-2 h j - 1e-9, 1e-9] at every stored time (the README's own slack 1e-9). Control: `E-hol` (expects L'(10) = h j) now
has target `E_hol_b`; effect computed by hand: |L' - h j| = 2.25 >> 1e-5, so it fails.

**A7 (coordinator accepted E_hol_b, 2026-11-24; this rule replaces the panel layout of A6 before its first run).** Run time, not
data, is the reason: 120 uniform panels would cost about 2.5 min per full script run, and the controls repeat it 19 times.
Fixed rule of `E_hol_b`: composite Gauss-Legendre of order 10 in s on [-3, 3] with 48 panels: 9 of width 0.25 on
[-3, -0.75], 30 of width 0.05 on [-0.75, 0.75], 9 of width 0.25 on [0.75, 3] (480 nodes); geodesics by RK4 at dt = 0.001
to t = 10, stored at t = 0, 1, .., 10. The error estimate is max(e_q, e_t), printed, with e_q = |L'(10) with every panel
halved (96 panels) - L'(10) with 48 panels| and e_t = |L'(10) at dt = 0.0005 - L'(10) at dt = 0.001|. It is a spread over
two resolutions, not an enclosure; it says nothing about error that both resolutions share. Pass iff e_q <= 1e-11 and
e_t <= 1e-11, |L'(10) - 2 h j| <= 1e-5 (the README's own tolerance, unchanged), L' nondecreasing over the stored times to
1e-12, and b at the panel boundaries (b = minus the cumulative integral of A') in [-2 h j - 1e-9, 1e-9] at every stored time
(the README's own slack 1e-9). E4 `E_hol` stays as worded and FAILED (coordinator ruling), and the run of record exits 1
because of it and of C2 (iv). Control `E-hol` (expects L'(10) = h j) has target `E_hol_b`; effect computed by hand before
the first run: |L'(10) - h j| = 2.25 against the tolerance 1e-5, so it fails, and the run will confirm it.

**A8 (written after the run of record `run_final.run1`, before the control it adds is run).** Control `E-ext` (support of J' is
[0, 2], target `E_ext`) was **SILENT** in `run_final.run1.log`: only `crit_pg_iv` failed. Cause, computed afterwards: I had
predicted that the geodesics with s = 3, 4, 5, 6 enter the support of K, which is wrong. A normal geodesic of S0 reaches
p = 0 at q = sqrt2 s, so it meets supp K only if sqrt2 s < (end of the support of J'); with the end at 2 that needs s < 1.41,
and E3 tests |s| = 3 .. 6 only. The README's prediction was a guess and is recorded as such. Added control `E-ext5` (the support
of J' is [0, 5], J(q) = j S(q/5); target `E_ext`). Its effect, computed before declaring it, in a scratch copy of the script
(not of record): `E_ext` fails, max |A - 1| = 1.61e-2, A' != 0 for s in [-0.46, 3.28] at t = 10. `E-ext5` is run alone as a
supplementary run (`ctl_E-ext5.run1.log`); `run_final.run1` stays the run of record, and the script differs from its commit
only by this one mutation entry. The same run shows `E-norm` and `E-kneg` firing with extras: `E-norm` also fails `E_hol_b`
and `E_geo`, `E-kneg` also fails `E_hol_b` and `E_geo` (A4's prediction named extras for `E-kneg` only; those for `E-norm` were
not predicted).

**A9 (order of events for E-ext5).** The first run of `E-ext5`, `ctl_E-ext5.run1.log`, was made before the script change was
committed; the coordinator asked for the commit first. The change is now its own commit (0707d9c on `wip/i161-planar-closure`) and
the control was rerun from that commit as `run_ctl_E-ext5.run1.log` (all checks with the mutation, no control loop). Both logs
are kept. The coordinator accepted A8: `E-ext` is recorded as SILENT (the geodesics with s >= 1.41 miss K), `run_final.run1`
stays the run of record, no full rerun.

**A10 (correction of A8, and the result of the supplementary run).** A8 says that A4 predicted extras for `E-kneg`. That is wrong:
A4 is the amendment for `ext-geo`. No prediction of extras was written in this README for any control; the table above names one
target per control and says that extras are reported. I had expected extras for `E-kneg` privately (it changes A in the ODE
only, so `E_hol_b` and `E_geo` follow) and had not expected them for `E-norm`. Both fired on target with the same extras,
`E_hol_b` and `E_geo`. `run_ctl_E-ext5.run1.log`: `E-ext5` fires on target (`E_ext`: max |A - 1| = 1.61e-2, exit 1) and
also fails `E_hol_b` (L'(10) - 2 h j = -1.59e-4: with the support of J' to 5 the slice at t = 10 is not above it), besides the
two baseline failures. Summary of the run of record `run_final.run1` (script commit 20d1fa4, 91 s for the checks, about 33 min
with the controls, exit 1): 12 of 14 checks pass; `crit_pg_iv` and `E_hol` fail as worded (rulings A of 2026-11-24); 19 controls:
16 fire on target only, 2 fire with extras (`E-norm`, `E-kneg`), 1 is silent (`E-ext`, A8).

**A11 (correction of A10).** The run of record took 31 min 0 s from the start of the unit to its exit code file (12:15:33 to 12:46:33), not "about 33 min".

## Results (written after `run_final.run1`; the criteria above are unchanged)

Branch `wip/i161-planar-closure`: script and run of record at 20d1fa4, control `E-ext5` at 0707d9c, note and output at ef1947b.

| file | what |
|---|---|
| `run_final.run1.log`, `.rc`, `.commit`, `final_mut1/mut_*.log` | the run of record (stdout = `notes/warp/planar_closure_output.txt`), exit 1 (31 min 0 s), the logs of its 19 controls |
| `run_final.sh` | the launcher (systemd user unit `nm-i161-final1`, nice 10) |
| `run_ctl_E-ext5.run1.log` | supplementary run of the control `E-ext5` from commit 0707d9c (A8, A9); `ctl_E-ext5.run1.log` is the same run before the commit |
| `dev_*.log` | development runs, including the failed ones (A1, A5): `dev_crit_null.run1.log` (helper defect), `dev_pg_horizon.run1.log` (stopped after 13 min), `dev_crit_pg.run2.log` (C2 (iv) fails), `dev_E.run1.log` (E_hol fails), `dev_E_hol_b.run1.log`, `dev_ctl_ext-geo.run1.log` |
| `diag_E_hol.run1.log`, `scratch/` | the s-spacing study behind A5 and the scratch scripts (`explore1.py` is the exploration of "What was explored before this README") |

Outcome: 12 of 14 checks pass; `crit_pg_iv` (C2 (iv)) and `E_hol` (E4) fail as worded, by the coordinator's rulings. Controls: 16 fire on
target only, `E-norm` and `E-kneg` fire with extras (`E_hol_b`, `E_geo`), `E-ext` is silent (A8), `E-ext5` fires with `E_hol_b` as an
extra. `E_hol_b`: L'(10) - 2 h j = +2.12e-12, e_q = 2.4e-12, e_t = 3.6e-13.

Peak memory, measured afterwards by `/usr/bin/time -v` on the checks alone (`run_nocontrols.run1.log`, `.time`): 95204 kB resident, 92 s, exit 1, same output as `run_final.run1` apart from timings.
