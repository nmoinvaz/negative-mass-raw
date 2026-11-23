# I138-mac: the coordinator's review of #138's review of Lemma A, L1, T1 and T2

Machine: macOS (the coordinator's Mac), Python 3.14, sympy 1.14.0, at nice 10 with at most 2 processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/138. Reviewed branch `wip/i138-lemma-a` at cf80583, raw
`I138-rpi5` at 30e4eb2.

## Independent check `ind138.py` (criteria written before its first run)

It shares no code with `review_lemma_a_*.py` or #2's scripts; formulas typed from RESULTS.md (Lemma A's c_n, the
Zerilli V of §4.2, N, r_s). The recurrence route differs from #138's: c_m and c_{m−1} are written as c_{m−2} times
ratios of the rising factorials, so dividing by c_{m−2}'s factorial part leaves a rational function of (l, m).

| id | criterion | kind |
|---|---|---|
| K1a | the χ-ODE derived from ψ₀,ₓₓ = Vψ₀, ψ₀ = χ/(cr − 6), has P₂ proportional to −r²(r + 2)(cr − 6); the coefficient of r^m in it involves only c_m, c_{m−1}, c_{m−2} | exact, symbolic in c |
| K1b | with c_n from Lemma A, the coefficient of r^m is identically 0 as a rational function of (l, m) for m ≥ 5 (all three indices ≥ 3), which covers the top orders m = l + 3, l + 4; and exactly 0 for m = 1..4 symbolic in l | exact |
| K1c | my coefficients of c_m and c_{m−2}, divided by RESULTS' 12(m − 1)² and c(l − m + 4)(l + m − 3), are the same constant; the middle one divided by that constant is printed and compared with −2(m − 2)(c(m − 4) − 3(m − 1)) (#138's W1) | exact |
| K2 | ψ₀,ₓₓ = Vψ₀ exactly in rationals at l = 41, 45, 60, 100 (outside #138's 2..40) | exact |
| K3 | L1, symbolic in c: the exponents at r_s are 0 and 3; χ′/χ(r_s) = −1/(r_s(r_s + 2)) from the ODE at r_s; the differentiated ODE at r_s forces χ″(r_s) = 0 | exact |
| K4 | T1: the per-term identity c_n r^{n−1}[6n − (n − 1)cr] = (n − 1)c_n r^{n−1}(6 − cr) + 6c_n r^{n−1}, symbolic in n; the cubic 9 + 18c₃r² + (6c₄ − 2cc₃)r³ has minimum over [0, r_s] equal to #138's 9/4 + (27/4)ε²/(1 + ε)², which is ≥ 9/4 | exact |
| K5 | T2 at l = 2..30, 50, 150: d₀ > 0, d₁ = −d₀/(r_s(r_s + 2)), d₂ = 0, d_m > 0 for 4 ≤ m ≤ l + 2, one sign change in (1 − m)d_m; at l = 2..30 and 50, N has exactly one real root in (r_s, ∞) (sympy count_roots) | exact |
| K6 | T1 at l = 2..30, 50: N has no real root in [0, r_s] (count_roots), N(0) = 9 | exact |

Mutations, each must exit 1 with its target failing: `ode` (9(λr + 1) in V; K1), `cn` ((n − 3) in place of (n − 4) in
c_n; K1b), `rs` (r_s = 6/(c + 1) in K3; K3), `cubic` (17c₃ in place of 18c₃; K4), `shift` (Taylor point
r_s(1 + 10⁻³) in K5; K5).
