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

## Results

| file | what |
|---|---|
| `rerun/` | every `review_lemma_a_*.py` from the branch on the Mac at nice 10, and `review_lemma_a_controls.py` (exit codes and times in `runA.log`) |
| `ind138_run1.py`, `ind138_run1.txt` | run 1 of the independent check: K1a to K1c pass, then a **crash** at K2, a `Poly.diff(r, 2)` call (sympy wants `diff((r, 2))`). A defect of my check |
| `ind138.py`, `ind138_run2.txt` | run 2: only that call changed, criteria unchanged. Exit 0, 14 s, every criterion passes |
| `ind138_mut_*.txt` | its 5 mutations |

**Reruns.** All seven scripts exit 0, with outputs identical to the committed ones apart from timings, and stderr
empty. The controls exit 0 in 200 s, 40 of 40 on target, identical to the committed output. That rerun includes every
mutation, for example `t2_window` on `review_lemma_a_t2.py`: exit 1, first FAIL `T2.6[l=2]`, on target.

**The controls parser.** The first control run on rpi5 said 29 of 40. Each of its 11 misses was read as a bare id
(`Z1`) against a target with a suffix (`Z1[l=2]`). In each run-1 log, the first FAIL line ends with the targeted
`[l=N]`. The matching rule written before that run says such ids match. So the fix applies that rule, and no target
changed.

**ind138 run 2.**

| criterion | result |
|---|---|
| K1a | P₂ = r²(r + 2)(cr − 6), P₁ = −2r(cr² + 3cr − 6), P₀ = −c²r² + 6cr − 12; the coefficient of r^m involves c_m, c_{m−1}, c_{m−2} only |
| K1b | residual 0 as a rational function of (l, m), m ≥ 5; orders 1 to 4 vanish symbolically in l |
| K1c | my normalisation is −1 times RESULTS'; middle coefficient −2(m − 2)(c(m − 4) − 3(m − 1)), as #138's W1 says |
| K2 | the χ-ODE residual is exactly 0 at l = 41, 45, 60, 100 |
| K3 | exponents 0 and 3; χ′/χ(r_s) = −1/(r_s(r_s + 2)); (P₁′ + P₀)P₀ − P₀′P₁ = 0 at r_s, so χ″(r_s) = 0 |
| K4 | the per-term identity holds symbolically in n. The cubic is g(u) = 9(12ε²u³ + 18εu³ − 18εu² + 6u³ − 9u² + 4)/4 with u = r/r_s, critical point u* = 1/(1 + ε) ∈ [0, 1], minimum 9/4 + (27/4)ε²/(1 + ε)², as #138 says |
| K5 | l = 2..30, 50, 150: d₀ > 0, d₁ = −d₀/(r_s(r_s + 2)), d₂ = 0, d_m > 0 for m ≥ 4, one sign change; d₃ > 0 at every l tested. One root of N beyond r_s (l ≤ 50) |
| K6 | no root of N in [0, r_s], N(0) = 9 (l ≤ 50) |

**Mutations:** `ode`, exit 1, K1a to K3 fail; `cn`, exit 1, K1b, K2 and K5 fail; `rs`, exit 1, K3 fails;
`cubic`, exit 1, K4 fails; `shift`, exit 1, K5 fails. All on target.
