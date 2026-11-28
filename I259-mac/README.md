# I259-mac: criteria, development runs and runs of record for #259, the static coefficient c1 of the c = -1 black universe's horizon data

Machine: the coordinator's Mac (Apple M5), runner `negative-mass-mac-i259`, worktree `~/Source/negative-mass-i259` on `wip/i259-static-c1`, at most 2 processes, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/259. Script: `notes/black_universe/static_c1.py` (imports `horizon_sector.py`, `full_slice.py`, `linear.py` read-only).
Python: `~/Source/negative-mass/.venv/bin/python`. Written before the runs of record (`runs/`); the development runs are in `dev/` (probes `p1`–`p9`, logs `d1`–`d5`).

## Question

#248 found the horizon law δr = c1 + c2 V on H+ and left c1 = Y(S) as "the static sector", with the data classes A0 and A1L at c1 ≠ 0. #258 found a first integral Θ of the
sum constraint on the slice V + U = 0 (gauge δF = δF_N = 0), with Θ = −c1 at S and Θ(∞) = −δM_ADM/κ, so c1 = δM_ADM/κ. This issue: put #248's classes through Θ, identify the
static perturbation c1 belongs to, and give c1 as a functional of slice data.

## Method

1. **Θ_gen.** Θ is extended to δF ≠ 0 as Θ_gen = a δr + μ δr' + c δφ + μ s r_Π δF (a, μ, c as in #258; r_Π = dr/dΠ). It is conserved because Θ' = −μ[E(1/r − 𝒱r) δF + s r_Π δF']
   on solutions of the sum constraint and (μ s r_Π)' = μ E(1/r − 𝒱 r) is a background identity (T1). It vanishes on exact pure gauge (T3), so it is gauge invariant.
2. **Exterior in ρ.** For δφ = δF = 0 beyond a cut the constraint is δr_xx + p δr_x + q δr = 0, x = ∫dρ/A, p = −A'/2 + Aρ/R², q = −(A/2)(A'' + ρA'/R²) (T2 against the
   chart's P, Q). R (δr_x − A' δr/2) = κΘ is a first integral (S1, sympy), δr = √A [C + κΘ ∫dρ/(R A^{3/2})], and δm = c_b δr − κΘ ρ/R with c_b = 1/(2ρ²) + O(ρ⁻³) (S2).
   So δM_ADM = lim δm = −κΘ, and it is read at ρ = 1e8 from the ODE (the closed form is the cross-check, T2). #258's 0.2% at ρ = 16 was the 1/ρ convergence of the finite-ρ reading.
3. **Cut extension.** A datum on [s_L, s_R] is made a full-slice datum by setting δφ = δF = 0 beyond a cut s_c. H then has a jump δr'(outer) − δr'(inner) = ε r s φ_Π δφ + s r_Π δF at s_c
   (from the δ in δφ', δF'); Θ_gen is continuous across it. The mutation `jump_off` drops the jump.
4. **Exact static mode.** The exact solution r = √L R, F = A + 1/L − 1, φ unchanged (#269, N6; same potential) is written in the Kruskal chart at fixed Π, d/dL at L = 1:
   δρ = ∂_L ρ_L(Π) =: q solves 2κΠ q' = A'(ρ) q − 1 − κ̂ A(ρ), κ̂ = κ'/κ = A''(0)/A'(0)² = −π²/8, q(0) = 1/A'(0); δr = R/2 + (ρ/R) q, δφ = √2 q/R², δF = κ̂ − dq/dρ.
   Exact: c1 = δr(S) = 1/2 per unit δL, c2 = 0, M_ADM(L) = 2 L^{3/2}/(3π) so δM_ADM = 1/π and κ c1 = 1/π. The chart's ρ(Π) is matched by a series at |Π| ≤ 0.03 (20 terms) and an ODE outside.
5. **Evolved classes.** `horizon_sector.KSetup` (#248's Kruskal solver, rectangle V ∈ [−0.05, 3], U ∈ [−2, 0.06], h = 0.01 … 0.00125) for A0, A1R, A1L (c1 ≠ 0) and L, G, R (c1 = 0).
   The slice V + U = 0 is read at s = −0.03 … 1.9 (4th-order difference along the slice for δr'), Θ_gen at each s, and the cut extensions at s_c = 1.0, 1.9, −0.03.
6. **#232's solver** (`linear.py`, c = −1, P = 7, h = 0.01, 0.005, 0.0025). It has no slice through S, so c1 is read by the horizon law extended to V = 0: c1 = δr(p0, H+) − e^{b p0} c2, with c2 the
   slice functional of #248 (c2 = ½(∂_T δr + ∂_N δr)/(b e^{b p0})), at the slices p + σ = const crossing H+ at p0 = 0.5, 1, 2, 4, 6.

Error bars are comparisons of two computations, not uncertainties: Richardson means (4 v(h/2) − v(h))/3 of the two finest steps, "relative" is divided by |c1|, and no bar is a fit spread.

## Planted cases (run before the real classes; known answers)

| case | known answer | where |
|---|---|---|
| exact pure gauge L_ξ(member), δF ≠ 0, c = −1, −1.5, both signs of s | Θ_gen = 0 (c1 = 0 and gauge) | T3 |
| exact static mode r = √L R | c1 = 1/2, c2 = 0, δM = 1/π (mpmath d/dL of lim m_L), κ c1 = δM | T4 |
| the same mode as ray data through the Kruskal solver (amplitude δL = 2e-3) | c1 = 1e-3, c2 = 0, δM = 2e-3/π, pointwise error falling by 4 | T8 |
| #258's compact datum G | Θ = 0 | T5 |
| #258's homogeneous starts with mass (δM = 1e-4, 2e-4 of #258) | κ c1 = δm(ρ → ∞) (#258 had 0.2% at ρ = 16) | T5 |

The mode's δF is not zero in this gauge (δF → κ̂ at S) and its δφ falls only as 1/ρ, so it exercises the δF term of Θ_gen and a tail #258's compact data do not have.

## Criteria (declared before the runs of record)

Bars from the issue are marked I. Bars of this runner's own checks were set from the development runs `d1`, `d2`, `d3` (logs in `dev/logs`), which are named where they moved a bar.

| id | check | bar | issue |
|---|---|---|---|
| S1 | sympy: d/dρ[R (A δr' − A' δr/2)] = 0 on the x-form of H with q from (vρ) and R² A'' = 2(A − 1) | residual 0 | |
| S2 | sympy: c_b = 1/(2ρ²) + O(ρ⁻³), R − ρ = 1/(2ρ) + O(ρ⁻³) | coefficients exact | |
| S3 | sympy: V_c/c has no c (the potential of the member c is proportional to c) | d(V/c)/dc = 0 | I (3) |
| S4 | sympy: μ s r_Π = ρA/(2κ) and (μ s r_Π)' = μE(1/r − 𝒱r) with 𝒱R² = 1 − (ρA)' (the identity of T1) | residual 0 | |
| T1 | (μ s r_Π)' = μ E (1/r − 𝒱 r), c = −1, −1.5, 8 points | ≤ 1e-8 relative (finite differences) | |
| T2 | ρ-form p, q, Θ, δm against the chart's s-form; closed-form tail against the ODE; Θ conserved on [ρ(1.05), 1e8] | ≤ 1e-9 each | |
| T3 | Θ_gen on exact pure gauge, δF ≠ 0 | ≤ 1e-8 of the largest term (jets by differences with step 1e-3: d2 gave 1.1e-9, so 1e-9 was too tight) | |
| T4 | exact static mode: c1 = 1/2; Θ_gen = −c1 at 14 s ∈ [0.05, 1e6]; δm of the slice code against d_L m at fixed Π; δM(ρ = 1e8) against mpmath; κ c1 = δM; seven cut extensions | 1e-12; 1e-9; 1e-9; 1e-6; 1e-6; 1e-6 | I (3) |
| T5 | compact datum G: |Θ_gen| at 22 points; homogeneous mass starts: κ c1 against δm(1e8) | ≤ 1e-12 (absolute); ≤ 1e-6 | I (1) |
| T6 | A0, A1R, A1L, Richardson of h = 0.0025, 0.00125: Θ_gen(s) = −c1 at s = −0.03 … 1.9, δr(S) = c1; δM of the cut extensions = κ c1; c1 against #248's table | ≤ 1e-6 relative each | I (1) |
| T7 | L, G, R (c1 = 0): max |Θ_gen(s)| after Richardson; raw values fall by 4 ± 1 per halving | ≤ 1e-12 (absolute); ratios in [3, 5] at the last two steps | I (1) |
| T8 | exact mode through the Kruskal solver: error/scale at h = 0.00125 and last ratio; c1 of the fit, δr(S), the functional c1 = δr − V0 c2 (V0 = 0.5, 1), Θ_gen(s), δM of the cuts, |c2| | ≤ 1e-3 (d1 gave 5e-4; the error grows with V and is largest at V = 3, U = 0.05) and 4.0 ± 0.3; ≤ 1e-6 relative; |c2| ≤ 1e-6 c1 | I (3) |
| T9 | #232's solver: c1 functional at p0 = 0.5, 1, 2, 4, 6 against the horizon fit (A0, A1R, A1L); |c1| for L, R | ≤ 1e-6 relative to |c1|; ≤ 1e-9 | I (2) |
| T10 | first law along the exact family at finite L (mpmath, 40 digits): dM/dL = κ_ξ (dA/dL)/(8π), A = 4π L R(ρ_h)², κ_ξ = √L A'(ρ_h)/2, L = 0.5 … 4 | ratio = 1 to 1e-12 | I (3) |

Printed, not criteria: the slice functional of the Kruskal solver at V0 = 0.5, 1 for A0, A1R, A1L (T6 line). Its error is V0 Δc2, and for A1R, where c2/c1 = 20, d3 gave 1.2e-6 relative to c1;
it was added as a criterion in a first draft of T6 and removed before the runs of record because the issue asks for the functional on #232's solutions (T9), not on #248's.

The issue's "Θ = 0 to 1e-12" for a class with c1 = 0 is T5 (compact datum, ODE path) and T7 (evolved L, G, R, which d3 gave at 2e-13, 3e-13, 3e-13 after Richardson; #248's c1 of G, −4.8e-12, is a horizon-fit value).

## Mutations

`static_c1.py check|derive --mutate=NAME`. Each is a change of the code under test. The declared fired sets and the effects were computed in the development runs `d4` (all 16) and `d5` (`dm_noT`, `s_q`, `s_pot`
again, after the fixes named below), logs `dev/logs/d4_mut_*.log`, `d5_mut_*.log`, before the runs of record. In the runs of record the fired sets must equal these (`static_c1.py mutations`).

| name | change | target | declared fired set | effect in the development run |
|---|---|---|---|---|
| s_q | q → −q in the symbolic x-form | S1 | S1 | residual ≠ 0 |
| s_pot | V + 1/R² in S1 and S4; K = −2c/π + c² in S3 | S1, S3, S4 | S1 S3 S4 | residuals ≠ 0, d(V/c)/dc ≠ 0 |
| th_noF | drop μ s r_Π δF from Θ_gen | T3 | T3 T4 T6 T7 T8 | T3 9.8e-1 and 9.7e-1 of the largest term; T4 Θ 4.7e1; T6 Θ 1.2, 2.7, 4.7e-1; T7 Θ 6.6e-6, 1.6e-4; T8 Θ 2.6 |
| th_nophi | drop c δφ | T3 | T3 T4 T5 T6 T7 T8 | T3 6.1e-1, 2.9e-1; T4 8.5e-1; T5 \|Θ\| 3.1e-4 (the compact datum, where δF = 0); T6 2.8e-1 …; T7 9.7e-5 … |
| th_asign | a → −a in Θ_gen | T3 | T3 T4 T5 T6 T7 T8 | T3 6.0e-1, 1.5; T4 2.0; T5 2.5e-4; T6 3.9, 8.6, 2.7 |
| dm_noT | drop the −ρ δr_x term of δm (ρ-form) and the (δF, δr′) group of the s-form | T2, T4 | T2 T4 T5 T6 T8 | T2 δm 4.1; T4 δm 4.9e-1, cuts 1.0; T5 δm(1e8) −3.3e-12 against κ c₁ = 1.0e-4; T6 δM 1.0 |
| kappa_off | κ → 1.01 κ in κ c₁ | T4 | T4 T5 T6 | T4 1.0e-2, cuts 9.9e-3; T5 1.0e-2; T6 δM 9.9e-3 |
| jump_off | no jump of δr′ at the cut | T4, T6 | T4 T6 T8 | T4 cuts 2.3e1; T6 δM 1.5, 3.0; T8 δM 3.1 |
| xform_p | drop Aρ/R² from p of the ρ-form | T2 | T2 T4 T5 T6 T8 | T2 p 8.1e1, closed form 1.1e8; T5 δm(1e8) 6.0e3 |
| xform_q | q → −q in the ρ-form | T2 | T2 T4 T5 T6 T8 | T2 q 2.0, closed form 3.5; T5 3.8 |
| mode_khat | κ̂ = 0 in the exact mode | T4 | T4 T8 | T4 Θ 1.5e-3, δm 4.4e-5; T8 error/scale 8.9e-1 … 9.2e-1, ratio 1.03 |
| mode_dF0 | δF = 0 in the exact mode | T4 | T4 T8 | T4 Θ 4.7e1, δm 4.6e1; T8 error/scale 15.4 … 15.5 |
| fn_c1_noV | c₁ = δr − c₂ (no V₀) | T9 | T9 | T9 1.8 … 7.0e2 relative |
| fn_c1_aT | c₂ = tangential half | T9 | T8 T9 | T9 1.8e-5 … 0.38; T8 functional 3.9 |
| fn_c1_sign | c₁ = δr + V₀ c₂ | T9 | T9 | T9 9.9 … 1.4e3 |
| law_norm | κ_ξ without √L | T10 | T10 | ratios 1.414, 1.054, 1.000, 0.816, 0.707, 0.500 |

Known blind spots, kept: `fn_c1_noV` and `fn_c1_sign` do not fire T8 because c₂ = 0 for the exact mode, so the V₀ term of the functional is not tested there (T9 tests it, where c₂ ≠ 0). `th_noF` does not fire T5
(δF = 0 on the compact datum) and `jump_off` does not fire T5 (no sources at the cut).

Two fixes came from the mutations, before the runs of record: `dm_noT` first did not fire T5, because T5 divided by δM, which the mutation makes negative, so the error was a negative number below the bar (the denominator is now |δM|);
and `s_pot` did not fire S4 because S4 did not exist (it was added, with the symbolic form of T1).

## What is shared and what is independent

- T3 (exact pure gauge) and T4 (exact static mode) are exact solutions of the field equations (#261/#262's gauge, #269's family); the mode shares with the code under test the chart's ρ(Π) (through ρ₁ and the table), the closed forms
  of A, R and the slice code's dm and Θ. Its reference values (δM = 1/π, the first law at finite L) are mpmath computations from A(ρ) alone.
- T2's ρ-form and the exterior reading at ρ = 1e8 use closed forms of A, A′, A″ (series in 1/ρ for ρ ≥ 6) and no chart table; the closed-form tail and the ODE are two methods for the same solution.
- S1–S4 are sympy, no code shared.
- T6–T8 use #248's solver and its slice functional; T9 uses #232's solver; T5 uses #258's constraint ODEs. The solvers are the code under test only through their data; the quantities read from them (Θ_gen, δM from the cut) are computed here.

## Files

`README.md` (this), `run_mut.sh` (one stream of mutation runs), `dev/` (`p1`–`p9`, `mut_summary.py`, `check_quotes.py`, `logs/`), `runs/` (runs of record, written after this file).
