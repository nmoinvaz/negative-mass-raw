# I146-mac: the coordinator's review of #146's gauge solve and the condition at r_s

Machine: macOS (the coordinator's Mac, arm64), Python 3.14, sympy 1.14.0, at nice 10 with at most 2 processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/146. Reviewed branch `wip/i146-gauge-rs` at b87b52e, raw
`I146-rpi5` at 34791d6.

## Independent check `ind146.py` (criteria written before its first run)

ind146 shares no code with `zerilli_gauge_rs*.py` or `zerilli_derivation_lib.py`, and no code with the coordinator's
`ind143.py` and `ind145.py` beyond sympy. The gauge part uses the coordinate Lie derivative
(L_ξg)_ab = ξ^c∂_c g_ab + g_cb ∂_aξ^c + g_ac ∂_bξ^c, not covariant derivatives, and its own projection of a symmetric h
onto the seven functions, with P_l explicit (l = 1..4). The r_s part uses DG06's own equations, typed from the arXiv TeX
(`I143-mac`'s download): (3)–(4), (6), (nv1), (RW17), (cz). It does not use #143's flow.

Shared with #146: the coordinates (t, r, x = cos θ, φ); the definitions of §2 of `zerilli_gauge_rs.md` (H0, H1, H2, J_t,
J_r, K, G with T_ab = D_aD_bP + (L/2)Pγ_ab; ξ^t = aPE, ξ^r = bPE, ξ_x = cP′E; E = e^{st} or 1); the formulas tested
below, typed from that note's §1. f = 1 − 2M/r, μ = −2M, λ = (l−1)(l+2)/2, L = l(l+1), r_s = 3μ/(2λ).

| id | criterion | kind |
|---|---|---|
| Q0 | planted: for h = L_η g, η^t = αPE, η^r = βPE, η_x = γP′E with α, β, γ arbitrary functions of r, the note's (a, b, c) are (−α, −β, −γ), and h + L_ξ g = 0 in all 10 components. l = 2, 3, 4, with e^{st} and with E = 1 | symbolic in r, x, M, s |
| Q1 | for a general h (seven arbitrary functions), the note's c = −r²G/2, b = −f(J_r − r²G′/2), a = (J_t − s r²G/2)/f give h′ = h + L_ξ g with J_t′ = J_r′ = G′ = 0, and h′'s K, H0, H1, H2 equal the note's formulas for K′, H0′, H1′, H2′. l = 2, 3, 4, e^{st} and E = 1 | symbolic |
| Q2 | the projection of L_ξ g equals the note's seven Δ formulas, l = 2, 3, 4. So ΔG = ΔJ_r = ΔJ_t = 0 forces c = b = a = 0 (no homogeneous solution). At l = 1: the traceless part of every h is 0, and c arbitrary with a = sc/f, b = −f(c′ − 2c/r) gives ΔJ_t = ΔJ_r = 0 | symbolic |
| Q3 | (nv1) against (3)–(4) with ψ = ζ/(2λr − 3μ), M = −μ/2, ∂_t → s: (a) K of (nv1) = K of (3); (b) H1 of (nv1) = (2/r) × H1 of (3); (c) H2 of (3) equals (nv1)'s H2 with the sign of its ζ term reversed, and its ζ′ and ζ″ terms unchanged. Coefficients of ζ, ζ′, ζ″ compared directly, symbolic in r, λ, μ, s | symbolic |
| Q4 | the condition at r_s: (a) the numerator of K of (3), times r²(2λr − 3μ), vanishes at r_s iff ζ′ = c*ζ with c* = −2λ²/(3μ(2λ+3)); (b) (RW17) with ∂_t² → s², times r⁴(2λr − 3μ), at r_s gives ζ′ = c*ζ, the same c*, for every s; (c) the printed (cz) coefficient is −c*; (d) at μ = 2, c* = −1/(r_s(r_s + 2)), RESULTS.md's L1 | symbolic in λ, μ, s |
| Q5 | (RW17) with ζ = (2λr − 3μ)ψ and ψ,ₓₓ = (V + s²)ψ, V of DG06 (6) at M = −μ/2, holds identically | symbolic in r, λ, μ, s |

Q4 and Q5 together give the r_s statement without the flow: for a smooth solution (K, H1, H2), ζ of (im) is smooth and
solves (RW17) off r_s, so by continuity ζ′(r_s) = c*ζ(r_s).

Mutations, each must exit 1 with its target failing: `lie` (the term g_cb∂_aξ^c dropped; Q0), `gform` (c = −r²G in
place of −r²G/2; Q1), `nv1k` ((λr − μ) → (λr + μ) in (nv1)'s K; Q3), `czs` (c* taken with the printed sign; Q4),
`rw17` (6λμr → 5λμr in the first numerator of (RW17); Q4 and Q5).

A run that has not finished after 2 hours is stopped and reported as not completed.

## Results

| file | what |
|---|---|
| `rerun/` | `zerilli_gauge_rs.py` (exit 0, 34 PASS, 0 FAIL) and `zerilli_gauge_rs_controls.py` (38 OK, 0 MISS, exit 0) on the Mac at nice 10, with the per-run control logs |
| `ind146_run1.py`, `.txt`, `.stderr.txt` | the independent check, run 1 (`ind146.py` is the same version) |
| `ind146_mut_*.txt` | its 5 mutations |

**Rerun.** Both outputs equal #146's apart from the timing lines.

**ind146 run 1** (exit 0, 3 s):

| criterion | run 1 |
|---|---|
| Q0 | pure gauge: the note's (a, b, c) are (−α, −β, −γ) and h′ = 0, l = 2, 3, 4, e^{st} and static |
| Q1 | general h: J_t′ = J_r′ = G′ = 0, and K′, H0′, H1′, H2′ equal the note's, l = 2, 3, 4, e^{st} and static |
| Q2 | the seven Δ formulas equal the note's, l = 2, 3, 4; at l = 1, T_ab ≡ 0 and the c-family is pure gauge in RW form |
| Q3 | (a) K of (nv1) = K of (3); (b) H1 of (nv1) = (2/r) × H1 of (3); (c) H2 of (3) = (nv1)'s H2 with its ζ term reversed |
| Q4 | (a) and (b) both give ζ′/ζ(r_s) = −2λ²/(3μ(2λ+3)), the (RW17) value for every s; (c) the printed (cz) is +2λ²/(3μ(2λ+3)); (d) at μ = 2, c* = −1/(r_s(r_s+2)) |
| Q5 | (RW17) holds identically for ζ = (2λr − 3μ)ψ with the Zerilli equation |

Re-solve, the condition at r_s from DG06's (RW17) alone: ζ′/ζ = −2λ²/(3μ(2λ+3)) at r = 3μ/(2λ), independent of s.

**Finding.** #146's three discrepancies with DG06's arXiv TeX hold, from DG06's own equations: (cz)'s sign, (nv1)'s
H1 factor 2/r, and (nv1)'s H2 ζ-term sign. (RW17), (3)–(4), (6) and the K of (nv1) are mutually consistent. The project's
L1 (χ′/χ(r_s) = −1/(r_s(r_s+2)), with χ = ζ at M = −1) has the derived sign. No project text uses the printed (cz).

| mutation | exit | failed | target met |
|---|---|---|---|
| `lie` | 1 | Q0 | yes |
| `gform` | 1 | Q1 | yes |
| `nv1k` | 1 | Q3 ((a) fails) | yes |
| `czs` | 1 | Q4 | yes |
| `rw17` | 1 | Q4 ((b) fails), Q5 | yes |
