# I133-mac: the coordinator's review of #133's count of the tanh wall's Type III points

Machine: macOS (the coordinator's Mac), Python 3.14, sympy 1.14.0, mpmath 1.3.0, at nice 10 with at most 2 processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/133. Reviewed branch `wip/i133-type3-count` at 2097a3d
(script c9148ff), raw `I133-rpi5` at 078a624.

| file | what |
|---|---|
| `rerun_he_type3_count.txt` | `python notes/warp/he_type3_count.py` from the branch: exit 0, 480 s; same as the committed output except four timing lines |
| `mutate_eps-typo.txt` | `--mutate=eps-typo` with all checks: exit 1, fails exactly its 6 frozen targets, 51 s |
| `resolve133.py`, `.txt` | Rodal's inadmissible root nearest the axis re-solved by Newton in (r, w) from 1e-3 away: r = 5.07635399284529, w = 1.03000296, det J = 3.6e10 |
| `ind133.py`, `ind133_run1.txt` | independent check, run 1: exit 1. D0 to D3 and D5 pass; **D4 fails** (below) |
| `ind133b.py`, `ind133b_run1.txt` | independent check, second version (D4 replaced by D4b, D6 added, criteria fixed before its run): exit 0 |
| `ind133b_mut_*.txt` | its 5 mutations (lead, sigma, asym, common, e2): each exits 1 on its target |
| `cmp133.py`, `.txt` | cross-load: #133's P table (`he_type3.shadow()`) equals the P of ind133b's Ricci route, 167 terms, term by term |

ind133 and ind133b share no code with `he_type3_count.py` or `he_type3.py`. Their E1, E2 come from the coordinator's Ricci
route of #102's review (`I102-mac/ind102.py`, copied), and the profile from the cosh form f = (1 + C)/(cosh z + C)
(#132, Lean-certified in #134). The grid scans are numerical evidence; D1 and D6 are exact.

**ind133 run 1, D4 failed.** Its float64 quadratic formula lost E1's small root to cancellation. That gave 6742 sign
changes of E2(w) along the branches that 50 digits did not confirm: |E2|/Σ|terms| was 0.004 to 0.05 at each, at Le
r ≈ 0.03 and at Rodal r ≈ 2.7 to 3.1. Its common-root test also accepted the root of y going to w = −1e35. Both are
defects of the check, not of #133. The failure stands. ind133b replaces D4 by D4b: the stable quadratic formula and a
50-digit confirmation of each candidate. It handles roots with |w| > 1e4 explicitly, and adds D6.

**Findings.** P has 4 (Le) and 6 (Rodal) sign changes on a 1e-4 grid in z over [1/4, z_t], at #133's radii within 1e-9.
The direct common roots of E1 and E2, found without the resultant, are at exactly those radii, with #133's w. Three per
wall have 0 < w < 1 and T ≠ 0. y = B − A has one root per wall. There E1's w² coefficient φ²y²/4 and E2's w³
coefficient φ²y²(9A² + 10Aφ − 10Bφ)/8 both vanish, so the only shared root is w = ∞. That is where the resultant's
factor (A − B)³ comes from. The finite root of E1 there is −0.35848289 (Le) and −6.3024138 (Rodal), the values ind102
printed as "rejected", with |E2|/Σ = 0.24 and 0.035. So the closing comment on #102 was wrong to say that every extra
sign change of ind102's resultant scan is a common root with w outside (0, 1). One per wall is the spurious factor's
root, as #133 reports.
