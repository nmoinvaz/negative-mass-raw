# I138-rpi5: independent review of dg_proof Lemma A, L1, T1 and T2 for every l (RESULTS.md §1, §3, §4 notation)

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process at a time, nice 10, one thread.
Issue: https://github.com/nmoinvaz/negative-mass/issues/138
Worktree: `~/Source/negative-mass-i138`, branch `wip/i138-lemma-a` (base main b61a56b).
Python: `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0, mpmath 1.3.0). Exact arithmetic only (sympy, `fractions.Fraction`); no floats, no tolerances.

The review is written from `phase2/dg_proof/RESULTS.md` alone (§1 Lemma A and L1, §3 Corollary T1/T2, the notation of §4 and the static Zerilli V of §4.2).
Not opened before step 7: `chi_lemma.py`, `lemmas_all_l.py`, `threshold_lemmas.py`, `verify_small_l.py`, `common.py`, any other script of `phase2/`,
every `*_output.txt` of those, and #104's `review_large_l_*.py`.
What this review shares with #2: the formulas typed from RESULTS.md (c_n of Lemma A, V of §4.2, f, N, the T1 bracket, the T2 statement). Nothing else.
Hand derivations done before any code (c = (l+2)(l-1), L = l(l+1), K = cL, r_s = 6/c, D = cr-6, f = (r+2)/r):
P2 = -r^2(r+2)D, P1 = 2r(c r^2 + 3c r - 6), P0 = c^2 r^2 - 6c r + 12 (from V of §4.2); recurrence on r^m:
12(m-1)^2 c_m + (m-2)(6(m-1) - 2c(m-4)) c_{m-1} + c(c-(m-2)(m-5)) c_{m-2} = 0; at r_s: P2' = -6r_s(r_s+2), P1 = 12 r_s(r_s+2), P0 = 12, exponents 0 and 3;
N = sum c_n [c(1-n) r^n + 6n r^{n-1}]; T1 cubic = 9 - (9/16)(1+2e)rho^2 + (1/16)(1+2e)(1+e)rho^3 with rho = cr, e = 1/c, minimum 9 - (27/4)(1+2e)/(1+e)^2.
The scripts check these; none of them is assumed.

Files (all in `phase2/dg_proof/`, each `X.py` with `X_output.txt`): `review_lemma_a_common.py` (shared formulas, planted problems, check harness),
`review_lemma_a_signs.py`, `review_lemma_a_recur.py`, `review_lemma_a_zerilli.py`, `review_lemma_a_l1.py`, `review_lemma_a_t1.py`, `review_lemma_a_t2.py`,
`review_lemma_a_controls.py`, and the note `review_lemma_a.md`.

Conventions. Every script prints one line per check, `PASS <id>` or `FAIL <id>: ...`. Exit 0: all pass. Exit 1: a real check failed. Exit 2: a planted check (PL*)
failed; the script stops before any real data. `--mutate=NAME` switches on one deliberate error (below). A check never changes after seeing data.
Every script begins with the planted checks it depends on (listed per script), through the same code that runs on real data.

## Planted problems (written first; run before any real data)

- PL1. Recurrence extractor (ODE P2 y'' + P1 y' + P0 y = 0 -> coefficients of the shifted terms on x^n) on E1: (1+x)^2 y'' - (N+M-1)(1+x) y' + N M y = 0, whose
  solutions are (1+x)^N and (1+x)^M. Pass: exact residual 0 on a_k = C(7,k) (N=7, M=4) and on C(4,k) for k = -2..12; and the symbolic
  identity in (N, M, k) for a_k = C(N,k) (ratios (N-k)/(k+1) and (N-k)(N-k-1)/((k+1)(k+2))) is exactly 0.
- PL2. Same extractor, a wrong planted sequence a_k = C(7,k) + [k=3] must give a nonzero residual (the check can fail).
- PL3. Exponents at a regular singular point from (P2, P1, P0, x0): three planted ODEs built from two known solutions by the Wronskian determinant, not by the code under test:
  E2 at x0 = 3/2 with y1 = 1 + 2t + 5t^2, y2 = t^3 (1+x), t = x - x0 -> exponents {0, 3};
  E3 at x0 = 3/2 with y1 = 1 + t^2, y2 = t^7 (x^2+3) -> {0, 7};
  E4: x y'' + (1/2) y' - y = 0 at x0 = 0 (solutions cosh(2 sqrt x), sqrt x sinh(2 sqrt x)) -> {0, 1/2}.
  Pass: the routine returns exactly these sets. Also the double-root case t y'' + y' = 0 returns {0} with multiplicity 2 (exponents {0, 0}).
- PL4. Relations at the singular point (y' and y'' of the exponent-0 solution from the ODE and its derivative, and the resonance condition coefficient 2P2'+P1):
  E2: y1'(x0)/y1(x0) = 2, y1''(x0) = 10, 2P2'+P1 = 0 and the second-differentiated ODE is satisfied by y1 (no log);
  E4: y'(0) = 2, y''(0) = 4/3 (cosh(2 sqrt x) = sum (4x)^k/(2k)!). Pass: exact equality.
- PL5. Sign-change counter on planted polynomials with known counts: (t-2)(t+1)(t+3) -> 1 change, 1 positive root; (t-1)(t-2)(t+3) -> 2 changes, 2 positive roots;
  t^2 - t + 1 -> 2 changes, 0 positive roots (the counter counts changes, not roots); t^3 + 2t^2 -> 0 changes. Zero coefficients are skipped.
- PL6. Minimum of a polynomial on an interval (critical points plus end points, exact): x^3 - 3x + 2 on [0,3] -> 0 at x = 1; on [2,3] -> 4 at x = 2 (end point);
  on [-3,0] -> -16 at x = -3 (end point). Pass: exact value and argument.
- PL7. Zerilli residual routine R[psi, V] = f (f psi_r)_r - V psi (f = 1 + 2/r) on psi = r^2, for which V = 2(r+2)/r^3 by hand: residual 0; with V' = (11/10) V the residual is nonzero.

## Checks (real data) and the scripts that run them

signs (`review_lemma_a_signs.py`; planted: none):
- A1.1 c_1 = 3/2, c_2 = 0, c_3 = -K/32, c_4 = K/96 from the closed form, symbolic in l (c_1 by the Pochhammer convention (x)_{-2} = 1/((x-1)(x-2))).
- A1.2 (n-2) > 0 and (n-4)L + n - 1 > 0 for n >= 4, l >= 2, symbolic (all coefficients positive after n = 4 + a, l = 2 + b).
- A1.3 sign of the Pochhammer (l-n+3)_{2n-4}: positive for 3 <= n <= l+2, zero for n >= l+3 (exact, l = 2..300, n = 3..l+6).
- A1.4 sign of every c_n, exact, l = 2..300, n = 1..l+6: c_1 = 3/2, c_2 = 0, c_3 < 0, c_n > 0 for 4 <= n <= l+2, c_n = 0 for n >= l+3; in particular c_{l+2} > 0.
recur (`review_lemma_a_recur.py`; planted PL1, PL2):
- A2.1 P2, P1, P0 computed by sympy from V (§4.2) and psi = chi/(cr-6), with chi a generic function, equal my hand forms above, and
  psi_xx - V psi = -(r+2)/(r^4 D^2) (P2 chi'' + P1 chi' + P0 chi) exactly (symbolic in c).
- A2.2 P2 = -r^2(r+2)(cr-6) as RESULTS states.
- A2.3 recurrence on r^m extracted from the ODE (symbolic m) equals my typed formula, and equals RESULTS' form -2(m-2)(c(m-4) - 3(m-1)) and c(l-m+4)(l+m-3)
  (exact polynomial identity in l, m with c = (l+2)(l-1)).
- A2.4 low orders m = 1, 2, 3, 4 symbolic in l with c_0 = c_{-1} = 0 and c_1..c_4 of A1.1: residual 0.
- A2.5 polynomial identity in (l, m) after dividing the recurrence by (l-m+5)_{2m-8}, with (l-m+3)_{2m-4} = (l-m+3)(l-m+4)(l+m-3)(l+m-2) Pi,
  (l-m+4)_{2m-6} = (l-m+4)(l+m-3) Pi, Pi = (l-m+5)_{2m-8}, and the factorial ratios: exactly 0.
- A2.6 the two Pochhammer reductions of A2.5 hold exactly on the grid l = 2..40, m = 4..l+4; Pi > 0 for m <= l+4; for m >= l+5 all of c_m, c_{m-1}, c_{m-2} vanish (exact).
- A2.7 the recurrence residual with the actual c_n is exactly 0 for m = 0..l+6, l = 2..60.
- A2.8 P2 chi'' + P1 chi' + P0 chi is the zero polynomial for l = 2..40.
zerilli (`review_lemma_a_zerilli.py`; planted PL7):
- Z1[l=*] psi_0,xx = V psi_0 exactly (rational functions of r over Q, psi_xx = f (f psi_r)_r from the definitions, no P's), l = 2..40.
l1 (`review_lemma_a_l1.py`; planted PL3, PL4):
- L1.1a exponents of the chi-ODE at r_s, from the routine of PL3, symbolic in c: {0, 3}.
- L1.1b local values p = P2'(r_s) = -6r_s(r_s+2), q = P1(r_s) = 12 r_s(r_s+2), P0(r_s) = 12, and P2(r_s) = 0.
- L1.2 chi'(r_s) = -chi(r_s)/(r_s(r_s+2)) from the ODE at r_s (no assumption on chi(r_s)).
- L1.3 chi''(r_s) = 0 from the differentiated ODE, symbolic in c.
- L1.4 resonance: coefficient of chi''' in the twice-differentiated ODE is 2p + q = 0 and the remaining terms vanish with L1.2 and L1.3 substituted (the exponent-0 solution has no logarithm).
- L1.5 consequences: residue of psi_0^2 dx/dr at r_s is 0, and phi_0,xx(r_s) = 0 with phi_0 = (cr-6)/chi (symbolic, using L1.2).
- L1.6[l=*] with the actual chi, exact, l = 2..40: chi(r_s) > 0, chi'/chi = -1/(r_s(r_s+2)), chi''(r_s) = 0.
t1 (`review_lemma_a_t1.py`; planted PL6):
- T1.1 N - [9 + 18 C3 r^2 + (6 C4 - 2 c C3) r^3] = sum_{m>=4}(m-1) C_m r^{m-1}(6 - cr) + sum_{j>=5} 6 C_j r^{j-1} for generic coefficients C_1 = 3/2, C_2 = 0, C_3..C_9 symbols
  (exact), and the termwise identity for symbolic n.
- T1.2[l=*] the same identity with the actual c_n as a polynomial identity in r, l = 2..40.
- T1.3 the bracket with closed-form c_3, c_4 equals 9 - (9/16)(1+2e)rho^2 + (1/16)(1+2e)(1+e)rho^3 (symbolic in l); its derivative is (3/16)(1+2e) rho ((1+e) rho - 6);
  the minimum on [0, 6] is at rho = 6/(1+e) with value 9 - (27/4)(1+2e)/(1+e)^2 = 9/4 + (27/4) e^2/(1+e)^2 >= 9 - 27/4 for every e > 0 (exact).
- T1.4[l=*] N has no root in [0, r_s] and N(0) = 9, N(r_s) = c chi(r_s) >= 9/4 (exact Sturm count, l = 2..40).
t2 (`review_lemma_a_t2.py`; planted PL5):
- T2.1 N(r_s + t) = c sum_m (1-m) d_m t^m with d_m = Taylor coefficients of chi at r_s, generic chi of degree 8 with symbolic coefficients and symbolic c (exact).
- T2.2 d_m = sum_{n>=m} c_n C(n,m) r_s^{n-m} (generic identity), and for l = 2..40 the d_m from the closed form agree with sympy's Taylor shift of chi.
- T2.3[l=*] d_0 = chi(r_s) > 0, d_1 = -d_0/(r_s(r_s+2)), d_2 = 0 (exact, l = 2..120).
- T2.4[l=*] d_m > 0 for 4 <= m <= l+2, d_m = 0 for m > l+2 (exact, l = 2..120). The sign of d_3 is recorded for each l (not asserted).
- T2.5[l=*] the coefficient list of N(r_s + t) has exactly one sign change (l = 2..120), and the leading coefficient is -c(l+1)c_{l+2} < 0.
- T2.6[l=*] exact Sturm count: N has exactly one root in (r_s, inf), simple, and none in [0, r_s] (l = 2..40).

## Mutations and targets (written before the first control run; not to be changed)

`review_lemma_a_controls.py` runs each script unmutated (target: exit 0) and each pair below (target: exit non-zero, first FAIL id as written; an id without
brackets matches that id with any bracket).

| mutation | what it changes | script: first FAIL id |
|---|---|---|
| plant_recur | extractor drops the P0 term | common: PL1; recur: PL1 |
| plant_exp | exponent routine uses 1 + q/p | common: PL3; l1: PL3 |
| plant_rel | y'' relation uses P1' instead of P1' + P0 | common: PL4; l1: PL4 |
| plant_sc | counter counts a zero as a change | common: PL5; t2: PL5 |
| plant_min | minimum ignores end points | common: PL6; t1: PL6 |
| plant_zer | residual routine uses f = 1 + 1/r | common: PL7; zerilli: PL7 |
| cn_n4to3 | c_n factor (n-4) -> (n-3) | signs: A1.1; recur: A2.4; zerilli: Z1[l=2]; l1: L1.6[l=2]; t1: T1.2[l=2]; t2: T2.3[l=2] |
| cn_poch | c_n Pochhammer (l-n+3)_{2n-4} -> (l-n+2)_{2n-4} | signs: A1.1 |
| cn_sign5 | c_5 -> -c_5 | signs: A1.4[l=3]; recur: A2.7[l=3]; zerilli: Z1[l=3]; t2: T2.3[l=3] |
| V_coeff | V typed with 9(lambda r - 1) -> 9(lambda r - 2) | recur: A2.1; zerilli: Z1[l=2] |
| P2_claim | RESULTS' P2 typed with (cr-6) -> (cr-5) | recur: A2.2 |
| P1_6c_5c | my P1 typed with 6c r^2 -> 5c r^2 | recur: A2.1; l1: L1.1a |
| P0_12to13 | my P0 typed with +12 -> +13 | recur: A2.1; l1: L1.1b |
| rec_12to11 | typed recurrence 12(m-1)^2 -> 11(m-1)^2 | recur: A2.3 |
| rec_m4to3 | typed recurrence c(m-4) -> c(m-3) in the c_{m-1} term | recur: A2.3 |
| poch_ratio | reduction (l-m+3)_{2m-4} drops the factor (l+m-2) | recur: A2.5 |
| ratio_claim | claimed chi'/chi = -1/(r_s(r_s+2)) -> -1/(r_s(r_s+1)) | l1: L1.2 |
| t1_coef18 | typed bracket 18 C3 r^2 -> 17 C3 r^2 | t1: T1.1 |
| t1_drop_sum2 | typed RHS drops sum_{j>=5} 6 C_j r^{j-1} | t1: T1.1 |
| t1_bound3 | claimed bound 9 - 27/4 -> 3 | t1: T1.3 |
| t2_shift | typed identity (1-m) -> (2-m) | t2: T2.1 |
| t2_flip_d0 | the sign pattern of T2.5 uses -d_0 | t2: T2.5[l=2] |
| t2_window | Sturm window (r_s, inf) -> (r_s, 6 r_s/5) | t2: T2.6[l=2] |

The criterion "every check has a `--mutate` that fires" passes only if every row matches. A miss stays a miss and is reported.

## Steps and logs

1 this README. 2 planted problems, signs, recur. 3 l1, zerilli. 4 t1, t2. 5 controls. 6 final runs (`review_lemma_a*_output.txt` in the repository).
Exploratory runs log to this folder as `step<N>_<script>.log`. Step 7 compares with `chi_lemma.py`, `lemmas_all_l.py`, `threshold_lemmas.py` and their outputs.
