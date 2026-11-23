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
| file | what |
|---|---|
| `rerun/` | `zerilli_derivation.py` (exit 0, 32 PASS, 0 FAIL, 60 s) and `zerilli_derivation_controls.py` (18 OK, 1 MISS) on the Mac at nice 10, with the per-run control logs |
| `ind143_run1.py`, `_run2.py`, `_run3.py` and their `.txt`, `.stderr.txt` | the three runs of the independent check (`ind143.py` is run 3's version) |
| `ind143_mut_*.txt` | its 6 mutations on run 3's code; `ind143_mut_psi9_run2code.txt` is the first `psi9` run, on run 2's code |

**Rerun.** `zerilli_derivation_output_mac.txt` equals #143's `zerilli_derivation_output.txt` apart from the timing lines.
The controls give the same rows as rpi5: 18 OK, 1 MISS (`fsign_bg` fires at PL.O.3, not at the target PL.0c), exit 1.

**ind143 run 1** (exit 1). Y0–Y2 pass. Y3 crashed: `DomainMatrix.from_list_sympy` ignores `domain=`, and the solve met
a domain mismatch (ZZ(r,s,M) against ZZ). A defect of my code; Y3–Y5 were not reached. **Run 2** (exit 1), with
`convert_to` and the criteria unchanged: Y0–Y2 pass, and Y3 crashed again. `sp.nsimplify` turned an exact rational value
into a radical guess. A defect of my code. **Run 3** (exit 0), with the exact value and the criteria unchanged:

| criterion | run 3 |
|---|---|
| Y0 | (a) and (b) δR = 0 in all 10 components; (c) 5 nonzero components |
| Y1 | all 10 components vanish for l = 2, 3, 4 |
| Y2 | all 10 components vanish for l = 2, 3, 4 |
| Y3 | (i) H0 − H2: rank 7, certificate of 7 coefficients, exact, for l = 2 and 3. (ii) Z: rank 15 of 57 forms (l = 2) and of 48 (l = 3), certificate of 15 coefficients, exact. Denominators: 3r²(2r + 3M)² at l = 2 and 1386r²(5r − 3)² at l = 3 |
| Y4 | (9) of (3)–(4) minus ψ = 0, symbolic in r, λ, M, s |
| Y5 | (a), (b) equal; (c) (λr + 3M)²V at r = −3M/λ is 2λ²(2λ + 3)²/9 = (L − 2)²(L + 1)²/18; −3M/λ = 6/c at M = −1 |

Re-solve, the l = 2 forward case of Y3 with M symbolic: Z = ψ,ₓₓ − (V + s²)ψ is a combination of the radial forms and
their first two r-derivatives. The coefficients have no denominator but r²(λr + 3M)², λ = 2.

**Observation, not a criterion.** The Y3 certificates' denominators contain neither s nor r − 2M. The identity is
polynomial in s, so it holds at s = 0: for l = 2 (M symbolic) and l = 3 (M = −1), every static solution in Regge–Wheeler
gauge gives a ψ by DG06 (9) with ψ,ₓₓ = Vψ off r = r_s. #143's reduction divides by s; this direction does not need to.

| mutation | exit | failed | target met |
|---|---|---|---|
| `lich` | 1 | Y0 ((b) fails) | yes |
| `rw` | 1 | Y1 (tφ, rφ at l = 2, 3, 4) | yes |
| `vz` | 1 | Y2, Y5 | yes |
| `hcoef` | 1 | Y2, Y4 | yes |
| `vres` | 1 | Y5 ((b) fails) | yes |
| `psi9` | 1 | Y3 ((ii) not in the span at the point, l = 2 and 3), Y4 | yes; its first run, on run 2's code, crashed in Y3 like run 2 |
