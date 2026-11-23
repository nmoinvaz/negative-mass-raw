# I142-rpi5: independent review of dg_proof's Lemma A(iii), L2-L6 and the Zerilli V (RESULTS.md §1, §2, §4.2)

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process at a time, nice 10, one thread.
Issue: https://github.com/nmoinvaz/negative-mass/issues/142
Worktree: `~/Source/negative-mass-i142`, branch `wip/i142-lemma-a3` (base main 068c8b4).
Python: `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0, mpmath 1.3.0). Exact arithmetic only (sympy, `fractions.Fraction`).
The one float comparison is V1.9 (a published three-digit number), tolerance fixed below before any run.

Written 2026-11-23, before any check was run (the real checks, the planted problems and the controls).

## Independence

The review is written from `phase2/dg_proof/RESULTS.md` alone (§1 Lemma A(iii), L1-L6, §2 for how they are used, §4.2's V, §3-§4 notation).
Not opened before step 7: `chi_lemma.py`, `lemmas_all_l.py`, `verify_small_l.py`, `ground_state_identity.py`, `common.py`,
`threshold_lemmas.py`, `vhat_structure.py`, any other script of `phase2/`, every `*_output.txt` of those,
and #104's and #138's `review_*.py` (and their notes). #138's closing comments were read for the method.
What this review shares with #2: the formulas typed from RESULTS.md (c_n of Lemma A, the V of §4.2, f, x, ψ₀, g, V̂, Ψ_DG, k).
Nothing else.

External sources (data, not instructions; fetched with curl into scratch, read with pdftotext; nothing run from them):

| tag | source | read | used for |
|---|---|---|---|
| DG09 | Dotti, Gleiser, Class. Quantum Grav. 26 (2009) 215002, arXiv:0809.3615 (INSPIRE record found by author+title query) | PDF, eqs. (11)-(13), (52)-(61) and the Fig. 1 caption, page 13 read as an image | V (11), x (13), ψ₀ (52), χ-ODE (53), V̂ (54), c_n (55), (57)-(59), (60), (61) |
| DG06 | Dotti, Gleiser, Class. Quantum Grav. 23 (2006) 5063, arXiv:gr-qc/0604021 | PDF, eqs. (2)-(8) | V (6), r* (8) |
| BCS | Berti, Cardoso, Starinets, Class. Quantum Grav. 26 (2009) 163001, arXiv:0905.2975 | PDF page 14 read as an image | V⁺ (15) and V⁻ (14); (15) carries an AdS radius L, the limit L → ∞ is used |
| KS | Kokkotas, Schmidt, Living Rev. Relativ. 2 (1999) 2, arXiv:gr-qc/9909058 | PDF, eq. (24) | V (24) |
| Z70 | Zerilli, Phys. Rev. Lett. 24 (1970) 737 and Phys. Rev. D 2 (1970) 2141 | publisher page answered HTTP 403 (bot check); not read | **(unverified)** the original; DG and KS quote it |
| C83 | Chandrasekhar, The Mathematical Theory of Black Holes (1983), §28 (the V⁺ and V⁻ relation) | book not read | **(unverified)**: used only as an identity to test, V1.4 |

Each of DG09, DG06, BCS, KS was read in full at the quoted equations. A form typed from a source is checked against the others, and the sources are checked against each other (V1.2).

## Hand derivations, written before any code (the checks test them; none is assumed)

Notation as RESULTS: c = (l+2)(l-1), L = l(l+1) = c+2, K = (l-1)l(l+1)(l+2) = cL = c(c+2), k = K/6, r_s = 6/c, f = 1+2/r, dx/dr = 1/f.
- c_1 = 3/2, c_2 = 0, c_3 = -K/32, c_4 = K/96, c_5 = K(L-6)(L+4)/6144 = K(K-24)/6144, because (l-2)_6 = K(L-6) and (L-6)(L+4) = L²-2L-24 = K-24.
- Lemma A(iii): q = 3/2 - a r² + b r³ + d r⁴ with a = K/32, b = K/96, d = c_5. q' = r(4d r² + 3b r - 2a); the quadratic has roots of opposite sign (product -2a/4d < 0), so one positive root, q decreases then increases.
  Discriminant 9b² + 32ad = K²(K-18)/6144 = (K s/192)² with s = sqrt(6(K-18)); r_0 = 4(s-6)/(K-24) = 24/(s+6) (using K-24 = (s-6)(s+6)/6).
  (Ks)² - (18(K-16))² = 6K²(K-18) - 324(K-16)² = 6K³ - 432K² + 10368K - 82944 = 6(K-24)³.
  q(r_0) > 0 iff Ks > 18(K-16) (both sides > 0 for K > 18), iff 6(K-24)³ > 0 iff K > 24. K ≥ 120 is only "l ≥ 3"; the argument needs K > 24. At l = 2, K = 24, c_5 = 0, s = 6, r_0 = 2, and the closed form is 0/0 with limit 1/2 (= the l = 2 minimum).
  DG09 (58) is 4(s-6)/(K-24); DG09 (59) is 16(s-6)(K-18)(Ks-18K+288)/(K-24)⁴ = r_0 q(r_0).
- L2: with ψ = r h/(cr-6), h(0) = 3/2, h'(0) = 0: ψ_r/ψ = 1/r + c/6 + O(r); g = f ψ_r/ψ = 2/r² + (1+c/3)/r + ...; V̂ = g² - f g_r = 12/r⁴ + 2(c+5)/r³ + ..., and c+5 = l²+l+3.
  In r the ODE f(f u_r)_r = (V̂ - E)u has indicial equation 4s(s-2) - 12 = 0 at the leading order: s = 3, -1. x = r²/4 - r³/12 + ..., so x^{3/2} ~ r³/8, x^{-1/2} ~ 2/r.
- L3: ψ ~ r^n (n = deg χ - 1 = l+1) gives g ~ n/r, V̂ ~ n(n+1)/r² = (l+1)(l+2)/r².
- L6: Ψ̂ = -fψ(Ψ/ψ)_r = -f (W'χ - Wχ')/((cr-6)χ) with W = r(r+2)^k e^{-kr/2} = 2^k r (1 - k r²/8 + k r³/24 + (k²/128 - k/64) r⁴ + ...).
  The coefficients of r^p in W'χ - Wχ' (p = i+j-1, over W = Σ w_i r^i, χ = Σ c_j r^j) vanish for p = 1, 2, 3, 4 once c_2 = 0, c_3 = -K/32, c_4 = K/96, K = 6k, and the p = 5 coefficient is 3·2^k k²/128 (uses c_5 = K(K-24)/6144).
  Hence Ψ̂ = (2^k k²/192) r³ + O(r⁴). At r_s regularity needs W'/W = χ'/χ there: W'/W(r_s) = -c²/(12(c+3)) = -1/(r_s(r_s+2)), which is L1's χ'/χ(r_s), true exactly when k = c(c+2)/6.
- L4: V = ψ_xx/ψ for ψ₀ (Lemma A(ii), #138); Ψ_k = (r+2)^k e^{-kr/2} = 2^k e^{-kx/2} is annihilated by ∂ₓ + k/2, so Ψ_DG = (r/(cr-6)) Ψ_k; the residual -Ψ_DG,xx + VΨ_DG + (k/2)²Ψ_DG, divided by Ψ_DG, is a rational function of (r, c, k), expected to be (6k - c(c+2)) times a rational function.
- V: DG09 (11) at M = -1 is RESULTS' V (read at the page). The tortoise coordinate DG06 (8) at M = -1 is x = r - 2ln(1+r/2).
  Fig. 1 of DG09 quotes the double pole of the l = 2, M = -2 potential at x ≃ 0.761: r_s = -3M/λ = 3, x(r_s) = 3 - 4 ln(7/4) = 0.76154.

## Planted problems (written first; run before any real data; same code path as the real checks)

A planted check that fails ends the script with exit 2 before any real data.
- PLA (a3 script, Lemma A(iii) machinery). PLA.1: q = 3/2 - 3r² + r³ + (3/4)r⁴ has q' = r(3r² + 3r - 6), so r_0 = 1 (discriminant 9 + 72 = 81) and q(r_0) = 1/4; the routine `crit_min` returns (1, 1/4) exactly. PLA.2: q = 3/2 - r² + r⁴/8 has r_0 = 2 and q(r_0) = -1/2 < 0: the routine reports "not positive". PLA.3: with symbols (a, b, d) the routine's r_0 satisfies 4d r_0² + 3b r_0 - 2a = 0 exactly.
- PLS (Sturm counter on (0, ∞)): (r-1)(r-2)(r+3) -> 2; r²+1 -> 0; (r-1)²(r+2) -> 1 (distinct roots); r³-2 -> 1; r³+r+2 -> 0 (only a negative root); r⁴ - 3r² + 3/2 -> 2 (roots r² = (3 ± sqrt 3)/2). Pass: exact counts.
- PLE (ends script). PLE.1: the indicial routine on four ODEs built from known solutions by the Wronskian determinant, not by the routine: y1 = r³(1+r), y2 = (1+2r+3r²)/r at 0 -> {3, -1}; Bessel r²u'' + r u' + (r² - 1/4)u = 0 -> {1/2, -1/2}; Euler r²u'' - 2r u' + 2u = 0 -> {1, 2}; (r-1)²u'' + (r-1)u' - 4u = 0 at r = 1 -> {2, -2}. PLE.2: the V̂ routine (V̂ = g² - g_x with g = f ψ_r/ψ) on ψ = r^n gives r⁴V̂ -> 4n(n+2) at 0 and r²V̂ -> n(n+1) at ∞ (hand values, n = 1, 2, 3, 5), and on ψ = r^n(1 + 3/r) gives the same limit at ∞. PLE.3: the order-and-leading-coefficient routine on (r²+1)/(r⁴(1+r)) -> order -4, coefficient 1 at 0; at ∞ -> r^{-2} with coefficient 1; on r³(2-r) -> order 3 coefficient 2.
- PLW (l6 script): the Wronskian-order routine (order and leading coefficient of W'χ - Wχ' at r = 0, from the series) on three planted pairs with hand values: (W, χ) = (r, r + r³) -> -2r³ (order 3, coefficient -2); (r + 2r², r²) -> (1+4r)r² - (r+2r²)2r = -r² (order 2, coefficient -1); (e^r, e^{2r}) -> e^{3r} - 2e^{3r} = -e^{3r} (order 0, coefficient -1).
- PLL (l4 script). PLL.1: the V̂ routine in x (generic ψ(x) = cosh x) gives V̂ = 1 - 2 sech²x with V = 1 (Pöschl-Teller, by hand). PLL.2: the eigen-residual routine on Ψ_k (V = 0): residual 0 at E = -(k/2)² for symbolic k, and nonzero (= 1·Ψ_k) at E = -(k/2)² + 1.
- PLV (v script). PLV.1: the comparison routine on a planted equal pair ((1-2M/r)·2[...] vs its expanded form) -> 0, and a planted unequal pair (one coefficient 3 -> 2) -> nonzero. PLV.2: the M -> -1 substitution on 1 - 2M/r gives 1 + 2/r.

## Checks (real data), their ids, and the scripts that run them

Each script prints one line per check, `PASS <id>` or `FAIL <id>: ...`; ids of per-l checks end `[l=N]`. Exit 0: all pass. Exit 1: a real check failed. Exit 2: a planted check failed (stop). A check never changes after seeing data; a criterion is never loosened.
`--mutate=NAME` switches on one deliberate error; targets are written before the first control run (end of this README, "Targets").

Acceptance criteria (each can fail):
- Every identity is exactly 0 in sympy (no tolerance), symbolic in l (or in c, K, k, λ, as stated) where the lemma is for all l, and exactly 0 for every l of the stated range otherwise.
- Every sign or count statement is decided by exact arithmetic (Sturm, exact rational/algebraic evaluation).
- Each check has a mutation that makes it exit non-zero on the target id.

a3 (`review_lemma_a3_a3.py`; planted PLA, PLS): Lemma A(iii).
- A3.1 c_3, c_4, c_5 from RESULTS' c_n equal -K/32, K/96, K(K-24)/6144, symbolic in l (polynomial identities after expanding the Pochhammers).
- A3.2 K = 24 at l = 2 and K ≥ 120 at l ≥ 3, K > 24; c_5 > 0 for l ≥ 3 and c_5 = 0 at l = 2 (exact, l = 2..50); the integer-l identity K - 24 = (l-2)(l+3)(l²+l+4).
- A3.3 for l = 3..50: the coefficients of χ/r - q are 0 at powers 0..4 and ≥ 0 at powers ≥ 5 (exact).
- A3.4 q' = r·(4d r² + 3b r - 2a); the quadratic's product of roots is negative; r_0 = 24/(s+6) satisfies it exactly (symbolic in s, with K = s²/6 + 18); q decreases on (0, r_0) and increases after (sign of the quadratic at the two sides).
- A3.5 q(r_0) = 4(K-18)(Ks - 18(K-16))/(K-24)³ exactly (symbolic in s); also equals DG09 (59)/r_0 (typed from the paper) with ρ = s.
- A3.6 (Ks)² - (18(K-16))² - 6(K-24)³ = 0 as a polynomial identity in K (using s² = 6(K-18)).
- A3.7 sign logic: for l = 3..50 (exact) Ks > 18(K-16) > 0 and q(r_0) > 0; where K ≥ 120 is used and that K > 24 suffices (report).
- A3.8 l = 2: χ/r = 3/2 - (3/4)r² + (1/4)r³ from the c_n; minimum 1/2 at r = 2; the K → 24 limits of r_0 and q(r_0) equal 2 and 1/2.
- A3.9[l=N] exact Sturm: χ/r has no root in (0, ∞), l = 2..50, cross-checked by sympy's `count_roots`.
ends (`review_lemma_a3_ends.py`; planted PLE, PLS not needed): L2, L3.
- E2.1 r⁴V̂ = 12 + 2(c+5) r + O(r²) symbolic (generic h with h(0) = 3/2, h'(0) = 0, symbolic c); l²+l+3 = c+5.
- E2.2[l=N] the same expansion exactly for the actual χ, l = 2..30, and the pole order of V̂ at 0 is exactly 4.
- E2.3[l=N] denominator of V̂ in lowest terms = const · r⁴ (χ/r)², l = 2..30 (RESULTS §5's claim, hence V̂ continuous on (0, ∞) given A3.9).
- E2.4 the indicial roots in r are {3, -1}: symbolic (V̂ = N(r)/r⁴, N(0) = 12, E symbolic) and exact from the actual V̂ for l = 2..30 (E2.4[l=N]).
- E2.5 x = r²/4 - r³/12 + ..., exponents in x: {3/2, -1/2}; ∫ (r^{-1})² dx diverges at 0, ∫ (r³)² dx converges (symbolic integrals).
- E2.6 V̂ in x: 3/(4x²) + (l²+l-1)/(4 x^{3/2}) - l(l+1)/(4x) + O(x^{-1/2}) (DG09 (61)), by series reversion of x(r).
- E2.7 φ₀ = (cr-6)/χ ~ -4/r at 0; ~ (c/c_{l+2}) r^{-(l+1)} at ∞; φ₀ ∈ L²(dx) at ∞, ∉ L² at 0; φ₀'(r_s) = c/χ(r_s) > 0 (exact, l = 2..50).
- E2.8 φ₀,ₓₓ = V̂φ₀ for generic ψ (symbolic), and exactly for the actual ψ₀, l = 2..20.
- E3.1 ψ = r^n(1 + a₁/r + a₂/r² + a₃/r³), n symbolic: r²V̂ → n(n+1).
- E3.2[l=N] deg ψ₀ = l+1 (so n = l+1) and lim r²V̂ = (l+1)(l+2) exactly, l = 2..30; V̂ > 0 for r large.
l6 (`review_lemma_a3_l6.py`; planted PLW): L6.
- L6.1 Ψ̂ = A*Ψ_DG = -f (W'χ - Wχ')/((cr-6)χ), generic W and χ (symbolic).
- L6.2 W's series 2^k r (1 + 0 r - (k/8) r² + (k/24) r³ + (k²/128 - k/64) r⁴), symbolic in k.
- L6.3 the Wronskian numerator's coefficients p = 1..4 are 0 and p = 5 is 3·2^k k²/128 (symbolic in k, with K = 6k and the c_n of A3.1); Ψ̂ = (2^k k²/192) r³ + O(r⁴).
- L6.4[l=N] the same exactly for the actual χ and k, l = 2..30 (Ψ̂ = E ρ̂ with E = (r+2)^k e^{-kr/2} stripped).
- L6.5 W'/W(r_s) = -1/(r_s(r_s+2)) symbolic in c with k = c(c+2)/6; fails for other k.
- L6.6[l=N] χ'/χ(r_s) = -1/(r_s(r_s+2)) for the actual χ and ρ̂ in lowest terms has no pole at r_s and no pole on (0, ∞) (Sturm on its denominator), l = 2..30; degree of ρ̂ finite, so Ψ̂ ~ e^{-kr/2} r^m is in L²(dx) at ∞.
l4 (`review_lemma_a3_l4.py`; planted PLL): L4.
- L4.1 intertwining algebra, generic ψ(x): AA* = -∂² + ψ''/ψ, A*A = -∂² + g² - g', Ĥ A* = A* H_Z, H_Z A = A Ĥ (symbolic).
- L4.2 residual R(r; c, k) = [-Ψ_DG,xx + VΨ_DG + (k/2)²Ψ_DG]/Ψ_DG, V of §4.2: numerator divisible by (6k - c(c+2)) and exactly 0 at k = c(c+2)/6 (symbolic in r, c).
- L4.3 k = K/6 is an integer (a multiple of 4) for l = 2..200; k > 0.
- L4.4[l=N] ψ₀,ₓₓ = Vψ₀ exactly for l = 2..20, from definitions (needed for H_Z = AA*).
- L4.5[l=N] ĤΨ̂ = -(k/2)²Ψ̂ exactly for l = 2..20, from definitions, no intertwining used; Ψ̂ ≢ 0.
v (`review_lemma_a3_v.py`; planted PLV): V.
- V1.1 RESULTS' V at M = -1 equals each published form at M = -1: DG06 (6), DG09 (11), KS (24), BCS (15) at L → ∞, exactly, symbolic in r and λ (or l).
- V1.2 the published forms agree with each other for generic M.
- V1.3 x(r) = r - 2ln(1+r/2) has dx/dr = 1/f and x(0) = 0, and equals DG06 (8) and DG09 (13) at M = -1.
- V1.4 Chandrasekhar's relation (unverified source): V^± = ±β dF/dx + β²F² + κF, F = Δ/(r³(μ²r+6M)), β = 6M, κ = μ²(μ²+2), μ² = c, tested for both signs against V_Z and V_RW = f(L/r² - 6M/r³) (BCS (14)), generic M; reported as "holds / does not hold"; it is a cross-check only.
- V1.5 V̂ from the definition (g² - g' with ψ₀ = χ/(cr-6), V of §4.2, χ'' eliminated with DG09 (53)) equals DG09 (54) at M = -1, generic χ, χ', symbolic in c.
- V1.6 the ODE for χ derived from ψ_xx = Vψ with ψ = χ/(cr-6) equals DG09 (53) at M = -1 (ratio of coefficients is a constant function), symbolic in c.
- V1.7 the pole of V at λr = 3 sits at r_s = 6/c > 0 only because M < 0; V is a rational function of M (no branch), so M = -1 is an ordinary substitution.
- V1.8 c_n of RESULTS equals DG09 (55) at M = -1 (Γ form), exactly, l = 2..30, every n; and c_3, c_4, c_5 equal DG09 (57)'s printed coefficients.
- V1.9 x(r_s) for l = 2, M = -2 is 3 - 4 ln(7/4) = 0.76154; DG09's Fig. 1 caption gives ≃ 0.761; criterion |x - 0.761| < 10⁻³ (the one float comparison).
controls (`review_lemma_a3_controls.py`): runs every script unmutated (exit 0) and once per (mutation, script) pair of "Targets" (exit non-zero, first FAIL id equal to the target).

Final runs (step 6): each `review_lemma_a3*.py > review_lemma_a3*_output.txt`, stdout only, each exiting 0; logs of every step go to this folder.

## Stop conditions and load

One process, `nice -n 10`, one thread (`OMP_NUM_THREADS=1`); any run over a few minutes as a systemd user unit `nm-i142-<step>` with its exit code in a file here.
A single run not finished in 2 h of wall time is stopped and reported. Nothing depends on memory (memory is reported only). choptuik-large-d's processes and files are not touched.

## Targets

(To be written before the first control run; not changed after.)
