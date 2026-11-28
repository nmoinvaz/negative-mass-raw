# I34-mac: mu_inf from the D = infinity inner Stokes problem (the test field on CLD's inner background)

Machine: the coordinator's Mac (Apple M5, 10 cores, macOS, shared and loaded), runner `negative-mass-mac-i34`, issue
https://github.com/nmoinvaz/negative-mass/issues/34. Code: worktree `~/Source/negative-mass-i34`, branch
`wip/i34-mu-inf-stokes`: `notes/wormhole_next/mu_inf_stokes.py` (solver, controls, results) and `mu_inf_stokes_bg.py`
(background refinement). choptuik-large-d (CLD) is imported read-only from the clone `~/Source/negative-mass-i34-cld` at
82e991a0 (`solver/inner_stokes/inner_np.py`, `hier.py`), run with CLD's Python 3.13 by path
(`~/Source/choptuik-large-d/.venv/bin/python`), `PYTHONDONTWRITEBYTECODE=1`; the script refuses a clone with local
changes. At most 2 processes of mine at `nice -n 10`. Every run is `runrec.sh NAME CMD...`: stdout `NAME.log`, stderr
`NAME.err`, exit code `NAME.rc`; reruns are numbered, nothing is overwritten.

Status: criteria declared below, before the runs of record (`run_*`). Files named `pilot_*` and `dev_*` are the pilot
and the development runs that produced the numbers quoted in "Planted cases" and "Mutations".

## Method

Inner variables (CLD README, Proposition 5): xi = r/(sqrt(n)(-t)), theta = omega tau, Dd = y, sigma, c, with
L = xi^2 d_xi + omega xi d_theta. The D = infinity discretely self-similar background solves

    L y = c sigma,   L sigma = c xi y_xi + c (y^2/2 - 1) y,   xi c_xi = c y^2/2,

y, sigma odd in theta (odd harmonics), c even. A test field psi ~ e^{mu tau} obeys the same two equations for
(Dd, sigma)_psi = (Psi, Sigma) of notes/wormhole_next.md 1.5, with c, y frozen, L -> xi^2 d_xi + xi (mu + omega d_theta),
and no delta c: the inner system linearized with delta c = 0 and the cubic coefficient 3/4 replaced by 1/4
(`inner_test_field.py`). (Psi, Sigma) = (2 psi_t / c, 2 psi_s): psi = const is invisible, so the heat equation's
mu = 0 is not a zero of this system (the boost, Psi = Y, is).

Mode condition: the solution regular at xi = 0 has no Stokes jump across the real xi axis (CLD's selection rule, applied
to the test field). Per harmonic seed e_kappa (unit leading profile of Dd_psi) the formal series at xi = 0 is built to
the optimal truncation at xi0 = r0 e^{3 i pi/8}, where every fast mode is exponentially large (lateral Borel sum from
above), and integrated together with the background on the ray to |xi| = r1 and the arc to the real axis (CLD's own
right-hand side for the background; the test field's is the same with the frozen c). For real mu and a real background
the sum from below is the conjugate with the harmonics reversed, so the jump is
J[nu, kappa] = Y+[nu, kappa] - conj(Y+[-nu, -kappa]). J is demixed as CLD's `residual_demixed` does (multiply by
e^{-Pi(theta)}, Pi = (1/omega) int (F^2 - <F^2>), shift to theta0 = theta - 2 omega ln xi, normalize by
e^{1/(2 r1^2)} r1^{-2<F^2> + 2 mu} / (2 pi |K'(i nu omega)|)). The factor r1^{2 mu} follows from the test field's
fast-mode amplitude equation xi a_xi + 2 omega a_theta = (2 F^2 - 2 mu) a (a hand derivation from c = 1 + F^2 xi^2,
E = 2 F^2 xi^2; the cE term enters one order higher). The demixing is a linear map, so it moves no zero. The condition
is det S(mu) = 0 (a real number for real mu, by J[-nu, -kappa] = -conj(J[nu, kappa]); the script prints the other part
as a check); real zeros are the sign changes of det S, refined by Brent.

Sector: odd harmonics of the test field, nu = +-1, ..., +-Mt, mu real. This is the sector of the boost (mu = 0) and of
the finite-D zero mu(D) of `ghost_mu_table.log`. The even-harmonic sector (the other half-period parity, the line
Im mu = omega at finite D) is used only for the planted heat equation, which has psi = t (nu = 0, mu = -1) there.

Background: CLD's M-harmonic zeros (A, w/w_inf, B3, C3, ...). The stored values have 10 to 12 digits. At M = 5 a
relative change of 1e-12 in B3 moves CLD's demixed r_1 by 70, and CLD's r_1 at the stored values is 4e4. So each
background is refined with CLD's hierarchical solver (`hier.Hier`, fixed A and w, Schur correction) to its
double-precision floor (`mu_inf_stokes_bg.py`, output `bg_M*_run*.json`, full-precision x). This is CLD's code with
the settings of its documented M = 5 and M = 7 runs, started from the stored values.

## Discretization and resolutions of record

| quantity | value |
|---|---|
| harmonics M (background and test field, Mt = M) | 3, 5, 7 |
| background | CLD's M-harmonic zero, refined: `bg_M3_run01.json`, `bg_M5_run01.json`, `bg_M7_run01.json` (M = 7 only if its refinement ends inside the stop condition) |
| r1 (radius of the jump; ray start r0 = r0_for(M) as CLD) | 0.18, 0.20, 0.22 |
| integrator | DOP853, rtol 1e-12 and 1e-13, atol 1e-15 |
| series | J = int(1.2/(2 r0^2)) + 40 terms, optimal truncation |
| mu grid | 7 points in each of [-1.25, -0.75], [-2.25, -1.75], [-0.12, 0.12], then Brent |

The runs of record are `result` at M = 3, 5, 7 on the 3 x 2 grid of (r1, rtol). A run longer than 2 h of wall time is
stopped and reported.

## Criteria (declared before the runs of record)

Controls, by `mu_inf_stokes.py check --M M --bg FILE` (exit 1 if one fails), and the symbolic check:

| tag | criterion | observed in the pilot |
|---|---|---|
| C0 | `inner_test_field.py` exits 0 (coefficient 1/4 passes, control 3/4 leaves a residual) | exit 0 |
| K1 | the background series of this code equals CLD's `Inner.series_at`, max relative difference < 1e-14 | 0 (M = 3) |
| K2 | planted heat equation (c = 1, E = 0), even class: zeros at mu = -1, -2, -3, error < 1e-6 | 9.5e-12 |
| K3 | boost: the test field has a zero within 1e-4 of mu = 0 | -3.4e-6 (M = 3), +2.6e-6 (M = 5) |
| K4 | CLD's Proposition 5 (full linearization, delta c dynamic, coefficient 3/4): zeros at lambda = 0 and 1 within 2e-3, and at lambda = 2 within 1.5e-2 (M = 3), 1e-3 (M = 5), 1e-4 (M = 7) | 3.8e-4, 1.3e-4, 6.8e-3 (M = 3); 3.8e-4, 1.4e-5, 3.3e-4 (M = 5) |

K3 also holds at every grid point of a result run (R0): a grid point whose boost zero is farther than 1e-4 from 0 is
dropped and listed (the background is not exact enough there).

Result:

- R1. mu_M is the mean over the valid grid points of the first real zero of the test field in [-1.25, -0.75]
  (and the second, in [-2.25, -1.75], reported alongside). The integration spread S_M is the half range over the grid.
  If S_M > 5e-3 the result at that M is "not resolved" and is not used.
- R2. The truncation error bar is E_M = |mu_M - mu_{M-2}| / (rho_c - 1), where rho_c is the contraction of the
  lambda = 2 error of K4 between the same two M (a planted case with a known answer). It is an estimate calibrated on
  a known case, not a bound and not an enclosure.
- R3. mu_inf is quoted as mu_M of the largest M with K1 to K4, R0 and R1 satisfied, with +-(E_M + S_M), named as a
  truncation estimate plus an integration spread. It is "consistent with -1" if |mu_M + 1| <= E_M + S_M, and
  "excludes -1" otherwise.

The form of R1 to R3 was written after the pilot showed zero1 = -0.9652 (M = 3) and -1.0015 to -1.0027 (M = 5), and
before any run of record. No threshold is changed after a run of record.

## Planted cases (pilot values)

- Heat equation psi_s = psi_tt, c = 1: `pilot_03_planted_flat_even_M1`: zeros -3.0000000000, -2.0000000000,
  -1.0000000000 (self-similar solutions t^k, t^2 + 2s, ...). Odd class, same code: no real zero in [-3.5, -0.3]
  (`pilot_04_planted_flat_odd_M1`: 0 zeros), as 1/Gamma(1 + mu + i nu omega) has none there.
- Boost (mu = 0 and its jump equal to CLD's): the boost combination of the test seeds, alpha = 2F, has jump 1.6438e-8
  against CLD's `Inner.jumps` 1.6437e-8 at M = 3 (ratio 1 +- 2e-5; session diagnostic, repeated in K3).
- Proposition 5 (lambda = 0, 1, 2): K4.

## Mutations (each computed in a development run before being declared)

| `--mutate=` | change | effect (M = 3 unless stated) |
|---|---|---|
| `mu_sign` | s = -mu + i nu omega in the test field | planted zeros move to +1, +2, +3 (`dev_mutscan_mu_sign_M1`): K2 fails; full mode finds no zero near 1, 2 |
| `coef34` | cE coefficient 1 -> 3 (cubic 1/4 -> 3/4) in the test field | boost zero 0 -> +0.3600 (`dev_mutscan_coef34_M3`; zeros at -2.4472, -1.0354, +0.3600): K3 fails |
| `dc_off` | full linearization with delta c = 0 and coefficient 3/4 | zeros at +0.3600 and +1.2122 only (`dev_mutscan_dc_off_M3`): K4 fails at 0, 1, 2 |
| `dropE` | drop the cE term | no zero in [-2.5, 0.7] (`dev_mutscan_dropE_M3`): K3 fails |
| `detune` | A -> A (1 + 1e-3) | no zero in [-2.5, 0.7] (`dev_mutscan_detune_M3`): K3 fails |
| `jump_sum` | J = Y+ + conj(Y+ reversed) | no zero for the test field; K2 sees one spurious double zero at -2.5: K2, K3, K4 fail |
| `bgdrop` | drop the CE term of the background series | K1 relative difference 6.5e-3: K1 fails; K3, K4 fail |

The check logs are `dev_mut_*_M3.log` (all exit 1); `dev_mutations.jsonl` has the records.

## Pilot and development records

`pilot_01` symbolic, `pilot_02` series, `pilot_03/04` planted, `dev_mut_*` and `dev_mutscan_*` mutations,
`dev_result_M5_b` M = 5 zeros on the (r1, rtol) grid (`dev_result_M5` failed on a relative `--bg` path and is kept),
`bg_M5_run01` and `bg_M3_run01` background refinements (54 s and 4 s). Mistakes of the session: a missing projection
of the test field's derivative onto its harmonic space (fixed before any record), a relative path in a `--bg` argument
of `runrec.sh`.
