# I142-mac: the coordinator's review of #142's independent review of Lemma A(iii), L2–L6 and the Zerilli V

Machine: macOS (the coordinator's Mac), Python 3.14, sympy 1.14.0, mpmath 1.3.0, at nice 10 with at most 2 processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/142. Reviewed branch `wip/i142-lemma-a3` at c2f4bd0, raw
`I142-rpi5` at 7e793da.

## Independent check `ind142.py` (criteria written before its first run)

ind142 shares no code with `review_lemma_a3_*.py` or with #2's scripts. What it shares with them: formulas typed from
RESULTS.md (c_n of Lemma A, V of §4.2, f, x, ψ₀, g, V̂, Ψ_DG, k) and the claims typed from `review_lemma_a3.md`
(q(r₀) closed form, r₀ = 24/(s+6), r⁴V̂ coefficients, Ψ̂ ~ (2ᵏk²/192)r³). Routes that differ from #142's:
- root counts by sympy `Poly.intervals` (continued-fraction isolation), not Sturm sequences;
- minima, the x-series of V̂ and the DG mode residual numerically in mpmath at 60–100 digits, not by sympy series;
- V̂ = 2g² − V (Theorem 3's (Z) route, needs only ψ₀′ and V), not g² − g,ₓ;
- the Zerilli V compared with the standard form typed from memory (M general), which I have not checked against a
  source here; #142 compared four sources.

Coordinator's hand derivation before the run (DG09 eq. (61)): x = r²/4 − r³/12 + r⁴/32 + …, so r = 2y(1 + y/3 + y²/36
+ …) with y = √x. With r⁴V̂ = 12 + 2a r + b r², a = l²+l+3, b = l(l+1): the x^{−3/2} coefficient is a/4 − 1 =
(l²+l−1)/4, and the x^{−1} coefficient is (3/4)(10/9 − 4/36) − a/4 + b/4 = 3/4 − (l²+l+3)/4 + l(l+1)/4 = 0. DG09 (61),
read in the arXiv TeX source (label `zm11`), prints −ℓ(ℓ+1)/(4|M|x).

| id | criterion | kind |
|---|---|---|
| H1 | χ/r has no root in [0, ∞) for l = 2..50, 75, 100 (`Poly.intervals(inf=0)` returns no interval) | exact |
| H2a | (Ks)² − (18(K−16))² − 6(K−24)³ = 0 with s² = 6(K−18) (polynomial in K); K − 24 = (l−2)(l+3)(l²+l+4); c₃, c₄, c₅ from c_n equal −K/32, K/96, K(K−24)/6144 for l = 2..60 | exact |
| H2b | for l = 3..50: the positive root of q′/r (mpmath polyroots, 50 digits) equals 24/(s+6) to relative 1e-40; q there equals 4(K−18)(Ks − 18(K−16))/(K−24)³ to relative 1e-40 and is > 0. For l = 3..30: every positive real critical point of χ/r (polyroots of (χ/r)′, imaginary part < 1e-30) has χ/r ≥ q(r₀)·(1 − 1e-30) and > 0. l = 2: χ/r = 3/2 − (3/4)r² + (1/4)r³ exactly and its value at r = 2 is 1/2 | numerical |
| H3 | for l = 2..12, the Taylor coefficients of r⁴V̂ at r = 0, V̂ = g² − f g_r, g = f ψ₀,ᵣ/ψ₀, are 12, 2(l²+l+3), l(l+1) (sympy series, exact) | exact |
| H4 | for l = 2, 3, 7 at r = 1e-10, 100 digits, V̂ = 2g² − V: R = x(V̂ − 3/(4x²) − (l²+l−1)/(4x^{3/2})) has |R| < 1e-6, and |R + l(l+1)/4| > 1; x^{3/2}(V̂ − 3/(4x²)) is within 1e-6 of (l²+l−1)/4 | numerical |
| H5 | for l = 2..8 at r = 0.05, r_s/2, 3r_s, 1, 4 (60 digits, mpmath.diff): |−Ψ,ₓₓ + VΨ + (k/2)²Ψ| < 1e-25 (k/2)²|Ψ| for Ψ = Ψ_DG, k = c(c+2)/6, Ψ,ₓₓ = f²Ψ″ + f f′Ψ′ | numerical |
| H6a | for l = 2..6 at r = 1e-12, 100 digits: Ψ̂ = f(Wχ′/χ − W′)/(cr−6), W = r(r+2)ᵏe^{−kr/2}, gives Ψ̂/r³ within relative 1e-6 of 2ᵏk²/192 | numerical |
| H6b | for l = 2..30, 100 digits: |W(r_s)χ′(r_s)/χ(r_s) − W′(r_s)| < 1e-50 |W′(r_s)|, W′ = W(1/r + k/(r+2) − k/2) | numerical |
| H7 | V_text = 2(1−2M/r)[λ²(λ+1)r³ + 3λ²Mr² + 9λM²r + 9M³]/(r³(λr+3M)²) at M = −1 equals RESULTS' V exactly (λ symbolic); r²V_text → 2(λ+1) = l(l+1) for symbolic M | exact |

Mutations, each must exit 1 with its target failing: `shift` (χ/r − 0.51 at l = 3; H1), `ident` (6(K−23)³; H2a),
`qform` (18(K−15) in the closed form; H2b), `zr` (g = ψ₀,ᵣ/ψ₀ without f; H3), `xlog` (x + r³/1000; H4), `kp1` (k + 1;
H5 and H6b), `c5` (c₅ × (1 + 1e-3) in H6's χ only; H6a), `vz` ((λ+1)r − 2 in place of − 3 in RESULTS' V; H7).

## Results

(after the run)
