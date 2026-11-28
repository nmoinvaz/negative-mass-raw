# I278-mac: the causal structure of #269's exact family (horizons, cone v = v*, conformal diagrams), its checks, mutations and development logs

Machine: the coordinator's Mac (Apple M5, macOS, shared with other agents, load 30 to 60), `~/Source/negative-mass/.venv/bin/python` (sympy 1.14.0, mpmath 1.3.0, numpy, scipy), `nice -n 10`, one thread
per process, at most two processes. Code: `notes/black_universe/family_causal.py` in worktree `~/Source/negative-mass-i278`, branch `wip/i278-causal-structure` on main 1d28bdb; the checks and the declared
mutation sets below are those of branch commit 90a9277. Issue: https://github.com/nmoinvaz/negative-mass/issues/278 (depends on #269). Written 2026-11-27 before the runs of record. Every development log is in
`dev/` (scripts `dev*.py`, `fam.py`, `devstream.sh`; logs `dev*_run<N>.txt`, `dev_base_*`, `devmut_*`, `m_*_run<N>.log`; frozen copies of the script `family_causal_frozen_dev*.py`).

## Question

#269 found the exact family `ds² = −F dv² + 2 dv dρ + r² dΩ²`, `r = λ(v)R(ρ)`, `F = A − 2ρλ′/λ + 1/λ² − 1`, `λ² = 1 + s`, `s = βe^{Kv}`, `φ = √2 arctan ρ`, `K = −2c/π`, for every member c
(b = 1, L = 1). What is its causal structure, for both signs of β, at c = −1 and c = −3/2: the apparent horizons (∇r)² = 0, the event horizon if there is one, the null hypersurface v = v*, the line ρ = −1/K,
the ends ρ → ±∞, conformal diagrams, each claim of a diagram tested by a null-ray integration with a control?

## Definitions and conventions (fixed before the runs)

- **Chart and members.** (v, ρ) ∈ ℝ × ℝ; v = const are the ingoing null rays (ρ is affine on them, S6); the outgoing rays solve dρ/dv = F/2. Time orientation: −∂_ρ is future-directed. β = ±1 (the family is
  invariant under v → v + δ, β → βe^{Kδ}, so only the sign of β matters: N8); β < 0 has v* = −ln|β|/K = 0. Members c = −1 (ρ_h = 0, K = 2/π) and c = −3/2 (ρ_h = 0.3396, K = 3/π). L = 1 only.
- **Domain of the diagrams.** The future of the ingoing null cone v = v₀ (v₀ = −7 in the figure, −10 in the ray tests), with the outgoing rays labeled by where they cross it. Any monotone relabeling is a conformal
  diagram; the scale of the label in the figure (log about the reference ray) carries no claim.
- **Null expansions.** n = −∂_ρ, ℓ = ∂_v + (F/2)∂_ρ, g(ℓ, n) = −1: n(r) = −r_ρ, ℓ(r) = r_v + F r_ρ/2, (∇r)² = −2 ℓ(r) n(r). Trapped: both negative; anti-trapped: both positive.
- **Apparent horizons.** The curves ℓ(r) = 0 (AH) and n(r) = 0 (the throat ρ = 0). The AH are the roots of (∇r)² other than ρ = 0.
- **Event horizon (β < 0).** The boundary of the causal past of the set of outgoing rays that end at ρ = +∞ on the cone v = v*: the separatrix between rays ending with 1 + Kρ → +∞ and rays ending at ρ = −∞
  (at v < v*, or on the cone with 1 + Kρ → −∞). The usual definition (past of I⁺) does not apply: on the AF side the rays reach v* at finite r. For β > 0 the same definition is tested: it is empty if no ray ends at ρ = +∞.
- **Rays.** Integrated as w = arctan ρ, DOP853, rtol 1e-11, in float64; the ray into P* = (v*, −1/K) by integrating backward from τ = v* − v = 1e-7 along 1 + Kρ = −(K A(−1/K)/3)τ (the C = 0 ray).

## What development found, in the order it happened

1. `dev1_symbolic.py` (run 1): (∇r)² of the metric equals (ρ/R²)[ρA + sR²A′/2] symbolically, with R²A′ = 2K + 2ρ(A − 1), and ℓ(r) = P/(2Rλ). Then s_AH(ρ) = −2ρA/(R²A′), A′ = 2K(1 − ρ arccot ρ) > 0.
2. `dev2_ah.py`: A′ has no zero for c = −1, −3/2; s_AH < 0 where ρA > 0, so for β > 0 there is no AH at c = −1 and a lens in (0, ρ_h) at c = −3/2.
3. `dev3_rays.py`: first with events on ρ at ±1e8, which crashed in scipy's event root finder; the variable w = arctan ρ replaced it (run 2). β > 0: every ray falls to ρ = −∞. β < 0: the rays split at one separatrix.
4. `dev4_eh.py`: the first run hung, because 1 + s = 0 at v* = 0 loses its digits; `λ² = −expm1(K(v − v*))` replaced it. The ray into P* (C = 0) equals the forward-bisection separatrix to 9e-11 and 2e-10 at v₀ = −10.
5. First full `check` run: N1 failed (linear grid too coarse for ρ < 0 near 0), N2 failed (the finite difference of r along a ray with step 1e-5 gave 1.5e-3 against the bar 1e-3; the step became 1e-6, the bar did not move),
   N4 failed (9e-3). The cause of N4, found with `dev5_debug.py` and `dev6_left.py`: **rays slightly left of the event horizon also reach v***, at ρ → −∞ with finite r, and my classifier took them for the AF side.
   Classifying by the sign of ρ at τ = 1e-12 then still lost rays with |C| < 1e-6 (1.5e-8); the sign of y = 1 + Kρ is the classifier (the sign of C).
6. `dev7_crit.py`: a critical offset d_crit separates the left rays that reach the cone from those that fall; at d_crit the fall time tends to v* and r_* to infinity: the point Q (N11). `dev8_vertex.py`: x/√τ converges, so every
   curve of finite ρ converges to the vertex P* as v → v* (the figure draws them to v* − 2e-3).
7. Added after the findings above: N11 (the left sheet), N12 (the expansion lens, s_max), the Ellis c = 0 planted truth in N0 (exact rays 1 − βρ = C(1 + βv)^{−1/2}), I⁺ monotonicity in N3 and N11, the line ρ = −1/K in S4 and N9.
8. First mutation round (`m_*_run1.log`, `_run2.log`): `rate_ray` (K·1.001 in the integrator only) fired nothing, because nothing compared the integrator with the metric; it became K·1.01 and N2 integrates with the mutated
   family against the metric jets of the explicit family. `ah_coef` and `ah_sign` crashed N1 and N4 instead of failing; missing roots are now failures. Second round `_run3`, `_run4`, `_run5`: the fired sets below.
   Nothing in the checks of record has been run before this README except these development runs.

## Declared before the runs of record

### Acceptance (issue #278), and the checks that decide each

| acceptance | checks |
|---|---|
| the apparent horizon (∇r)² = 0 in closed form, against a numerical root to 1e-12 | S1–S4 (symbolic), N1 (root of (∇r)² from the metric components against the root of s_AH(ρ) = s, 20 roots, 1e-12), N5, N12 |
| each claim of the diagram tested by a null-ray integration | N0 (planted: static horizons and the Ellis family, exact rays), N2 (regions), N3 (β > 0: no ray reaches ρ = +∞; I⁺), N4 (event horizon), N6 (P*), N7 (throat, AH character), N10 (affine length of I⁺), N11 (left sheet, Q), N12 (lens) |
| a control: a ray started on the wrong side of a claimed horizon reaches the other end | N4: the throat, the static horizon and both AH branches are each claimed as the horizon at three start times; the ray on one side reaches the wrong end for each (declared: they all fail, the event horizon alone separates); mutation `eh_shift` displaces the claimed event horizon and N4 fires |

### Checks (S: sympy, symbolic for symbolic c and β; N: ray integrations in float64 and mpmath at 40 digits; a check fails when its residual is nonzero symbolically or above its bar)

| id | what | bar |
|---|---|---|
| S0 | static member (β = 0): (∇r)² = ρ²A/R² (planted truth) | symbolic zero |
| S1 | family: (∇r)² = (ρ/R²)[ρA + sR²A′/2] from the metric | symbolic zero |
| S2 | R²A′ = 2K + 2ρ(A − 1), A′ = 2K(1 − ρ arccot ρ) > 0 (by arctan x < x) | symbolic zero |
| S3 | ℓ(r) = P/(2Rλ), n(r) = −λρ/R, (∇r)² = −2ℓ(r)n(r) | symbolic zero |
| S4 | P = (R²A′/2)(s − s_AH(ρ)); F(v, 0) = c + 1/λ²; F(v, −1/K) = A(−1/K) | symbolic zero |
| S5 | A → 1: the (v, ρ) part is exactly −dT² + 2 dT dr, T = ∫dv/λ, r = λρ | symbolic zero |
| S6 | Γ^a_{ρρ} = 0 for any F: ρ is affine on v = const | symbolic zero |
| N0 | planted: β = 0, c = −1, −3/2, −3/10: separatrix of the ray code = ρ_h; Ellis c = 0, β = ±1: rays = exact, β = −1 separatrix = −1 | 1e-9 |
| N1 | root of (∇r)² from the metric against the closed-form root of s_AH(ρ) = s: c = −1, −3/2; β = −1 both branches at four s; β = 1, c = −3/2 both roots; and (∇r)² = 0 on ρ = 0 | 1e-12; 1e-30 |
| N2 | labels: sign n(r), sign ℓ(r) from the metric jets = closed-form labels; ℓ(r) = P/(2Rλ); dr/dv along an integrated ray = ℓ(r); 264 points | signs equal; 1e-9; 1e-3 |
| N3 | β = +1: 72 rays (v₀ = −10 … 2, ρ₀ = −30 … 1e8) all fall to ρ = −∞ with r > 1e6, v_b rises with ρ₀; late F = −KR² arccot ρ < 0 | as stated; 1e-9 |
| N4 | β = −1: ray into P* = forward bisection (v₀ = −10, −3); at EH ± 1e-3 (v₀ = −10, −5, −2) escape / fall; controls: throat, ρ_h, AH⁺, AH⁻ do not separate | 1e-8; as stated |
| N5 | β = −1: ρ_AH⁻ < ρ_EH < ρ_AH⁺ at 55 values of v from v* − 1e-3 to −10 | strict |
| N6 | β = −1: (ρ_EH + 1/K)/τ → −A(−1/K)/3, r/√τ → √K R(−1/K) at τ = 1e-5; r_*(d) for d = 1e-3 … 1e-7 falls strictly, r_*(1e-7) < 0.1 r_*(1e-4) | 1e-3; 2e-3; as stated |
| N7 | rays on ρ = 0 move at (c + 1/λ²)/2; null at λ² = −1/c; the ray from an AH point ends on the side the closed-form slope predicts (β = −1 both branches at v = −6, −2, −0.5; β = 1, c = −3/2 both lens roots at v = −6, −4) | 1%; 1e-6; 10% |
| N8 | the ray into P* gives the same ρ_EH at the same s for |β| = 1 and 0.3 | 1e-8 |
| N9 | information: Kretschmann on the EH, on ρ = −1/K and off both near P*; the line ρ = −1/K | not a check |
| N10 | outgoing rays into ρ = −∞: λ_aff(−1e6)/λ_aff(−1e3) = 1e3 | 2% |
| N11 | β = −1: d_crit; r_*(d_crit(1 − ε)) rises (> 100 at ε = 1e-3), τ_fall(d_crit(1 + ε)) falls (< 1e-6); τ_fall monotone over 8 offsets | as stated |
| N12 | β = +1: c = −1 ℓ(r) > 0 for every ρ > 0 at 49 values of v; c = −3/2 trapped points at 0.995 s_max, none at 1.005 s_max; ρ < 0 anti-trapped | as stated |

### Mutations: each with the checks it must fire (development runs `dev/m_*_run3.log`, `_run4`, `_run5`)

| name | what it changes | fires |
|---|---|---|
| `ah_coef` | coefficient of the s term of (∇r)² and s_AH × 1.01 | S1 S4 N1 N12 |
| `ah_sign` | sign of the s term and of s_AH | S1 S4 N1 N2 N4 N5 N7 N12 |
| `ell_sign` | sign of ℓ(r) in the labels | S3 N2 |
| `throat` | F(v, 0) = c − 1/λ² | S4 N7 |
| `eh_shift` | the claimed event horizon displaced by 5e-3 | N4 N6 N11 |
| `pstar` | the claimed end point P* at ρ = −1/(1.01K) | N4 N6 |
| `beta_sign` | the β > 0 claims run at β < 0 | N3 |
| `rate_ray` | the integrator's rate K × 1.01 (closed forms and metric jets unchanged) | N2 N6 |
| `hz_shift` | the claimed static horizon ρ_h + 0.01 | N0 |
| `inv_k` | the v-shift of the |β| comparison with K × 0.99 | N8 |
| `ellis` | the sign of β in F of the planted Ellis family | N0 |
| `aff_sign` | the affine-parameter integrand e^{−a} for e^{+a} | N10 |
| `kA` | the coefficient of ρ + R² arctan ρ in A × 1.01, against the rate K | S1 S2 S3 |
| `r_scale` | r = 1.01 R in the planted static member | S0 |
| `f2` | 2.02 for 2 in F of the large-ρ metric | S5 |
| `gpp` | a g_{ρρ} = 0.01 F term in the metric of the S6 check | S6 |

Every check S0–S6, N0–N8, N10–N12 appears in at least one fired set. N9 prints information only. The runs of record must reproduce each fired set exactly.

### Status words

S0–S6 *checked symbolically*; the sign of A′ is *proved* by hand (arctan x < x). N1 repeats S1's closed form against the metric at 40 digits (an independent evaluator of the same member); N2, N12 compare the
closed-form labels with the metric jets of `exact_mode.py`'s explicit family. N0, N3–N8, N10, N11 are ray integrations: *numerical evidence*. The unique ray into P* and its equality with the bisection separatrix
(N4) is *numerical evidence*; the local expansion y = −(K A(−1/K)/3)τ + O(τ²) at P* is the declared starting point of that ray and is tested by N4 and N6, not proved here. No sentence says a result is new.

### Not claimed

- Extendibility past v = v*, or what P* is as a point of a larger spacetime: only the chart's behavior is tested.
- L ≠ 1, other members, the nonlinear stability of the family, or anything for asymptotically flat data (#250).
- The event horizon of β < 0 under any other definition than the one above.
- Positions in the figure (the label is a log scale).

## Runs of record

(to be filled after the runs)
