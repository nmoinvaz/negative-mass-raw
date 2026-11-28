# I302-mac: criteria, development runs and runs of record for #302, the horizon basis (c1, c2, c2') with the decaying partner of #262's mode

Machine: the coordinator's Mac (Apple M5), runner `negative-mass-mac-i302`, worktree `~/Source/negative-mass-i302` on `wip/i302-horizon-basis`, at most 2 processes, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/302. Script: `notes/black_universe/horizon_basis.py` (imports `horizon_sector.py`, `full_slice.py`, `static_c1.py`, `linear.py` read-only).
Python: `~/Source/negative-mass/.venv/bin/python`. Written before the runs of record (`runs/`); development runs are in `dev/` (probes `p1`–`p6`, logs `logs/d1`–`d10`, mutation development runs `mut_d1`–`mut_d3`).

## Question

#259 and #258 left one task open: put the time reverse of #262's mode, Y = c2' U R(rho(Pi)), through the slice code, with c2' = d_U dr(S) = (n - dr')/2, and reproduce the (c1, c2, c2') of a random regular datum from the three exact
modes (static mass mode c1, growing mode c2, decaying mode c2'). The issue's acceptance: c2' of the slice equals the mode's to 1e-6; a random datum's (c1, c2, c2') is reproduced by the three modes to 1e-6; swapping V and U fails.
The coordinator added (hc, before the runs of record): decide whether the ln|s| found below is a property of the solution or of the slice gauge; if the solution's, list each sentence of the repository that must change.

## What the development found, which changes how the acceptance is met

The exact modes Y = c2 V R and Y = c2' U R cannot be put through S at all, in the sense the issue words it ("c2' read at S from the slice equals the mode's"). The slice constraint M (`full_slice.py`, `rhs_odd`) gives, for any
representation with C^2 fields, `Y_N'' (0) = -F_Pi(0) Y_N(0)` (Y_N = d_N Y on V + U = 0, F_Pi = dF/dPi): the terms with delta phi_N and delta F_N carry the factors g = O(s^2), s r_Pi = O(s^3). The exact mode has
Y_N = c2 R(rho(s^2)) = c2 (1 + O(s^4)), so Y_N'' (0) = 0 and the condition fails by F_Pi(0) c2 = 3.88 c2. Its d_N delta phi, in the gauge where it is solved for, is -(pi/sqrt2) c2 ln|s| + O(1) (S1, P1). #269's family in
a double-null gauge has delta phi = -(beta/(sqrt2 kappa)) V ln V (L2), the same coefficient from a different formalism. So the evolved smooth data of #248, #258, #259 never contained the exact mode through S; their Y is
c2 V R + c2' U R + c1 Y_static + (a smooth-u remainder fixed by the condition above).

## Decision on the ln|s| (the coordinator's question): a property of the solution

Declared: it is the solution's, by (b). The argument: (1) the condition Y_N''(0) = -F_Pi(0) Y_N(0) is on the gauge-invariant Y (Y = dr - (rho R/sqrt2) dphi is invariant under every linear diffeomorphism, #248 D3a) and holds for every
representation whose delta phi, delta phi_N, delta F, delta F_N are C^2 at S (S1; L1 tests it on evolved smooth data: ratio 1 to 1e-6 where the data are resolved); (2) a representation smooth in any gauge reaches a smooth double-null
representation through a smooth gauge vector (d_V xi^U = h_VV/(2 g_VU), d_U xi^V = h_UU/(2 g_VU) are integrals of smooth functions), and a perturbation of a smooth tensor by L_xi g stays smooth only if xi is; (3) the
double-null representation of the mode is unique up to xi^V(V), xi^U(U), and these shift delta phi by -Phi'G (U xi^V(V) + V xi^U(U)): the V ln V term of delta phi has the coefficient -(beta/(sqrt2 kappa)) independent of U
(L2 at U = -0.5, -1), which U xi^V(V) cannot cancel (its coefficient is proportional to U, and it puts ln V into delta F). The EF-derived fields are checked against the exact mode's Y (P3, P4); the smoothness condition is
checked against the exact mode's closed form (L1). What is not shown: that no non-double-null gauge with a non-smooth gauge vector gives smooth fields; (2) says such a gauge would need a non-smooth xi that maps back to a smooth
double-null representation, which (3) excludes. The consequence for the repository is a list of sentences (in the note, not edited) and the finding that #258's task 2 and #259's task 2 cannot be done as worded.

## Method

1. **S1** (sympy): series of rho(Pi) at S from d rho/d Pi = A/(2 kappa Pi): A'(0) = 2 kappa, A''(0) = -2, F_Pi(0) = G0/kappa, a = lim g/s^2 = G0/sqrt2, the exact identity g' + eps r s phi_Pi = 2 sqrt2 s G rho^2/R; so
   M reads g z' = -(Y_N' + s F_Pi Y_N) + O(s^3) for z = d_N dphi, and the exact mode (Y_N = c2 R) has z = -(pi/sqrt2) c2 ln|s| + O(1).
2. **S2** (sympy, and 50 digits): Y = V R and Y = U R solve the Kruskal master equation (#232's `M_at` form, 2 kappa^2 Pi u_VU + Vhat u/2 = 0, u = Y/rho) through the same ODE for f = R/rho.
3. **S3**: the slice code under time reversal, (n, dphi_N) -> -(n, dphi_N): c2(TD) = -c2'(D), c2'(TD) = -c2(D), c1(TD) = c1(D), on datum G of #258 and three random compact data.
4. **P1**: #258's E9 data of the exact growing mode on [0.3, 1.6] (M = 0): Theta_gen = 0 (the mode carries no mass, which is why M = 0 fixes E9's initial value); the M equation for Y_N = c2 R integrated inward from
   s = 0.3 has d z/d ln s -> -(pi/sqrt2) c2.
5. **L1**: the condition of S1 on evolved smooth classes (4th-order stencils along the slice, from the evolved arrays of the Kruskal solver), and on the exact mode's closed form.
6. **L2**: #269's ingoing-null family, linearized (delta r = (beta/2) R V, delta F_EF = -beta(1 + kappa rho) V, delta phi = 0), transformed to a double-null gauge by xi^u with d_v xi^u = H_vv/A, xi^v = 0, then to the Kruskal chart
   (V = e^{kappa v}, U = -e^{-kappa u}): delta r = R V/2 - xi^u A rho/(2R), delta phi = -xi^u A/(sqrt2 R^2), delta F = A' xi^u/2 - d_u xi^u (beta = 1; xi^u and d_U xi^u by quadrature along a line of constant U, zero on a base ray).
   d_V delta phi at fixed U against ln V at V down to 1e-6, two U and two base rays.
7. **P2, P3, P4**: the three exact modes as ray data of the Kruskal solver (`hs.march_K`): the static mode with #259's closed-form data (rectangle of #248), the growing mode with the L2 data on V in [0.05, 3.05], the decaying mode as its time
   reverse (V, U) -> (-U, -V) on U in [-3, -0.05] (the data rays are the images of the growing mode's gauge-fixed ray and of a constant-U ray). c1, c2, c2' by the horizon fits and by the slice functionals (the 4th-order d_V = (T + N)/2 and
   d_U = (N - T)/2 of `hs.slice_V_derivative`, T = d_V - d_U along the slice nodes, N = d_V + d_U along the diagonal, at the slices crossing the horizon at V0 = 0.5, 1 on U = 0 and U0 = -0.5, -1 on V = 0).
8. **H1, H2, H3**: #248's classes L, G, A0, A1R, A1L, three new classes (Lm: pulse on the ray V = V0 centred at U = -1; Rb: pulse on the ray U = U0 centred at V = -0.05, width 0.03; Gb: both) and 8 random data (corner constants and pulses,
   amplitudes <= 1e-3), on the rectangle V in [-0.1, 3], U in [-2, 0.06]: the law Y_h(U) = c1 + c2' U on V = 0 (H1), the slice functional d_U at S, U0 = -0.5, -1 against the fit (H2), and the reproduction of both horizons'
   dr_h by the three modes' horizon values c1 + c2 V (U = 0) and c1 + c2' U (V = 0) with (c1, c2, c2') read at S (H3).

Error bars are comparisons of two computations, not uncertainties: Richardson means (4 v(h/2) - v(h))/3 of the two finest steps; "relative" is divided by the stated scale.

## Planted cases (run before the real data; known answers)

| case | known answer | where |
|---|---|---|
| exact static mass mode, dL = 2e-3, #259's closed-form ray data | (c1, c2, c2') = (1e-3, 0, 0) | P2 |
| exact growing mode, beta = 2e-3, double-null ray data from #269's family | Y = 1e-3 V R; c2 = 1e-3 | P3 |
| its time reverse | Y = c2' U R with c2' = -1e-3 | P4 |
| #258's M = 0 data of the growing mode | Theta_gen = 0, M = 0; with the E9 initial value left at 0 (`alpha_off`) Theta_gen != 0 | P1 |
| time reversal of the slice code | c2(TD) = -c2'(D) | S3 |

## Criteria (declared before the runs of record)

Issue acceptance is marked I1 (c2' of the slice equals the mode's to 1e-6), I2 (a random regular datum's (c1, c2, c2') is reproduced by the three modes to 1e-6), I3 (swapping V and U fails); C is the coordinator's question.
All bars of this runner's own checks were set from the development runs `d2` to `d10`, named in "Changes after development" below where they moved.

| id | check | bar | issue |
|---|---|---|---|
| S1 | sympy: A'(0), A''(0), F_Pi(0) = G0/kappa, a = G0/sqrt2, zeta = -F_Pi/a = -pi/sqrt2, the identity g' + eps r s phi_Pi = 2 sqrt2 s G rho^2/R | exact (residual 0) | C |
| S2 | Y = V R and Y = U R solve the master equation (the f = R/rho ODE) | symbolic 0, or 6 points at 50 digits below 1e-40 | I1 |
| S3 | time reversal of the slice code on G and 3 random compact data | 1e-10 relative to max(\|c2\|, \|c2'\|) | I1, I3 |
| P1 | E9 data: \|Theta_gen\| / largest term; M of the data over its scale before the fix; slope of z against ln s over -(pi/sqrt2) c2 | 1e-8; 1e-9; 1 to 1e-5 at s = 1e-4 and 1e-3 at s = 1e-3 | C |
| L1 | Y_N''(0) / (-F_Pi(0) Y_N(0)) on evolved smooth classes A0, A1R, A1L, L, G, Lm, Rb, Gb with \|Y_N(0)\| >= 1e-4 (Richardson of h = 0.00125, 0.000625); the exact mode's R''(0) | 1 to 1e-3; \|R''(0)\| <= 1e-6 | C |
| L2 | d_V delta phi of the exact double-null fields against ln V, slope over -(pi/sqrt2) c2 (c2 = 1/2), U = -0.5, -1, base rays 0.05, 1 | 1 to 1e-3 at V = 1e-6, to 1e-2 at V = 1e-5 | C |
| P2 | static mode through the solver, Richardson of h = 0.0025, 0.00125: c1 at S and on both horizons; c2, c2' by the slice functionals and both fits | c1 to 1e-6 relative; \|c2\|, \|c2'\| <= 1e-6 c1 | I2 |
| P3 | growing mode: Y error / max at h = 0.00125 and the last Cauchy ratio; c2 by the fit and the functional at V0 = 0.5, 1; c1 of the fit | <= 1e-3, 4.0 +- 0.3; 1e-6 relative; <= 1e-6 c2 | I2 |
| P4 | decaying mode: Y error / max and ratio; c2' by the fit on V = 0 and the functional d_U at U0 = -0.5, -1; c1 of the fit | <= 1e-3, 4.0 +- 0.3; 1e-6 relative; <= 1e-6 \|c2'\| | I1, I3 |
| H1 | horizon law on V = 0: least-squares residual of dr(0, U) at h = 0.00125, and its fall per halving (h = 0.005, 0.0025, 0.00125), classes L, G, A0, A1R, A1L, Lm, Rb, Gb | residual <= 2e-5 of max(max\|dr\|, 1e-3); ratio 4 +- 0.5 where max\|dr\| >= 1e-5 | I1 |
| H2 | c2' by the slice functional at S, U0 = -0.5, -1 against the fit on V = 0 (Richardson of h = 0.00125, 0.000625), 8 classes and 8 random data | 1e-6 of max(\|c2'\|, 1e-5); every random \|c2'\| >= 1e-6 | I1 |
| H3 | dr(V, 0) - (c1 + c2 V) and dr(0, U) - (c1 + c2' U), (c1, c2, c2') read at S by the slice, every node of both horizons, same data (Richardson of h = 0.00125, 0.000625) | 1e-6 of max(max\|dr_h\|, 1e-3) | I2 |

The unit 1e-3 is the data amplitude (every datum is specified at amplitude <= 1e-3); the floors 1e-3 and 1e-5 keep a class whose horizon values are at the truncation seed (as #248's class R, N3) from being judged relative to its seed.

## Mutations (declared; each effect computed in development before this README: `dev/mut_d1`, `mut_d2`, `mut_d3`)

| name | what it breaks | fires |
|---|---|---|
| s_zeta | F_Pi(0) doubled in S1 | S1 |
| s_kappa | kappa -> 1.01 kappa in the master equation | S2 |
| s_noflip | time reversed datum built without flipping (n, dphi_N) | S3 |
| s_swapfn | `fs.MUT = fn_sign`: the slice functionals' c2 and c2' swapped in #258's code | S3 |
| fn_swap | d_U reads d_V (V and U swapped in the functional) | P2, P4, H2, H3 |
| fn_aT | d_U from the tangential half only | P2, P4, H2, H3 |
| law_c1 | the law on V = 0 without c1 | H3 |
| law_x | the fit on V = 0 against -U (V and U swapped through the time reversal without the sign of c2') | P4, H2 |
| law_off | the line V = 0.025 (not a horizon) read instead of V = 0 | P2, P4, H1, H2, H3 |
| gauge_dF | the d_u xi^u term of delta F dropped from the exact data | P3, P4 |
| gauge_dphi | delta phi of the exact data set to its EF value 0 | L2, P3, P4 |
| alpha_off | E9's initial value of delta phi left at 0 (`fs.MUT = mode_M`) | P1 |
| sc_off | F_Pi(0) = 0 in the smoothness condition | L1 |
| zeta_F | F_Pi doubled in the z equation of P1 | P1 |

Blind spots, kept: `law_c1` does not fire P4 or H2 (c2' does not depend on c1); `fn_swap` does not fire P3 (the growing mode is read by d_V); no mutation fires S2 other than the equation's own `s_kappa`; L1 and L2 are not
fired by the reading mutations (they do not use the functionals).

## Changes after development runs (named so the bars of record are not read as pre-registered against data)

- Classes: first draft had Rm (pulse on the ray U = U0 centred at V = 0) and Gm; their c2' was 4e-6 because the data in the past of V = 0 is a strip 0.05 wide. Replaced by Lm, Rb, Gb on the wider rectangle V0 = -0.1 (Pi = -0.2 at the corner,
  #248's interior reaches -0.37); the random R pulses moved to the strip (centre in [-0.08, 0], width 0.02 to 0.05); the minimum |c2'| of the random data was 9.2e-6 (d3) and is declared at 1e-6.
- Scales: H1, H2, H3 first compared residuals to max|dr_h| of each datum, which is at the truncation seed (1e-10) for classes with no horizon amplitude (d3: H1 residual 1.2, H3 4.7e-6); declared relative to max(., 1e-3) (H1, H3) and max(., 1e-5) (H2).
- Richardson pair: H2, H3 and L1 use h = 0.00125, 0.000625 (d5: the narrow pulse Rb has 1e-6 relative error at 0.0025, 0.00125 and L1's Rb ratio was 1.0046).
- L1 scoring needs |Y_N(0)| >= 1e-4: the class Rm had Y_N(0) at the truncation seed and a ratio of 0.83 (d4).
- L2: V range extended from 1e-4 to 1e-6; the slope's correction falls like V ln V (d4: 1.0024 at 1e-4, 1.00004 at 1e-6). Bar at 1e-6.
- F_Pi(0) is read at s = 1e-6 (at s = 1e-3 it carries 3.5e-6 of relative error, d6; F_Pi(0) = (pi/2) G0 to 1e-14 with G0 = 2.472545959360).
- Mutations: `law_x` first fitted against the shifted node index, which changes only c1 (fired P4 only); replaced by x -> -U. `law_off` added because no mutation could fire H1 (d1, d2).
- H2 used the seed 3020 for its random data and H3 3021; both use 3021 from `d10`.

## Layout

```
I302-mac/
  README.md          this file
  run_mut.sh         run_mut.sh ABSOLUTE_OUT PREFIX NAME...   (derive for s_*, check otherwise; one process, nice 10)
  dev/               probes p1 (collocation: regular solutions of the inverse problem are not unique), p2, p3, p4 (z log), p5 (planted modes), p6 (F_Pi); logs/; mut_d1..mut_d3
  runs/              the runs of record: derive.log, check.log, table.log, mut_*.log (added after this README)
  cache/             readouts of the evolved rectangles (reused by the mutation runs; no mutation changes an evolution)
```
