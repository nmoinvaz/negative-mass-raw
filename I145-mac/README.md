# I145-mac: the coordinator's review of #145's static (s = 0) even-parity reduction

Machine: macOS (the coordinator's Mac, arm64), Python 3.14, sympy 1.14.0, at nice 10 with at most 2 processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/145. Reviewed branch `wip/i145-zerilli-static` at 8a7cfb6, raw
`I145-rpi5` at 0761705.

## Independent check `ind145.py` (criteria written before its first run)

ind145 shares no code with `zerilli_static*.py`, `zerilli_derivation*.py` or `zerilli_derivation_lib.py`. It reuses the
coordinator's `I143-mac/ind143.py` (the Lichnerowicz form of δR, its own covariant derivatives, DG06 (3)–(6) and (9)
typed from the TeX, the span-certificate routine). #145's note says its runner did not open `ind143.py`. This is the
note's recommended task 4: a second operator on the static equations.

It shares with #145: sympy; the coordinates (t, r, x = cos θ, φ); DG06's even ansatz (eq. (2), m = 0, Y → P_l(x)) and the
odd ansatz h_tφ = h0(1−x²)P′, h_rφ = h1(1−x²)P′; static means no t-dependence (s = 0). F = 1 − 2M/r, λ = (l−1)(l+2)/2,
L = l(l+1), ψ,ₓₓ = F(Fψ′)′, V is DG06 (6). The flow in X4 is typed from #145's closing comment.

| id | criterion | kind |
|---|---|---|
| X0 | planted, static: (a) l = 1 odd, h0 = 1/r (the Kerr term linear in the spin) and h0 = r² (rigid rotation, pure gauge) give δR = 0 in all 10 components, M symbolic; h0 = 1/r² gives δR ≠ 0. (b) Static even pure gauge, ξ = (A P, B P, C P′, 0), A, B, C arbitrary functions of r, l = 2: δR = 0 | symbolic |
| X1 | the H1 sector, l = 2, 3, 4: for h with H1 only, δR_tr = σ L H1 P/(2r²) and δR_tx = σ′ (F H1)′ P′/2 with σ, σ′ ∈ {+1, −1} (reported), and the other 8 components are 0 | symbolic in r, x, M |
| X2 | converse at s = 0: DG06 (3)–(4) with H1 = 0, H0 = H2, ψ,ₓₓ = Vψ: all 10 components vanish, l = 2, 3, 4 | symbolic in r, x, M |
| X3 | forward at s = 0, the case re-solved at l = 2: the static radial forms are the 10 components with general H0, H1, H2, K at x = 0, 1/3, 3/5. (i) H1 and H0 − H2 are in their span; (ii) Z0 = ψ,ₓₓ − Vψ, ψ from DG06 (9), is in the span of the forms and their r-derivatives to order 2. For l = 2, 3, 4 over Q(r, M), and for l = 2, 3, 4 at M = 0 over Q(r). Denominators printed | symbolic; exact certificates |
| X4 | the flow K′ = (λ/M)K − ((λr + 2M)/(Mr))H, H′ = (λ/M)K − ((λr² − 2(λ−1)Mr − 2M²)/(Mr(r − 2M)))H. (a) With H1 = 0, H0 = H2 = H and the flow, all 10 components vanish, l = 2, 3, 4. (b) Both flow equations (with H = H2) are in the span of the forms and their first r-derivatives, l = 2, 3 | symbolic; certificates |
| X5 | (3)∘(9) on solutions: K − K₃(ψ) and H2 − H₃(ψ), with ψ from (9) and K₃, H₃ from DG06 (3) at s = 0, are in the span of the forms and their r-derivatives to order 2, l = 2, 3 | certificates |

X3 at M = 0 answers part of #145's open point (the forward direction at M = 0) for l = 2, 3, 4 only.

Mutations, each must exit 1 with its target failing: `lich` (the ∇_a∇_b h term dropped; X0), `kerr` (h0 = 1/r² in place
of 1/r; X0), `h1c` (L/(2r²) → L/r² in X1's coefficient; X1), `vz` (9M² → 8M² in DG06 (6); X2 and X3), `flowc` (λ/M →
(λ+1)/M in the K′ equation; X4), `psi9` (λ + 1 → λ + 2 in the first denominator of (9); X3 and X5).

A run that has not finished after 2 hours is stopped and reported as not completed.

## Results

| file | what |
|---|---|
| `rerun/` | `zerilli_static.py` (exit 0, 35 PASS, 0 FAIL) and `zerilli_static_controls.py` (40 OK, 0 MISS, exit 0) on the Mac at nice 10, with the per-run control logs |
| `ind145_run1.py`, `.txt`, `.stderr.txt` | the independent check, run 1 (`ind145.py` is the same version) |
| `ind145_mut_*.txt` | its 6 mutations |

**Rerun.** Both outputs equal #145's apart from the timing lines.

**ind145 run 1** (exit 0, 65 s):

| criterion | run 1 |
|---|---|
| X0 | (a) h0 = 1/r and h0 = r² give δR = 0; h0 = 1/r² is nonzero in tφ; (b) static even pure gauge gives δR = 0 |
| X1 | δR_tr = +L H1 P/(2r²) and δR_tx = +(F H1)′P′/2 for l = 2, 3, 4 (σ = σ′ = +1); the other 8 components 0 |
| X2 | all 10 components vanish for l = 2, 3, 4 |
| X3 | (i) H1 and H0 − H2 in the span (rank 7) for l = 2, 3, 4, M symbolic and M = 0. (ii) Z0 in the span (rank 15), certificate exact. Denominators with M symbolic: 3r²(2r + 3M)², 1386r²(5r + 3M)², 225r²(3r + M)² (l = 2, 3, 4), that is r²(λr + 3M)² up to a constant; at M = 0: 3r, 6930r, 675r |
| X4 | (a) all 10 components vanish on the flow, l = 2, 3, 4. (b) both flow equations in the span, rank 11; denominators M r(r − 2M) up to a constant |
| X5 | K − K₃(ψ) and H2 − H₃(ψ) in the span, rank 15, l = 2, 3; denominators (λr + 3M) and (r − 2M)(λr + 3M)² up to a constant |

Re-solve, the l = 2 forward case of X3 with M symbolic: Z0 = ψ,ₓₓ − Vψ is a combination of the static radial forms and
their first two r-derivatives with no denominator but r²(2r + 3M)².

**Finding.** The forward certificates (X3) have no M in their denominators for l = 2, 3, 4, and X3 passes at M = 0
directly. So for those l the forward direction holds at M = 0, which #145 left open: its flow divides by M (X4's
certificates carry M too), but the forward direction does not need the flow.

| mutation | exit | failed | target met |
|---|---|---|---|
| `lich` | 1 | X0 ((b) fails) | yes |
| `kerr` | 1 | X0 ((a) fails) | yes |
| `h1c` | 1 | X1 (no tr sign fits) | yes |
| `vz` | 1 | X2, X3 | yes |
| `flowc` | 1 | X4 ((a) and (b)) | yes |
| `psi9` | 1 | X3, X5 | yes |
