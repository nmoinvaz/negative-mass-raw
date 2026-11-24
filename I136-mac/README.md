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

## Run 1 and the change for run 2 (written before run 2)

Run 1 (`ind136_run1.py`, `.txt`) exits 1: every criterion passes except J4b at both walls, on its limit half. S(300) =
0.533204123 (Le) and 4.59001679 (Rodal) against 4v³ = 0.5 and 4 within 10⁻². The bound half passes (min S along the curve
0.5332 ≥ 0.49998278, 4.590 ≥ 3.9999386). `diag_j4b.py` (written after the failure) expands S = Σ Lₙ z⁻ⁿ + O(e⁻ᶻ) from the
P table: L₀ = 4v³ exactly, L₁ = 1323/128 (Le) and 180 (Rodal), and the sum at z = 300 is 0.533204123 and 4.590016795, the
values of the scan. So #136's limit 4v³ is right, and the 10⁻² test at z = 300 was wrong because of the 1/z terms. A defect of
ind136, not of the claim; run 1 stays failed.

J4b for run 2: min S ≥ #136's bound and y > 0 as before; L₀ = 4v³ exactly, from ind136's own P; S(300) equal to Σₙ₌₀⁹ Lₙ 300⁻ⁿ to
relative 10⁻⁶. The other criteria and the mutations are unchanged.

## Results

| file | what |
|---|---|
| `rerun/` | `review_he_type3_count.py` (full run), the comparison with #133 and its two controls (`runA.sh`), and the 13 controls (`runB.sh`), on the Mac at nice 10; exit codes and seconds in `runA.log`, `runB.log` |
| `ind136.py`, `ind136_run{1,2,3}.{py,txt}` | the independent check above; `ind136.py` is the run-3 version |
| `ind136_mut_*.txt` | its 6 mutations, on the run-3 version |
| `run2_crashed_mutations/` | the mutations started with the run-2 version: each crashed at J4b (below) or was stopped; not results |
| `diag_j4b.py`, `.txt` | the large-z expansion of S from the P table, written after run 1's failure |
| `resolve136.py`, `.txt` | one case re-solved by hand: G(0) at both walls |

**Reruns.** The full run exits 0 in 127 s (rpi5: 398 s); its output equals the committed one apart from timings. The
comparison exits 0 in 117 s (rpi5: 350 s), equal apart from timings; its dump of P equals `I136-rpi5/P_table.tsv` byte for
byte; its two controls exit 1. Each of the 13 controls exits 1 with the same failed checks as on rpi5, and every line of
each log other than timings is identical.

**Re-solve.** With K = 1 + C and u = cosh z − 1, f = K/(K + u) gives φ = v z²/(2K) + O(z⁴) and y = B′ − A′ = −v z⁴ (K − 6)/(3K²)
+ O(z⁶) (hand expansion of A′ = v z f_z, B′ = v z² f_zz). With #136's weight-24 part 774144 φ⁸δ², G(0) = 774144 (v/2K)⁸
(v(K − 6)/(3K²))² = 1.0945107 × 10⁻⁶⁷ (Le) and 6.5894091 × 10⁻¹⁶⁹ (Rodal), the printed values to 6.6 × 10⁻⁷ and 1.3 × 10⁻⁷.
y/z⁴ from the tanh form at z = 10⁻⁴ equals −v(K − 6)/(3K²) to 10⁻⁹ relative.

**ind136.**

| run | exit | result |
|---|---|---|
| 1 | 1 | all PASS except J4b at both walls, on the limit test (above) |
| 2 | 1 | J1 to J4a PASS at Le, then a crash at J4b: `sp.Rational` of an mpmath float. A defect of ind136 |
| 3 | 0 | v given to J4b as an exact rational, criterion unchanged: ALL PASS |

| criterion | run 3 |
|---|---|
| J1a | det(λ − ηR) monic and even in cs; c₂, E1 and E2 equal the printed ones; E2 a cubic form with 10 monomials |
| J1b | 17 and 42 terms in (φ, A′, B′, w) |
| J1c | the resultant divides exactly; P irreducible, 167 terms, degrees 10, 12, …, 18 |
| J1d | P equals `P_table.tsv` term by term |
| J1e | j + k takes every value 9..15; k ≤ 9 |
| J1f | P̂: 358 terms, weights 24..66, weight-24 part 774144 φ⁸δ² |
| J2 | P: 4 sign changes (Le), 6 (Rodal); y: 1 each; within 4.7 × 10⁻¹⁰ of the printed roots |
| J3a | one common w at every root of P (relative \|E2\| below 10⁻⁴⁴, the other root of E1 above 0.0077); w as printed (58.459064354; 4.1006548618, 8.71726377, 1.0300029568 outside (0, 1)); 3 admissible per wall, T as printed |
| J3b | 2D Newton in (r, w): r within 4.4 × 10⁻¹³ to 3.6 × 10⁻¹² of the printed radii, residual below 10⁻⁷⁹ |
| J3c | at y's root the leading coefficients are 10⁻⁸³ of the largest; E1's one root with \|w\| ≤ 10⁴ has relative \|E2\| 0.82 (Le), 0.046 (Rodal) |
| J4a | P/z²⁴ at z = 10⁻³ within 2.9 × 10⁻⁶ and 2.1 × 10⁻⁶ of G(0); P > 0 and y < 0 at 500 points of [10⁻³, 1/4] |
| J4b | min S along [z_t, 300] 0.533204 and 4.590017, above the bounds; L₀ = 4v³ = 1/2 and 4; S(300) equals Σ Lₙ 300⁻ⁿ to 10⁻⁸⁰ |

**Mutations** (run-3 version).

| mutation | exit | failed | target met |
|---|---|---|---|
| `tab` | 1 | every criterion | yes (J1a) |
| `drop` | 1 | J1c, J1d, J1f, J2, J3a, J4a | yes |
| `sig` | 1 | J2, J3a, J3b, J4a, J4b | yes |
| `win` | 1 | J3a at both walls (Rodal's w = 1.030003 also enters) | yes |
| `yatp` | 1 | J3c at both walls | yes |
| `zt` | 1 | J4b at both walls | yes |

**Findings on #136.**
- No discrepancy in the count or in any number of #136 or #133.
- #136's wording point 2 is wrong. Lemma 4 of he_type3_count.md does not need k ≤ 9. Π_n has degree at most n in z, so
  for z ≥ 1, t^(n−9) |Π_n| ≤ M_n t^(n−9) zⁿ = z⁹ M_n (tz)^(n−9) with no condition on k. #136's own L9 needs k ≤ 9 (S is a
  polynomial in s = 1/z only then). It holds: J1e.
- The independence slips #136 disclosed are real. The runner's auto-memory on rpi5 held #133's method, because #133 ran on
  the same machine, and it read 25 lines of `I133-rpi5/README.md`. The code is its own and every formula is checked by an
  exact identity, so the confirmation stands. The shape of the method (the cosh form, the z²⁴ and (τz)⁹ factorizations) is
  not independent of #133's.
