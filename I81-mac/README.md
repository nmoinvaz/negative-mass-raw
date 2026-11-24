# I81-mac: the coordinator's review of #81's scalar-form test for a sheared warp shift

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, sympy 1.14.0, mpmath 1.3.0, at nice 10 with at most 2
processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/81. Reviewed branch `wip/i81-sheared` at 0219825 and raw
`I81-rpi5` at 77c0a13.

## Rerun of the runner's script

`python3 notes/warp/sheared.py`, full, with its 20 controls, from a detached worktree of 0219825 (`rerun/`).

## Independent check `ind81.py` (criteria written before its first run)

ind81 imports nothing from the repository: no `sheared.py`, `nonaxisymmetric.py` or `phantom_source.py`. Its Ricci
routine is the coordinator's, from `I77-mac` to `I80-mac`. The note's by-hand reduction is checked in its ingredients.
The corollary itself stays a by-hand argument, which the coordinator read and rederived in this review.

Shared with #81: the metric, the frame (E₀ = ∂_t − b∂_x, ∂_x, ∂_y, ∂_z), q = X² + y² + 2z² + Xy/2, w = ∇⊥q,
wp = (−q_z, q_y), the printed formulas (typed here from `sheared.md`), and the z-axis jets.

| id | criterion | kind |
|---|---|---|
| L0 | planted: the own Ricci routine finds Painlevé–Gullstrand Schwarzschild Ricci-flat | symbolic |
| L1 | generic b(t, x, y, z): the ten frame components equal the printed closed forms, R₀₀ = −\|∇⊥b\|²/2 − b_x² + b_xt − b b_xx, R₁₁ = b_x² − \|∇⊥b\|²/2 − b_xt + b b_xx, R₀₁ = −Δ⊥b/2, R₀ₐ = ∂ₐb_x/2, R₁ₐ = b_x∂ₐb/2 − ∂ₐ(D_t b)/2, R_ac = ∂ₐb ∂_c b/2, D_t b = b_t − b b_x | symbolic |
| L2 | b = −v F(q), X = x − vt, generic F: ∇⊥∂_x b × ∇⊥b = 2v²F′²z; (R(wp, E₀), R(wp, E₁), R(wp, w), R(wp, wp)) = (vF′z, v²F′(1 − F)z, 0, 0); \|w\|²(R₀₀ + R₁₁) + 2R(w, w) = 0; R(w, E₁) − v(1 − F)R(w, E₀) = v²F′²q_X\|w\|²; R(w, E₀) = −(v/2)(F″q_X\|w\|² + F′q_y/2) | symbolic |
| L3 | the algebra of case (B): for N = R − λη with R₂₂ = λ, R₀₂ = R₁₂ = R₂₃ = R₃₃ = 0, the 2 × 2 minors of N include −(c3), −(c4), −(c5) up to sign, and every minor vanishes when R₀₀ = −λ − r₀²/λ, R₁₁ = λ − r₁²/λ, R₀₁ = −r₀r₁/λ | symbolic |
| L4 | the z-axis point: v = 1, z = 1/2, X = y = 0, 1 − F = √p with 32p² + 32p − 1 = 0 (p > 0), F′ = −1/(256(1 − F)z²), F″ = (−(1 − F)/(64z²) − 6F′)/(16z²). With the own R there and λ = R(E₃, E₃): every 2 × 2 minor of R − λη is below 1e-40 and the trace of R − λη is negative (ε = −1). With F″ + 1/10 the largest minor exceeds 1e-6. 60 digits | 60 digits |

Mutations, each must exit 1 with its target failing:

| mutation | change | target |
|---|---|---|
| `pg` | √(2M)/r for √(2M/r) | L0 |
| `r1a` | the −∂ₐ(D_t b)/2 term dropped from the typed R₁ₐ | L1 |
| `ident` | 2v² for v² in the typed identity | L2 |
| `c5` | R₀₁ = +r₀r₁/λ in the substitution | L3 |
| `zoff` | the passing check run with F″ + 1/10 | L4 |

## Results

Written after the runs.
