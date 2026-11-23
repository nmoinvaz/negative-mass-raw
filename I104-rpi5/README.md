# I104-rpi5: independent review of #2's computer-assisted large-l proofs (RESULTS.md §4.2 to §4.5)

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process at a time, nice 10, one thread.
Issue: https://github.com/nmoinvaz/negative-mass/issues/104
Worktree: `~/Source/negative-mass-i104`, branch `wip/i104-review-large-l` (base main f9007ce).
Python: `~/Source/negative-mass-venv314/bin/python` (3.14.10, sympy 1.14.0, mpmath 1.3.0).

The review is written from `phase2/dg_proof/RESULTS.md` alone. Not opened before step 7: `rescaled.py`, `vhat_structure.py`,
`threshold_isolation.py`, `large_l_proof.py`, `monotone_proof.py`, `common.py`, any other script of `phase2/`, and every
`*_output.txt` of those. Certified parts use mpmath `iv` (outward-rounded intervals). Identities use sympy.
What this review shares with #2: the formulas typed from RESULTS.md (a_n(eps), X, N, N_Z, Psi, V, the Zerilli ODE, T1/T2), nothing else.

Files (all in `phase2/dg_proof/`): `review_large_l_common.py`, `review_large_l_roots.py`, `review_large_l_theorem3.py`,
`review_large_l_brackets.py`, `review_large_l_thm_l.py`, `review_large_l_thm_m.py`, `review_large_l_controls.py`,
each with `_output.txt`, and `review_large_l.md`.

## Acceptance criteria (written before the first run; none is loosened after seeing data)

A1. rho_* and rho_neg, the roots of N_inf and Psi_inf (RESULTS 4.1, 4.4), by own root finding at 60 digits, printed to 25 digits.
    Pass: (a) the series of X_inf and the Bessel closed form agree to 1e-40 at 5 test points; (b) iv enclosures of width 2e-30 around each root
    with N_inf (Psi_inf) enclosures excluding 0 at the two ends with opposite signs and the derivative enclosure over the interval excluding 0;
    (c) |mine - RESULTS| < 1e-15 for 8.485700967373530 and 9.635989442586144.
A2. Planted problem through the same bracket code (`certify_bracket`), before any real data. P(r) = (r-3)(r-a)(r-b)(r-11),
    a = 17/2, b = a + 1e-10 (exact rationals). Expected verdicts:
    - [a-1e-14, a+1e-14] CERTIFIED (one root); [b-1e-14, b+1e-14] CERTIFIED;
    - [a-1e-12, b+1e-12] (two roots) REFUSED, reason: no sign change;
    - P times (r-(a+b)/2), same bracket (three roots) REFUSED, reason: derivative enclosure contains 0;
    - [a, a+1e-14] (endpoint on a root) REFUSED, reason: enclosure of P at the end contains 0;
    - [a+1e-9, a+2e-9] (no root) REFUSED, reason: same signs;
    - P times (r-a) (double root at a), bracket [a-1e-14, a+1e-14] REFUSED, reason: no sign change.
    Any wrong verdict stops the run (exit 2) before real data.
A3. Theorem 3, derived in sympy from the definitions of RESULTS §1 to §4.2:
    (Z) psi_0,xx = V psi_0 exactly for l = 2..14 (own chi from Lemma A); V in the (rho, c) variables equals 8c^4(2+eps rho)N_Z/(rho^4(rho-6)^2);
    Vhat = g^2 - g' = 2g^2 - psi_0,xx/psi_0 for generic X, and Vhat = 2c^4(2+eps rho)Psi/(rho^4(rho-6)^2 X^2) exactly for l = 2..9 from the definition (no (Z) used);
    (P1) numerator of V is a polynomial in (sigma, mu) with all positive coefficients (and the f > 0, lambda > 0 facts);
    (P2) the numerator Q of V_r = -2Q/(r^5(cr-6)^3), as c^5 Q(tau, m) with r = (6+tau)/c, l = 2+m, has all positive coefficients (count reported, RESULTS says 64);
    N_Z(6+tau) has positive coefficients; leading coefficient of Psi at rho -> inf is (l+1)(l+2)/(2c) a^2 > 0 (symbolic in l);
    S (RESULTS 4.3) has the sign of Vhat (identity derived from g^2 - g' with generic X);
    exact root counts for l = 2..16: N has exactly one root beyond rho = 6 (T2 check, not a proof), Psi has exactly one root beyond rho_*(l) (Theorem 3 check).
A4. 200 brackets of c r_* and c r_neg at the l below (seed 104: `sorted(random.Random(104).sample(range(2, 3001), 200))`).
    Per l: all l+2 terms summed in iv (no truncation, no tail bound); bracket width 2e-14, endpoints decimals with 20 digits; N (resp. Psi) enclosures
    at the two ends exclude 0 with opposite signs; N' (Psi') enclosure over the whole bracket excludes 0; S has the same sign change on the
    same bracket as Psi (an (Z)-free certificate for r_neg); lo(c r_neg) > hi(c r_*); the coefficients a_n(eps) for n <= 40 lie inside the
    exact Fraction values of Lemma A's closed form. Across the sample: c r_*, c r_neg strictly decrease with l (bracket separation),
    stay above the limits, and l^2 r_*, l^2 r_neg increase for the sampled l >= 5. In step 7 each bracket is compared with #2's table for overlap.
    Supplementary (not counted in the 200): l = 2..30 and l in {138, 139, 140, 499, 500, 501, 1000, 2000, 2999, 3000}; l = 2..12 also against sympy exact root isolation.
A5. Theorem L and Theorem M with own constants, each inequality in iv: coefficient bound, perturbation bounds, slopes, localisation, comparison
    N_{l+1}(rho_l) < 0, Psi_{l+1}(rho_l) > 0, localisation s-bounds, the l^2 r criterion. A step whose conclusion fails is an error; a step that cannot
    be completed is a gap. The constants are compared with #2's (91.51, 229.87; 3.709, 6.101) in step 7.
A6. Each check has `--mutate=NAME` that exits non-zero, and fires at the check named in the target list (a section added below before step 5).

## The 200 values of l (seed 104)

29, 34, 42, 47, 48, 70, 78, 82, 95, 104, 108, 116, 122, 131, 134, 155, 158, 162, 165, 168, 169, 225, 231, 251, 256, 294, 295, 296, 297, 298, 303, 314, 342, 348, 353, 358, 361, 384, 389, 412, 421, 431, 485, 507, 509, 513, 514, 531, 543, 548, 596, 604, 610, 632, 644, 658, 668, 670, 684, 687, 704, 720, 730, 736, 738, 749, 764, 772, 791, 806, 812, 817, 821, 833, 866, 867, 870, 890, 900, 926, 934, 940, 945, 975, 981, 1000, 1001, 1023, 1035, 1041, 1054, 1060, 1075, 1108, 1131, 1191, 1227, 1257, 1272, 1322, 1352, 1356, 1358, 1402, 1430, 1435, 1459, 1512, 1552, 1560, 1584, 1598, 1603, 1604, 1616, 1621, 1679, 1700, 1712, 1713, 1751, 1769, 1811, 1813, 1826, 1854, 1859, 1882, 1890, 1895, 1912, 1934, 1957, 1961, 1966, 1986, 1993, 2000, 2026, 2064, 2075, 2085, 2102, 2128, 2141, 2142, 2164, 2176, 2191, 2198, 2205, 2219, 2220, 2244, 2254, 2299, 2301, 2302, 2306, 2315, 2330, 2370, 2371, 2373, 2383, 2419, 2423, 2450, 2509, 2512, 2513, 2545, 2547, 2554, 2561, 2563, 2575, 2584, 2588, 2593, 2609, 2645, 2674, 2684, 2686, 2736, 2819, 2826, 2844, 2850, 2865, 2892, 2906, 2925, 2926, 2941, 2949, 2959, 2962, 2999

(15 values below l = 138, 157 at l >= 500.)

## Stop and load rules

One process, nice 10, `OMP_NUM_THREADS=1`. Any run over 3 h of wall time is stopped and what finished is reported. Memory is reported only.
Runs longer than a few minutes are systemd user units `nm-i104-<step>`, with the exit code written to `<step>.rc`.

## Added before the sweep run (2026-11-23)

Design parameters of Theorems L and M (own constants; chosen before their final runs):
- Theorem L (first order): eps0 = 1/(140*137) (l >= 138), windows rho_* +- 0.01 and rho_neg +- 0.03, 40 subintervals, 60 explicit terms then a tail
  majorant n^D g_n rho_hi^n (g_n = 1/(2^n (n-1)!^2)), coefficient bound B_n of the hand lemma C1.
- Theorem M and the second order refinement of L: a_n = alpha_n + eps alpha^1_n + eps^2 omega_n, windows rho +- K' eps_max with K' = 46 (N) and 339 (Psi),
  eps_max = 1/c(500) for M and 1/c(138) for the refinement ("L2").
- A first attempt took the maximum of the two coefficient regimes (n <= l+2 and n >= l+3) for every n, which gave Z = 12169 and E_max = 4.06e8, and the M
  comparison failed (2l+2) nu_min > 2.004 Z by a factor 1.2 (N) and 4.2 (Psi). The regimes are exclusive: the 60 explicit terms satisfy n <= l+2 for
  every l >= 138, so they use the n <= l+2 bound, and the tail (n > 60) uses the uniform majorant n^8 g_n. This changes the proof's bookkeeping, not an inequality
  under review. Logs: `step4_thm_m_try1.log` (first attempt) and `step4_thm_m_try2.log`.
- The coefficient bound |a_n - alpha_n| <= eps B_n is an equality at n = 4 for l = 138 (eps = eps0), so its iv test is "not definitely violated"
  (the enclosure of |a_n - alpha_n| - eps B_n does not lie above 0).

Supplementary sweep `review_large_l_sweep.py`: the brackets of the 200-bracket code for every l = 2..3000 (full table in `sweep_brackets.csv`), with the criteria
every bracket certified; hi(l+1) < lo(l) for both c r_* and c r_neg for every consecutive l; lo above the limits; l^2 r_* and l^2 r_neg increase for every
consecutive l >= 5; lo(c r_neg) > hi(c r_*). It is not part of the acceptance count.
