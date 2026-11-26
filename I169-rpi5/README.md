# I169-rpi5: sums of two products u = X₁R₁ + X₂R₂ + v with det R₃ = 0

Machine rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores shared), one process, one thread, nice 10. Issue
https://github.com/nmoinvaz/negative-mass/issues/169 . Worktree `~/Source/negative-mass-i169`, branch
`wip/i169-sum-products`. sympy 1.14.0, mpmath 1.3.0, Singular 4.4.1 (dev attempts only, no certificate is used).
Script `notes/warp/sum_products.py`, its stdout `notes/warp/sum_products_output.txt`, note `notes/warp/sum_products.md`.

**Order of events, stated plainly.** Development runs 1 to 3 (`dev/`) came before this README was pushed. Dev 1 is a numerical
formal-series solver, dev 2 the checks of the script without controls, dev 3 the checks with all controls. The criteria in §4 are
coded exactly as worded below; the run of record comes after amendment A1 (§8), which declares what each control does.

## 1. Setting

I ⊂ ℝ and J ⊂ (0, ∞) open intervals, B = I × J. X₁, X₂ ∈ C²(I), R₁, R₂ ∈ C²(J), v ∈ ℝ the travel speed, and

    u = X₁R₁ + X₂R₂ + v,   D = h(h² − P² − Q² + Y² + Z²) − P(Y² − Z²) + 2QYZ,

P = −(u_x² + u u_xx), Q = −(u_ρρ + u_ρ/ρ)/2, Z = u_xρ/2, Y = u_x u_ρ + u u_xρ/2, h = u_ρ²/2 (#80 Setup, retyped as in #160). The question is
whether D = 0 on B has a solution under (N) below.

Notation. a = (X₁, X₂), r = (R₁, R₂), s = r″ + r′/ρ = (S₁, S₂), wedge p∧q = p₁q₂ − p₂q₁, V_X = span{X₁, X₂}|_I, V_R = span{R₁, R₂}|_J.
Jets: A_k = X₁^(k), B_k = X₂^(k), a_0, a_1, a_2 = R₁, R₁′, S₁ and b_0, b_1, b_2 = R₂, R₂′, S₂. **E := 8D**, a polynomial in these 12 jets and
v with 376 terms. D has no common factor to divide out: E is irreducible over ℚ (one factor of 376 terms, multiplicity 1; `factor_list`,
68 s, `dev/irreducible.log`, optional flag `--irreducible`). So the "factor that cannot vanish" of #160 is 1 here.

## 2. Nondegeneracy (N), what it leaves out

**(N1)** W_x = a∧a′ ≠ 0 on I. **(N2)** W_ρ = r∧r′ ≠ 0 on J. **(N3)** not (1 ∈ V_X and 1 ∈ V_R).

With (N1), (N2): a″ = αa + βa′ and s = Γr′ + δr with α = (a″∧a′)/W_x, β = (a∧a″)/W_x, Γ = (r∧s)/W_ρ, δ = (s∧r′)/W_ρ, all continuous.
X₁′X₂″ − X₂′X₁″ = −αW_x gives: 1 ∈ V_X ⟺ α ≡ 0 (by hand in the note, identities in `ode_form`); 1 ∈ V_R ⟺ δ ≡ 0 likewise. So (N3) is "α ≢ 0 on I or δ ≢ 0 on J".

**The excluded forms are the decided ones.**

1. X₁, X₂ dependent on I (or R₁, R₂ on J), or W_x ≡ 0: u − v is one product X(x)R(ρ). #160: no solution with X X′ R R′ ≠ 0 for every v (X′ ≡ 0 is #65's
   b(ρ), R′ ≡ 0 planar).
2. α ≡ 0 and δ ≡ 0 (1 ∈ V_X and 1 ∈ V_R): u = a + bX + cR + dXR (constants a, b, c, d; X, R functions). For d ≠ 0 it is d(X + c/d)(R + b/d) + (a − bc/d), one
   product plus a constant: #160 for every v. For d = 0 it is additive: #80 Theorem A. `case_a` checks the algebra.
3. A box on which X₁, X₂ are independent but W_x vanishes at points: shrink to a subbox where W_x ≠ 0, or on which W_x ≡ 0 (item 1). The same for W_ρ, α and δ
   (continuous, so ≡ 0 or ≠ 0 on a subbox). Every solution on a box therefore restricts to a subbox of item 1, item 2 or (N).

**What (N) leaves out altogether.** Complex X, R; functions that are not C²; boxes touching ρ = 0. Nothing else is excluded beyond items 1 and 2.

Cases inside (N): (b) α ≡ 0, δ ≠ 0 (u = X(x)β(ρ) + γ(ρ)); (c) α ≠ 0, δ ≡ 0 (u = A(x)R(ρ) + B(x)); (d) α ≠ 0 and δ ≠ 0.

## 3. What can be claimed, and what the issue's second criterion needs

The issue asks for "either a proof that no solution exists under the stated nondegeneracy (each algebraic step checked symbolically) or an explicit
solution that goes through closure". That is claimed only if every case of (N) is decided by checks of §4 that pass. The development runs say the rank route
of #160 cannot do this: the exact ranks of E are 59 (v = 0), 93 (v = 1/3), 87 (v = 1) and 102 (symbolic v) against 6 and 10 in #160, and an exponential pair on
both sides satisfies d_F + d_G ≤ r with room (`slack`). **That criterion is therefore expected not to be met, and the note will say so**; what the script
decides is: the reductions (§2), the stratum "ρ-side with constant ODE coefficients" (`rho_const`, no solution), the ranks, the planted additive truth.
Not decided: (b), (c), (d) outside that stratum.

## 4. Criteria (each can fail)

Declared values come from the development runs. A check passes iff every item holds.

- **C1 `e_two`.** (i) E equals 8D computed from sympy derivatives of undefined X₁(x), X₂(x), R₁(ρ), R₂(ρ) with the jets substituted. (ii) 4hD = C² − A² − B²
  as an identity in abstract P, Q, Z, Y, h, with A = 2hP + Y² − Z², B = 2hQ − 2YZ, C = Y² + Z² + 2h². (iii) With X₂ = 0, E = R₁′² · `det_classify.E_mult_poly`. (iv)
  With X₂ = 1, R₁ = 1, E = 4R₂′² · `det_classify.E_add_poly(X + v, …)`.
- **C2 `ode_form`.** (i) a″ = αa + βa′ and s = Γr′ + δr, with the wedge formulas, as rational identities. (ii) E with a″, s eliminated equals D̃(N; α, β, Γ, δ), D̃ the
  polynomial in the entries n₀ = u − v, n₁ = u_x, n₂ = u_ρ, n₃ = u_xρ given in the script. (iii) det N = W_x W_ρ. (iv) X₁′X₂″ − X₂′X₁″ = −αW_x, and
  pX₁″ + qX₂″ = α(pX₁ + qX₂) + β(pX₁′ + qX₂′).
- **C3 `case_a`.** (i) a + bX + cR + dXR = d(X + c/d)(R + b/d) + (a − bc/d). (ii) d = 0 is a + bX + cR. (iii) X₂ = 1 gives α = 0 and R₂ = 1 gives δ = 0. (iv)
  X(b + dR) + 1·(a + cR) equals the same u.
- **C4 `sep_rank`.** The exact ranks of the coefficient matrix of E in x-monomials × ρ-monomials (v appended to the ρ-side when symbolic) equal, for v = 0, 1/3, 1 and
  symbolic v: full 59, 93, 87, 102; one product (X₂ = 0) 6, 10, 9, 11 (the values of #160); additive (X₂ = 1, R₁ = 1) 5, 5, 5, 5; (b) X₂ = 1: 21 each; (c) R₂ = 1:
  12, 12, 12, 24. Lemma L (#160 §2): Σ_{i ≤ r} F_iG_i = 0 on a box forces d_F + d_G ≤ r.
- **C5 `slack`.** For (X₁, X₂) = (eˣ, e^{κx}) and (R₁, R₂) = (e^ρ, e^{μρ}) with κ, μ transcendental, the exact ranks over ℚ(κ), ℚ(μ) of the spans of the two sides are
  (d_F, d_G) = (12, 22) at v = 0 with r = 59, and (22, 36) at v = 1/3 with r = 93, E is a nonzero polynomial on the pair, and d_F + d_G ≤ r. So Lemma L does not exclude
  this pair, which is not a solution.
- **C6 `rho_const` (Theorem K).** (i) For r = (e^{μ₁ρ}, e^{μ₂ρ}), S_i = (μ_i² + ιμ_i)R_i, ι = 1/ρ, E is a polynomial of degree 2 in ι with ι² coefficient
  −(A₀μ₁w₁ + B₀μ₂w₂)⁴ = −u_ρ⁴ (w_i = e^{μ_iρ}); (ii) its w₁⁴ and w₂⁴ coefficients are −(A₀μ₁)⁴ and −(B₀μ₂)⁴. (iii) For r = (e^{μρ}, ρe^{μρ}) the ρ⁻² coefficient of E as a
  Laurent polynomial in ρ is −e^{4μρ}(μA₀ + B₀)⁴ and no lower power occurs. The consequence (by hand in the note, with the independence of ρ^m e^{ωρ}): no solution
  under (N1), (N2) whose ρ-side has constant ODE coefficients.
- **C7 `add_decomp`.** E at X₂ = 1, R₁ = 1, v = 0 equals Σ_{k ≤ r} f_k(x)g_k(ρ) from the pivot columns of its coefficient matrix, with exact rank r = 5.
- **C8 `add_stratum`.** For the f_k of C7, the elimination of {f_k − k_k} with A₀ free (conditions on k from the A₀-coefficients, then a second Gröbner basis) contains A₂²
  (X″ = 0), and for every constant c the jets (A₀ free, A₁ = c, A₂ = 0) have f independent of A₀.
- **C9 `add_planted_exact`.** For R = −ε ln ψ with ψ″ + ψ′/ρ + 2c²ψ = 0, E_add(X = cx) = 0 identically, ε = ±1.
- **C10 `add_planted`.** For c ∈ {3/10, 1/2, 1, 3/2, 2} (all ≥ 0.3), ε = ±1, R = −ε ln(J₀(z) + 0.3 Y₀(z)), z = √2cρ: f(x) is constant in x, the largest relative residual of
  f·g over 5 points per case is ≤ 1e-50 (130 digits), and the numerical d_G (12 points, singular values below 1e-40 of the largest count as zero) is ≤ 4, so d_F + d_G = 5 = r.
- **C11 `add_perturbed_exact`.** E_add(X = cx, R + δ) with R on the Bessel equation, δ ∈ {ρ²/10, ρ³/10}, ε = ±1, is a nonzero polynomial in (γ, ρ, c) and nonzero at the exact points
  (c, ε, ρ, γ) = (1/2, 1, 1, 1/3), (1, −1, 3/2, 2), (2, 1, 1/2, −1). (An exact test, as the issue asks; #160's thresholded one failed and is not used.)
- **C12 `add_xperturbed`.** For X = cx + x²/10 with the same R, the exact d_F ≥ 2 and the numerical d_G = 4 in all ten cases, so d_F + d_G > 5 = r.

## 5. Planted cases

The additive family u = cx + g(ρ), g = −ε ln(αJ₀(√2cρ) + βY₀(√2cρ)) of `det_classify.md` §3, found through the same E (C7 to C10), with c ≥ 3/10. Perturbed members: X = cx + x²/10
rejected by the rank bound (C12), R + δ rejected by an exact test (C11).

## 6. Controls

Each is `--mutate=NAME`, exits non-zero, and must fire on its target check and on no other. Names and targets as declared in A1 (computed in dev 3, which ran 13 mutations; one of them, `s-rank-drop`, was silent and is replaced by `s-rank-qyz`):
`s-d-sign` (e_two), `s-compact-b` (e_two), `s-ode-alpha` (ode_form), `s-casea-const` (case_a), `s-rank-qyz` (sep_rank), `s-slack-kappa` (slack), `s-rhoconst-iota` (rho_const),
`s-rhoconst-double` (rho_const), `s-add-freq` (add_planted), `s-add-exact` (add_planted_exact), `s-stratum-drop` (add_stratum), `s-pexact-zero` (add_perturbed_exact),
`s-xperturb-zero` (add_xperturbed). No control is planned for C7.

## 7. Development findings that are not criteria

- **Singular, prolongation ideal.** The ideal of E, ∂ₓ^i∂_ρ^j E (i, j ≤ 2) in the jets (n; α, β, γ, δ), saturated by det N·α, did not finish `std` in 5 min (`dev/gen_prol.py`). The same for case (c)
  (u = AR + B, jets A_k, B_k, R_k, ι) at truncations (2,2) and (3,3), 2 min each (`dev/gen_prol_c.py`). No certificate was produced and none is claimed.
- **Numerical formal series** (`dev/formal2.py`, `dev/dev1.log`): Taylor series of α, β, γ, δ and N₀ in Levenberg–Marquardt against the coefficients of s^iρ^j (i ≤ p, j ≤ q) of E. At (3,3) nondegenerate formal solutions exist
  (cost 1e-28; 17 equations, 20 unknowns). At (4,4) and (5,5) the best costs are 3e-8 to 1e-5 in case (d) **and in the planted additive case (a)**, so the planted control is silent and the runs are
  not evidence about (d). Not used anywhere.
- E is irreducible over ℚ; D is quadratic in u_xρ, and 4hD = C² − A² − B² (C1).

## 8. Amendments

**A1 (before the run of record; after dev 3).** Dev 3 ran the 12 checks and 13 mutations. Twelve fired on their target check and on no other: `s-d-sign` and `s-compact-b` (e_two),
`s-ode-alpha` (ode_form), `s-casea-const` (case_a), `s-slack-kappa` (slack), `s-rhoconst-iota` and `s-rhoconst-double` (rho_const), `s-add-freq` (add_planted), `s-add-exact`
(add_planted_exact), `s-stratum-drop` (add_stratum), `s-pexact-zero` (add_perturbed_exact), `s-xperturb-zero` (add_xperturbed). **`s-rank-drop` (the term 8hZ² removed from E before the
ranks) was silent on sep_rank**: it changes the column counts (72 to 67 at v = 0) and leaves every rank unchanged. It is declared silent here, kept as a control that is run and reported
and not counted, and replaced by `s-rank-qyz` (the term 2QYZ removed from D), which changes the ranks at all four v (59 → 56, 93 → 84, 87 → 78, 102 → 93 for the full form; computed in
`dev/probe10` before it was coded). Nothing else changed: no threshold, point, rank or range was moved. The 12 checks pass (dev 2, 72 s).
