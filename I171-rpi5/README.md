# I171-rpi5: logs of notes/warp/planar_residual.py (residual stage of #161's Theorem E with explicit scalars)

Machine rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process, one thread, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/171. Branch `wip/i171-planar-residual`, worktree
`~/Source/negative-mass-i171` (main cfe865d). Python `~/Source/negative-mass-venv314/bin/python` (3.14.10, sympy
1.14.0). Written 2026-11-25, before the first run of record. Stop condition: a single run not finished after 1 h of wall
time is stopped and reported. Memory is reported, never a stop condition.

## Question

`planar_closure.md` §3 says that for g = −2 exp(2H(p)J(q)) dp dq + dy² + dz², R = a a − b b with a = ½(c dH − (4/c) dJ),
b = ½(c dH + (4/c) dJ), any real c ≠ 0, so that φ₁ ∝ cH − (4/c)J (normal) and φ₂ ∝ cH + (4/c)J (phantom), λ = 0, "by hand;
the residual stage with these fields is not computed here". Find α₁, α₂ and the potential in φ₁ = α₁(cH − (4/c)J),
φ₂ = α₂(cH + (4/c)J) such that G_ab = 8π(T₁ − T₂)_ab exactly, with H(p), J(q) undefined functions and c symbolic, and say
for which c it holds.

## What was explored before this README (not of record)

Two scratch scripts, kept here with their logs: `explore_residual.py` (`explore.run1.log`) and `explore_planted.py`
(`explore_planted.run1.log`). They gave, with a Christoffel/Ricci routine written for them:

1. For the Theorem E metric, G = diag(0, 0, −K, −K) in (p, q, y, z) with K = 2H′J′e^{−2HJ}, R_pq = −2H′J′.
2. With unknown A1 = α₁², A2 = α₂² and a potential value V, the residual is pp: 8πc²H′²(A2 − A1), qq: 128π(A2 −
   A1)J′²/c², pq: −8πV e^{2HJ}, yy = zz: 2e^{−2HJ}(4π(4A1 + 4A2)H′J′ + 4πV e^{2HJ} − H′J′). `solve` returns A1 = A2 =
   1/(32π), V = 0, with no c.
3. #78's P1 and P2 in the sheared coordinates of `same_sign_scalars.md` have an exactly zero residual with the same
   routine (2.5 s and 5 s).

So I expect α₁ = α₂ = 1/(2√(8π)) = 1/(4√(2π)) (a sign of α is irrelevant: only ∂φ∂φ and (∂φ)² enter), V = 0, every c ≠ 0.
Everything below is fixed after this exploration and is not changed after the first run of record, except by a dated
amendment written before the run it concerns.

## Conventions

Signature (−,+,+,+). R_bc = ∂_aΓ^a_bc − ∂_cΓ^a_ab + Γ^a_adΓ^d_bc − Γ^a_cdΓ^d_ab, G_ab = R_ab − ½R g_ab. A normal scalar has
T_ab = ∂_aφ∂_bφ − ½g_ab(∂φ)², positive energy density (Minkowski, φ = ωt: T_tt = +ω²/2). A phantom enters with the
opposite sign (T_tt = −ω²/2). With a potential V, as in `two_scalars.md` (Setup),

    T_ab = ∂_aφ₁∂_bφ₁ − ∂_aφ₂∂_bφ₂ − g_ab(½(∇φ₁)² − ½(∇φ₂)² + V),

which is the issue's T₁ − T₂ with V = V₁ − V₂ (V is one potential V(φ₁, φ₂) there; only its value along the solution
enters). G_ab = 8πT_ab is equivalent to R_ab = λg_ab + a_aa_b − b_ab_b with λ = 8πV, a = √(8π)dφ₁, b = √(8π)dφ₂ (the
trace reversal in four dimensions).

## Independence

`planar_residual.py` imports nothing from the repository. Its Christoffel/Ricci/Einstein routine and its stress tensor
are written for it and share only sympy with `phantom_source.py`, `two_scalars.py` and `planar_closure.py`, from which
#161's K and the equivalence were derived. P1 and P2 are retyped from `same_sign_scalars.md`. The zero test is
`sympy.simplify(e) == 0`; a component that does not simplify to 0 is reported with its value and the check fails, it is
not retested with a weaker test.

## Criteria (each can fail)

Notation: `residual(g, X, fields, signs, V)` returns G_ab − 8π Σ s_i(∂_aφ_i∂_bφ_i − ½g_ab(∂φ_i)²) + 8π g_abV, all 16
components, computed by one function for every case below.

- **`conv_energy`.** In Minkowski (−dt² + dx² + dy² + dz²), φ = ωt with ω a positive symbol, the function used for T gives
  T_tt = +ω²/2 and T_xx = +ω²/2 for a normal scalar, and T_tt = −ω²/2 and T_xx = −ω²/2 for a phantom, exactly.
- **`planted_p1`** (planted, #78). P1: AdS₂ × R², (−dτ² + dz²)/z² + dR² + R²dΘ², in coordinates (T, Z, R, Θ_n) sheared as
  τ = T + Z/3, z = Z, Θ = Θ_n + T/7 + Z/5; two normal scalars φ_I = X_I/√(8π), X = R(cos Θ, sin Θ); V = −1/(8π). All 16
  components of the residual are exactly 0.
- **`planted_p2`** (planted, #78). P2: dS₂ × R², (−dτ² + dz²)/τ² + dR² + R²dΘ², the same shear; two phantoms with the same
  fields; V = +1/(8π). All 16 components are exactly 0.
- **`planted_flat`** (planted, one normal and one phantom). Minkowski in (t, x, y, z), φ₁ = φ₂ = f = t²x + sin y · e^z,
  V = 0. All 16 components of the residual are exactly 0, and T₁ (the normal scalar's own stress tensor) has a nonzero
  component, so the zero is not vacuous.
- **`E_solve`.** For g = −2e^{2HJ} dp dq + dy² + dz² with H(p), J(q) undefined and c a real nonzero symbol, take
  φ₁ = α₁(cH − (4/c)J) normal and φ₂ = α₂(cH + (4/c)J) phantom with unknowns A1 = α₁², A2 = α₂² and V (the value of the
  potential at the point). The nonzero components of the residual are linear in (A1, A2, V). Pass iff, after H′ → h,
  J′ → j, e^{2HJ} → E with h, j, E positive symbols, (i) the coefficient matrix has rank 3, and the gcd of its 3 × 3
  minors is printed, so that the rank is 3 wherever h j E c ≠ 0 (**superseded by A1**); (ii) the unique solution is A1 =
  A2 = 1/(32π), V = 0; (iii) the solution does not contain c.
- **`E_residual`.** With α₁ = α₂ = 1/(4√(2π)), V = 0, H(p), J(q) undefined and c a real nonzero symbol, all 16 components of
  G_ab − 8π(T₁ − T₂)_ab are exactly 0. Not vacuous: G_yy = G_zz = −2H′J′e^{−2HJ} are nonzero, and T₁ has a nonzero
  component. Because c is a free symbol and the residual is a rational function of c, this holds for every c ≠ 0.
- **`E_rform`.** With a = √(8π)dφ₁, b = √(8π)dφ₂, λ = 8πV = 0 (the form of `two_scalars.md`, Setup), all 16 components of
  R_ab − λg_ab − (a_aa_b − b_ab_b) are exactly 0, and a = ½(c dH − (4/c) dJ), b = ½(c dH + (4/c) dJ) as 1-forms (the
  identification of `planar_closure.md` §3).
- **`E_explicit`.** The same `residual` function with explicit functions: (H, J, c) = (p³ − p, q² + q, 3/2) and (sin p,
  q³ − q, −2/5), α₁ = α₂ = 1/(4√(2π)), V = 0. All 16 components are exactly 0 for both, and H′J′ takes both signs on the
  second.

Exit status 1 if a check fails or a control does not fire.

## Controls

One mutation each, `--mutate=NAME`, all checks are run with it, and the checks it must fail are declared in the section
"Declared targets" after a development run (step 3), before the run of record. Outcomes other than the declared targets
are reported as extras.

| control | change |
|---|---|
| `scale11-normal` | φ₁ multiplied by 11/10 in `E_residual`, `E_rform`, `E_explicit` |
| `scale11-phantom` | φ₂ multiplied by 11/10 in `E_residual`, `E_rform`, `E_explicit` |
| `flip-phantom` | the phantom's kinetic sign flipped in T (T₁ + T₂), and in the form of `E_rform` (a a + b b) |
| `swap-roles` | normal and phantom exchanged: φ₁ = α(cH − (4/c)J) phantom, φ₂ = α(cH + (4/c)J) normal |
| `wrong-partner` | φ₂ = α₂(cH + (2/c)J) |
| `potential` | V = 1/(80π) in `E_residual` |
| `ricci-sign` | the Ricci tensor with the opposite sign in the Einstein routine |
| `conv-flip` | the sign of T flipped in the stress function |
| `p1-sign` | one kinetic sign flipped in P1 |
| `p2-scale11` | one of P2's fields multiplied by 11/10 |
| `flat-flip` | the phantom's sign flipped in `planted_flat` |

## Run plan

1. This README (step 1). 2. The script with the checks, development runs `dev_*.runN.log` (step 2, posted). 3. The controls
in a development run, then "Declared targets" below (step 3). 4. The run of record, stdout of the default mode with the
controls, to `notes/warp/planar_residual_output.txt` and `run_final.run1.log` here (step 4). Logs are numbered, never
overwritten.

## Amendments

**A1 (2026-11-25, before any run of record).** Criterion (i) of `E_solve` is replaced by: (i) the 3 × 3 minors of the
coefficient matrix, with the row denominators cleared and π replaced by a positive symbol P, together with t h j E c P − 1,
generate the unit ideal of ℚ[t, h, j, E, c, P] (Gröbner basis [1]), so that the matrix has rank 3 at every point with
h j E c ≠ 0; the gcd of the minors is printed. Reason: a gcd that is a monomial does not exclude common zeros of the
minors elsewhere, so "rank 3 wherever h j E c ≠ 0" needs the ideal statement. (ii) is read as: `linsolve` returns the
single point (1/(32π), 1/(32π), 0), and that point makes every equation vanish identically; (iii) as: the point does not
contain c.

**A2 (2026-11-25, after `run_final.run1.log`, before `run_final.run2.log`).** Run 1 of the script at 2dfb6dd passed: exit 0,
8 of 8 checks, 11 of 11 controls fire on their declared targets, no extras, none silent (164 s). The note needs the
components of the residual equations and of G and T_1 − T_2 quoted from an output file, not from the exploration log, so
the script now also prints, as information that is not a check and is not tested: the five numerators of `E_solve`'s
equations, and in `E_residual` the nonzero components of G and of 8π(T_1 − T_2) and the count of nonzero components of
d/dc of 8π(T_1 − T_2). No criterion, mutation or declared target changes. Run 2 is the run of record whose stdout is
`notes/warp/planar_residual_output.txt`; run 1 is kept.

## Declared targets

Written 2026-11-25 after the development run of step 3 (`dev_controls.run1.log`, 11 controls, 8 checks, 164 s), and
before the run of record. The predictions from reading the code (`dev_controls_predictions.txt`, written before that run)
agree with the outcome for all 11 controls, including the checks I expected to stay silent. Each control must fail
exactly the checks listed; a control that does not fail one of them is silent, and any other failing check is an extra.
Controls act on the checks they list only because of where the mutation is read: `scale11-*` only in `fields_E` of the
three checks that fix the amplitude (`E_solve` has unknown amplitudes), `potential` only in `E_residual`, `ricci-sign`
and `conv-flip` in the shared routines, so `planted_flat` (flat, G = 0 and T_1 − T_2 = 0) and `conv_energy` stay silent
under `ricci-sign`, `planted_flat` and `E_rform` (it does not call the stress function) stay silent under `conv-flip`.

| control | declared targets (all must fail) |
|---|---|
| `scale11-normal` | `E_residual`, `E_rform`, `E_explicit` |
| `scale11-phantom` | `E_residual`, `E_rform`, `E_explicit` |
| `flip-phantom` | `E_solve`, `E_residual`, `E_rform`, `E_explicit` |
| `swap-roles` | `E_solve`, `E_residual`, `E_rform`, `E_explicit` |
| `wrong-partner` | `E_solve`, `E_residual`, `E_rform`, `E_explicit` |
| `potential` | `E_residual` |
| `ricci-sign` | `planted_p1`, `planted_p2`, `E_solve`, `E_residual`, `E_rform`, `E_explicit` |
| `conv-flip` | `conv_energy`, `planted_p1`, `planted_p2`, `E_solve`, `E_residual`, `E_explicit` |
| `p1-sign` | `planted_p1` |
| `p2-scale11` | `planted_p2` |
| `flat-flip` | `planted_flat` |

Development logs, all kept: `dev_checks.run1.log` (8 of 8 pass, 11 s), `dev_checks.run2.log` and `.time` (the same under
`/usr/bin/time -v`: 11.3 s wall, 64 MB peak resident), `dev_controls.run1.log`.
