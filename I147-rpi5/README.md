# I147-rpi5: a mutation for each of the 16 checks of zerilli_derivation.py that had none

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process at a time, nice 10, one thread.
Issue: https://github.com/nmoinvaz/negative-mass/issues/147
Worktree: `~/Source/negative-mass-i147`, branch `wip/i147-zerilli-mutations` (base main 3400e74).
Python: `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0, mpmath 1.3.0).

Written 2026-11-23, before any run of the changed script and before any control run. Mutation names, what each changes, targets and exit
codes below are fixed here. Anything added after seeing data is listed at the end under "Added after the first run".

## Files and what stays fixed

- Written: `phase2/dg_proof/zerilli_derivation.py` (the `mut(...)` hooks and the header list), `zerilli_derivation_controls.py` (16 pairs
  appended after the existing 18), their `*_output.txt`. Not touched: `zerilli_derivation_lib.py`, the notes, #145's and #146's files.
- Unmutated criterion: exit 0, 32 PASS, 0 FAIL, printed output equal to the committed `zerilli_derivation_output.txt` apart from the
  `# [ n s]` timing lines.
- The 18 existing pairs and the `fsign_bg` MISS line (target PL.0c, first FAIL PL.O.3) stay as they are.
- A pair is OK iff the exit code equals the listed one and the first `FAIL` line has the listed id. Anything else is a MISS, reported as a
  MISS and not retargeted. A mutation that crashes with a traceback is a MISS too (no FAIL line).
- Exit 2 = a planted check (PL.*) failed (stops at once); exit 1 = a real check failed (`--failfast` stops at the first).
- Skip arguments: `--skip=PL.G,PL.X` only where the mutation touches nothing that PL.G.* or PL.X.* read (the pair's row says what it
  touches); the unmutated baseline runs every check.

## The 16 pre-registered pairs

Order is the script's execution order. "Reads" = what the check reads; the mutation changes only that or something the check alone reads,
so no earlier check can fire first.

| # | check | what the check tests | mutation | what it changes (all in `zerilli_derivation.py`) | target | exit | args |
|---|---|---|---|---|---|---|---|
| 1 | PL.0b | Ricci code on a known curved background: static de Sitter, Ric = (3/a²) g | `ds_sign` | the planted metric's f = 1 − r²/a² becomes 1 + r²/a² (anti-de Sitter, Ric = −(3/a²) g) | PL.0b | 2 | none |
| 2 | PL.G.odd | pure odd gauge h = L_ξ g gives δR = 0 | `gauge_odd` | the t-φ component of the odd gauge h is doubled (h is no longer a Lie derivative); PL.G.even runs first and reads the even h only | PL.G.odd | 2 | none (PL.G.even runs, about 90 s) |
| 3 | PL.X.odd | route 1 (dual numbers) = route 2 (covariant) for the odd ansatz, all components | `x_odd` | route 2 is handed the odd h with h_rφ → −h_rφ; route 1 gets h. PL.X.even and PL.G.* read other h | PL.X.odd | 2 | `--skip=PL.G` |
| 4 | PL.X.gauge_even | the same for the even gauge h | `x_gauge` | route 2 is handed the even gauge h with h_tt → −h_tt; route 1 gets h. PL.G.even reads the unflipped h | PL.X.gauge_even | 2 | `--skip=PL.G` |
| 5 | PL.O.1 | odd components have the angular form (1−x²)P' (x-independent coefficients) and the even components vanish | `odd_norm` | the t-φ component is read with norm 1 instead of 1/(1−x²) in `coef_eqs`; h_odd itself is unchanged, so PL.X.odd cannot see it | PL.O.1 | 2 | `--skip=PL.G,PL.X` |
| 6 | PL.O.2 | h0 is algebraic in the x-φ equation, and the t-φ equation is implied by the x-φ and r-φ equations on the h1 flow | `odd_flow` | the h1″ flow `F2odd` from the r-φ equation is scaled by 2 after it is solved | PL.O.2 | 2 | `--skip=PL.G,PL.X` |
| 7 | PL.O.4 | the comparison routine `same` reports a planted unequal pair as unequal and an equal pair as equal | `same_m0` | `same` evaluates its two arguments at M = 0 before comparing, so an M-dependent difference is invisible; PL.O.3 still passes (its difference is 0 at M = 0 too) | PL.O.4 | 2 | `--skip=PL.G,PL.X` |
| 8 | E.2 | tr, tx, rx and δG_rr hold no second derivatives, det ≠ 0, A is a function of the states | `grr_trace` | the angular-trace term of δG_rr = R_rr/2 + R_tt/(2f²) − E_trace/(2 f r²) gets the coefficient of 1/(f r²) instead of 1/(2 f r²), so δG_rr keeps second derivatives. A.1, A.2, E.1 read other quantities | E.2 | 1 | `--skip=PL.G,PL.X` |
| 9 | E.3b | d(H_expr)/dr along the 2-D flow = the r-θ flow component H′ | `hexpr_sign` | H solved from A = 0 gets the wrong sign: H_expr = +(aK K + a1 H1)/aH. It is defined after E.2, E.3 and E.4 | E.3b | 1 | `--skip=PL.G,PL.X` |
| 10 | E.4 | on the flow, tt, tr, rr, tx, rx and trace are multiples of A | `e4_drop` | E.4 reads the tt equation with its undifferentiated K_0 terms dropped; E.2 and E.3 build A from the unmutated equations | E.4 | 1 | `--skip=PL.G,PL.X` |
| 11 | E.5a | the map (K, H1) → (ψ, ψ_x) has det ≠ 0 | `e5a_det0` | the det that E.5a reads is replaced by 0 (see "Predicted limitation" below) | E.5a | 1 | `--skip=PL.G,PL.X` |
| 12 | E.5c | V = a − s² does not depend on s | `v_s2` | the s² is not subtracted: V = a. E.5b (b = 0) is before V is formed and passes | E.5c | 1 | `--skip=PL.G,PL.X` |
| 13 | E.6b | (9) ∘ (3) = id on the converse's jets | `back_coef` | in the typed copy of (9) inside E.6b the second term has λ instead of λ + 1; E.6a does not read it, E.5 has its own copy | E.6b | 1 | `--skip=PL.G,PL.X` |
| 14 | D.3 | the divisor set contains s (the derivation needs s ≠ 0) | `d3_s1` | s = 1 is substituted into every recorded divisor before the factors are classified; every other factor is still in the allowed set, so D.1 passes | D.3 | 1 | `--skip=PL.G,PL.X` |
| 15 | D.4 | r − 2M is a divisor, and no step divides by L − 2 | `d4_l2` | a divisor 1/λ (denominator L − 2) is appended to the recorded divisors; L − 2 is in the allowed set, so D.1 passes | D.4 | 1 | `--skip=PL.G,PL.X` |
| 16 | D.5 | det3, aH and det_e are nonzero | `d5_ah0` | the aH that D.5 reads is replaced by 0 (see "Predicted limitation") | D.5 | 1 | `--skip=PL.G,PL.X` |

Why `--skip=PL.G,PL.X` is allowed for rows 5 to 16: the mutation acts on a quantity defined after the planted checks, and neither PL.G.* nor
PL.X.* read it. The existing pairs use the same convention. Rows 2 to 4 run the earlier planted checks they could disturb.

## Predicted limitation (E.5a and D.5)

Both checks test that a quantity is nonzero. The same quantity is a divisor before the check is reached: `master_reduce` (in the library)
divides by det_e, and the code divides by aH and det3 earlier. A mutation that really makes the quantity 0 therefore ends in an earlier crash
or an earlier FAIL, not in E.5a or D.5. Prediction from reading: ψ ≡ 0 raises ZeroDivisionError inside `master_reduce` (no FAIL line, exit 1).
Step 2 runs that probe once (`probe_psi_zero.py` here) and records the result. The pairs use the other way to break the check's input: the
value that the check reads is replaced by 0, which shows that the comparison fires but not that the pipeline reaches it. #145's `psi_zero`
and `d5_zero` are the same kind of control but #145 split the division out of its reduction.

## Predictions I am least sure of

- `odd_norm` (row 5): the t-φ P' coefficient of δR carries a factor (1−x²); read with norm 1 it depends on x, so `coef_eqs` returns not ok. If
  the coefficient has no x dependence the run passes PL.O.1 and the pair is a MISS (silent control, reported as such).
- `grr_trace` (row 8): the angular-trace equation holds second derivatives of K and H (visible in the printed pp (P) equation), so doubling
  its weight in δG_rr leaves second derivatives. The check's other conjuncts may fail too; the id is the same.
- `d3_s1` (row 14): after s = 1 no recorded factor may fall outside the allowed set; if one does, D.1 fires first and the pair is a MISS.
- `gauge_odd` (row 2): 2 h_tφ(gauge) is the gauge h plus a pure odd (h0 only) perturbation, whose δR_tφ is not 0.

## Plan and limits

1. This README, then the mutations, then one unmutated run diffed against the committed output (step 2).
2. Controls: `zerilli_derivation_controls.py` (baseline + 34 pairs) as a systemd user unit `nm-i147-controls`, logs in `controls_logs/`.
3. Stop condition: a single run longer than 1 h of wall time is stopped and what finished is reported. Memory is reported, never a stop
   condition.

## Added after the first run

(none yet)
