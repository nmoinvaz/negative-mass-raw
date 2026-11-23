# I139-mac: the coordinator's review of #139's comparison of #2's bracket table with #104's

Machine: macOS (the coordinator's Mac), Python 3.14, sympy 1.14.0, mpmath 1.3.0, at nice 10 with at most 2 processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/139. Reviewed branch `wip/i139-bracket-csv` at 901dd70, raw
`I139-rpi5` at 31e66a1.

## Independent check `ind139.py` (criteria written before its first run)

ind139 shares no code with `compare_brackets.py`, `threshold_isolation.py`, `rescaled.py` or #104's scripts. What it shares:
the two csv files it reads, Lemma A's c_n, the Zerilli V and V̂ = 2g² − V (typed from RESULTS.md, as in the coordinator's
`I142-mac/ind142.py`), and the claims of RESULTS.md 4.3 and of #139's closing comment. The re-solve route (mpmath roots of N
and V̂ from the terminating χ, no rescaled series, no intervals) is neither #2's nor #104's; it is *numerical evidence*.

| id | criterion | kind |
|---|---|---|
| K1 | both files have 2999 rows, l = 2..3000 once each, c = (l+2)(l−1), lo < hi; for every l both c·r_* brackets and both c·r_neg brackets intersect (closed); #2's widest bracket 2.0e-13, #104's 2.0e-14 and the largest midpoint gap 4.59e-15 as #139 reports, each to 1% | exact |
| K2 | #2's csv from the Mac rerun of `threshold_isolation.py --csv` equals `I139-rpi5/brackets_i2.csv` byte for byte | exact |
| K3 | on #2's table and on #104's, for every l: hi(c·r_*) < lo(c·r_neg); hi(l+1) < lo(l) for both; lo > ρ_* = 8.485700967…, ρ_neg = 9.635989443…; l²·r increases strictly from l = 5 (lo(l+1) > hi(l) scaled); l = 5 is the minimum, 7.6826 and 8.7803 to 5e-5; l²·r below ρ for l ≥ 3 | exact |
| K4 | for l = 2, 3, 10, 100, 1500, at 80 digits: N(ρ) = X − (ρ−6)X′, X(ρ) = cχ(ρ/c), has exactly one sign change on (6, 20] (step 0.01) and V̂ exactly one on (c·r_*, 40]; each bisected root lies inside #2's bracket and inside #104's | numerical |

Mutations, each must exit 1 with its target failing: `shift` (#2's c·r_* bracket at l = 2222 moved up by 10⁻¹²; K1),
`mono` (#2's rows l = 1000 and 1001 exchanged; K3:#2), `bytes` (one digit of the Mac csv changed; K2), `rho` (ρ_* taken as
8.4858; K3), `chi` (c₃ scaled by 1 + 10⁻⁶; K4).
