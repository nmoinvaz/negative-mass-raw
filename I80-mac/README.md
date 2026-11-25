# I80-mac: the coordinator's review of #80's classification of shifts with det R₃ = 0 on an open set

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, sympy 1.14.0, mpmath 1.3.0, at nice 10 with at most 2
processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/80. Reviewed branch `wip/i80-det-classify` at af5f269 and raw
`I80-rpi5` at a945d08.

## Rerun of the runner's script

`python3 notes/warp/det_classify.py`, full, with its controls, from a detached worktree of af5f269 (`rerun/`). Expected,
as #80 reports: exit 1, with exactly `bessel_pert` and `conical_limit` failing and 19 of 19 controls firing.

## Independent check `ind80.py` (criteria written before its first run)

ind80 imports nothing from the repository. It builds D from #65's formula D(P, Q, Z, Y, h), which the coordinator's
`I79-mac/ind79.py` (H1) checked against its own Ricci routine for a generic b(t, x, ρ). Its Ricci routine is the
coordinator's, from `I77-mac`–`I79-mac`. Shared with #80: the formula for D, the reductions, the printed formulas (typed
here from `det_classify.md`), and the claims tested.

| id | criterion | kind |
|---|---|---|
| K0 | planted: the own Ricci routine finds Painlevé–Gullstrand Schwarzschild Ricci-flat | symbolic |
| K1 | with a = b_t − b b_x: P = a_x and Y = ½(b_x b_ρ − a_ρ) identically; for b(t, x) (b_ρ ≡ 0), h = Q = Z = Y = 0 and D ≡ 0 | symbolic |
| K2 | traveling: for b = B(x − vt, ρ), D(b) = D_static(B + v); Galilean: b(t, x + ct, ρ) + c has the same D | symbolic |
| K3 | planar static u(x), own Ricci of −dt² + (dx + u dt)² + dy² + dz²: R = (uu′)′ g₂ ⊕ 0; p = t − A(x), q = t + B(x) with A′ = 1/(1 − u), B′ = 1/(1 + u) give −(1 − u²) dp dq = g₂, R_pq = −Φ/2 with Φ = (uu′)′(1 − u²), and q − p = s(x) with s′ = 2/(1 − u²) | symbolic |
| K4 | u = c x + g(ρ): D = g′²(2c² + g′² − S)(2c² + g′² + S)/8, S = g″ + g′/ρ; with g = −ε ln ψ and ψ″ + ψ′/ρ + 2c²ψ = 0, S = ε(g′² + 2c²). At 8 points of u = c x − ε ln(α J₀(√2cρ) + β Y₀(√2cρ)) (own α, β, c ∈ {½, 3/2}, ε = ±1) and of c = 0 (ψ = C₁ + C₂ ln ρ), \|D\| < 1e-40 at 60 digits | symbolic + 60 digits |
| K5 | additive u = X(x) + R(ρ): D = h·E with E = (h + X′²)² − ((X + R)X″)² − Q², and E = Σ f_i g_i with f = (1, X′², X″², XX″², X′⁴ − X²X″²), g = (A² − B, 2A, −R², −2R, 1), A = R′²/2, B = (R″ + R′/ρ)²/4 | symbolic |
| K6 | conical u = F(η), η = x/ρ: ρ²(P, Q, Z, Y, h) = (−(F′² + FF″), −ηw/2, −w/2, −(ηF′² + Fw/2), η²F′²/2), w = F′ + ηF″. The part of 8ρ⁶D of degree 3 in (F′, F″) is 2Fw²((F² − 1)F″ − ηw); the part of total degree 4 in (F, F′, F″) is −w²[(η² + 1)(η² + 2)F′² + 2F(ηw + F″)]. With F = F_∞ + c η^{−2}, the leading coefficient of 8ρ⁶D in 1/η vanishes at c = −2F_∞ for every F_∞ | symbolic |
| K7 | re-solve of #80's observation: in F = F_∞ + Σ_{k=2..6} a_k η^{−k} on the branch a₂ = −2F_∞, solving N order by order leaves, at the third order after the leading one, the condition F_∞⁴(F_∞² + 7) = 0 | symbolic |
| K8 | far field: for u = u_∞ + εw(x, ρ), D has no ε⁰, ε¹, ε² terms, and its ε³ coefficient is −u_∞ Z²[(1 − u_∞²) w_xx + w_ρρ + w_ρ/ρ], Z = ½w_xρ | symbolic |
| K9 | the #158 remark: for a planar shift, R − λg at λ = K = (uu′)′ (static) is −K(dy² + dz²) in coordinates, so (+,+) iff K < 0 | symbolic |

Mutations, each must exit 1 with its target failing:

| mutation | change | target |
|---|---|---|
| `pg` | √(2M)/r for √(2M/r) | K0 |
| `ysign` | Y = ½(b_x b_ρ + a_ρ) | K1 |
| `travel` | D_static(B) without + v | K2 |
| `null` | A′ = 1/(1 + u) | K3 |
| `bessel` | J₀(cρ) for J₀(√2cρ) at the points | K4 |
| `addf` | f₄ = X X″ for X X″² | K5 |
| `cone3` | the typed degree-3 part with F²F″ for (F² − 1)F″ (the README's original) | K6 |
| `series` | the expected condition F_∞⁴(F_∞² + 8) = 0 | K7 |
| `far` | + u_∞ for −u_∞ | K8 |
| `msign` | expected +K(dy² + dz²) | K9 |

## Results

| file | what |
|---|---|
| `rerun/det_classify_full.*` | the rerun at af5f269: stdout, `/usr/bin/time -l`, exit code |
| `ind80_run1.py`, `.txt` | run 1: every criterion passes (`ind80.py` is the same version) |
| `ind80_mut_*.txt` | its 10 mutations |

**Rerun** (exit 1, 6 min 22 s, 90 MB peak). As #80 reports: `bessel_pert` and `conical_limit` fail, 13 of 15 checks
pass, and 19 of 19 controls fire on their targets only. The output equals rpi5's line for line apart from the timings
and the Python version.

**ind80 run 1** (exit 0, 3 s):

| criterion | run 1 |
|---|---|
| K0 | Painlevé–Gullstrand Ricci-flat |
| K1 | P = a_x and Y = ½(b_x b_ρ − a_ρ); planar h = Q = Z = Y = 0 and D = 0 |
| K2 | traveling D(B(x − vt, ρ)) = D_static(B + v); Galilean covariance |
| K3 | R = (uu′)′g₂ ⊕ 0; −(1 − u²) dp dq = g₂; R_pq = −Φ/2; s′ = 2/(1 − u²) |
| K4 | the factorization of D for u = cx + g(ρ); the Bessel reduction for ε = ±1; largest \|D\| at 8 own points 4.4e-60 |
| K5 | D = hE and E = Σ f_i g_i |
| K6 | the conical entries; the parts of degree 3 and 4 as printed, lower parts 0; leading coefficient at η⁻⁸ is −64c³(c + 2F_∞) |
| K7 | on the branch a₂ = −2F_∞: η⁻⁹ gives a₃ = 0, η⁻¹⁰ gives −512 F_∞⁴(F_∞² + 7) = 0 |
| K8 | far field: ε⁰, ε¹, ε² vanish; the ε³ coefficient as printed |
| K9 | R − Kg = −K(dy² + dz²) for a planar static shift, so (+,+) iff K < 0 |

Re-solve: K7, #80's series observation, by its own order-by-order solve.

Two findings:
- K7 puts the condition F_∞⁴(F_∞² + 7) = 0 at η⁻¹⁰, the *second* order after the leading η⁻⁸. det_classify.md §6
  says the third.
- K9 has the sign that #78's Lemma S needs: M = −K(dy² + dz²). det_classify.md §12's remark for #158 says
  M = K(dy² + dz²).

| mutation | exit | failed | target met |
|---|---|---|---|
| `pg` | 1 | K0 | yes |
| `ysign` | 1 | K1 | yes |
| `travel` | 1 | K2 | yes |
| `null` | 1 | K3 | yes |
| `bessel` | 1 | K4 | yes |
| `addf` | 1 | K5 | yes |
| `cone3` | 1 | K6 | yes |
| `series` | 1 | K7 | yes |
| `far` | 1 | K8 | yes |
| `msign` | 1 | K9 | yes |
