# I212-rpi5: radial stability of the phantom black universes of Bronnikov and Fabris, against [BKZ12] (#212)

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared with choptuik-large-d), at most 3 processes, `nice -n 10`,
`OMP_NUM_THREADS=1`, runner `negative-mass-rpi5-i212`.
Issue: https://github.com/nmoinvaz/negative-mass/issues/212
Worktree `~/Source/negative-mass-i212`, branch `wip/i212-black-universe` (base main 6256f53). Code
`notes/black_universe/stability.py` (commits 2c22cdd, 629a1a4). Python `~/Source/negative-mass-venv314/bin/python` (3.14.10, numpy,
scipy, sympy 1.14.0, mpmath).

This README was written after the development runs listed in "Development history" and before the first run of record. Section
"Amendments" at the end lists any later change. Status words as in AGENTS.md: a count of modes from a converged computation is
*numerical evidence*; a step done in sympy is *checked symbolically*.

## 1. The family

Equations are those of [BF06] (K. A. Bronnikov, J. C. Fabris, PRL 96, 251101, gr-qc/0511109), read from the arXiv TeX source:
action (1) `S = ∫√g [R + ε (∂φ)² − 2V(φ)]`, ε = −1 for the phantom; metric (2) `ds² = A dt² − dρ²/A − R² dΩ²`; field equations
(3) `(A R² φ')' = ε R² V_φ`, (4) `(A' R²)' = −2 R² V`, (5) `2R''/R = −ε φ'²`, (6) `A (R²)'' − R² A'' = 2`, (7) `B' = 2(ρ₀ − ρ)/R⁴`,
`B = A/R²`; the example (9) `R = (ρ² + b²)^½`, (10) `B(ρ)`, (11) `φ = √2 arctan(ρ/b)`, (12), (14) `V`, (13) asymptotics. [BKZ12] (K. A.
Bronnikov, R. A. Konoplya, A. Zhidenko, PRD 86, 024028, arXiv:1205.2224v3) write the same family in (3), (4), with `3m = ρ₀` and
asymptotic flatness at ρ → +∞ iff `2bc = −3πm` (5).

```
R = √(ρ² + b²),   φ = √2 arctan(ρ/b),   A = R² [ c/b² + 1/R² + (3m/b³)( bρ/R² + arctan(ρ/b) ) ]
V(φ) = −(c/b²)(3 − 2cos²ψ) − (3m/b³)( 3 sinψ cosψ + ψ (3 − 2cos²ψ) ),   ψ = φ/√2 = arctan(ρ/b)
```

Units **b = 1** (b is the minimum of R, the throat radius). Then `3m = K = −2c/π`, one parameter c. Signature and conventions of this
work: mostly plus, `R_μν = ε ∂_μφ ∂_νφ + V g_μν` (the sympy check S4 below reproduces (3)–(6) from it).

| c | what the member is |
|---|---|
| c > 0 | M-AdS wormhole (m < 0). Not computed here (it needs a Dirichlet condition at the AdS end, [BKZ12] Sec. V.B). |
| c = 0 | Ellis wormhole, V = 0, A = 1: the planted case |
| −1 < c < 0 | black universe, one horizon ρ_h < 0, the throat ρ = 0 lies in the static region ρ > ρ_h |
| c = −1 | black universe whose horizon sits at the area minimum, ρ_h = 0 (3πm = 2b) |
| c < −1 | black universe, ρ_h > 0, no throat in the static region |

The static region is ρ > ρ_h, ρ → +∞ is flat. κ = A'(ρ_h)/2 is the surface gravity. Beyond the horizon the Kantowski–Sachs region
(a T region) is not part of the problem, as in [BKZ12].
[BF06] (8) prints `A'(h) = (ρ₀ − h)/R²(h)`. From (7) and `A(h) = 0`, `A'(h) = 2(ρ₀ − h)/R²(h)`; S3 checks this at 40 digits and
`--mutate=bg_kappa` uses the printed form.

## 2. The perturbation problem

Perturbations `δν, δλ, δR ≡ Y, δφ` of `ds² = −e^{2ν} dt² + e^{2λ} dρ² + r² dΩ²`, all ∝ e^{Wt}, W > 0 (growth rate in 1/b).
sympy linearizes `R_μν − ε ∂_μφ ∂_νφ − V g_μν = 0` and the scalar equation about the generic static background (A, R, φ₀, with V from
(4), V_φ from (3)), no family input (S4).

**Gauge δφ = 0** (regular everywhere, since φ₀' ≠ 0). The tρ equation gives `δλ = (Y' − A'Y/2A)/R'`; the scalar equation gives
`δν'`; the θθ equation then gives the master equation; the tt and ρρ equations hold identically (S4, residual 0):

```
Y'' = W² Y/A² − ε R φ₀'² Y'/R' − ε φ₀'² Y/2 + ε R A' φ₀'² Y/(2 A R') − 2(φ₀''/φ₀') Y' − 2(R'/R) Y' + (A' φ₀''/(A φ₀')) Y
      − (A'/A) Y' + 2 A' R' Y/(A R) − 2 Y/(A R²)
```

For the family (ε = −1, b = 1), with x = ∫dρ/A (the tortoise coordinate):

```
Y'' = (2/ρ − A'/A) Y' + ( 1/R⁴ − A'/(A ρ R²) − 2/(A R²) + W²/A² ) Y
Y_xx = (2A/ρ) Y_x + ( A²/R⁴ − A A'/(ρ R²) − 2A/R² ) Y + W² Y
u = Y/ρ :  u_xx = (V̂ + W²) u,   V̂ = 2A²/ρ² − (1 + 1/R²) A A'/ρ + A²/R⁴ − 2A/R²
```

S5 checks the family forms against the generic one (30 digits). At the throat (R' = 0, A(0) ≠ 0) the equation has a regular
singular point with exponents 0 and 3 in Y (the wall `2A²/ρ²` of V̂, u ~ ρ⁻¹, ρ²). At c = 0 it is the equation of
`notes/wormhole_largeD/master.py` for D = 4.

**Comparison with [BKZ12].** Their gauge is δR = 0 (35), `δφ ≡ F`. The gauge map is `F = −φ₀' Y/R'` (singular where R' = 0, the
infinite wall at a throat they describe); S4 checks symbolically that it maps the master equation above onto the δR = 0 one derived
by sympy in the same run. Their effective potential (40), (41) is reproduced symbolically, `A·Ũ = ε φ'²/R'² (R²V − 1) + 2φ'R V_φ/R'
+ ε V_φφ` (S4, for ε = ±1), and numerically at 30 digits against V̂ (S8): `Ψ = −√2 u`, `V_eff = U + R_{r*r*}/R = V̂`. **Printed (36), (37) and
(38) do not agree with this derivation, (40) and (41) do.** With (7), (36) as printed has the coefficients 1 and −2R'/R where the
derived equation has 1/A² and A'/A + 2R'/R; (38) `δφ = Ψ e^{μ₃}` should read `δφ = Ψ/R`; (37) differs from (41) in the first term
(`ε(e^{2μ₃} − V)` against `ε(V − e^{−2μ₃})`) and in the sign of the V_φ term (the check prints three values). The sign pattern is that of
μ₂ → −μ₂, μ₃ → −μ₃ in (36), (38), (37)'s V_φ term, but not of its first term. These are reported, not corrected; nothing below uses (36)–(38).

## 3. Boundary conditions

[BKZ12] (43) quasinormal conditions `Ψ ∝ e^{±iωr*}, r* → ±∞`, with their later convention Ψ ∝ e^{−iωt}. A growing mode has ω = iW,
so Ψ ∝ e^{+W r*} at the horizon (r* → −∞) and Ψ ∝ e^{−W r*} at infinity: decaying at both ends, an eigenvalue problem of a
Schrödinger operator, W² real. Here:
- **Horizon** (ingoing, regular on the future horizon): `Y ~ (ρ − ρ_h)^{W/A'(ρ_h)}`; at c = −1, where R' = 0 at the horizon, the exponents
  are `1 ± W/A'(0)` and the ingoing one is `1 + W/A'(0)` (u ~ ρ^{W/A'}). Started at z = ρ − ρ_h = z₀ with the leading Frobenius
  term, integrated outward in the variable ln z. The ingoing solution is the one that dominates outward, so the start vector cannot be
  changed to select the other one (dev result below).
- **Infinity**: `u_x/u = −W − V̂/(2W)` at ρ_max, integrated inward (the decaying solution is the dominant one inward).
- **c = 0, second infinity**: the mirror of the above at ρ = −ρ_max.
- **Throat** (−1 < c ≤ 0): no condition. Both Frobenius solutions are analytic; the horizon solution is continued from ρ = −d to +d along the upper
  half circle |ρ| = d in the complex ρ-plane, with the ρ-form of the equation. The imaginary part of Y after the arc (arc_imag in the
  JSON) is the monodromy test: a logarithm at the exponent difference 3 would show as a nonzero value. [BKZ12] regularize the throat
  by an S-deformation (47)–(51) and use time-domain integration; not used here.

## 4. Counting method

For each W the mismatch `D(W) = Y_L Y_R,x − Y_L,x Y_R` at ρ_m (1.0, or ρ_h + 1 when ρ_h > 0.5) of the unit-normalized horizon-ingoing
solution and the decaying solution. A growing mode is a sign change of D(W) on W ∈ [0.01, 8] (units 1/b), on a log grid of nW
points, refined by Brent (xtol 1e-14). **Bound on the range searched: W ∈ [0.01, 8].** Each root's eigenfunction is integrated and its nodes in Y
counted (the ground state has none; a root with nodes would have a root above it). A pair of roots closer than the grid spacing would be
missed by sign changes; the node counts and the spectral check below are the guards. No argument-principle count is made.

**Independent check, S6.** A matrix eigenvalue problem by Chebyshev collocation on x ∈ [−X, X] with Dirichlet ends, u-form for c ≤ −1 and
Y-form for c > −1 (the Y form has the factor 1/ρ at the throat). It shares with the shooting code the background A, A' and the
coefficients, and nothing of the boundary conditions, the throat crossing, the matching or the root finding. Finds also complex
eigenvalues. S-A: N = 401, X = 45. S-B: N = 801, X = 90. Pass: the same number of positive real eigenvalues λ = W² (1e-3 < λ < 100) as
shooting, no complex eigenvalue with Re λ > 1e-3, and W within 1e-2 (S-A), 1e-4 (S-B, c ≤ −1) or 2e-2 (S-B, c > −1) of shooting's. The
looser throat values are the dev result that the Y-form collocation does not converge with N near the throat (Ellis: λ = 1.4027 at
N = 401, 1.4103 at N = 801, exact 1.39705).

## 5. Planted case, P1

c = 0 through the same code path. The reference is `notes/wormhole_largeD/w2_output.txt`, D = 4, crate (qd) column:
**W²a² = 1.39705243433350684047** (a = b = 1). Pass: exactly one growing mode, and |W² − reference| ≤ **1e-7 at R1, 1e-9 at R2**.
The tolerances were written when the code was written, after a first development script had reproduced the value to 2.8e-13 at
rtol 1e-12; they are 10³ to 10⁵ above that error and were not changed afterwards.
Control `--mutate=eps`: the kinetic sign flipped (ε = +1) in the master equation with the same background.

## 6. Members, resolutions, criteria

Members c (20): **−10, −3, −2, −1.5, −1.1, −1.01, −1.001, −1.0001, −1, −0.9999, −0.999, −0.99, −0.95, −0.9, −0.7, −0.5, −0.3, −0.2, −0.1, −0.01**,
and the planted c = 0. [BKZ12] shows explicitly: time-domain growth at c = −0.1, −0.2, −0.3 (Fig 7), −0.9, −0.95, −0.99 (Fig 8), −1.001 (Fig 5),
decay at c = −1 (Fig 5); effective potentials with a negative region at c = −1.01 (Fig 5), −1.5, −2, −3 (Fig 6). Their Conclusion 2: stable only at c = −1,
unstable for c ≠ −1. This list was fixed before the dev scans of the members except c = −0.95, added after them to cover Fig 8.

| setting | R1 | R2 |
|---|---|---|
| integrator | DOP853, rtol 1e-9 | DOP853, rtol 1e-12 |
| horizon start z₀ | 1e-9 | 1e-13 |
| ρ_max | max(150, 30/W) | max(300, 45/W) |
| throat arc radius d | min(0.3, ½\|ρ_h\|) | min(0.2, ½\|ρ_h\|) |
| W grid | 60 points | 150 points |

**Resolutions agree** when the number of growing modes is equal and every rate agrees to 1e-6 relative (R1 against R2).
**Verdict against [BKZ12]** (member by member): agrees when a growing mode exists exactly for c ≠ −1.
Rates are reported in units 1/b and in [BKZ12]'s units (m = 1/3, i.e. times 3m = K = −2c/π), and as W/κ.

## 7. Checks and controls

Every check can exit 1; `stability.py controls` runs each `--mutate=` and requires its target to fail. Targets below are what the development
runs showed (`dev/controls_dev1.log`, `dev/ctl_*.log`).

| check | what it tests |
|---|---|
| S1 | (3)–(6) and θθ on the closed forms of A, R, φ, V, sympy, residual 0 |
| S2 | the same at 40 digits, 5 members × 7 points, residual ≤ 1e-30 |
| S3 | A'(h) = 2(ρ₀ − h)/R² at the horizon, 40 digits |
| S4 | linearization in sympy: tt and ρρ after the master equation, δR = 0 gauge, (41), gauge map, all 0 |
| S5 | family coefficients against the generic master equation, 30 digits, ≤ 1e-25 |
| S6 | spectral count and values (Sec. 4) |
| S7 | c → −1: V̂ tends in x to the Pöschl–Teller well with ℓ(ℓ+1) = 2, whose ground state sech(κx) has W = κ = A'(ρ_h)/2; sympy, and the member c = −1.0001 against the well, ≤ 3e-3 |
| S8 | V̂ against (40), (41), 30 digits, ≤ 1e-25 |
| P1 | planted Ellis (Sec. 5) |
| R | R1 against R2 (Sec. 6) |
| V | verdict against [BKZ12] (Sec. 6) |

| `--mutate=` | what it does | target | dev outcome (before declaring) |
|---|---|---|---|
| `bg_V` | 3 sinψ cosψ → 2 sinψ cosψ in V | S1, S2 | S1 residuals 6mρ/b² (4), 3√2 m(ρ²−b²)/(2b³) (3); S2 6.5e1 |
| `bg_A` | 3m → 2m in A | S1, S2, S3 | S1 nonzero; S2 3.0e2; S3 no root in the bracket |
| `bg_kappa` | the printed (8), without the 2 | S3 | 0.60 |
| `master_p` | an extra R'/R · Y' in the master equation | S4, S5 | tt, ρρ residuals nonzero; S5 0.38 |
| `bkz41_sign` | sign of the V_φ term in (41) | S4 | (41) residual nonzero for ε = ∓1 |
| `family_q` | an extra 1/(A R²) in the Y coefficient | S5 | 0.81 |
| `veff_sign` | sign of the V_φ term in (40)–(41) numerics | S8 | 1.2e2 |
| `pt_ell` | 2 → 3 in the wall term of V̂ | S7 | residual of sech(κx) nonzero |
| `eps` | ε = +1 | P1 | c = 0: 3 growing modes (declared 1), lowest W² = 0.0091; c = −0.3: also 3, arc_imag 0.05 to 0.86 (monodromy) |
| `throat_wall` | independent sides, Dirichlet Y ~ ρ³ at the throat, as the singular potential would give | P1 | no growing mode (0) |
| `rmax` | ρ_max = 4 | P1 | \|ΔW²\| 4.7e-7 against 1e-7 (R1) |
| `hz_start` | horizon start z₀ = 0.05 | R | c = −0.3: \|ΔW\|/W 1.9e-4 against 1e-6 |
| `scan_range` | W ∈ [3, 8] | V | c = −0.3: 0 modes, [BKZ12] says unstable |
| `spec_sign` | sign of the potential in S6 | S6 | c = −1.5: 0 positive eigenvalues (shooting 1) |

A control that was **silent**: starting the horizon integration with the outgoing exponent (−W/A') gives the same eigenvalue (c = −0.3,
R1: W = 0.970078 against 0.970080, 2e-6), because the ingoing solution dominates outward and takes over from any start vector. No control is declared for the horizon
exponent; `hz_start` replaces it. The throat check is `eps`, `throat_wall` (count 1 → 0, the claim of [BKZ12] that the initial singular potential is positive
and "stable") and the monodromy column.

## 8. Runs of record, files

All run as `systemd-run --user --unit=nm-i212-<name> nice -n 10`, log and exit code in this folder; reruns are numbered, nothing is overwritten.
Unit names are in `units.txt`. Commands, from `notes/black_universe`:

```
stability.py check                          > check.log
stability.py planted                        > planted.log
stability.py count <c> --res=R1|R2 --out=results/member_<c>_<res>.json   (20 members × 2, three units)
stability.py report results                 > report.txt
stability.py spectral results               > spectral.log
stability.py controls                       > controls.log
```
`notes/black_universe/stability_output.txt` is these logs in that order, with a header naming the raw commit.

## Development history (before this README)

- `dev/scripts/core.py`, `shoot.py`, `t_ellis.py`: first numerics. Ellis W² = 1.3970524343332 (2.8e-13 from the reference).
- `dev/devscan_*.log`: scan of all members at rtol 1e-10, 70 log-spaced points on [0.01, 8]: one root for every c ≠ −1, none at c = −1;
  W(−1.0001) = 0.63658, W(−1.001) = 0.63627, κ(−1) = 2/π = 0.63662.
- `dev/check_dev*.log`, `dev/mut_check_dev1.log`, `dev/planted_dev1.log`, `dev/ctl_*.log`, `dev/controls_dev1.log`: the checks and every control (all 13 then declared fired).
- `dev/members/`: R1 of all 19 earlier members (one mode each for c ≠ −1, none at c = −1, all eigenfunctions without nodes); `dev/spectral_dev.log`: S6 on them (all pass).
- The `bg_A` run first crashed in S3 (a mutated horizon outside the root bracket); S3 now reports an infinite error instead (fixed before this README).

## Amendments

(none)
