# I104-mac: the coordinator's review of #104's independent review of #2's large-l proofs

Machine: macOS (the coordinator's Mac), Python 3.14, sympy 1.14.0, mpmath 1.3.0, at nice 10 with at most 2 processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/104. Reviewed branch `wip/i104-review-large-l` at 154a345,
raw `I104-rpi5` at 4a6b044.

## Independent check `ind104.py` (criteria written before its first run)

ind104 shares no code with `review_large_l_*.py` or with #2's scripts. What it shares with them: formulas typed from
RESULTS.md (Lemma A's c_n, the Zerilli V for M = −1, the definitions of N, V̂, Ψ, N_Z, S, X_∞). It works in the
variable r with Lemma A's c_n directly (not the rescaled a_n(ε)), at 60 digits with mpmath mpf (numerical, not
intervals), and gets V̂ from its definition V̂ = g² − g_x, g = ψ₀,x/ψ₀, ψ₀ = χ/(cr − 6), not from Ψ or S. Its own
derivation (by hand, before the run): V̂ = c³ f S/(ρ²(ρ − 6)X²) for any X, using only N = X − (ρ − 6)X′, so sign V̂ =
sign S on ρ > 6 without (Z).

l set: 2..30, 80, 100, 137, 138, 139, 499, 500, 501, 502, 1000, 1001, 2000, 2999, 3000, and 6 drawn by
`random.Random(10404).sample(range(31, 3001), 6)` = 36, 464, 864, 1461, 1644, 1995.

| id | criterion | kind |
|---|---|---|
| F1a | X_∞ by its series (200 terms) equals the Bessel closed form to 1e-45 at ρ = 3, 8.5, 11. N_∞ has one sign change on a 0.01 grid of (6, 30], Ψ_∞ one on [ρ_*, 30]; bisection roots agree with #104's 8.485700967373530340930500822 and 9.6359894425861440206961577 to 1e-24 | numerical |
| F1b | ρ_*, D₁, D₂ fitted to c·r_*(l) = ρ + D₁/c + D₂/c² at l = 1000, 2000, 3000 (direct roots, F3): ρ within 1e-12 of F1a, D₁ within 2e-6 of RESULTS' 3.515486; the same for r_neg with 5.839393 | numerical |
| F2 | Lemma A(ii) at every l of the set: c₁..c₄ = 3/2, 0, −K/32, K/96; relative residual of ψ₀,xx − Vψ₀ below 1e-40 at ρ = 7, 8.5, 9.6, 12 | numerical |
| F3 | at every l: N has exactly one sign change on the 0.02 grid of (6, 16] and N < 0 at ρ = 20, 40, 80, 160, 320; V̂ has exactly one sign change on the grid from my c·r_* to 16 and V̂ > 0 at those ρ; both bisected roots lie inside #104's brackets in `I104-rpi5/sweep_brackets.csv` | numerical |
| F4 | D = (c·r − ρ)·c at every l ≥ 138 of the set: 0 < D_* ≤ 3.5525479 and 0 < D_neg ≤ 6.6818585 (#104's second-order L); for l ≥ 500, D_* ≤ 3.5186068 and D_neg ≤ 5.9363952 (#104's M) | numerical |
| F5 | r_* < r_neg at every l. c·r_* and c·r_neg strictly decrease over 2..30 and over the consecutive pairs (137..139, 499..502, 1000..1001, 2999..3000), and stay above ρ. l²·r has its minimum over 2..30 at l = 5 and strictly increases on 5..30 and on the pairs; l²·r < ρ for l ≥ 3. RESULTS 4.3's table rows (l = 2, 3, 5, 10, 20, 80, 100, 500, 1000, 3000) within 1e-6 | numerical |
| F6 | Theorem 3 in sympy, own derivation: (P1) the numerator of V in (σ, μ) has positive coefficients; (P2) Q = −V_r r⁵(cr − 6)³/2 is a quintic in r, and c⁵Q at r = (6 + τ)/c, l = 2 + m is a polynomial in (τ, m) with exactly 64 terms, all positive | exact |
| F7 | at l = 2, 7, 30, 500, 3000 and ρ = 7, 9, 11: V̂ (direct) equals c³fS/(ρ²(ρ − 6)X²) and 2c⁴(2 + ερ)Ψ/(ρ⁴(ρ − 6)²X²), each to relative 1e-35 | numerical |

Mutations, each must exit 1 with its target failing: `cn` (c₅ × (1 + 1e-12); F2), `vsign` (−9(λr − 1) in V; F2, F6),
`rho` (#104's ρ_* + 1e-23; F1a), `csv` (#104's r_* bracket at l = 500 shifted by 1e-13; F3), `l2` (c in place of l² in
F5; F5), `sM` (3.515 in place of 3.5186068; F4), `vhat` (g² + g_x; F7).

## Results

| file | what |
|---|---|
| `rerun/` | every `review_large_l_*.py` from the branch, run on the Mac at nice 10 (`runA.log`, `runB.log` hold exit codes and times) |
| `ind104.py`, `ind104_run1.txt` | the independent check above, run 1: exit 0, 60 s, every criterion passes |
| `ind104_mut_*.txt` | its 7 mutations |
| `resolve104.py`, `.txt` | one case re-solved by exact real-root isolation (sympy `real_roots`), l = 29 |

**Reruns.** All exit 0 except `review_large_l_controls.py`, which exits 1 as on rpi5 (47 of 52 on target, the same 5
not). Each output equals the committed one apart from timings and, in `table`, the csv path. The sweep took 684 s
(2437 s on rpi5); its `sweep_mac.csv` is byte-identical to `I104-rpi5/sweep_brackets.csv`. This rerun includes every
one of the 52 mutations, for example `review_large_l_sweep.py --mutate=l2r_reverse`: exit 1, first FAIL "l^2 r
increases (N), l=5 -> 6", on target.

**Re-solve, l = 29** (outside #2's Sturm range 2..24 and #104's 2..16). N has one real root beyond ρ = 6, c·r_* =
8.489743651547031155464895. S has three positive roots: 6 (r_s, forced by L1), 6.1690082, and c·r_neg =
9.642705229862547021022613, the only one beyond c·r_*. Both lie inside #104's brackets.

**ind104 run 1.**

| criterion | result |
|---|---|
| F1a | ρ_* = 8.4857009673735303409305008219, ρ_neg = 9.63598944258614402069615769984; differ from #104's by 1e-28 and 2e-28 |
| F1b | the fit of the direct roots at l = 1000, 2000, 3000 gives ρ within 4e-19, D₁ = 3.515485851 and 5.839392647, D₂ = −5.597 and −8.772 |
| F2 | Zerilli residual below 4e-61 at all 49 l (2 to 3000); c₁..c₄ as Lemma A states |
| F3 | one sign change of N and of V̂ beyond r_* at all 49 l; every root inside #104's bracket |
| F4 | D_* rises from 3.51519 (l = 138) to 3.51549 (l = 3000), D_neg from 5.83894 to 5.83939: below #104's 3.5186 and 5.9364 (l ≥ 500) and 3.5525 and 6.6819 (l ≥ 138) |
| F5 | r_* < r_neg; c·r decreasing; l²r minimum at l = 5 (7.6825922, 8.7802767); RESULTS' table within 4.9e-7 |
| F6 | (P1) 8 positive terms; (P2) quintic Q, 64 terms, all positive, least coefficient 1 |
| F7 | direct V̂ = S form = Ψ form to 2e-60 at l = 2, 7, 30, 500, 3000 |

**Mutations.**

| mutation | exit | failed | target met |
|---|---|---|---|
| `cn` | 1 | F2, F3, F7 | yes (F2) |
| `vsign` | 1 | F2, F6 | yes |
| `rho` | 1 | F1a | yes |
| `csv` | 1 | F3 | yes |
| `l2` | 1 | F5 | yes |
| `sM` | 1 | F4 | yes |
| `vhat` | 1 | F3 at every l, then a crash in F1b (no root to fit) | **no**: the target F7 is never reached |

The `vhat` result is a defect of ind104, which does not guard a missing root. F7 is shown to fail by `cn` (3.9e-12 at
l = 7).

**Findings on #104.**
- The coefficient-bound test of `review_large_l_thm_l.py` step 1 was relaxed after a failed first run, from "the
  enclosure of bound − |a_n − α_n| is ≥ 0" to "not definitely violated". The runner records this in its §9. The comment
  in the code and the printed message say the equality is "only at n = 4, l = 138". That is wrong: in exact rationals,
  |a₃ − α₃| = 2ε|α₃| = εB₃ at every l (S₃ = 0, α′₃ = 0), and n = 4 is an equality at l = 138 only. The bound H3 holds
  (with equality there), so no conclusion changes.
- The acceptance item "each of the 200 brackets compared with #2's table for overlap" can be met for 2 of the 200
  only: `threshold_isolation_output.txt` prints 16 l. The other 198 were compared with #2's Theorem L and M bounds.
