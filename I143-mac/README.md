# I143-mac: the coordinator's review of #143's derivation of the even-parity potential

Machine: macOS (the coordinator's Mac, arm64), Python 3.14, sympy 1.14.0, at nice 10 with at most 2 processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/143. Reviewed branch `wip/i143-zerilli-derivation` at 47dfd88,
raw `I143-rpi5` at 62b1b61.

## Independent check `ind143.py` (criteria written before its first run)

ind143 shares no code with `zerilli_derivation.py`, `zerilli_derivation_lib.py` or `zerilli_derivation_controls.py`, and
was written without opening them. It computes the linearized Ricci tensor from the Lichnerowicz form
δR_ab = ½(∇^c∇_a h_bc + ∇^c∇_b h_ac − □h_ab − ∇_a∇_b h), with its own background Christoffel symbols and covariant
derivatives. #143 used the Christoffel definition with dual numbers and the Palatini form δR = ∇δΓ − ∇δΓ.

It shares with #143: sympy; the coordinates (t, r, x = cos θ, φ); DG06's even ansatz (gr-qc/0604021 eq. (2), m = 0,
Y → P_l(x), time dependence e^{st}) and the odd ansatz h_tφ = h0 e^{st}(1−x²)P′, h_rφ = h1 e^{st}(1−x²)P′. DG06 eqs. (3)–(6)
and (9) are typed here from the arXiv TeX source, read on 2026-11-23, not from #143's files. F = 1 − 2M/r,
λ = (l−1)(l+2)/2, L = l(l+1), ′ = d/dr, ψ,ₓₓ = F(Fψ′)′.

| id | criterion | kind |
|---|---|---|
| Y0 | planted, the operator: δR = 0 in all 10 components for (a) h = ∂_M g, (b) h = ∇_aξ_b + ∇_bξ_a with ξ = e^{st}(A P, B P, C P′, 0) and with ξ = e^{st}(0, 0, 0, D(1−x²)P′), A..D arbitrary functions of r, l = 2; and (c) δR ≠ 0 for the non-solution h_tt = r e^{st}P, l = 2. M and s symbolic | symbolic |
| Y1 | planted, odd parity (Regge–Wheeler): h1 = rΨ/F, s h0 = F(F h1)′, Ψ,ₓₓ = (V_RW + s²)Ψ with V_RW = F(L/r² − 6M/r³). All 10 components vanish for l = 2, 3, 4 | symbolic in r, x, M, s |
| Y2 | converse, even parity: DG06 (3)–(4) with ∂_t → s, H0 = H2, and ψ,ₓₓ = (V + s²)ψ with V of DG06 (6). All 10 components vanish for l = 2, 3, 4 | symbolic in r, x, M, s |
| Y3 | forward, even parity, the case re-solved: the radial forms are the 10 components with general H0, H1, H2, K, divided by e^{st}, at x = 0, 1/3, 3/5. (i) H0 − H2 is in their span over Q(r, M, s). (ii) Z = ψ,ₓₓ − (V + s²)ψ, with ψ from DG06 (9), is in the span of the forms and their r-derivatives to order 2. For l = 2 with M symbolic and for l = 3 at M = −1; s symbolic | symbolic; a certificate (coefficients in Q(r, M, s)) checked by cancellation |
| Y4 | DG06 (9) applied to the map (3)–(4) returns ψ, modulo ψ,ₓₓ = (V + s²)ψ | symbolic in r, λ, M, s |
| Y5 | (a) DG06 (6) equals #143's form 2F[λ²(λ+1)r³ + 3λ²Mr² + 9λM²r + 9M³]/(r³(λr + 3M)²), symbolic in r, λ, M. (b) At M = −1 it equals RESULTS.md §4.2's V, 2f[λ²r²((λ+1)r − 3) + 9(λr − 1)]/(r³(λr − 3)²), f = 1 + 2/r. (c) (λr + 3M)²V at r = −3M/λ equals (L−2)²(L+1)²/18, and −3M/λ = 6/c at M = −1, c = (l+2)(l−1) | symbolic |

Y3 proves the forward direction only where its certificate's denominators do not vanish; they are printed. Y2 and Y4
together with Y3 give the equivalence for those l. Y1 and Y0 come first: a failure there stops the reading of Y2–Y5.

Mutations, each must exit 1 with its target failing: `lich` (the ∇_a∇_b h term dropped; Y0), `rw` (−6M → −5M in V_RW; Y1),
`vz` (9M²(λr + M) → 8M²(λr + M) in DG06 (6); Y2 and Y5), `hcoef` (−3M² → −2M² in DG06's h(r); Y2 and Y4), `psi9`
(λ + 1 → λ + 2 in the first denominator of DG06 (9); Y3 and Y4), `vres` (9(λr − 1) → 9(λr + 1) in §4.2's V; Y5).

A run that has not finished after 2 hours is stopped and reported as not completed.

## Results
