# I264-rpi5 derivations: E4 (k = 6), E2W and E5 (k = 7), written before any comparison with omega4.md or omega5.md

Runner `negative-mass-rpi5-i264`, issue #264. Written 2026-11-27 (rpi5 clock), before any comparison and before any script of this
review ran. Status words as in AGENTS.md: *proved* (by hand, each step with its boundary terms), *checked symbolically* (sympy, planned
in `identity_review.py sym`), *checked numerically* (planned in `identity_review.py exch`). Nothing below has been run yet. Where a step
was found by sympy rather than by hand, it says so.

## 0. What I read before writing this, and what I did not

Read in full: AGENTS.md, issue #264 and its widening comment, the three handovers `i209`, `i220`, `i263` of my auto-memory,
`notes/wormhole_largeD/README.md`, and `notes/wormhole_largeD/exchange_review.md` (#209: E1 to E3 and the Clausen integrals, which I
reuse as established).

Read from `omega4.md`: lines 68 to 83 (the order equations, the definition of c₆) and 93 to 98 (the *statement* of E4: w₄, W₄, and
∫Y₄w₄ = −2∫(22ℓ² − 8Ω₀ℓ − 2Ω₁ + 16uC)F₃). Read from `omega5.md`: lines 74 to 86 (the order equations, the definition of c₇) and 98 to 105
(the *statements* of E2W: g₄ and P, and of E5: w₄′, W and ∫Y₄w₄′ = −2∫WuF₃). Those lines also carry short sketches: for E2W the
sentence "from (L cot θ)′ = 2h/S and L cot θ → 0 at π/2 (G_m = 0): ∫L_m g = −2∫P h_m/S with P′ = g tan θ, P(0) = 0", for E5 the
cancellation of ∫C cot θ between 32∫uC/S and −16∫D₃/S, and a one-line boundary remark. I saw them. So the key equation of E2W and the
shape of the E5 primitive were not found by me; what I did from the order equations alone is below: the equations (L cot θ)′ = 2h/S
and the by-parts lemmas with their conditions (§2), the growth and throat bounds (§1), the Y and L weights at k = 6 and 7 by tracking
each term through the chain (§4, §5), the primitives, and every boundary term (§3). The handovers `i220` and `i263`, which the task told me to read, state
w₄ and W₄ (`i220`) and name E2W, E5 and the cancellation of Z (`i263`).

Not read before this file was committed: `omega4.md` outside the lines above, `omega5.md` outside them, `order6.py`, `order7.py`,
`PanelK`, `order6_output.txt`, `order7_output.txt`, the raw folders `I220-rpi5`, `I263-rpi5`, the coordinator's `I220-mac-review` and
`I263-mac-review`. Read for the hierarchy design: nothing; I write my own (§7).

## 1. Setting, order equations, growth and throat bounds

Variables as in #209: R = r^s = sec²θ, u = tan θ = √(R−1), l = ln R = −2ℓ, ℓ = ln cos θ, S = sin²θ = 1 − 1/R, θ ∈ [0, π/2),
x = π/2 − θ. Facts: dl/dθ = 2u, dℓ/dθ = −u, d(cot θ)/dθ = −1/S, 1/R = cos²θ = 1 − S.

**Order equations from the master equation.** From README's exact system Y_R = ε L r/R, (R−1)L_R = (1+εΩ) r Y + L/(2R) +
(½+ε)L(R−1)/R − (½+ε)Y(R−1)/(R r) − Y/(2rR), r = e^{εl}, Ω = Σ ε^iΩ_i, write d/dl = R d/dR and (R−1)L_R = S dL/dl. Then
dY/dl = εLe^{εl}, and S L′ − L/(2R) − (½+ε)SL = Y·[(1+εΩ)e^{εl} − (½+ε)Se^{−εl} − e^{−εl}/(2R)]. Because S + 1/R = 1 the bracket is

  K(ε) = (1+εΩ)e^{εl} − ½e^{−εl} − εS e^{−εl},    c_m = [ε^m]K, c₀ = ½,

and the left side is S L′ − L/2 − εSL. So with Y = ΣεᵏY_k, L = ΣεᵏL_k:

  dY_k/dl = F_{k−1} = Σ_{j<k} L_{k−1−j} l^j/j!,   S L_k′ − L_k/2 = h_k = S L_{k−1} + S_k + ½Y_k,   S_k = Σ_{j<k} Y_j c_{k−j}.

In ℓ (l = −2ℓ), with Ω_i the coefficients of Ω:

  c_m = Σ_{i=0}^{m−1} Ω_i (−2ℓ)^{m−1−i}/(m−1−i)! + [1 − ½(−1)^m](−2ℓ)^m/m! − S (2ℓ)^{m−1}/(m−1)!.

So c₁ = Ω₀ − 3ℓ − S, c₂ = Ω₁ − 2Ω₀ℓ + ℓ² − 2Sℓ, c₃ = Ω₂ − 2Ω₁ℓ + 2Ω₀ℓ² − 2ℓ³ − 2Sℓ². c_m at l = 0, R = 1 (ℓ = 0, S = 0) is Ω_{m−1}.
The solution analytic at the throat: L_k = −2Ω_{k−1} + uC_k, C_k = 2∫₀^θ (h_k − Ω_{k−1})/S dφ, G_k = C_k(π/2), and Y_k(l = 0) = 0.
**Hypothesis H_k:** G_j = 0 for 2 ≤ j ≤ k − 1 (Ω₀ … Ω_{k−3} at their roots); Ω_{k−2} is free.

**Throat bounds (T).** h_k(R = 1) = Y₀c_k(0,1) = Ω_{k−1} (Y_j(0) = 0, j ≥ 1), so h_k − Ω_{k−1} = (R−1)a_k with a_k analytic in R − 1 =
tan²θ, by induction. Then C_k = 2∫₀^θ a_k sec²φ dφ is odd and analytic in θ, C_k = O(θ), L_k = −2Ω_{k−1} + O(θ²), and Y_k = ∫₀^l F_{k−1}
= O(l) = O(θ²) for k ≥ 1.

**Growth bounds (G).** Under H_k, with x → 0: L_j, h_j (j ≤ k−1), Y_j (j ≤ k), F_j are O(l^p) for some p, and C_j(θ) = O(x l^q).
Proof by induction on j. L₀ = −1. If L_i are O(l^p) for i < j, then h_j = S L_{j−1} + S_j + ½Y_j is O(l^q) (c_m are polynomials in l
and S, Y_i = ∫F_{i−1}dl is a polynomial in l at most of degree growth +1). Since G_j = 0, C_j(θ) = −2∫_θ^{π/2}(h_j − Ω_{j−1})/S dφ. On
[π/4, π/2], 1/S ≤ 2 and l(φ) is increasing, so |C_j(θ)| ≤ 4K ∫_θ^{π/2} l(φ)^q dφ ≤ 4K x l(θ)^q. Then u C_j = O(x⁻¹ x l^q) = O(l^q) because
tan θ = cot x ≤ 1/x. So L_j = O(l^q), and Y_{j+1} = ∫₀^l F_j = O(l^{q+1}). Without G_j = 0, C_j(θ) → G_j and L_j ≈ G_j tan θ, which is not O(l^p).
Consequence: for every term below the integrals converge at both ends (an integrand is a polynomial in l times a bounded function at π/2,
and ∫₀^{π/2} l^n dθ < ∞; at 0 it is bounded by (T)), so splitting integrals is legal, and ∫₀^{π/2} is an ordinary integral.

## 2. Two lemmas, from which every identity follows

**Equation for L in θ.** (R−1) dL/dR = tan²θ L_θ/(2 sec²θ tan θ) = ½ sin θ cos θ L_θ, so the L equation is sin θ cos θ L_θ − L = 2h.
Dividing by sin²θ:

  (L_m cot θ)′ = 2h_m/S.                                                               (2.1)

**Lemma Y (by parts for Y_m).** Let w be a function on (0, π/2) and W an antiderivative, W′ = w. Since dY_m/dθ = 2uF_{m−1} (m ≥ 1),

  ∫₀^{π/2} w Y_m dθ = [W Y_m]₀^{π/2} − 2∫₀^{π/2} u W F_{m−1} dθ.

*Conditions.* At θ = 0: Y_m = O(θ²) (T), so [W Y_m] → 0 when W = o(θ⁻²), which holds when w = O(θ⁻²) (then W = O(θ⁻¹)).
At π/2: Y_m = O(l^p) (G), so [W Y_m] → 0 when W = O(x l^s). That holds when W(π/2) = 0 and w = O(l^s): W(θ) = −∫_θ^{π/2} w is
O(x l^s). *W is not free:* W + K has the boundary term K Y_m(π/2^−), which diverges like l^p. The constant is fixed by W(π/2) = 0.
The integrals converge (§1). So the lemma is proved for each w, W below.

**Lemma L (weighted exchange for L_m).** Let g be a function and P an antiderivative of g tan θ with P(0) = 0, P′ = g tan θ. By (2.1),
with g = P′ cot θ,

  ∫₀^{π/2} g L_m dθ = [P L_m cot θ]₀^{π/2} − 2∫₀^{π/2} P h_m/S dθ.

*Conditions.* At 0: g bounded gives P = O(θ²), and L_m cot θ = −2Ω_{m−1}/θ + O(θ), so the product is O(θ). At π/2: L_m cot θ = −2Ω_{m−1} cot θ +
C_m = O(x l^q) uses **G_m = 0** (G), and P = O(l^s) for g = O(l^{s−1}): the product is O(x l^{q+s}) → 0. The right side converges: at 0,
P = O(θ²), h_m bounded, 1/S = O(θ⁻²). With G_m ≠ 0, L_m ≈ G_m tan θ ≈ G_m/x at π/2, so g L_m ~ g G_m/x and ∫ g L_m diverges (logarithmically for g(π/2) ≠ 0, and with
powers of ln x when g contains ℓ), and L_m cot θ → G_m, so the boundary term P·G_m also diverges. The identity then has no meaning.
So E2W and E2 need G_m = 0, not just a bounded L_m.

E1, E2, E3 as special cases (these are #209's, re-derived in this form):
- w = 1/S, W = −cot θ (W(π/2) = 0): uW = −1, so ∫Y_k/S = 2∫F_{k−1}. This is E1 with the boundary [−cot θ Y_k] = O(θ) at 0.
  With G_k = 2∫(h_k − Ω_{k−1})/S dθ and h_k = SL_{k−1} + S_k + ½Y_k:
  **E1:** G_k = 4∫L_{k−1} + 2∫(F_{k−1} − L_{k−1}) + 2∫(S_k − Ω_{k−1})/S.
- g = 1, P = −ℓ (P′ = tan θ = −ℓ′, P(0) = 0): **E2:** ∫L_m = 2∫ℓ h_m/S (needs G_m = 0).
- w = (4ℓ + 2c₁)/S = 2P_E′ with P_E = cot θ(ℓ − Ω₀): since c₁ = Ω₀ − 3ℓ − S, (4ℓ + 2c₁)/S = 2(Ω₀ − ℓ)/S − 2, and
  P_E′ = −(ℓ − Ω₀)/S − 1. W = 2P_E is O(x l) at π/2 and −2Ω₀/θ at 0. uW = 2(ℓ − Ω₀). So
  **E3:** ∫Y_m (4ℓ + 2c₁)/S = −4∫(ℓ − Ω₀)F_{m−1}.

## 3. Boundary terms of every step used (the table asked for by the issue)

| step | boundary term | at θ = 0 | at θ = π/2 | uses |
|---|---|---|---|---|
| E1 at k | [−cot θ Y_k] | O(θ): −cot θ·Y_k ≈ −F_{k−1}(0)θ = 2Ω_{k−2}θ | O(x l^p) | Y_k = O(θ²), G |
| E2 at m | [P L_m cot θ], P = −ℓ | ℓ = O(θ²), L_m cot θ = O(θ⁻¹): O(θ) | O(x l^{q+1}) | G_m = 0 |
| E3 at m | [2P_E Y_m], P_E = cot θ(ℓ − Ω₀) | 2P_E ≈ −2Ω₀/θ, Y_m ≈ −2Ω_{m−2}θ²: O(θ), leading 4Ω₀Ω_{m−2}θ | O(x l^{p+1}) | Y_m = O(θ²), G |
| E4 on Y₄ (k = 6) and on Y₅ (k = 7) | [W₄ Y_n] | W₄ = −2Ω₁/θ + O(θ), Y_n = O(θ²): O(θ) | W₄ = O(x l²) + 16C, C = Cl₂(2x) = O(x ln x): O(x l^s) | Ω₀, Ω₁ roots (the θ term of W₄ cancels, W₄(π/2) = 0) |
| E2W on L₄ | [P L₄ cot θ] | P = 2Ω₁θ² + …, L₄ cot θ = O(θ⁻¹): O(θ) | P = O(l³) (ℓ³, and uC = O(l)), L₄ cot θ = O(x l^q): O(x l^{q+3}) | G₄ = 0 |
| E5 on Y₄ | [W Y₄] | W = −2Ω₂/θ + O(θ): O(θ) | W(π/2) = 0, W = O(x l^s) | Ω₀, Ω₁ roots (W(π/2) = 0 needs them, §5) |

All boundary terms tend to 0 under H_k, so the identities hold as stated, with ordinary integrals. #209's O(θ³) is for ℓ C_m,
a different product from the L_m cot θ P used here.

## 4. k = 6: E4

**The chain (m = 5, H₆: Ω₀ … Ω₃ roots, Ω₄ free).**

1. E1 at k = 6: G₆ = 4∫L₅ + 2∫(F₅ − L₅) + 2∫(S₆ − Ω₅)/S.
2. E2 at m = 5 (G₅ = 0): 4∫L₅ = 8∫ℓ L₄ + 8∫ℓ S₅/S + 4∫ℓ Y₅/S, from h₅ = S L₄ + S₅ + ½Y₅.
3. E3 at m = 5: Y₅'s weight is 4ℓ/S (step 2) + 2c₁/S (from S₆ = S₆′ + Y₅c₁) = 2P_E′, so these two give −4∫(ℓ − Ω₀)F₄.
4. L₄ weight: 8ℓ (step 2) + 2l (F₅ − L₅ ∋ L₄ l) − 4(ℓ − Ω₀) (F₄ ∋ L₄) = 8ℓ − 4ℓ − 4ℓ + 4Ω₀ = 4Ω₀. So the L₄ terms are 4Ω₀∫L₄.
5. E2 at m = 4 (G₄ = 0): 4Ω₀∫L₄ = 8Ω₀∫ℓ L₃ + 8Ω₀∫ℓ S₄/S + 4Ω₀∫ℓ Y₄/S.
6. Y₄ terms: 4Ω₀ℓ/S (step 5), 8ℓc₁/S (S₅ ∋ Y₄c₁ in step 2), 2c₂/S (S₆′ ∋ Y₄c₂):
   w₄ = (4Ω₀ℓ + 8ℓc₁ + 2c₂)/S. With c₁ = Ω₀ − 3ℓ − S, c₂ = Ω₁ − 2Ω₀ℓ + ℓ² − 2Sℓ:
   8ℓc₁ = 8Ω₀ℓ − 24ℓ² − 8Sℓ, 2c₂ = 2Ω₁ − 4Ω₀ℓ + 2ℓ² − 4Sℓ, so the numerator is 2Ω₁ + 8Ω₀ℓ − 22ℓ² − 12Sℓ and

     **w₄ = (2Ω₁ + 8Ω₀ℓ − 22ℓ²)/S − 12ℓ.**
7. Primitive. ∫1/S = −cot θ; ∫ℓ/S = −cot θ ℓ − θ (d(cot θ ℓ) = −ℓ/S − 1); ∫ℓ²/S = −cot θ ℓ² − 2∫ℓ (d(cot θ ℓ²) = −ℓ²/S − 2ℓ); ∫ℓ dθ = C/2 − θ ln 2, from
   C = Cl₂(π − 2θ), C′ = 2 ln(2 cos θ) = 2(ℓ + ln 2) (#209 S9). So
   ∫w₄ = 2Ω₁∫1/S + 8Ω₀∫ℓ/S − 22∫ℓ²/S − 12∫ℓ = −2Ω₁ cot θ − 8Ω₀(cot θ ℓ + θ) + 22 cot θ ℓ² + (44 − 12)∫ℓ
   = cot θ(22ℓ² − 8Ω₀ℓ − 2Ω₁) − 8Ω₀θ + 32(C/2 − θ ln 2), so

     **W₄ = cot θ(22ℓ² − 8Ω₀ℓ − 2Ω₁) + 16C − (8Ω₀ + 32 ln 2)θ,**

   and Ω₀ = −4 ln 2 (G₂ = 0) kills the last term. W₄(π/2) = 0 (cot θ → 0, C → 0). uW₄ = 22ℓ² − 8Ω₀ℓ − 2Ω₁ + 16uC.
8. Lemma Y with m = 4 (conditions of §2 and the table: W₄ = O(1/θ) at 0, w₄ = O(θ⁻²); W₄ = O(x l²) at π/2):

     **E4:** ∫₀^{π/2} Y₄ w₄ dθ = −2∫₀^{π/2}(22ℓ² − 8Ω₀ℓ − 2Ω₁ + 16uC) F₃ dθ,   F₃ = L₃ + L₂l + ½L₁l² + ⅙L₀l³.

   It needs Ω₀ and Ω₁ at their roots (θ terms of W₄ cancel; L₃ and Y₄ bounded), and Y₄ = O(θ²) and polynomial in l. It does not use Ω₂.
   In the form used in the chain it is the one extra step beyond E1 … E3: it removes Y₄, and with it every Y_j, j ≥ 4.
9. The reduced form. Every term with Y₄ or higher or with L₄ or higher is gone:

   G₆ = 8Ω₀∫ℓL₃ + 8Ω₀∫ℓS₄/S + 8∫ℓS₅″/S + 2∫(L₃l²/2 + L₂l³/6 + L₁l⁴/24 + L₀l⁵/120)
        − 4∫(ℓ − Ω₀)(L₃l + L₂l²/2 + L₁l³/6 + L₀l⁴/24) + 2∫(S₆″ − Ω₅)/S − 2∫(22ℓ² − 8Ω₀ℓ − 2Ω₁ + 16uC)F₃,

   with S₄ = Σ_{j≤3}Y_jc_{4−j}, S₅″ = Σ_{j≤3}Y_jc_{5−j}, S₆″ = Σ_{j≤3}Y_jc_{6−j}. (G₆ is affine in Ω₄ through Y₀c₆, Y₁c₅ and the
   c₅, c₆ in S₅″, S₆″; Ω₅ cancels in S₆″ − Ω₅ because c₆ ∋ Ω₅.)

## 5. k = 7: E2W and E5

**The chain (m = 6, H₇: Ω₀ … Ω₄ roots, Ω₅ free).**

1. E1 at k = 7: G₇ = 4∫L₆ + 2∫(F₆ − L₆) + 2∫(S₇ − Ω₆)/S.
2. E2 at m = 6 (G₆ = 0): 4∫L₆ = 8∫ℓL₅ + 8∫ℓS₆/S + 4∫ℓY₆/S.
3. E3 at m = 6: Y₆'s weight (4ℓ + 2c₁)/S, giving −4∫(ℓ − Ω₀)F₅.
4. L₅ weight: 8ℓ + 2l − 4(ℓ − Ω₀) = 4Ω₀. E2 at m = 5 (G₅ = 0): 4Ω₀∫L₅ = 8Ω₀∫ℓL₄ + 8Ω₀∫ℓS₅/S + 4Ω₀∫ℓY₅/S.
5. Y₅ terms: 4Ω₀ℓ/S (step 4), 8ℓc₁/S (S₆ ∋ Y₅c₁), 2c₂/S (S₇ ∋ Y₅c₂): the same weight w₄ as at k = 6. Lemma Y at m = 5:
   ∫Y₅w₄ = −2∫(22ℓ² − 8Ω₀ℓ − 2Ω₁ + 16uC)F₄, F₄ = L₄ + L₃l + ½L₂l² + ⅙L₁l³ + (1/24)L₀l⁴ (E4 one level up; [W₄Y₅] = O(θ) at 0, O(x l^s) at π/2).
6. L₄ weights: from step 4: 8Ω₀ℓ; from F₆ − L₆ ∋ L₄l²/2, times 2: l² = 4ℓ²; from E3: −4(ℓ − Ω₀)·L₄l = 8ℓ(ℓ − Ω₀);
   from step 5: −2(22ℓ² − 8Ω₀ℓ − 2Ω₁ + 16uC). Sum:

     **g₄ = −32ℓ² + 16Ω₀ℓ + 4Ω₁ − 32uC.**   (ℓ²: 4 + 8 − 44; Ω₀ℓ: 8 − 8 + 16; constants 4Ω₁; uC: −32.)
   Of it, 12ℓ² comes from F₆ − L₆, F₅ and step 4 (4ℓ² + 8ℓ² and the Ω₀ℓ terms 8 − 8 cancel), and −2(22ℓ² − 8Ω₀ℓ − 2Ω₁ + 16uC) from E4's step.
7. Lemma L for L₄ (G₄ = 0): P′ = g₄ tan θ = u g₄. With ∫uℓ^n = −ℓ^{n+1}/(n+1) (ℓ′ = −u) and ∫u = −ℓ, ∫u²C: u² = sec²θ − 1, so
   ∫u²C = uC − ∫u C′ − ∫C = uC − 2∫u(ℓ + ln 2) − D₃/2 = uC + ℓ² + 2 ln 2 ℓ − D₃/2, where D₃ := ∫₀^θ 2C dφ (D₃′ = 2C, D₃(0) = 0). Hence

     **P = (32/3)ℓ³ − 8Ω₀ℓ² − 4Ω₁ℓ − 32(uC + ℓ² + 2 ln 2 ℓ − D₃/2)**, P(0) = 0.

   (−32∫uℓ² = (32/3)ℓ³, 16Ω₀∫uℓ = −8Ω₀ℓ², 4Ω₁∫u = −4Ω₁ℓ, −32∫u²C as above.) Then

     **E2W:** ∫₀^{π/2} g₄ L₄ dθ = −2∫₀^{π/2} P h₄/S dθ,  h₄ = S L₃ + S₄ + ½Y₄.

   The weight 12ℓ² alone has P_a = −4ℓ³ (P_a′ = 12ℓ²u: d(ℓ³) = −3ℓ²u dθ), and the same lemma applies (check E2Wa in the plan).
   After E2W: −2∫PL₃ − 2∫PS₄/S − ∫PY₄/S.
8. Y₄ weights: 8Ω₀ℓc₁/S (from step 4's 8Ω₀∫ℓS₅/S ∋ Y₄c₁), 8ℓc₂/S (step 2's S₆ ∋ Y₄c₂), 2c₃/S (S₇ ∋ Y₄c₃), −P/S (step 7):

     w₄′ = (8Ω₀ℓc₁ + 8ℓc₂ + 2c₃ − P)/S.

   With c₃ = Ω₂ − 2Ω₁ℓ + 2Ω₀ℓ² − 2ℓ³ − 2Sℓ², by hand: 8Ω₀ℓc₁ + 8ℓc₂ + 2c₃ = 2Ω₂ + (4Ω₁ + 8Ω₀²)ℓ − 36Ω₀ℓ² + 4ℓ³ − S(20ℓ² + 8Ω₀ℓ), and
   −P = −(32/3)ℓ³ + 8Ω₀ℓ² + 4Ω₁ℓ + 32uC + 32ℓ² + 64 ln 2 ℓ − 16D₃, so

     **w₄′ = [2Ω₂ + (8Ω₁ + 8Ω₀² + 64 ln 2)ℓ + (32 − 28Ω₀)ℓ² − (20/3)ℓ³ + 32uC − 16D₃]/S − 20ℓ² − 8Ω₀ℓ.**
9. Primitive W with W′ = w₄′ and W(π/2) = 0. The pieces:
   - ∫ℓ^b/S = −cot θ ℓ^b − b Lc_{b−1}, Lc_n(θ) := ∫₀^θ ℓⁿ dφ (Lc₀ = θ, Lc₁ = (C − 2θ ln 2)/2); by parts, d(cot θ ℓ^b) = −ℓ^b/S − bℓ^{b−1}.
   - uC/S = C/(sin θ cos θ) = C cot θ + C tan θ. Let Z = ∫C cot θ. ∫C tan θ = −Cℓ + ∫ℓC′ = −Cℓ + 2Lc₂ + 2 ln 2 Lc₁.
   - ∫D₃/S = −cot θ D₃ + ∫cot θ · 2C = −cot θ D₃ + 2Z.
   So 32∫uC/S − 16∫D₃/S = 32Z + 32∫C tan θ + 16 cot θ D₃ − 32Z: **Z cancels** and what is left is elementary in Lc₁, Lc₂, C, D₃.
   With a₁ = 8Ω₁ + 8Ω₀² + 64 ln 2, a₂ = 32 − 28Ω₀, a₃ = −20/3:

     W = −2Ω₂ cot θ − a₁(ℓ cot θ + θ) − a₂(ℓ² cot θ + 2Lc₁) − a₃(ℓ³ cot θ + 3Lc₂) + 32(−Cℓ + 2Lc₂ + 2 ln 2 Lc₁) + 16 D₃ cot θ − 20 Lc₂ − 8Ω₀ Lc₁ + K.

   **K = 0 exactly when Ω₀ and Ω₁ are at their roots.** At π/2 the cot terms and Cℓ vanish, Lc₁(π/2) = J₁ = −(π/2) ln 2,
   Lc₂(π/2) = J₂ = (π/2)(ln²2 + π²/12) (§8). So

     W(π/2) = K − a₁π/2 − 2a₂J₁ + (−3a₃ + 64 − 20)J₂ + (64 ln 2 − 8Ω₀)J₁,   and −3a₃ + 44 = 64.

   With Ω₀ = −4 ln 2, Ω₁ = 2π²/3 + 8 ln²2 the five terms are −(8π³/3 + 96π ln²2 + 32π ln 2), +(32π ln 2 + 112π ln²2), +(32π ln²2 + 8π³/3)
   and −48π ln²2 (the last from (64 ln 2 − 8Ω₀)J₁ = −(π/2) ln 2 (96 ln 2)): they sum to 0 in π³, π ln²2 and π ln 2 separately (by hand).
   So K = 0 under H₇. For other Ω₁ the constant is nonzero, and the boundary term [W Y₄] would carry K·Y₄(π/2⁻) = ∞: the identity then fails.
10. Lemma Y with m = 4: W = −2Ω₂/θ + O(θ) at 0 (all other terms are odd in θ and O(θ)), O(x l^s) at π/2:

     **E5:** ∫₀^{π/2} Y₄ w₄′ dθ = −2∫₀^{π/2} W u F₃ dθ.

11. The reduced form of G₇ (Y₀ … Y₃, L₀ … L₃ only):

   G₇ = 8Ω₀∫ℓS₅″/S + 8∫ℓS₆″/S + 2∫(S₇″ − Ω₆)/S − 2∫P S₄/S − 2∫P L₃ + 2∫(L₃l³/6 + L₂l⁴/24 + L₁l⁵/120 + L₀l⁶/720)
        − 4∫(ℓ − Ω₀)(L₃l²/2 + L₂l³/6 + L₁l⁴/24 + L₀l⁵/120) − 2∫(22ℓ² − 8Ω₀ℓ − 2Ω₁ + 16uC)(L₃l + L₂l²/2 + L₁l³/6 + L₀l⁴/24) − 2∫W u F₃,

   with S_n″ = Σ_{j≤3}Y_jc_{n−j} (S₄ = S₄″). Here the L₄ and Y₄ coefficients vanished: L₄ through E2W, Y₄ through E5.

## 6. What a mistake in each identity would do (used to set the mutations)

- E4's 22: the identity holds for the true w₄ only; with 20ℓ² in the right-hand side the difference is 4∫ℓ²F₃, which is not zero (the plan computes it).
- E2W's g₄ and P are tied (P′ = u g₄): a wrong P (for example without the D₃ term) fails E2Wb by ∫(D₃)h₄/S-type terms.
- E5's W: K = 0 and the Z cancellation. A W with the D₃ cot θ term dropped fails by 16∫D₃ cot θ·u F₃-type terms.
- The hypothesis: G₄ ≠ 0 (Ω₂ shifted) makes E2W fail; Ω₂ shifted leaves E4 true (E4 uses L₃, G₃ = 0 only).

## 7. Plan for the hierarchy (not run yet)

A Taylor-jet hierarchy of my own: the order equations of §1 (c_m by sympy from K(ε), no table), the solution analytic at the throat
(Frobenius recursion at l = 0, power series in l about centers l_c = 1, 2, … with step 1), fixed-point integers (Python ints) at 400 to
512 bits, orders Y₀ … Y₇, L₀ … L₆, and θ-integrals by Gauss–Legendre panels in v = √l (dθ = v dv/u, analytic in v), truncated at
l ≈ 340 (e^{−170}). C and D₃ from mpmath's `clsin(2, π − 2θ)` and `D₃ = (3/4)ζ(3) + clcos(3, π − 2θ)`, cross-checked by nested
quadrature at a few θ. The throat, G_j = 0 at the closed forms of Ω₀ … Ω₄, and Y₁, L₁, Y₂, L₂ against README's closed forms are
the planted truth.

## 8. Moments (what I can state by hand without Fourier series)

J_n = ∫₀^{π/2} ℓⁿ dθ = B^{(n)}(0), with B(a) = ∫₀^{π/2} cos^aθ dθ = (√π/2)Γ((a+1)/2)/Γ(a/2 + 1). With lt = ln(2 cos θ) = ℓ + ln 2,
B̃(a) = ∫(2 cos θ)^a = 2^aB(a) = (π/2)Γ(1 + a)/Γ(1 + a/2)² (Legendre duplication), and
ln[Γ(1+a)/Γ(1+a/2)²] = Σ_{k≥2}(−1)^k ζ(k)(1 − 2^{1−k})a^k/k: the γ terms cancel, so the moments of lt are polynomials in π and ζ(odd) with
no ln 2. J₁ = −(π/2) ln 2, J₂ = (π/2)(ln²2 + π²/12). D₃ = (3/4)ζ(3) + Cl₃(π − 2θ) (D₃(0) = 0 since Cl₃(π) = −(3/4)ζ(3)); D₃(π/2) = (7/4)ζ(3).

The averages ∫ℓ²D₃, ∫lt²C², ∫lt³D₃ are *not* derived here. The second route for them is numerical (quadrature of the definitions at ≥ 60
digits, no series) and a PSLQ identification of that value; the closed forms of the notes are compared with it after this file is
committed. By parts only: ∫ℓ²D₃ = J₂D₃(π/2) − 2∫Lc₂C.

## 9. Finite parts (a lemma, not a calculation)

For f with an expansion at π/2 in x^a ln^b x, define FP∫₀^{π/2} f as the constant term (x⁰ ln⁰ x) of ∫₀^{π/2−x} f dθ as x → 0.
(a) FP is linear, and FP∫ = ∫ when f is integrable. (b) A convergent integrand split into divergent pieces: ∫ = Σ FP∫ pieces, since at
each finite cutoff the integral of the sum is the sum of the integrals, and the constant term of a finite sum of expansions is the sum
of constant terms. (c) By parts at the cutoff: FP∫fg′ = FP[fg]_{x=0-end} − FP∫f′g + [fg]_{θ=0}, where FP[fg] is the constant term of
(fg)(π/2 − x). It is exact at every cutoff, so exact for the constant term. (d) No oscillating terms occur: the expansions at π/2 of
ℓ, C = Cl₂(2x) = 2x(1 − ln 2x) + O(x³), D₃ = (7/4)ζ(3) + O(x² ln x), cot θ = x − x³/3 + …, tan θ = 1/x + x/3 + … are series in x with
polynomial-in-ln x coefficients, so FP is well defined. These four statements are the whole calculus; the numerical test planned
is a planted split (a convergent integral written as two divergent finite parts, evaluated by the rule and by direct quadrature).
