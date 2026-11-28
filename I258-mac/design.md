# I258-mac design: a compactly supported datum on a full slice of the c = −1 black universe (#258)

Runner `negative-mass-mac-i258` (coordinator's Mac), issue <https://github.com/nmoinvaz/negative-mass/issues/258>, worktree
`~/Source/negative-mass-i258` (`wip/i258-full-slice`). Stage 1: no code of record exists. Numbers marked *dev* come from
development probes (`probe/`, logs in `probe/logs/`), not runs of record. Bars and mutations below are declared before the runs of
record. Status words as in AGENTS.md. No sentence claims novelty.

## What the probes show (dev)

- Compact data exist on the full slice with c₂ ≠ 0. Datum G (amplitude 1e-3): c₁ = 1e-15, c₂(slice) = −6.653515e-4.
- The evolved horizon fit reaches the slice value at second order: Richardson of h = 0.005, 0.0025 gives a relative error 2.7e-8.
- Only two conditions on the data are non-trivial, neither is "δM_ADM = 0": first-order δM_ADM of compact data vanishes by itself.
- Data supported away from S on both sides still have c₂ ≠ 0 (1.4e-5, p6). That bears on the README's "includes data supported
  away from the horizon". Reported in stage 2, not fixed.

## 1. Slice and variables

```
 left exterior                         S                        right exterior
 ρ → ∞ ····· zero ····· [ support ] ···┼··· [ support ] ····· zero ····· ρ → ∞      slice T = 0:  V = s, U = −s
 s = −∞                            s = 0                               s = +∞         Π = s², ρ = ρ(Π) (chart of #248)

                  U ↑   future interior (VU > 0)
          V = 0    ╲ │ ╱   U = 0 : H⁺, V > 0   (c₂ fitted here)
                    ╲│╱
        ─────────────S─────────────→ V
                    ╱│╲
        evolved: triangle D⁺[0, V₁] (V₁ = 3, right half) and diamond D⁺[−0.5, 0.5] (both future horizons, interior)
```

- Perturbation U = (δr, δF, δφ), double-null chart `−2e^{−F} dV dU + r² dΩ²` of #248, ε = −1. On the slice T = ∂_V − ∂_U = d/ds
  (values), N = ∂_V + ∂_U (normal, ∂_t = κ s N). Background functions of Π: r′, F′, φ′ (d/dΠ), E = e^{−F}, potential 𝒱, 𝒱′.
- Free data: δφ(s) and δφ_N(s) = ∂_N δφ, C^∞ bumps with support ⊂ [−0.75, 0.75] (ρ ≤ 0.75 on both sides).
- Gauge: δF = δF_N = 0 on the slice (residual null reparametrizations used up). Solved for: δr(s) and n(s) = ∂_N δr.

## 2. The two linearized constraints on the slice

C_VV ± C_UU of #261's lemma (L1 form), reduced with the evolution equation for δr_VU (`linear.py` B0, Bp, Bm). Hand derivation;
checked below against exact pure-gauge solutions, not against the solver.

```
H (sum, 2nd order in δr):   δr'' + P δr' + Q δr = −[E 𝒱′ r δφ + ε r s φ′ δφ'] − [E (1/r − 𝒱 r) δF + s r′ δF']
M (difference, 1st order):  n' + s F′ n = −s r′ δF_N − ε r s φ′ δφ_N
P = sF′ + 2sr′/r,   Q = E𝒱 + E/r² − 2s²r′²/r² + ε s²φ′²,      ' = d/ds
```

- Homogeneous solutions: M has `n_h = e^{−F/2}` (≈ 1/s at large s, so ∂_t δr = κ s n_h → const: a velocity tail). H has two, u₁, u₂.
- Even and odd sectors decouple (the background is time symmetric on T = 0). H carries δr, δφ (even in t); M carries n, δφ_N.
- Slice functionals (gauge invariant at c = −1: g = ρR/√2 vanishes at S, R′ = 0 there):
  `c₁ = δr(0)`, `c₂ = ∂_V δr(S) = ½(δr'(0) + n(0))`, `c₂′ = ∂_U δr(S) = ½(n(0) − δr'(0))` (left future horizon).
- Mass perturbation (no δr_N in it): `δm = δr (½ − e^F s² r′²) − r e^F s r′ (s r′ δF + δr')`; `δM_ADM = lim_{s→∞} δm`.
- Parity P: (V, U) → (−V, −U), s → −s, an isometry of the background. H, M are P-covariant. The growing mode has Y odd, Y_N even.
  Data with δφ odd and δφ_N even need no condition below (dev: end vector 1e-17, and they carry all of c₂ of datum G). The P-even part of δφ
  and the P-odd part of δφ_N need C1 and C2, and after them contribute nothing to c₂ (dev: δr(0), δr'(0), n(0) all ≤ 4e-16, p23).

## 3. Conditions at the two ends

Left (declared): (δr, δr', n) = 0 at s = −1.05, outside the support. It fixes δM_L = 0 and removes both tails there.
Right (declared): integrate H, M across the support from the left. Beyond the support the solution is homogeneous. Require it to vanish:

| condition | what it removes | scalar condition on the data | probe fact (dev) |
|---|---|---|---|
| C1 | constant tail of Y = δr (δφ = 0 there), δm → 0 | end vector (δr, δr')(1.05) = 0 | end vectors of all compact data are parallel (second singular value 1.7e-14), so 1 condition, not 2 |
| C2 | velocity tail ∂_t δr → const | n(1.05) = 0 | 1 condition |

- The mass mode (δr ∼ ln ρ, δm → finite) is never excited by compact data: δm(3e4) = 9e-16 for datum G. Static solutions
  extremize M_ADM, so its first-order change vanishes. `δM_ADM = 0` is therefore an identity of the construction, tested as such.
- The conditions are met by two correction bumps with solved amplitudes: `δφ += k_m b(s/0.6)`, `δφ_N += k_o [b((s−0.3)/0.3) − b((s+0.3)/0.3)]`.
  `b(x) = e·exp(−1/(1−x²))` for |x| < 1, else 0 (peak 1). Both have support inside the declared one.
- Result: the solution (δr, n, δφ, δφ_N, δF = 0) is exactly zero outside the support, pure gauge in the trivial sense. A pure-gauge
  tail with δF = δF_N = 0 and δφ = 0 would need δr = 0, so the trivial gauge is the only one in this class.
- c₁ = δr(0) = 0 for every compact datum (≤ 1.4e-14 on G and X20, p10, p23): the translation mode makes ∫ u₂ S/W ds vanish. c₁ ≠ 0 needs
  δM_L ≠ 0: with δM_L = 1e-4, c₁ = 1.57e-4 (dev).

## 4. Evolution (Cauchy, diagonal march)

- Reuse `horizon_sector._cellK` (the cell of `linear.py`, Kruskal background of #248): N from S, E, W corners. Nodes (j, i) = (V/h, U/h).
- Layer 0: nodes (j, −j), values at s = jh. Layer 1: nodes (j, 1−j), the points (h/2)(1, 1) off the slice midpoint s = (j − ½)h:
  `U₁ = U + (h/2) U_N + (h²/8) U_NN`, `U_NN = U_TT + 4 (B0 U + Bp U_V + Bm U_U)`, `U_V = (U_T + U_N)/2`, `U_U = (U_N − U_T)/2`.
  U_T, U_TT from the ODEs and analytic bumps, U_N from n and δφ_N. Error O(h³) per node, O(h²) overall (dev ratios 4.0).
- Layers ℓ ≥ 2: node (j, ℓ − j) from layers ℓ − 2 and ℓ − 1. Right half: j ∈ [0, 3/h], i ≤ 0 (domain of dependence of the right half-slice,
  bounded by H⁺). Diamond: |s| ≤ 0.5 (Π ≥ −0.25, the interior ends at −0.37), both future horizons and the interior.
- Fits: δr_h = c₁ + c₂ V on U = 0 (all nodes, V ∈ [0, 3]); on V = 0 for c₂′. h = 0.01, 0.005, 0.0025, 0.00125, Richardson of consecutive pairs.
- The solution beyond s = 1.05 is set to zero exactly, not extrapolated. A probe that extrapolated the ODE dense output gave a fake
  floor of 1e-6 in c₂ for one of 20 random data and in the one-sided control; clamping removed it.
- Left half-slice data enter c₂ only through the constraints. Only the diamond evolves them.

## 5. Data

| id | datum | role |
|---|---|---|
| G | δφ₀ = 1e-3 [b((s−0.30)/0.45) − 0.5 b((s+0.25)/0.45)], δφ_N0 = 1e-3 [b((s−0.30)/0.45) + 0.5 b((s+0.25)/0.45)], plus the two corrections (dev k_m = −3.26e-4, k_o = −3.96e-4) | main datum, both parities |
| R | one-sided, support [0.55, 1.0]: δφ₀ = 1e-3 b((s−0.775)/0.225) − 0.6e-3 b((s−0.70)/0.15), δφ_N0 = 1e-3 b((s−0.775)/0.225) + 0.4e-3 b((s−0.70)/0.15), corrections `b((s−0.775)/0.225)` and `b((s−0.70)/0.15) − b((s−0.85)/0.15)` | class R analog: c₂ = 0 |
| X20 | 20 random data: 3 bumps each for δφ and δφ_N, centers U(−0.5, 0.5), widths U(0.2, 0.45), amplitudes N(0, 1e-3), seed 258, same corrections | spread of c₂ |
| two-sided | bumps at |s| ∈ [0.6, 1.0] on both sides, odd/even parity | observation, no bar |

## 6. Planted cases and controls (written before any run of record)

- **Q1 planted ODE.** Exact pure-gauge `L_ξ(member)`, ξ(V), η(U) cubic polynomials, c = −1 and −1.5, with δF ≠ 0. The ODEs with the exact
  δφ, δF sources and exact initial values reproduce δr and n on [0.3, 1.6]. Same function as the production path (δF = 0 there).
- **Q2 planted δm.** Schwarzschild (kind 2 of #248), scaling solution δr = ε r, δF = −2ε plus a pure-gauge piece: δm = ε/2 at every s.
- **E1 planted evolution.** The exact pure-gauge slice data (U, U_T, U_N, U_TT by 4th-order differences of the exact fields) through layers and march:
  error against the exact solution at 8 fixed points, h = 0.01 … 0.00125.
- **E2 planted c₂.** c = −1.5: c₂ of δr is the known coefficient −η(0) R′(ρ_h) G(ρ_h) = −1.12925016e-2 (η(0) = 0.03; #248's N6). c = −1: exact
  pure gauge has r stationary on H⁺, so the true c₂ is 0 and the fit is the truncation seed.
- **E7 control R.** c₂(slice) = 0 exactly; the evolved fit is a seed falling by 4.
- **Independent of the slice ODEs.** E5 evaluates C_VV, C_UU of #261's lemma by finite differences on the evolved fields at fixed points.
  Shared with the code under test: the background jets, potential and linear system of `horizon_sector.py` / `linear.py` (also used by the march).

## 7. Criteria (declared)

Units: amplitude max|δφ| ≈ max|δφ_N| = 1e-3. "Rich(h, h/2)" = (4 c₂(h/2) − c₂(h))/3.

| id | check | bar | dev value |
|---|---|---|---|
| Q1 | ODE reproduces exact pure-gauge δr, n (relative, max over [0.3, 1.6]) | ≤ 1e-9 | 1.5e-11, 4.3e-11 (c = −1); 3.6e-12, 6.5e-12 (−1.5) |
| Q2 | \|δm − ε/2\|, ε = 1e-3, s = 0.2, 1, 5 | ≤ 1e-10 | 8e-14, 1.3e-13, 8e-12 |
| Q3 | tails of G on \|s\| ∈ [1.05, 3e4] (ρ ≤ 16): max of \|δr\|, \|δr'\|, \|κ s n\|; left end by right-start integration | ≤ 1e-12 | right 2.5e-15 (δr), 8.6e-17 (κ s n); left 6.9e-17 |
| Q4 | δm(s) at s = 10 … 3e4 on both ends (δM_ADM) | ≤ 1e-12 | 9e-16 (right), 6.9e-17 (left) |
| Q5 | left-start against right-start: \|Δc₂\|, \|c₁\| | ≤ 1e-12 | 1e-15, 1.4e-15 |
| E1 | planted evolution: error/scale at h = 0.00125; last Cauchy ratio | ≤ 3e-5; 4.0 ± 0.3 | 6.5e-6 (c = −1), 1.5e-6 (−1.5); ratios 4.00, 4.00, 4.00 |
| E2 | c = −1.5: slice and Rich(0.005, 0.0025) fit against the known coefficient (relative); c = −1: \|c₂ fit\|/max\|δr\| at h = 0.0025, last ratio | ≤ 1e-5, ≤ 1e-5; 4.0 ± 0.3 | slice ≤ 1e-7 (7 printed digits), fit 3.5e-7; 4.6e-6, 4.0 |
| E3 | G: horizon values linear, residual/max at h = 0.00125; last ratio | ≤ 1e-5; 4.0 ± 0.3 | 4.9e-7; 4.0 |
| E4 | G: c₂ slice against evolved fit, relative, Rich(0.005, 0.0025) (acceptance 2; the issue's 1e-6 read as relative, absolute 1e-6 at amplitude 1e-3 follows) | ≤ 1e-6 | 2.7e-8 (3.7e-9 at the next pair) |
| E5 | max \|C_VV\|, \|C_UU\| of the evolved G at 8 fixed points, h = 0.0025, over the largest term; last ratio | ≤ 1e-3; 4.0 ± 0.3 | 2.4e-4; 4.09, 4.00 |
| E6 | diamond: c₂ and c₂′ fits against the slice, relative, Rich(0.005, 0.0025) | ≤ 1e-6 each | 3.9e-8, 1.2e-7 |
| E7 | R: \|c₂ slice\|; \|c₂ fit\| at h = 0.00125; last ratio | ≤ 1e-12; ≤ 1e-7; 4.0 ± 0.3 | 0; 2.3e-9; 4.0 |
| E8 | X20: \|Rich(0.005, 0.0025) − slice\| absolute; min \|c₂\| | ≤ 1e-6; ≥ 1e-5 | 1.1e-9; 3.7e-5 (median 3.9e-4, max 9.4e-4) |
| O1 | two-sided away-support: c₂ slice, no bar, reported with the README sentence | none | 1.4e-5 |

A failed check is reported as not met. The acceptance of the issue: (1) = Q3, Q4, Q5; (2) = E4 (E6, E8 widen it); (3) = the asymptotic mutations below.

## 8. Mutations (`full_slice.py check --mutate=NAME`); effect computed in a development run, set that must fire declared

| name | change | must fire | dev effect |
|---|---|---|---|
| H_P | drop the 2sr′/r term of P | Q1, E3, E4, E5 | Q1 0.20; E3 2.6e-3; E4 2.3e-2; E5 0.16 |
| H_eps | flip ε in the φ′² term of Q | Q1, E3, E4, E5 | Q1 7.8e-2; E3 1.8e-3; E4 2.9e-2; E5 0.11 |
| M_phi | flip the δφ_N source of M | Q1, E3, E4, E5 | Q1 1.55; E3 4.0e-2; E4 0.68; E5 0.67 |
| M_F | flip sF′ in M | Q1, E3, E4, E5 | Q1 3.4; E3 6.0e-3; E4 8.0e-2; E5 0.15 |
| fn_aT | c₂ = ½ δr′(0), n dropped | E2, E4 | E4 0.30 (c₂ −5.11e-4 for −6.65e-4) |
| fn_sign | c₂ = ½ (δr′(0) − n(0)) | E2, E4 | E4 0.86 |
| l1_sign | layer 1 built with −(h/2) U_N | E1, E2, E4 | E1 error 0.29, ratio 1.0; E4 0.46 |
| l1_noquad | layer 1 without the h²/8 U_NN term | E1, E2, E3, E4, E5 | E1 ratio 2.5, 2.2; E3 5.7e-5; E4 2.9e-4; E5 8e-3 |
| dm_noT | δm without the (δF, δr′) group | Q2 | 1.9e-2 … 0.44 against 5e-4 |
| mass_off | C1 not imposed (seed + C2 only) | Q3, Q4, Q5 | δr tail 4.2e-4; δm 6.6e-5 at s = 1.05, 8e-7 at 3e4 (decays); c₂ left-start −4.78e-4, right-start −8.52e-4 |
| odd_off | C2 not imposed | Q3, Q5 | κ s n → 8.4e-5; c₂ −6.06e-4 against −7.25e-4 |
| asym_S | constants set to zero at S, integrate outward | Q3, Q4 | tails δr = ±4.6e-4 at 1.05; δm 1.1e-6 at 3e4; c₂ = 0 for −6.65e-4 |
| left_mass | start at s = −1.05 with δM_L = 1e-4 (hom. solution, no Y tail) | Q4, Q5 | δM_R = 1.00e-4; c₁ = 1.57e-4; c₂ left-start −3.59e-4, right-start −6.65e-4 |

- `mass_off` leaves a constant Y tail and a δm that decays like 1/ρ^{1.3}; it violates "decays to pure gauge", not δM_ADM in the limit.
  `left_mass` is the mutation that violates δM_ADM = 0. Both change c₂ (acceptance 3).
- Two ODE mutations in the dev table (H_eps, M_F) change c₂ of the slice and of the fit differently because the evolved data violate the constraints.

## 9. Cost

| item | dev |
|---|---|
| slice ODEs (DOP853, rtol 1e-12) | ≈ 1 s per datum |
| march, right half, h = 0.00125 | 2 s march, 0.3 s layers, 140 MB |
| all four h for one datum | ≈ 5 s |
| diamond, h = 0.0025 | 0.6 s |
| X20 at three h | 55 s |

Whole `check` ≈ 4 min, 13 mutations ≈ 10 min, one thread, nice 10. The estimate of 8 to 12 h in the task is revised: compute ≈ 20 min of record
runs, effort 3 to 4 h. No run needs a stop condition beyond the 2 h rule.

## 10. For the coordinator

1. **Strict compact reading.** "Decays to pure gauge outside the support" is met by the solution being exactly zero there. Alternatives need δφ ≠ 0 tails.
2. **Bars.** E4 reads "to 1e-6" as relative to c₂ (stricter than #248's absolute reading at amplitude 1e-3). Say if you want the absolute one.
3. **Scope added:** the diamond E6 (both future horizons, interior) and X20. Both are cheap; drop on request.
4. **Discrepancies to be reported in stage 2, no text fixed:** (a) δM_ADM = 0 is not a condition on compact data but an identity; the
   operative conditions are C1 and C2. (b) `horizon_sector.md` says c₁ ≠ 0 data exist (A0, A1L): for compact data c₁ = 0, and c₁ ∝ δM_L.
   (c) the README sentence about data supported away from the horizon: dev holds for one-sided support (E7), c₂ ≠ 0 for two-sided support (O1).
   The constraint solution fills the gap between the two supports, so the gauge-invariant Y is not supported away from S there.
5. **No planted physical solution with c₂ ≠ 0.** #262's closed form has no regular (δr, δφ) split at S in the δF = 0 gauge, so the planted
   c₂ ≠ 0 is a pure-gauge one at c = −1.5 (E2). Say if you want an inverse construction from Y.

## 11. Files and provenance

- Stage 2 writes `notes/black_universe/full_slice.py`, `full_slice_output.txt`, `full_slice.md`; raw `I258-mac/runs`.
- `probe/`: development probes. `fs.py` is the shared module, `p1` the constraint check on exact gauge solutions, `p6`/`p10`/`p23` away-support, c₁, parity,
  `p9`/`p11` datum G, `p12`/`p13`/`p15`/`p22` planted cases, `p14`/`p19` constraint residuals and mutation effects, `p16` control R, `p17`/`p18`
  Schwarzschild plant, tails, δM mutation, X20. `p15`'s last block fails (NameError), kept as it ran; `p17`, `p19` supersede it.
  Probes import `horizon_sector.py` and `linear.py` read-only from the worktree.
- Mistakes: M's first draft had `½ δr_TN` (the difference of second derivatives is `δr_TN`); caught by the exact-gauge check, residual 3e-2 before, 3e-11 after.
