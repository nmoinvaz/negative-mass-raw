# I104-mac: the coordinator's review of #104's independent review of #2's large-l proofs

Machine: macOS (the coordinator's Mac), Python 3.14, sympy 1.14.0, mpmath 1.3.0, at nice 10 with at most 2 processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/104. Reviewed branch `wip/i104-review-large-l` at 154a345,
raw `I104-rpi5` at 4a6b044.

## Independent check `ind104.py` (criteria written before its first run)

ind104 shares no code with `review_large_l_*.py` or with #2's scripts. What it shares with them: formulas typed from
RESULTS.md (Lemma A's c_n, the Zerilli V for M = −1, the definitions of N, V̂, Ψ, N_Z, S, X_∞). It works in the
variable r with Lemma A's c_n directly (not the rescaled a_n(ε)), at 60 digits with mpmath mpf (numerical, not
intervals), and gets V̂ from its definition V̂ = g² − g_x, g = ψ₀,x/ψ₀, ψ₀ = χ/(cr − 6), not from Ψ or S. Its own
derivation (by hand, before the run): V̂ = c³ f S/(ρ²(ρ − 6)X²) for any X, using only N = X − (ρ − 6)X′, so sign V̂ =
sign S on ρ > 6 without (Z).

l set: 2..30, 80, 100, 137, 138, 139, 499, 500, 501, 502, 1000, 1001, 2000, 2999, 3000, and 6 drawn by
`random.Random(10404).sample(range(31, 3001), 6)` = 36, 464, 864, 1461, 1644, 1995.

| id | criterion | kind |
|---|---|---|
| F1a | X_∞ by its series (200 terms) equals the Bessel closed form to 1e-45 at ρ = 3, 8.5, 11. N_∞ has one sign change on a 0.01 grid of (6, 30], Ψ_∞ one on [ρ_*, 30]; bisection roots agree with #104's 8.485700967373530340930500822 and 9.6359894425861440206961577 to 1e-24 | numerical |
| F1b | ρ_*, D₁, D₂ fitted to c·r_*(l) = ρ + D₁/c + D₂/c² at l = 1000, 2000, 3000 (direct roots, F3): ρ within 1e-12 of F1a, D₁ within 2e-6 of RESULTS' 3.515486; the same for r_neg with 5.839393 | numerical |
| F2 | Lemma A(ii) at every l of the set: c₁..c₄ = 3/2, 0, −K/32, K/96; relative residual of ψ₀,xx − Vψ₀ below 1e-40 at ρ = 7, 8.5, 9.6, 12 | numerical |
| F3 | at every l: N has exactly one sign change on the 0.02 grid of (6, 16] and N < 0 at ρ = 20, 40, 80, 160, 320; V̂ has exactly one sign change on the grid from my c·r_* to 16 and V̂ > 0 at those ρ; both bisected roots lie inside #104's brackets in `I104-rpi5/sweep_brackets.csv` | numerical |
| F4 | D = (c·r − ρ)·c at every l ≥ 138 of the set: 0 < D_* ≤ 3.5525479 and 0 < D_neg ≤ 6.6818585 (#104's second-order L); for l ≥ 500, D_* ≤ 3.5186068 and D_neg ≤ 5.9363952 (#104's M) | numerical |
| F5 | r_* < r_neg at every l. c·r_* and c·r_neg strictly decrease over 2..30 and over the consecutive pairs (137..139, 499..502, 1000..1001, 2999..3000), and stay above ρ. l²·r has its minimum over 2..30 at l = 5 and strictly increases on 5..30 and on the pairs; l²·r < ρ for l ≥ 3. RESULTS 4.3's table rows (l = 2, 3, 5, 10, 20, 80, 100, 500, 1000, 3000) within 1e-6 | numerical |
| F6 | Theorem 3 in sympy, own derivation: (P1) the numerator of V in (σ, μ) has positive coefficients; (P2) Q = −V_r r⁵(cr − 6)³/2 is a quintic in r, and c⁵Q at r = (6 + τ)/c, l = 2 + m is a polynomial in (τ, m) with exactly 64 terms, all positive | exact |
| F7 | at l = 2, 7, 30, 500, 3000 and ρ = 7, 9, 11: V̂ (direct) equals c³fS/(ρ²(ρ − 6)X²) and 2c⁴(2 + ερ)Ψ/(ρ⁴(ρ − 6)²X²), each to relative 1e-35 | numerical |

Mutations, each must exit 1 with its target failing: `cn` (c₅ × (1 + 1e-12); F2), `vsign` (−9(λr − 1) in V; F2, F6),
`rho` (#104's ρ_* + 1e-23; F1a), `csv` (#104's r_* bracket at l = 500 shifted by 1e-13; F3), `l2` (c in place of l² in
F5; F5), `sM` (3.515 in place of 3.5186068; F4), `vhat` (g² + g_x; F7).
