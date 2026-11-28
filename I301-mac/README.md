# I301-mac: criteria, development runs and runs of record for #301, κ r_S c₁ = δM_ADM at the black universes c = −1.5, c = −0.3 and on Schwarzschild

Machine: the coordinator's Mac (Apple M5), runner `negative-mass-mac-i301`, worktree `~/Source/negative-mass-i301` on `wip/i301-c1-members`, at most 2 processes, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/301. Script: `notes/black_universe/static_c1_members.py` (imports `horizon_sector.py`, `full_slice.py`, `linear.py` read-only).
Python: `~/Source/negative-mass/.venv/bin/python`. Written before the runs of record (`runs/`); the development runs are in `dev/` (probes in the session scratchpad, logs `d1_*`).

## Question

#259 showed at c = −1 that c₁ = δr(S) is the coefficient of a static mass mode and that κ c₁ = δM_ADM (r_S = 1 there). #259's Θ_gen has a(0) = −r_S, so at a member with r_S ≠ 1
the first-law reading predicts κ r_S c₁ = δM_ADM. This issue: run #259's slice functional on the exact static family of #269 at c = −1.5 and c = −0.3 (r_S ≠ 1, R′(ρ_h) ≠ 0) and on
Schwarzschild (the mass family), and say what c₁ is when R′(ρ_h) ≠ 0 (#261).

Conventions (stated in the note): G = c = 1; r_S = R(ρ_h), the areal radius of the bifurcation surface S; κ = A′(ρ_h)/2 for the Killing field ∂_t with A → 1 at infinity (Schwarzschild: κ = 1/(4M));
δM_ADM is the Misner–Sharp mass at infinity (Schwarzschild r_S = 2M); the length unit is the throat radius of the Ellis profile. Perturbation parameters: δL of r = √L R (Ellis members), δr_S of
r_S → r_S (1 + ε) (Schwarzschild, r_S = 1). The chart of #248 has Π = 1 at ρ = 1 for every Ellis member.

## Method

1. **Exact modes through the slice code** (planted truth). Ellis members: r = √L R, F = A + 1/L − 1 (#269, N6), written in the Kruskal chart at fixed Π, d/dL at L = 1: q = ∂_L ρ_L(Π) solves
   A q′ = A′q − 1 − κ̂A (′ = d/dρ), regular at ρ_h with q(ρ_h) = 1/A′(ρ_h) iff κ̂ = A″(ρ_h)/A′(ρ_h)² (Taylor series about ρ_h from R²A″ = 2(A − 1), ODE beyond); δr = R/2 + R′q, δφ = √2 q/R²,
   δF = κ̂ − q′. Exact per unit δL: c₁ = R_h/2 + R′_h/(2κ) (the horizon moves by δρ_h = δL/(2κ)), δM_ADM = K/2 = −c/π, c₂ = 0. Schwarzschild: δr = r, δF = −2, δφ = 0 per unit δr_S; c₁ = 1, δM = 1/2.
   References are mpmath at 120 digits (derivative of √L R(ρ_h(L)) and of lim m_L at ρ = 1e20), independent of the chart.
2. **Θ_gen and the exterior.** Θ_gen = a δr + μ δr′ + c δφ + μ s r_Π δF is conserved on the slice V + U = 0 at every member (S2: (μ s r_Π)′ = μE(1/r − 𝒱r) from (θθ) for generic R, A) and
   a = −R A′/(2κ), so a(0) = −r_S and c₁ = −Θ_gen/r_S. Beyond a cut (δφ = δF = 0) the constraint is y_xx + p y_x + q y = 0, p = −A′/2 + A R′/R, q = −(A/2)(A″ + A′R′/R), y = δr, d/dx = A d/dρ;
   R(y_x − A′y/2) = κΘ is its first integral and δm = ½(1 − AR′²) y − R R′ y_x = c_b y − κΘ R′ with c_b = ½(1 − AR′² − RR′A′) = O(ρ⁻²), so δM_ADM = −κΘ and **κ r_S c₁ = δM_ADM**. The reading is the ODE
   solution to ρ = 1e8 (closed-form tail as the cross-check).
3. **Through the solver.** The exact modes as ray data (amplitude 2e-3) and #248's classes A0, A1R, A1L, G (amplitude 1e-3) through the Kruskal solver of `horizon_sector.py`, rectangle V ∈ [−0.05, 3], U ∈ [−2, 0.06],
   h = 0.005 … 0.000625 (Richardson of the last two): c₁ of the horizon fit, δr(S), Θ_gen at s = −0.03 … 1.9, and δM_ADM of the cut extensions at s = 1.0, 1.9, −0.03 read at ρ = 1e8.
4. **Gauge.** Exact pure gauge L_ξ(member) (δF ≠ 0): Θ_gen = 0, δr(S) = 0; c₂ shifts by −η(0) R′(ρ_h) G(0) (mpmath), c₁ does not.
5. **First law at finite L.** dM = κ_ξ dA/(8π) along each family, κ_ξ = √L A′(ρ_h(L))/2, A = 4π L R(ρ_h(L))², M the Misner–Sharp limit at ρ = 1e20 (120 digits), central differences.

Error bars are comparisons of two computations, not uncertainties: "relative" is divided by the exact value (classes: by max(|c₁|, 1e-5)), Richardson means (4 v(h/2) − v(h))/3 of the two finest steps.

## Planted cases (run before the real classes; known answers)

| case | known answer | where |
|---|---|---|
| c = −1 (R′(ρ_h) = 0, r_S = 1), #259's member | reproduces #259: c₁ = 1/2, δM = 1/π, #248's classes | T4, T7, T8 |
| exact family r = √L R at c = −1.5, −0.3; mass homothety of Schwarzschild | c₁ = R_h/2 + R′_h/(2κ), δM = −c/π (1/2), κ r_S c₁ = δM | T1, T4 |
| the same modes as ray data through the solver | pointwise error falls by 4; c₁, Θ_gen, δM as above | T7 |
| exact pure gauge L_ξ(member) | Θ_gen = 0, δr(S) = 0, c₂ = −η(0) R′_h G(0) | T6 |
| Schwarzschild 2M = 1 | r_S = 1: "wrong r_S" cannot fail there | T5 |

## Criteria (declared before the runs of record)

| id | what | bar |
|---|---|---|
| S1 | chart Q → ρ-form q; d/dρ[R(A y′ − A′y/2)] = 0 (Ellis generic A, Schwarzschild) | residual 0 |
| S2 | (μ s r_Π)′ = μE(1/r − 𝒱r) and a = −R A′/(2κ) for generic R, A | residual 0 |
| S3 | K constant on R²A″ = 2(A − 1); κ r_S c₁ = K/2; lim ρ(1 − A)/2 = K/3; Schwarzschild | residual 0 |
| T1 | ρ_h, κ, r_S against mpmath; c₁ closed form against d_L r_S(L); δM against −c/π; κ r_S c₁ = δM from the constants | 1e-12 |
| T2 | dM = κ_ξ dA/(8π) at L = 0.5 … 4 (c = −1.5, −0.3, −1) and Schwarzschild r_S = 0.5, 1, 2; M_MS against K L^{3/2}/3 | 1e-12 (issue) |
| T3 | ρ-form p, q against the chart's P, Q; a = −R A′/(2κ), a(1e-6) = −r_S; κΘ, δm in ρ against the s-form; closed-form tail against the ODE; κΘ conserved to ρ = 1e8 | 1e-8 |
| T4 | exact mode, slice code: c₁(S), Θ_gen = −r_S c₁ at 8–14 values of s, c₁ = −Θ_gen/r_S, δm against the exact; κ r_S c₁ = δM; 6–7 cut extensions at ρ = 1e8 | 1e-9; 1e-6 (issue) |
| T5 | r_S set to 1 fails at c = −1.5, −0.3 and Schwarzschild 2M = 2; holds at c = −1 and Schwarzschild 2M = 1 | fails by > 1e-3; holds to 1e-12 |
| T6 | pure gauge: Θ_gen = 0, δr(S) = 0, c₁ = 0; c₂ against −η(0) R′_h G(0) | 1e-8 of the largest term; 1e-14; 1e-12; 1e-8 |
| T7 | exact mode through the solver: error/scale, last two ratios; c₁ fit, δr(S), Θ_gen, δM of the cuts, κ r_S c₁ against δM | ≤ 5e-2, 4.0 ± 0.3; 1e-6 (issue) |
| T8 | classes A0, A1R, A1L, G through the solver: Θ_gen = −r_S c₁, δr(S) = c₁, κ r_S c₁ = δM of the cuts | 1e-6 of max(\|c₁\|, 1e-5) (issue) |

## Mutations (declared effects, computed in the development run d1 before the runs of record)

`static_c1_members.py check|derive --mutate=NAME`. Each is a change of the code under test; every check is in scope. The fired sets were computed in `dev/d1_*.log` (the script at 08789b2) and
are the `DECLARED` dictionary of the script; `static_c1_members.py mutations DIR PREFIX` compares stored logs with it. The runs of record must reproduce them (20 of 20).

| mutation | change | declared fired set | computed effect (d1) |
|---|---|---|---|
| `s_q` | sign of q in the symbolic ρ-form | S1 | residual ≠ 0 |
| `s_pot` | V + 1/R² in the (θθ) identity | S2 | residual ≠ 0 |
| `s_k` | K without the + ρ term | S3 | dK/dρ ≠ 0 |
| `rs_one` | r_S set to 1 in κ r_S c₁ | T1, T4, T7, T8 | κ r_S c₁ vs δM 5.3e-2 (c = −1.5), 2.7e-1 (c = −0.3), 0 at c = −1 and Schwarzschild; cut readings 5.6e-2, 3.6e-1 |
| `ctl_true` | the "wrong" arm of T5 uses the true r_S | T5 | the arm holds at c = −1.5, −0.3, 2M = 2 (T5 needs it to fail) |
| `c1_noshift` | closed-form c₁ without R′_h/(2κ) | T1 | c₁ = 0.528048 for 0.819501 at c = −1.5; κ r_S c₁ vs δM 3.6e-1 |
| `th_noF` | no μ s r_Π δF term in Θ_gen | T4, T6, T7, T8 | Θ_gen + r_S c₁ 3.9e+1, 3.8e+1, 4.9e+1, 5.3 on the exact mode |
| `th_nophi` | no c δφ term | T4, T6, T7, T8 | 8.5e-1, 4.5e-1, 3.4 (Ellis); 2.7e-15 at Schwarzschild (δφ = 0) |
| `th_asign` | sign of a | T3, T4, T6, T7, T8 | 2.0 (= 2 r_S c₁) at every member |
| `dm_noT` | no −R R′ y_x term in δm (s-form and ρ-form alike) | T4, T7, T8 | δm slice vs exact 4.8e-1, 3.3e-1, 8.0e-1; not T3 (both forms mutated alike) |
| `kappa_off` | κ → 1.01 κ in the comparisons | T1, T4, T5, T7, T8 | 1e-2 at every member (T5 needs the r_S = 1 arm to hold at c = −1) |
| `jump_off` | no jump of δr′ at the cut | T4, T7, T8 | cut readings off by 23, 22, 30, 5.3 relative |
| `xform_p` | p without A R′/R | T3, T4, T7, T8 | p vs chart 81, 59, 310, 5.3 |
| `xform_q` | sign of q | T3, T4, T7, T8 | q vs chart 2.0 |
| `rho_ellis` | Schwarzschild exterior with R = √(1 + ρ²) | T3, T4, T7, T8 | p 5.0, q 0.33 vs chart at Schwarzschild |
| `mode_khat` | κ̂ = 0 in the exact mode | T4, T7 | pointwise error 1.2–1.7, 13, 2.7 with ratios 0.95, 1.00, 1.83 (no convergence) |
| `mode_dF0` | δF = 0 in the exact mode | T4, T7 | error 15, 13, 1400, ratio 1.00 |
| `law_norm` | κ_ξ without √L | T2 | ratio 1.414 at L = 0.5 |
| `law_mass` | M ∝ L² for L^{3/2} | T2 | M_MS vs closed form ≠ 1 |
| `gauge_noRp` | expected c₂ without R′_h | T6 | −3.5e-2 for −1.13e-2 (c = −1.5), −2.0e-1 for +1.36e-1 (c = −0.3); not at c = −1 (c₂ = 0 either way) |

Blind spots kept: `dm_noT` does not fire T3 (the s-form and ρ-form δm share the mutation; T4 catches it against the exact); `mode_*` do not fire T8 (it does not use the mode);
`gauge_noRp` is silent at c = −1 and at Schwarzschild (R′_h = 0, 1: Schwarzschild's c₂ is only required to be nonzero).

## Changes made between the first development run and the runs of record

- T5: the Schwarzschild 2M = 2 arm first used c₁ = 2 per unit δM mixed with a per-unit-δr_S κ; fixed to c₁ = 1, δM = 1/2, κ = 1/4 (closed forms; the solver chart is fixed at r_S = 1).
- T3: the probe of a(0) = −r_S used s = 1e-4, where a = −r_S + O(s²) = 4e-8; moved to s = 1e-6 (bar 1e-8 unchanged).
- Schwarzschild: the chart's Newton start fails for Π ≳ 150 (NaN); the slice reads stop at s = 10 and the integration of H at s = 12.
- Step ladder h = 0.01 … 0.00125 of #259 became 0.005 … 0.000625: at c = −0.3 the chart has e^{−F} = 11 at S and the second-order constant is larger (error/scale 8.5e-2 at h = 0.00125, ratio 4.00); with
  Richardson of 0.00125, 0.000625 the c₁ readings are 9e-7 (exact mode) and ≤ 2.5e-7 (classes), inside the issue's 1e-6.
- T7 pointwise bar: 1e-3 (#259) → 5e-2, with both of the last two ratios 4.0 ± 0.3 as the convergence criterion (c = −0.3: 2.1e-2 at h = 0.000625, ratio 4.00; c = −1, −1.5, Schwarzschild: 1.2e-4, 1.6e-6, 9.6e-8).
  A plateau (a wrong mode) gives ratio 1: `mode_khat`, `mode_dF0`. The bars of the issue (1e-6, 1e-12) were not touched.
- T8: bars relative to max(|c₁|, 1e-5) so that a class with c₁ ≈ 0 (G: |c₁| ≈ 1e-12 from truncation) is held to the absolute 1e-11.
- First mutation chain A of d1 failed to start (a relative path to `run_mut.sh`); the eight logs were produced by a second launch with the same script.
