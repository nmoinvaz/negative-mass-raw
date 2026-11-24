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

| file | what |
|---|---|
| `rerun/sheared_full.*` | the rerun at 0219825: stdout, `/usr/bin/time -l`, exit code |
| `ind81_run1.py`, `.txt` | run 1: every criterion passes (`ind81.py` is the same version) |
| `ind81_mut_*.txt` | its 5 mutations |

**Rerun** (exit 0, 96 s, 91 MB peak): 20 of 20 checks pass and 20 of 20 controls fire. The output equals rpi5's line
for line apart from the timings and the Python version.

**ind81 run 1** (exit 0, 1 s):

| criterion | run 1 |
|---|---|
| L0 | Painlevé–Gullstrand Ricci-flat |
| L1 | the own Ricci of a generic b(t, x, y, z) in the frame equals the ten printed closed forms |
| L2 | the cross product, the (I1) residues, (I2), the identity, and R(w, E₀) for the sheared shift, exactly |
| L3 | c3, c4, c5 are minors of N; every minor vanishes on the solved forms |
| L4 | F = 0.82584465013, F′ = −0.089718748297, F″ = 0.1318569451; largest minor 9.6e-64, trace −0.0483 < 0; with F″ + 1/10 the largest minor is 0.0378231 |

Re-solve: L4, the z-axis point, from the coordinator's own Ricci tensor. #81 reports 1.2344e-63 and 0.037823.

The by-hand reduction and corollary of `sheared.md` were read and rederived step by step. The steps were case (A) and
the lemma, case (B) giving u₂ = 0 and c1–c5, and r₀ ≠ 0 forcing (B). Then c1, c2 and the identity give q_X = 0, then
q_y = 0, then X = y = 0. No gap was found.

| mutation | exit | failed | target met |
|---|---|---|---|
| `pg` | 1 | L0 | yes |
| `r1a` | 1 | L1, L2, L4 (both build on the closed forms) | yes |
| `ident` | 1 | L2 | yes |
| `c5` | 1 | L3 | yes |
| `zoff` | 1 | L4 | yes |
