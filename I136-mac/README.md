# I136-mac: the coordinator's review of #136's independent interval review of #133's Type III count

Machine: macOS (the coordinator's Mac), Python 3.14, sympy 1.14.0, mpmath 1.3.0, at nice 10 with at most 2 processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/136. Reviewed branch `wip/i136-type3-review` at 2a8a0f9 (script
frozen at b2c4ac7), raw `I136-rpi5` at eeb8d72.

## Independent check `ind136.py` (criteria written before its first run)

ind136 shares no code with `review_he_type3_count*.py`, `he_type3_count.py` or `he_type3.py`. What it shares with them:
the frame table of he_type3.md section 1 and the printed c₂ and E1 (typed from the note), the printed E2 (read as text
from `notes/warp/he_type3_output.txt`, #102), the tanh profile, and the claims typed from `review_he_type3_count.md`
(roots, w, T, G(0), the bound on S); sympy's `resultant` and `factor_list` (#136 also uses them). Routes that differ:
- E1 = c₂² − 3c₁ and E2 = 27c₀ − c₂³ from sympy's determinant of λ − ηR, not by hand;
- roots by a sign scan of the tanh form (mpmath floats, analytic f′, f″, no cosh or ε form, no intervals), so J2–J4 are
  *numerical evidence*, not a certification;
- the admissible points re-solved by 2D Newton on E1 = E2 = 0 in (r, w), without the resultant;
- the ends as limits along the curve, not bounds over a box.

| id | criterion | kind |
|---|---|---|
| J1a | det(λ − ηR) is monic and even in cs = cos θ sin θ; c₂, E1 equal the printed ones of he_type3.md §1, E2 equals the printed E2 of he_type3_output.txt; E2 is a cubic form in (X, γ, y) with 10 monomials | exact |
| J1b | with (X, γ, y) = (A′², A′, B′ − A′), E1 and E2 have 17 and 42 terms in (φ, A′, B′, w) | exact |
| J1c | Res_w(E1, E2) = (27/256) φ³ (A′ − B′)³ P exactly, P irreducible over ℚ, 167 terms, total degrees {10, 12, …, 18} | exact |
| J1d | P equals `I136-rpi5/P_table.tsv` term by term (the Lean input) | exact |
| J1e | every term φⁱA′ʲB′ᵏ of P has j + k in {9, …, 15}, all values taken, and k ≤ 9 | exact |
| J1f | P̂(φ, ψ, δ) = P(φ, ψ − 2φ, ψ − 2φ + δ) has 358 terms, least weight 24 (weights 2, 4, 4), weight-24 part 774144 φ⁸δ² | exact |
| J2 | per wall, a scan of z = 2σr over [1/4, z_t] in steps of 10⁻³ (80 digits), bisected: P has 4 (Le) and 6 (Rodal) sign changes and y = B′ − A′ has 1, each within 10⁻⁹ of the printed root; no grid value is exactly 0 | numerical |
| J3a | at each root of P, exactly one root of E1(w) is a root of E2 (relative |E2| < 10⁻²⁰, the other > 10⁻⁶), real, equal to the printed w within 10⁻⁶ max(1, |w|); exactly 3 per wall have 0 < w < 1 and |T| > 10⁻⁶, at the printed r within 10⁻⁹ and T within 10⁻⁴ | numerical |
| J3b | 2D Newton on (E1, E2) in (r, w) from the printed (r, w) rounded to 4 and 3 decimals converges to each admissible point: relative residual < 10⁻⁴⁰, r within 10⁻⁹ | numerical |
| J3c | at the root of y, the leading coefficients of E1 and E2 are below 10⁻²⁰ of their largest coefficient, and every root of E1 with |w| ≤ 10⁴ has relative |E2| > 10⁻⁶ | numerical |
| J4a | P/z²⁴ at z = 10⁻³ (160 digits) within relative 10⁻⁴ of the printed G(0) (1.09451e-67, 6.58941e-169); P > 0 and y < 0 at 500 points of [10⁻³, 1/4] | numerical |
| J4b | S = P/(τz)⁹, τ = 2v(1 + C)z e⁻ᶻ, at 1000 points of [z_t, 300]: min S ≥ #136's bound (0.49998278, 3.9999386), S(300) within relative 10⁻² of 4v³, and y > 0 | numerical |

Mutations, each must exit 1 with its target failing: `tab` (R₀ₓ = γ − (1 − w)y/2; J1a), `drop` (the term A′⁴B′⁶ of P
removed; J1c, J1d, J4a), `sig` (σ + 10⁻³ in the profile; J2, J3a, J3b), `win` (admissible window (0, 100); J3a:le),
`yatp` (J3c run at the first root of P; J3c), `zt` (the S scan starts at z = 4; J4b).
