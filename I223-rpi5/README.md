# I223-rpi5: radial modes of the sourced black bounce and the magnetic black universes (#223)

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared with choptuik-large-d), at most 3 processes, `nice -n 10`,
`OMP_NUM_THREADS=1`, runner `negative-mass-rpi5-i223`.
Issue: https://github.com/nmoinvaz/negative-mass/issues/223
Worktree `~/Source/negative-mass-i223`, branch `wip/i223-black-bounce` (base main 13aa6fe). Code `notes/black_universe/bounce.py`
(imports the integrator helpers of #212's `stability.py`). Python `~/Source/negative-mass-venv314/bin/python`.

Written before any run of `bounce.py`. Two scratch derivations preceded it (sympy only, no count run): the linearized equations
with the extra source terms, and a horizon survey of the declared members. Section "Amendments" at the end lists every later
change with its reason. Status words as in AGENTS.md: a mode count is *numerical evidence*, algebra done in sympy is *checked
symbolically*. The result is stated for these sources only; other sources of the same metric may differ ([BW22], Sec. IV).

## 1. What is computed

Static, spherically symmetric solutions `ds² = A dt² − dx²/A − R(x)² dΩ²` (signature +−−−) of Einstein gravity with a phantom
scalar φ (ε = −1) with potential V(φ) and a magnetic field with Lagrangian L(F), F = F_μν F^μν, F_θφ = q sin θ, so
F = 2q²/R⁴. [BW22] (10)–(17) and [BBS12] (1), (5)–(7). In both families R = √(x² + b²); units b = 1 (the throat radius).

| family | metric function | source |
|---|---|---|
| **S**, sourced black bounce ([SV19] with [BW22]'s source, Q = 0) | `A = 1 − 2m/R`, m = M/a | φ = arctan x ([BW22] (19), ε = −1); `V(φ) = 4m cos⁵φ/5`; `L(F) = (12 m/5)(F/2q²)^{5/4}`, i.e. `L = 12 m/(5R⁵)` ([BW22] (21), (22) at Q = 0, a = 1) |
| **B**, magnetic black universes ([BBS12]) | `A = R² B(x)`, [BBS12] (15)–(18): `B′ = 2(p − x + 2q² arctan x)/(1+x²)²`, `p = 3m − πq²`, B → 0 at x → +∞ | φ = arctan x ([BBS12] (19)); V from (9), printed in (20); Maxwell field, `L = F` up to normalization: energy density `q²/R⁴` ([BBS12] (7)) |

The [BW22], [BBS12] scalar is φ; this work's φ_c = √2 φ is #212's normalization (`R_μν = ε ∂_μφ_c ∂_νφ_c + …`), so
`P0 = √2 arctan x`. S has the one parameter m/a (a = b = 1): wormhole for a > 2m, one-way wormhole (extremal horizon at the throat) for
a = 2m, black bounce for a < 2m, Ellis wormhole at m = 0. B has two parameters (m, q) with p > 0 (a de Sitter end at x → −∞);
q = 0 is #212's family with `3m = −2c/π`.

Field equations used, signature −+++ (as #212), with Λ(r) = L/2 the NED energy density (Maxwell: Λ = q²/r⁴):

```
R_μν − ε ∂_μφ ∂_νφ − V g_μν − g_μν S_μ = 0,   S_t = S_x = Λ + ½ r Λ′(r),   S_θ = S_φ = Λ,    ε □φ = V_φ
```

This is [BW22] (11)–(17) (`T_t^t = T_x^x = L/2`, `T_θ^θ = ½(L − 4q²L_F/r⁴)`), trace-reversed. In spherical symmetry the
Bianchi identity `dF = 0` forces `F_θφ = q sin θ` with q constant, so a radial perturbation changes F only through the area radius:
the NED stress tensor is a given function Λ(R) of R, with no field of its own. Planned symbolic check S4: the linearized system
for (δν, δλ, δR, δφ) in the gauge δφ = 0 (regular, since φ′ ≠ 0) reduces to one second-order equation for Y = δR, with the
tx equation giving δλ, the scalar equation δν′ and the θθ equation the master equation; the tt and xx equations then hold
identically. That is the conjecture of the issue (a magnetic field adds no radial degree of freedom).

## 2. The equation (derived in a scratch run before this README; to be re-derived inside `bounce.py check`, S4)

Generic background A, R, φ₀ and source function Λ(R): the background equations give `R″ = −εφ₀′²R/2`,
`A″ = (A(R²)″ − 2)/R² − R Λ_R` (with `Λ_R = dΛ/dR`; for Maxwell this is [BBS12] (11)) and
`V + Λ + ½RΛ_R = −(A′R²)′/(2R²)` ([BBS12] (9) for Maxwell). The master equation, e^{Wt} time dependence:

```
Y″ = (2R″/R′ − 2φ₀″/φ₀′ − 2R′/R − A′/A) Y′ + (…) Y,   which for R = √(x²+1), φ₀′ ∝ 1/R² is
Y″ = (2/x − A′/A) Y′ + ( 1/R⁴ − A′/(A x R²) − 2/(A R²) − R Λ_R / A + W²/A² ) Y
```

Only Λ_R enters (Λ_RR and Λ itself drop out). At Λ_R = 0 it is #212's equation. With `dx_* = dx/A` and `u = Y/x`:

```
u_{x*x*} = (V̂ + W²) u,   V̂ = 2A²/x² − (1 + 1/R²) A A′/x + A²/R⁴ − 2A/R² − R A Λ_R
```

S: `R Λ_R = −6m/R⁵`. B: `R Λ_R = −4q²/R⁴`. So the NED term is `+6mA/R⁵` (S) and `+4q²A/R⁴` (B) in V̂.
The operator `−∂²_{x*} + V̂` is real, so growing modes (ω = iW, W > 0) have real W² and are its negative eigenvalues.

## 3. Boundary conditions and method

The static region is the one outside the outermost horizon x_h (A > 0 for x > x_h), open to the flat end x → +∞. Inner horizons
and the T-region are not part of the problem (B at q = 0.8, 0.81 of slice B2 has inner horizons; only the outermost is used).

- infinity: `u_x*/u = −W − V̂/2W`, integrated inward from `r0 = max(rmax0, rmaxW/W)`;
- simple horizon, x_h ≠ 0: ingoing, `Y ~ (x − x_h)^{W/A′(x_h)}`, started at `z0 = x − x_h` in `ln z`; x_h = 0 (horizon at the throat):
  `Y ~ x^{1 + W/A′(0)}`; for B2, `A′(0) = 2p` exactly;
- extremal horizon at the throat (S, a = 2m: `A ≈ x²/2` at x = 0, κ = 0): `x_* → −∞` like −2/x, `u ~ e^{W x_*}`; started at
  `x0 = clip(0.04 W, 1e-4, 0.1)` with `u_x*/u = W + V̂/2W`, `Y_x*/Y = A/x + u_x*/u`;
- no horizon (S, a > 2m; Ellis): decaying at both ends, `u ~ e^{+W x_*}` at x → −∞;
- throat inside the static region (x_h < 0 or no horizon): a regular singular point of Y (exponents 0 and 3, both analytic).
  Y is continued along the upper half circle `x = d e^{iθ}` in the complex x-plane, `d = min(delta, ½|x_h|)`;
  the relative imaginary part of Y afterwards is the monodromy test (no logarithm). `d` is below the distance to the
  complex zero of A (S: `√(1 − 4m²)` at x = ±i, 0.436 for the declared m = 0.45) and below the branch point x = ±i.

A growing mode is a sign change of the Wronskian mismatch of the two solutions at `x = 1` (or `x_h + 1` for x_h ≥ 0.5) on
a log grid of W, refined by Brent. Each root's eigenfunction is integrated and its nodes counted. The count is reported with its
range W ∈ [1e-3, 8] (units 1/b).

Settings, declared now, fixed for the runs of record (R1 and R2 as in #212; the grid is denser for the wider range):

| | rtol | z0 | rmax0 | rmaxW | delta | nW |
|---|---|---|---|---|---|---|
| R1 | 1e-9 | 1e-9 | 150 | 30 | 0.3 | 80 |
| R2 | 1e-12 | 1e-13 | 300 | 45 | 0.2 | 200 |

Agreement of R1 and R2: equal counts and every W within 1e-6 relative.

**Independent checks.**
- **S6 spectral**, Chebyshev collocation of the same equation as a matrix problem (u-form when the static region has no throat,
  x_h ≥ 0; Y-form otherwise), `N = 401, X = max(45, 12/W)` (S-A) and `N = 801, X = max(90, 24/W)` (S-B), W the shooting rate (45 and
  90 where there is no mode). It shares the background and the coefficients, nothing of the boundary conditions, the throat crossing
  or the root finding, and finds complex eigenvalues. Criteria: equal counts, no complex eigenvalue with Re λ > 1e-3, rates within
  S-A 1e-2 and S-B 1e-4 (x_h ≥ 0), S-A 1e-2 and S-B 2e-2 (throat in the region).
- **S9 Sturm count** (members with x_h ≥ 0 only): the zero-energy solution of `u_x*x* = V̂ u` regular at the horizon has as many
  nodes on the line as `−∂² + V̂` has negative eigenvalues. It has no W grid and no range, so it covers rates outside [1e-3, 8].
  It shares V̂ with the shooting and nothing else. Criterion: equal to the shooting count. For members with the throat in the
  region the analogue is the spectral count only (the wall `2A²/x²` makes the problem a continuation, not a Sturm problem).

## 4. Planted cases and tolerances (declared)

- **P1.** S at m = 0 is the Ellis wormhole. Through the same code: one growing mode, `W² a² = 1.39705243433350684`
  (`notes/wormhole_largeD/w2_output.txt`, D = 4), absolute difference ≤ 1e-7 (R1) and ≤ 1e-9 (R2), as #212.
- **P2.** Zero charge returns #212's table: B at q = 0, `3m = −2c/π`, c ∈ {−10, −3, −1.1, −1, −0.9, −0.3, −0.01}: the same
  count as `notes/black_universe/stability_output.txt` (1 mode, 0 at c = −1) and `|W − W_212|/W_212 ≤ 1e-7` (R1), `≤ 2e-9` (R2);
  the table prints W to 10 decimals. c = −3, −1, −0.3 are the q = 0 members of the slices B1, B2, B3 below.
- The P1 and P2 members do not exercise the NED term (Λ ≡ 0 there). The NED term is guarded by S1, S4, S5, S8 below and by
  the control `ned_off`, which changes the rate.

## 5. Members (declared)

W in units 1/b. m is M/a for S.

| slice | members | what it covers |
|---|---|---|
| **S** | m = 0 (Ellis, P1), 0.1, 0.2, 0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.75, 1, 1.5, 2, 3, 5, 10 | a/m = ∞, 10, 5, 3.33, 2.5, 2.22, 2 (one-way), 1.82, 1.67, 1.33, 1, 0.667, 0.5, 0.333, 0.2, 0.1: 6 wormholes, the one-way wormhole, 9 black bounces |
| **B1** | m = 2/π (c = −3 at q = 0); q = 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.74, 0.76, 0.77, 0.775 | x_h > 0 for q ≤ 0.74, x_h = −0.0147 at 0.76 (the horizon crosses the throat at q ≈ 0.7595), x_h < 0 beyond; p from 1.91 to 0.023 |
| **B2** | `m_c(q) = (2/3π)(1 + q² + π²q²/4)`, the horizon at the throat, A(0) = 0, `κ = p`; q = 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.78, 0.8, 0.81 | q = 0 is #212's stable member c = −1; the locus ends at the extremal regular black hole q = 0.825, p = 0; κ from 0.64 to 0.024 |
| **B3** | m = 0.2/π = 0.0636620 (c = −0.3 at q = 0); q = 0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.2, 0.22, 0.23, 0.24 | throat in the static region, x_h from −0.93 to −5.5 |
| **P2** | c = −10, −3, −1.1, −1, −0.9, −0.3, −0.01 at q = 0 | the zero-charge table of #212 |

The charge slices are one-parameter cuts through the two-parameter family, chosen before any count: fixed mass (B1, B3) and the
locus where the horizon sits at the area minimum (B2, the knife edge of #212). Counts between the members are not computed.
Not computed: the symmetric (p = 0) twice-flat members of [BBS12] Sec. 3.2, p < 0 (M-AdS), the electric field, the RN-SV source of [BW22],
other static regions, the region beyond the horizon.

## 6. Checks and controls

Checks in `bounce.py check` (sympy where stated, mpmath otherwise; exit 1 when a check fails):

| check | what |
|---|---|
| S1 | background of S and B against the field equations above: residuals 0 (sympy); [BW22] (21), (22) at Q = 0 against the Einstein equations; [BBS12] (15) for B, printed (20) for V against (9) |
| S2 | the same at 40 digits at members and points; the series of `A/z` at the horizon and the large-x form of B against mpmath |
| S3 | `A′(x_h)`: S closed form, B2 `A′(0) = 2p` |
| S4 | linearization, generic A, R, φ₀, Λ(R): the five background equations, tt and xx after the master equation (gauge δφ = 0), the same in the gauge δR = 0, the gauge map `F = −φ₀′Y/R′`; `dF = 0` ⇒ q constant; the NED equation `∇_μ(L_F F^{μν}) = 0` holds for the perturbed metric with δF = 0 |
| S5 | family coefficients against the generic derived equation, 30 digits (S and B) |
| S8 | V̂ of the u-form against the δR = 0 gauge potential plus `R_{x*x*}/R`, with the NED term |
| S6, S9 | spectral and Sturm counts (above) |
| P1, P2, R | planted Ellis, zero charge, R1 v R2 |

Control names (the target of each is declared after its development run, in "Amendments"; a control that is silent on its target
is a result and is reported): `sv_V`, `sv_L`, `bbs_A`, `bbs_V20`, `ned_T`, `master_ned`, `master_p`, `family_ned`, `veff_ned`
(check-level); `eps`, `throat_wall`, `rmax` (planted); `ned_off`, `hz_start`, `scan_range`, `spec_sign`, `sturm_sign` (counts).
Predictions are written before the development run of each.

## 7. Operations

Runs longer than a few minutes are systemd user units `nm-i223-<name>` (`nice -n 10`, one thread), at most 3 at once, the log and
exit code in this folder, reruns numbered (`<name>_run2.log`), no log overwritten. Stop condition: any run not finished in 1 h of
wall time is stopped and reported with what finished. Results: `results/<id>_<R1|R2>.json`.

## Development history

Development runs are in `dev/` (R1 unless stated; never part of the record). Newest facts first within each item.

- **D1, scratch derivation (sympy, before this README).** The master equation of Sec. 2 with `tt` and `xx` residual 0, the gauge
  `δR = 0`, the gauge map, and the NED extension of [BKZ12] (41): `A·Ũ = ε φ′²/R′² (R²(V + Λ) − 1) + 2φ′R V_φ/R′ + ε V_φφ`, i.e. V → V + Λ in the
  first term only. `bounce.py check` now re-derives all of it.
- **D2, horizon survey (scratch, no count).** Every declared B member has one outermost horizon, simple except at B2; A > 0 outside it.
  B2 at q = 0.8, 0.81 has two further, inner horizons (x = −1.64, −0.31 and −2.61, −0.16), unused.
- **D3, `check` development.** The first `check` failed S2 and S8 because of errors in the checks, not in the background: S8 compared
  `A·Ũ + R_{x*x*}/R` where the potential is `A²Ũ + R_{x*x*}/R`; S2 took A/z at z = 1e-9 with the float horizon (a float x_h is off by 4e-15,
  which at z = 1e-9 is a relative 1e-6), and for B2 the float throat mass gives A(0) = −5e-17. The checks were corrected (exact x_h,
  exact throat mass in the reference); the numerical background code was not changed. `check` then exits 0 (about 42 s).
- **D4, first R1 runs.** `planted --res=R1`: W²a² = 1.397052434007020, 3.265e-10 from the reference, the same as #212's R1. P2 at c = −10, −1.1, −0.9,
  −0.3, −0.01, −1 equal #212's table (one mode each, none at c = −1; |ΔW|/W 3e-10 to 3e-9 at R1). About 11 s to 47 s per member at R1, S at m = 0.5 (extremal) 146 s,
  B2 at q = 0.81 88 s.
- **D5, the Sturm count.** First version (u form): a wrong `2·A·Ar` for `2·Ar²` in `Vhat` (8 nodes at c = −1, caught by comparing with the shooting
  count of 0), then, after the fix, a hang at x_h = 0: `Vhat` there is a cancellation of O(1) terms down to O(x) and the noise in it (1e-16) is
  larger than rtol·|u_x| at z0 = 1e-8, so the step size collapsed. `P2_c-1` and `B2_q0.5` ran 16 min without finishing; their units `nm-i223-dev1`
  and `nm-i223-dev3` were stopped by hand at 01:04 (log empty, a stop below the 1 h condition but with the cause known). The Sturm count is now
  integrated in the Y form at W = 0 (u = Y/x, x > 0, the same nodes). The same wrong `2·A·Ar` had been written into the spectral
  routine, which had not been run.
- **D6, the weak second mode.** Dev R1: the black bounce S at m = 0.55, 0.6 and B1 at q = 0.5 have two growing modes in the declared range (second W =
  0.0046, 0.0024, 0.0067, one node). S at m = 0.75, 1, 3 have Sturm 2 and shooting 1; at m = 1 a probe finds the second root at W ≈ 1.1e-4 (the mismatch
  changes sign between 9.4e-5 and 1.4e-4), at m = 3 there is no sign change down to 3e-5. S at m = 10 has Sturm 1. Reported to the coordinator, ruling
  below (A2).
- **D7, the planted weak bound state.** The first version of P3 found no root: for the exponentially decaying planted potential the integrator's step
  grows to thousands in the free region and steps over the well (u unchanged, D = −2W). Fixed by integrating the free part with `run_chunks` to
  |x| = 40 and the well with `max_step = 0.5`. The real potentials have power-law tails and showed no such skipping (P1, P2 agree with #212).

- **D8, the spectral check.** First run (box from the largest shooting rate): B1 at q = 0.5 lost its weak mode (box too small), B3 at q = 0.15 gave 4.6e-2
  at S-A. Box from the smallest rate on the plain grid: garbage for X > 250 (spacing at the centre of the Chebyshev grid 7 to 14 against structure of
  size 1 to 3). A sinh-mapped grid fixed it (A4): 12 R1 members, 5e-8 at worst for the mapped ones, including the weak mode of B1 at q = 0.5 (6.7e-3) and the
  throat member B3 at q = 0.15 (1e-8; #212's plain grid gave 4.5e-3 at throat members).
- **D9, the glitch in P3.** With the range excluded (`lowW_range`) `planted_low` found 2 roots, one of them a single wrong point of D(W) (W = 2.57e-4: D = +1.3e-3
  between neighbours of −4.5e-4). Cause: a step of `run_chunks` crossed the well (|x| < 40) in the free region and the terminal event at x = −40 was located
  from a dense-output polynomial of that step. Fixed: free flow up to |x| = 1040, the well with `max_step = 0.5`. The real runs use power-law tails and
  have not shown it; every root of record is checked against a second resolution, Sturm and the spectral count.
- **D10, the controls (dev).** All 21 controls fire (`dev/controls_dev{1,2,3}.log`). Differences from A3's predictions: `hz_start` moves W of B3 at q = 0.15 by 0.17
  (predicted 1e-4); `ned_off` removes the second mode of that member (2 modes → 1; predicted a 1 % change of the rates), so the weak-ish mode (W = 0.045) is
  produced by the charge; `B1` at q = 0.3, the member chosen for the Sturm and spectral controls, has two modes in range (a weak one of 1.8e-3) and Sturm 2, not
  1 (the detail strings of the controls were corrected, nothing else changed); `lowW_range` first returned the glitch of D9, then 0 roots; `rmax_low` removes the
  root of S at m = 1 (low stage), as predicted.

- **D11, the low stage on B (record runs).** After the 126th job (all main-stage runs and the S low-stage R2 runs done), the low-stage R2 runs of B1 at q = 0, 0.1,
  0.2 ran 16 min each without finishing; the units `nm-i223-w1..3` were stopped by hand at 03:38 (below the 1 h condition, cause then found; their `.log` files are empty
  and are kept as `results/B1_q0*_R2_low.log`, the status line is in `results/status.txt`). Cause: at W = 1e-5 the right start is at r0 = 2e6 and the closed form of A
  for B loses accuracy there (B ~ 1/x² from O(p/x) terms: the absolute noise 1e-16 x in A reaches 1e-11 at x = 1e5), so the integrator's step collapses (status −1) at
  x ≈ 1e5 at rtol 1e-12. The main stage reaches r0 = 4.5e4 where the noise is 2e-12, below its tolerances (P2 agrees with #212 to 3e-10).

## Amendments

All written before the runs of record they govern.

**A1. Details left open in Sections 3 and 6.**
- S6: real eigenvalues are counted for `λ > W_LO² = 1e-6` (W = 1e-3), complex ones are flagged for `Re λ > 1e-3`, as declared.
- S2 criteria: `|ΔA|/|A| ≤ 1e-11` (where |A| > 1e-3), `|ΔA′| ≤ 1e-11` absolute, `|Δ(A/z)|/|A/z| ≤ 1e-11`, at 7 members, z from 1e-9 to 0.3, x to 3000.
- Added checks (so S1 also holds the printed forms): S1 against [BBS12] (8)–(12), (15) as printed, printed (20) against (9) at 30 digits (declared ≤ 1e-25),
  [BW22] (11)–(13), (16), (17), (21), (22) at Q = 0 against an independent Einstein tensor in their conventions (signature +−−−, `G^ν_μ = −T^ν_μ`), S4 NED source
  (`T^t_t = T^x_x = −L/2`, `T^θ_θ = F L_F − L/2`, `F = 2q²/r⁴` on the perturbed metric), `dF = 0`, and the NED equation.
- S9 is integrated in the Y form at W = 0 (D5). Criterion as worded: the Sturm count equals the shooting count in the declared range. Where it does not,
  S9 is reported NOT MET with both counts (coordinator's ruling).

**A2. The low-W stage (coordinator's ruling on D6: "keep the declared range, add a declared low-W stage").**
- Shooting on W ∈ [1e-5, 1e-3], log grid, `nW` = 40 (R1) and 100 (R2), the declared rtol, z0, delta and rmax0 of Sec. 3, and its own outer radius
  `r0 = max(rmax0, 20/W)` (3e6 at W = 1e-5, below the integrator's guard of 1e7; the wrong solution is suppressed by e^{-40} over the distance 1/W-scaled
  r0). Same code path as the main stage (`count ID --stage=low`), JSON `<id>_<res>_low.json`. Run for every member, at R1 and R2.
- Tolerances: R1 and R2 of the low stage agree in the count and in W to 1e-4 relative.
- **P3, planted weak bound state:** `u'' = (V + W²)u`, `V = −ν(ν+1)κ² sech²(κx)`, κ = 1, ν = 3e-5, one bound state at `W = νκ = 3e-5` exactly, run through the low stage's
  outer-radius rule, chunked integration, log grid and Brent (not through the background code). Declared: exactly one root on [1e-5, 1e-3] and
  `|W − νκ|/(νκ) ≤ 1e-3` (R1), `≤ 1e-4` (R2). Dev: 1.3e-10 (R1), 5.0e-13 (R2).
- Reporting: the count of a member is its main-stage count plus its low-stage count; where the Sturm count (x_h ≥ 0) is larger still, the Sturm count is the
  count and the missing rate is stated to lie below 1e-5, unresolved. Each weak mode is confirmed at a second resolution (R1 and R2 roots, and the Sturm
  count). The rates of the second mode are given against m and q as observed; no reading of the mode is offered.

**A3. Control predictions, written before the development run of the controls** (`controls` runs each `--mutate=` and asserts its target):

| control | target | predicted effect |
|---|---|---|
| `sv_V`, `sv_L` | S1 | the S-family V and Λ equations and the [BW22] printed components fail, residual O(m) |
| `bbs_A` | S1 background | the B-family equations fail |
| `bbs_V20` | S1 [BBS12] printed (20) | printed (20) against (9) off by O(1) |
| `ned_T` | S4 NED source | `S_th − Λ` fails, and the S4 background lines |
| `master_ned`, `master_p`, `bkz41_sign` | S4 linearized | G1 tt/xx residuals ≠ 0, gauge map ≠ 0; (41) line |
| `family_ned` | S5 | difference of the size of the NED term |
| `veff_ned` | S8 | difference `A R Λ_R`-sized |
| `bg_kappa`, `az_series` | S3, S2 | S3 off by a factor 2; S2 about 5e-4 |
| `eps`, `throat_wall`, `rmax` | P1 | 3 growing modes at Ellis (as #212); 0 modes; error about 5e-7 against 1e-7 |
| `hz_start` | R1 v R2 on B3, q = 0.15 | W differs by about 1e-4 (#212: 1.9e-4) |
| `ned_off` | R1 v R2 on B3, q = 0.15 | a change of the rates of order 1 %, the NED term being 0.09 A/R⁴ in V̂ |
| `scan_range`, `sturm_sign` | S9 on B1, q = 0.3 | shooting 0 against Sturm 1; Sturm differs from 1 |
| `spec_sign` | S6 on B1, q = 0.3 | count mismatch |
| `lowW_V`, `lowW_range` | P3 | root at 6e-5 (relative error 1); no root |
| `rmax_low` | low-stage R1 v R2 on S, m = 1 | the root moves or disappears |

`ned_off` and `hz_start`, `rmax_low` are agreement controls: the NED term itself is guarded by S1, S4, S5, S8 (the zero-charge members P1, P2 have Λ ≡ 0), and
`ned_off` shows that it matters at the member.

**A4. The spectral grid (S6), after D8.** The box rule is `X = max(X0, kX/W)` with W the smallest shooting rate of the member in the declared range (the
declared "W the shooting rate" for a member with one mode). For X > 150 the Chebyshev nodes ξ are mapped, `x_* = X sinh(aξ)/sinh(a)` with a = 5 (derivative by
the chain rule); for X ≤ 150 the grid is the plain one of Sec. 3. N, X0, kX and the tolerances are as declared. Counted: real eigenvalues λ > 1e-6; modes
below W = 1e-3 are outside this check, as they are outside the declared range.

**A5. Control targets, declared after the development run of D10** (`CONTROLS` in `bounce.py`; kind in brackets; check/planted: exit 1 with a FAIL line holding the target):
`sv_V`, `sv_L` (check, S1); `bbs_A` (check, S1 background); `bbs_V20` (check, S1 [BBS12] printed (20)); `ned_T` (check, S4 NED source); `master_ned`, `master_p`,
`bkz41_sign` (check, S4 linearized); `family_ned` (check, S5 family); `veff_ned` (check, S8 Vhat); `bg_kappa` (check, S3 horizons); `az_series` (check, S2 float64);
`eps`, `throat_wall`, `rmax` (planted, P1); `hz_start`, `ned_off` (agree: R1 with the mutation against the unmutated R2 of B3 at q = 0.15, fires when the counts differ or
a rate differs by more than 1e-6); `scan_range`, `sturm_sign` (sturm: B1 at q = 0.3, shooting count in range against the Sturm count, fires when they differ);
`spec_sign` (spectral, S6, B1 at q = 0.3); `lowW_V`, `lowW_range` (plantedlow, P3); `rmax_low` (agreelow: low-stage R1 with the mutation against the unmutated low-stage R2 of S at m = 1).
The agreement controls do not test the NED term itself (see A3); the Sturm controls fire against the Sturm count, which is not mutated by `scan_range`
and is the mutated quantity in `sturm_sign`.

**A6. Runs of record.** Main stage R1 and R2 and low stage R1 and R2 for the 55 members (S 16, B1 12, B2 12, B3 11, P2 4; B1 q = 0, B2 q = 0, B3 q = 0 are the P2 members
c = −3, −1, −0.3), three worker units at a time, logs and JSON in `results/`. `bounce.py` at the commit named in the closing comment; no edit to it while the runs go.

**A7. A and A′ of B at large x in the low stage (after D11).** For the B family in the low stage (`Bg(..., stage="low")`), A and A′ are evaluated for x ≥ 30 from the
series of B in y = 1/x (`B(x) = (1+q²+px)/(1+x²) + πq²x/(1+x²) − (p+πq²)t − 2q²xt/(1+x²) + q²t²`, t = arctan y, 40 terms, coefficients by
convolution; A = (1 + y⁻²)B, so A = Σ c_n yⁿ without cancellation). Against mpmath at 60 digits: |ΔA| ≤ 1.1e-16 and |ΔA′|/|A′| ≤ 3e-16 at x from 30 to 2e6, at 5 members.
`check` S2 includes it (declared |ΔA| ≤ 1e-14, |ΔA′| ≤ 1e-12 |A′|; control `ser_coef`). The main stage and the S family are unchanged: the main-stage runs of record, the S low-stage R2
runs and the first 126 jobs are from `bounce.py` at 9b3db56; the B low-stage runs (and every later `check`, `planted`, `controls`, `spectral`, `report`) from f6d1802, which
differs from 9b3db56 only in this flag and its check. The remaining low-stage jobs are in `jobs_low.txt` (the queue pointer of the first run is `results/qpos_run1`).
