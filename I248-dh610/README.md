# I248-dh610: is the c = −1 black universe's growing horizon sector free in physical Cauchy data

Machine: dh610-fedora (20 cores, 62 GB, Fedora; shared with choptuik-large-d), Python 3.14 (`~/Source/negative-mass-venv314`: sympy,
mpmath, numpy, scipy, numba), `nice -n 10`, one thread per process, at most four processes, long runs as systemd user units
`nm-i248-*`. Code: `notes/black_universe/horizon_sector.py` at commit 69de2ea in worktree `~/Source/negative-mass-i248`, branch
`wip/i248-horizon-sector` on main de0b930. Issue: https://github.com/nmoinvaz/negative-mass/issues/248 (depends on #232).
Written 2026-11-27 before the runs of record. The development runs, which fixed the bars and the mutation targets below, are in
`dev/` (every log kept; the two first runs of `k_emF` and `k_FV` stopped with an IndexError, a bug of the mutation plumbing, and
were rerun as `dev07_*`).

## Question and formulation

#232: at c = −1 the linear double-null response grows at κ for data with Y_h = c₁ + c₂ e^{bp} on the horizon, c₂ ≠ 0. Is c₂ free in
regular Cauchy data on a slice through the horizon? Formulation, all in the Kruskal chart of the member, which contains the bifurcation
surface S, both horizons and the interior ρ < 0:

- x⁺ = V = e^{bp}, x⁻ = U = −Q(σ), Π = −VU = e^{2κx} (static region V > 0 > U); `ds² = −2e^{−F} dV dU + r² dΩ²`, `e^{−F} = G/κ`,
  `G = dρ/dΠ = A/(2κΠ)`, r = R(ρ), φ = √2 arctan ρ, ρ(Π) analytic through Π = 0. The interior ends at Π ≈ −0.37 (ρ → −∞), so a
  rectangle V ∈ [−0.05, 3], U ∈ [−2, 0.06] (−Π ≤ 0.18) reaches ρ ≈ −1.5.
- Y = δr − (ρR/√2)δφ is invariant under every linear diffeomorphism; on the horizon ρ = 0 and Y_h = δr_h. The linearized constraint on
  U = 0 is δr_VV = 0, so Y_h = c₁ + c₂V exactly, c₂ = ∂_V δr there. The functional of slice data is c₂ = ∂_V δr at the point where the
  slice V + U = const crosses U = 0 (4th-order stencils: tangential derivative from the slice values, normal derivative from the
  slice and its neighbours at ±1, ±2 nodes).
- Data: characteristic data on two rays (δφ a Gaussian pulse, δF = 0, δr from the linearized constraint along the ray with corner
  constants), exactly as #232, here on a rectangle whose left ray V = −0.05 and right ray U = −2 enclose S. Classes L, R, G (pulses
  on the left ray, the right ray, both) and corner constants A0 (δr), A1R (δr_V), A1L (δr_U); amplitudes 1e-3.

## Verdicts (declared before the runs of record)

Each verdict reads "decided" only if every check named for it is met; otherwise it reads "not decided" and the failing check is reported.
No sentence of the note says the member is unstable or stable beyond these.

| verdict | statement | checks |
|---|---|---|
| V1 | c₂ is a functional of the slice data, and equals c₂ of #232's solutions | D2, N4, N5, N9, N11 |
| V2 | c₂ is free: no constraint restricts the first-order jet at the crossing point, the data realizing c₂ ≠ 0 satisfy the constraints, and random regular data have c₂ ≠ 0 | D2, D4, N3, N10, N11 |
| V3 | the W = κ solution Y ∝ V is regular across S and into the interior | D6, D7, D8, N2, N8 |
| P | planted: the extraction recovers a known coefficient where no growing sector exists | N6 |
| C | control: data with c₂ = 0 give zero | N7 |

## Criteria (as worded in `horizon_sector.py`, which prints each text with its numbers)

| id | what | bar |
|---|---|---|
| D1 | the Kruskal-chart member solves the 3 evolution equations and 2 constraints, symbolic κ, c = −1, −3/2, −3/10 | residual identically 0 (15 of 15) |
| D2 | on U = 0 of the c = −1 member C_VV is a_VV = 0; g = ρR/√2 = 0 there | sympy equality |
| D3a, D3b | Y is invariant under every diffeomorphism; r_U on the horizon is −R′(ρ_h)G(ρ_h)V: zero at c = −1, nonzero at c = −1.5 | sympy identity; R′(ρ_h) > 0.3 at c = −1.5 |
| D4 | d_U C_VV = −(r_U/r) C_VV and d_V C_UU = −(r_V/r) C_UU on solutions of the evolution equations (generic background jets, exact rational points) | residual exactly 0 |
| D6 | formal series of the Y equation at S (c = −1, M = 0, degree ≤ 7): free coefficients exactly y_mn with m = 1 or n = 1 (13), consistent; y_00, y_0n, y_m0 (n, m ≠ 1) vanish | sympy |
| D7 | Frobenius series of Y at W = κ, exponent 1/2, has no logarithm (orders ≤ 5) | solvable at every order |
| D8 | Y equation at W = κ: A < 0 on ρ < 0, A > 0 on ρ > 0, no singular point; the ρ^{1/2} solution integrates to ρ = ±40 | finite |
| N1 | Kruskal jets against `linear.bg`, c = −1 and −1.5, 8 points each | 1e-12 |
| N2 | exact pure-gauge solutions reproduced at second order through S and the interior: c = −1, −1.5, Schwarzschild; h = 0.02, 0.01, 0.005 | last ratio in [3.7, 4.3], error below 5e-4 of the largest field |
| N3 | horizon values linear in V on [−0.05, 3] for classes L, G, A0, A1R, A1L; h = 0.005, 0.0025, 0.00125 | residual at the finest below 2e-5, ratios 4 ± 0.5 |
| N4 | c₂ from the slices crossing at V = 0 (S), 0.5, 1 against the horizon fit; Richardson of h = 0.0025, 0.00125 | relative difference below 1e-6 |
| N5 | #232's own solutions at c = −1 (σ* = 16, L3a's three left-ray pulses, P = 10): c₂ from slices crossing at p = 1, 2, 4, 6 against the fit and #232's two-point c₂; Richardson of h = 0.005, 0.0025 | 1e-6 (the raw value at h = 0.005 is reported) |
| N6 | planted: pure-gauge data with known δr_h = −η(0)R′(ρ_h)G(ρ_h)V (c = −1.5; G from an mpmath quadrature) and −η(0)e^{−1}V (Schwarzschild); the Y-version is 0; a Schwarzschild test field leaves δr = 0 and has no linear horizon law | exact data 1e-8, marched 1e-6, Y-version 0 to the same; test field: δr below 1e-14, fit residual above 0.1 of the maximum at h = 0.01, 0.005 and not falling |
| N7 | control: exact pure gauge at c = −1; class R; L + λA1R with λ from the horizon fits | 1e-5 at h = 0.005 falling by 10 to 22; R below 1e-5 of L's c₂, seed ratios 3 to 5; tuned sum below 1e-5 of L's c₂ |
| N8 | the fields dr, dF, dφ, Y at S, two interior points, the static region and the left side converge at second order, classes G and A0; h = 0.01 … 0.00125 | Cauchy ratios 3.0 to 5.5 (coarse), 3.5 to 4.5 (fine) |
| N9 | the Kruskal solver against `linear.py` on the same corner-constant data (V, U) = (1, −1) = (p, σ) = (0, 0); Richardson of three resolutions each | 1e-5 |
| N10 | the linearized constraints C_VV, C_UU of the evolved solution (classes G and A0) shrink by 4 from h = 0.01 to 0.005 | ratios in [3.3, 4.7], below 5e-3 of the largest term |
| N11 | 20 random smooth data (seed 248): slice functional equals the fit; no draw has c₂ near 0 | 1e-6 of max(\|c₂\|, 1e-3); \|c₂\| > 1e-5 for every draw |

Status words for the answer: the symbolic checks are *checked symbolically*; the solver checks are *numerical evidence*. Where the two
agree the answer is stated as both.

## Planted case and control

- **Planted (P, N6).** At c = −1.5 (ρ_h ≠ 0) and in Schwarzschild (r_s = 1, φ = 0, V = 0) the quantity δr_h = c₂V is pure gauge (the
  horizon shifts, r_U ≠ 0 there) and no growing sector exists; its coefficient for a given exact gauge solution is known in closed form.
  The extraction (the functional, the fit, the Richardson step) is run on exact gauge data and on the marched solution and must return
  the known number; the gauge-invariant Y-version must return 0. The Schwarzschild test field (φ decoupled from δr) must give δr = 0
  and a horizon value of δφ that obeys no linear law, the contrast with Y_h at c = −1.
- **Control (C, N7).** Data with c₂ = 0 by construction: exact pure gauge at c = −1 (r is stationary on the horizon), class R (zero in the
  continuum, the truncation seed falls by 4 per halving, as #232's L5), and a superposition with c₂ cancelled by the fit's values and
  tested by the slice functional.

## Mutations (each fires its declared checks; declared from development runs `dev/`)

| name | what it breaks | fires (declared) | development run |
|---|---|---|---|
| `d_emF` | e^{−F} = 1.01 G/κ in the symbolic Kruskal background | D1 | dev07_derive_d_emF |
| `d_Gode` | d ln G/dρ scaled by 1.01 | D1 | dev07_derive_d_Gode |
| `d_hz` | C_VV evaluated at U = 0.1, off the horizon | D2 | dev07_derive_d_hz |
| `d_prop` | sign of the ε r φ_V e_V term of the constraints | D4 | dev07_derive_d_prop |
| `d_gauge` | g = ρR/2 instead of ρR/√2 in Y | D3a | dev07_derive_d_gauge |
| `d_res` | b² scaled by 1.1 in the formal series | D6 | dev07_derive_d_res |
| `d_log` | W = 1.1κ in the Frobenius series | D7 | dev07_derive_d_log |
| `k_emF` | e^{−F} 1 % off in the Kruskal-chart solver | N1 N2 N3 N4 N6 N7 N9 N10 N11 | dev08_check_k_emF |
| `k_FV` | sign of F_V, F_U in the Kruskal-chart background | N1 N2 N3 N4 N6 N7 N9 N10 N11 | dev08_check_k_FV |
| `k_cross` | sign of the (r_V/r)δφ_U + (r_U/r)δφ_V terms in the solver | N2 N3 N4 N6 N7 N9 N10 N11 | dev09_check_k_cross |
| `k_con` | ray constraint with the wrong sign (the data violate C_VV, C_UU) | N3 N4 N7 N11 | dev04_check_k_con |
| `fn_aT` | the functional uses the tangential half d_T only | N4 N5 N6 N7 N11 | dev09_check_fn_aT |
| `fn_dirU` | the functional takes d_U instead of d_V | N4 N5 N6 N7 N11 | dev05_check_fn_dirU |
| `fn_b` | b = √2κ 1 % off in the e^{bp} → V conversion of #232's solutions | N5 | dev05_check_fn_b |
| `plant_sign` | sign of the planted known coefficient | N6 | dev05_check_plant_sign |
| `ctl_lambda` | λ of the tuned superposition 10 % off | N7 | dev05_check_ctl_lambda |

In a run of record the fired set must equal the declared set; the run prints both. Development notes: the unmutated development runs are
`dev01_derive`, `dev01_check` (N1–N9), `dev01_check_N10`, `dev06_check_N11`, `dev07_derive` (8 of 8) and `dev03_table`. Runs that were
superseded and kept: `dev02_derive_*` (before the D1 numeric pre-test; D1 then failed in every mutated run because of a precision slip, and `d_Gode`
took 8.6 min of CPU in sympy before it was stopped by its PID), `dev04_check_k_emF` and `dev04_check_k_FV` (IndexError in the mutation plumbing,
fixed), `dev04_check_k_cross`, `dev05_check_fn_aT` (before N11 existed). Fired sets of `d_*` are the `dev07` runs; those of `k_*`, `fn_*`, `plant_sign` and
`ctl_lambda` are the runs in the table, all with the code of the commit below.

## Runs of record (`runs/`; commands from `notes/black_universe`)

```
horizon_sector.py derive                 # D1 - D8, ~1 min
horizon_sector.py check                  # N1 - N11, ~7 min
horizon_sector.py table                  # the c1, c2 table and the samples, ~1 min
horizon_sector.py derive|check --mutate=NAME   # every mutation below
```

## Amendments

**A1, 2026-11-27, after the runs of record.** The runs of record are of code commit 69de2ea. After them the subcommand `horizon_sector.py mutations DIR PREFIX`
(a report of stored mutation logs against the declared sets) and its line in the docstring were added; no check, bar or mutation changed. Its output over the
16 logs is `runs/run01_mutations_report.txt` (16 of 16 equal).

## Runs of record (files in `runs/`)

| file | what | result |
|---|---|---|
| `run01_derive.log` | `derive` | 8 of 8 |
| `run01_check.log` | `check` | 11 of 11, 562 s |
| `run01_table.log` | `table` | the class table |
| `run01_mut_<name>.log` | 16 mutations (7 derive, 9 check) | every fired set equals the declared one |
| `run01_mutations_report.txt` | `mutations` over the 16 logs | 16 of 16 equal |
