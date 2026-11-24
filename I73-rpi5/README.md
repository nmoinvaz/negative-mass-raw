# I73-rpi5: the Hawking–Ellis type of the accelerating bubble, closed-form D of the (E_0, E_1, e_ρ) block (#73)

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process at a time, nice 10, one thread.
Issue: https://github.com/nmoinvaz/negative-mass/issues/73
Worktree: `~/Source/negative-mass-i73`, branch `wip/i73-he-accel` (base main c1c3deb).
Python: `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0, mpmath 1.3.0, numpy 2.5.4, scipy 1.18.1).

Written 2026-11-23, before the first run of `notes/warp/he_accel.py`. The criteria, the planted case, the control names and
the control targets below are fixed here. Anything changed after seeing data is listed at the end under "Added after the first
run". Before this README I read #61's, #64's and #71's closing comments, `he_type.py`, `he_type.md`, `phantom_source.py` and
its "An accelerating bubble"; I ran nothing and derived no entry of the block.

## What is built

`notes/warp/he_accel.py` imports, unchanged:

- from `phantom_source.py` (`ps`): `ricci`, `shift_metric`, `shift_tetrad_ricci`, `bubble_rule`, `JetD`, `ricci_at_point`,
  `reduce_R`, the jet symbols `VS`, `XS`, `F`, `X`, `y`, `z`, `R` (route D, #61's frame Ricci tensor of the accelerating bubble,
  and route E, the exact-point planted truth for its time derivatives);
- from `he_type.py` (`ht`): `mixed_block`, `cubic`, `disc`, `exact_sign`, `he_type_exact`, `planted_cases`, `route_C`,
  `ClosedForm`, `numeric_type`, `einstein_N`, `tanh_jets`, `wall_radii`, `polar_grid`, `fraction_I`.

It adds: the block of route D at z = 0 in (c, s) = (cos θ, sin θ); the discriminant of its cubic with v_s, v_s′, x_s′ free;
its structure; and route N′, a numerical Einstein tensor for an explicit b(t, x, y, z) whose derivatives come from sympy's `diff`
of the explicit function, assembled with numpy (no `ricci`, no frame, no jets).

The block is (E_0 = n = ∂_t − b ∂_x, E_1 = ∂_x, e_ρ) with b = −v_s(t) f(r_s), r_s² = (x − x_s(t))² + y² + z². At z = 0, y > 0
the frame (E_2, E_3) = (∂_y, ∂_z) is (e_ρ, e_ϕ). Notation: v = v_s, α = v_s′, u = x_s′ (so Alcubierre's journey is u = v).
Classification is #64's: D > 0 Type I, D < 0 Type IV, D = 0 the rank test (`he_type_exact`).

## Acceptance of the issue, and what each becomes

| issue criterion | check | pass criterion |
|---|---|---|
| closed-form D agrees with numerical eigenvalues at every grid point, for at least one accelerating v_s(t) | `closed_vs_numeric` | at every point of every grid below, sign of D (exact at 50 digits where float64 is in doubt) gives route N′'s eigenvalue type; unresolved = 0 |
| `accel-static` fires | `--mutate=accel-static` here, and `phantom_source.py --mutate=accel-static` run as a subprocess | both exit 1; the second fails `gen_xcheck` and `accel_xcheck` |
| dropping the acceleration terms changes the map, detected | `drop_detected`, `--mutate=drop-accel` | see thresholds |
| constant-speed limit reproduces #64's map | `const_limit` | see below |

## Profiles and grids (fixed now)

- **P1**, Alcubierre's journey, x_s′ = v_s: v_s(t) = sech²(2t), x_s(t) = tanh(2t)/2. α = −4 sech²(2t) tanh(2t).
- **P2**, x_s free, v_s through 0: v_s(t) = tanh(2t), x_s(t) = (3/10) ln cosh 2t − (2/15) cos 3t + t/4, so
  u = (3/5) tanh 2t + (2/5) sin 3t + 1/4 and α = 2 sech²(2t).
- Times t ∈ {−0.6, −0.3, 0, 0.3, 0.6} for each, so 10 slices. P1 has α = 0, u = v at t = 0 (a planted slice that must equal the
  constant-speed map at v = 1), α of both signs, v > 0. P2 has v < 0, v = 0 (t = 0, with α = 2 and u = 1/4) and v > 0, and u ≠ v
  at every t. Why this is generic enough: D is a polynomial in (v, α, u) (the symbolic checks cover all values); the grid check
  runs the whole chain, entries → cubic → sign, against independent numerics at 10 distinct triples (v, α, u) with every sign
  pattern of v and α and with u = v and u ≠ v.
- Walls, as #64: Le (σ = 8, R_b = 1, f ∈ [0.1, 0.9], r_s ∈ [0.8627, 1.1373]) and Rodal (σ = 4, R_b = 5, r_s ∈ [4.25, 5.75]),
  `polar_grid` 240 × 240 midpoints in (r_s, θ), a random azimuth per point for route N′, plus Rodal's axis θ = 0, π at 301 radii each.
  Per slice 2 × 57 600 + 602 points, 10 slices: 1 156 120 points.
- A float64 disagreement, and any point with |D| < 1e-10 scale⁶, plus the three points nearest D = 0 per grid, are rechecked at 50
  digits (up to 100 per grid) with both routes in mpmath, as in `he_type.py`.
- Controls run the whole script. If the full run takes more than 15 min on this machine, controls use `--quick`: slices
  t = ±0.3 of each profile and every 2nd index of each polar grid. That is a subset of the checked points, so a failure there
  is a failure of the full check. The output header says which.
- Stop condition: a run not finished after 1 h of wall time is stopped and what finished is reported. Memory is only reported.

## Checks, controls and targets (predictions, written before any run)

A control is a `--mutate=NAME` run. It fires if its exit is 1 and every target check fails. Other checks failing too is allowed
and listed. A target that does not fail is reported as SILENT, not adjusted.

| check | what it tests | controls and targets |
|---|---|---|
| `planted_cls` | #64's nine planted tensors get their type through `he_type_exact` | `disc-sign`, `no-rank` → `planted_cls` |
| `routeN_planted` | route N′ at α = 0, u = v equals `ht.einstein_N` (mixed G, 40 random points, relative 1e-10) | `num-drop-w2` (g_tt without b²), `num-static` (every t-derivative of b zeroed) → `routeN_planted` |
| `routeN_vs_E` | route N′ at accelerating exact points: eigenvalues of mixed R equal those of η R_frame from route E | `num-drop-w2`, `num-static` → `routeN_vs_E` |
| `entries_E` | route D's block at z = 0 equals route E (exact rationals, explicit rational v_s, x_s, f) at 8 points | `accel-static`, `alc-drop-w2` (route D with g_tt = −1), `accel-lapse` (lapse 1 + b) → `entries_E` |
| `decouple` | (I1) R(e_ϕ, ·) = 0 and (I2) R_00 + R_11 + 2R_ρρ = 0 for the block, exact symbolic identities in (v, α, u, f, f′, f″, r, c) | `alc-drop-w2`, `accel-lapse` → `decouple` |
| `const_limit` | at α = 0, u = v the block equals `ht.route_C()` entry by entry (exact); the type map equals `ht.ClosedForm`'s sign map at every point of Le's wall at v = 0.5, 1, 2, 2.5 and Rodal's band at v = 1 (240²); P1 at t = 0 equals it at v = 1; the Le fractions at 2000² equal `he_type_output.txt` (1.151, 5.60, 17.28, 22.63) to its digits | `alc-drop-w2`, `accel-static` → `const_limit` |
| `time_lemma` | R(v, u, α) − R(v, v, 0) is supported on (00, 11, 1ρ), linear in ΔT_x and ΔT_ρ (ΔT = ∂_t∂b minus its constant-speed value), as an exact identity | `time-lemma-sign` (claim with the sign of the ΔT_ρ term flipped) → `time_lemma` |
| `structure` | under (v, u, α) → (λv, λu, λ²α) the entries R_0i scale as λ, the others as λ², so D has only the weights λ⁶, λ⁸, λ¹⁰, λ¹²; the λ⁶ part is −4\|j\|⁶; the λ¹² part is χ(λ₀)²[(S₁₁ − S_ρρ)² + 4S₁ρ²] ≥ 0 (symbolic, in generic block entries, then in the bubble's) | `weight-break` (α counted as weight 1) → `structure` |
| `axis` | on c = ±1, D = −4 R_01² (R_00² + R_01²)², so Type IV wherever v f′ ≠ 0 for every α and u (symbolic); D < 0 at all axis radii of Rodal's band on all 10 slices that have v ≠ 0 | `axis-flip` (the claimed form with + 4), `alc-drop-w2` → `axis` |
| `rest` | at v = 0 the momentum entries vanish and D ≥ −1e-12 scale⁶ on both walls at P2 t = 0 (Type I, with the rank test at exact points of D = 0) | `rest-v` (the slice at t = 0.05, v = tanh 0.1 ≠ 0) → `rest` |
| `closed_vs_numeric` | as in the table above | `drop-accel` (D evaluated at α = 0, u = v), `alc-drop-w2`, `num-drop-w2`, `num-static`, `accel-static`, `disc-sign` → `closed_vs_numeric` |
| `drop_detected` | the type labels with the acceleration terms dropped (α = 0, u = v at the same v) differ from the full ones at ≥ 1 grid point at every slice with v ≠ 0 and (α ≠ 0 or u ≠ v), on both walls, and the Le Type I fraction differs by ≥ 1 percentage point at ≥ 1 slice of each profile; at P1 t = 0 they are identical | `drop-accel` → `drop_detected` (the full D is the dropped one, so no label differs) |

Predicted not to fire: `drop-accel` leaves `const_limit` alone (the dropped D is the constant-speed D); `disc-sign` and `no-rank`
leave the route checks alone. `phantom_source.py --mutate=accel-static` is expected to fail `gen_xcheck` and `accel_xcheck`
(its stored output header lists them).

## Predictions about the answer (not criteria; each is tested above)

1. The block contains only the jets v_s, v_s′, x_s′, f, f′, f″. Neither x_s″ nor v_s″ enters, so the issue's "x_s″" does not.
   If a check finds otherwise this is reported as a disagreement with `phantom_source.md`.
2. The momentum entries R_01 and R_0ρ do not depend on α or u.
3. The axis is Type IV wherever v_s f′ ≠ 0, at every acceleration.
4. At v_s = 0 with α ≠ 0 every point is Type I, where #64's map at v → 0 is Type IV. Acceleration therefore moves the Type I set up
   at low speed.
5. The type at a point depends on the motion through (v, ΔT_x, ΔT_ρ) only.

## Not covered

The surface D = 0 off the points that `he_type_exact` is run on (#72's results are for constant speed), the time evolution of the
map along a journey, any lapse other than 1, Lean statements (#135). The lemma lists in `he_accel.md` are written for #135.

## Changed before the first run of the script (2026-11-23, no run of `he_accel.py` exists yet)

1. **`drop_detected`.** The criterion said the labels differ "at every slice with α ≠ 0 or u ≠ v". At v = 0 (P2, t = 0) that cannot
   hold: with the acceleration dropped the block is the zero tensor, which is Type I, and with it the point is Type I too, so
   the I/IV labels coincide. That is prediction 4, not a failure of the check. The criterion is now "at every slice with
   v ≠ 0 and (α ≠ 0 or u ≠ v)"; the labels at P2 t = 0 are reported, and `rest` covers that slice.
2. **Scratch derivation.** After writing this README and before the script I derived the closed form in scratch files (not in
   the repository): route D's block at z = 0 equals R_00 = T_x − A, R_01 = j₁, R_0ρ = j_ρ, R_11 = A − q − T_x,
   R_1ρ = B − T_ρ/2, R_ρρ = q/2, with T_x = ∂_t∂_x b, T_ρ = ∂_t∂_ρ b, and the cubic of M − M_00 I has the coefficients
   c₂ = q − p, c₁ = j₁² + j_ρ² − pq − h², c₀ = 2 j₁j_ρh − p j₁² + q j_ρ², with p = R_ρρ + R_00, h = R_1ρ, q = 2R_ρρ. So predictions
   1, 2 and 5 held in scratch and the script re-checks them as stated, with the controls above. `ht.route_C()` takes 17 s here, so
   no cache of symbolic results is used.

## Added after the first run

**First full run** (`step3.log`, `--no-controls`, exit 1, 178 s, 11 of 12 checks pass): `closed_vs_numeric` FAILS, with 86 float64
disagreements and 516 unresolved points, all of them on Rodal's axis at P2 t = 0. There v = 0 and s = 0, so D = al⁶ f′⁶ s⁴/16 = 0
exactly and R^a_b is diagonal. Route N′'s eigenvalues are real (max |Im| = 0), as Type I requires. The check read the sign of
D = −8e-59 at 50 digits (rounding noise) as Type IV, and `compare` counts every flagged point beyond the first 100 per grid as
unresolved, here 602 flagged. So the result of the check as written is FAIL. It is not a disagreement between the closed form and
the numerics: both give "not Type IV", and `rest` gives Type I at the exact points of this locus (he_type_exact, rank test).
The written criterion did not say what a point with D = 0 exactly is, and #64's classification says the rank test decides.

Changes made after seeing this, before run 2:

1. **How D = 0 is decided in the recheck: exact factor, option (a) of the coordinator.** At a flagged point, D = 0 only if the
   closed form has an exact vanishing factor: at v = 0 exactly (the slice value tanh 0 is exactly 0), D = α⁶ f′⁶ s⁴/16, proved in
   `structure`, and s⁴ = (1 − c²)² is evaluated in exact rationals from the float c. It is zero exactly at c = ±1. Such a point
   is D = 0, hence not Type IV, and route N′ must then show no complex eigenvalue (|Im| ≤ 1e-30 scale at 50 digits, as before).
   Every other flagged point is classified by the sign of its 50-digit D, so a tiny negative D stays Type IV. No tolerance decides
   D = 0. A D = 0 point off this locus would be reported as unresolved. My first version of this change, "|D| ≤ 1e-40 scale⁶ is
   D = 0", was vetoed by the coordinator (a tolerance chosen after seeing the data, which would also pass a tiny negative D). A
   rerun with it began and was stopped by me in section 2 before it reached any grid; its files are in `aborted_vetoed_rule/` and
   it is not a result.
2. The recheck cap of 100 points per grid is raised to 1000, so every flagged point of a grid is rechecked. This is a resource
   limit, not a pass criterion.
3. New check `parity`: D(v, −α, u; −c) = D(v, α, u; c) as an exact identity, seen in the tables of the first run (the Type I fraction is
   even in α). Control `parity-break` (c not flipped) → `parity`.

The criterion of `closed_vs_numeric` is otherwise as written above. Run 1's `closed_vs_numeric` FAIL (`step3.log`) stands as the result of
the check as written; run 2 is `step3b.log`.

The first run's other results are unchanged by these changes.

## Added before the control runs (step 4), after run 2

- **First control queue stopped.** The first `disc-sign` control, with the recheck cap of 1000, took about 11 min, because every grid
  of a mutated run has tens of thousands of float64 disagreements and 1000 of them were rechecked at 50 digits. I stopped the queue
  and set its files aside in `aborted_slow_controls/` (not a result).
- **No recheck when more than 1000 points are in doubt.** Then the check fails whatever the first 1000 rechecks give, because
  every point beyond the cap counts as unresolved, so the pass/fail result is unchanged and only the time is saved. A grid with at
  most 1000 flagged points is rechecked in full, as in run 2. Every grid of run 2 was in that case.
- The script also prints the list of monomials of 64 r⁶ D (section 5). No check changes.
- The controls are the single runs of `launch_controls.sh`, one `--mutate=NAME` per process, log `ctl_NAME.log`, exit code
  `ctl_NAME.rc`. Their targets are the table above.
- **Second stop, `accel-lapse`.** The control with the lapse 1 + b was still in `structure` after 6 min, doing symbolic algebra on a
  block with rational entries that violates (I2). I stopped the queue (`aborted_lapse_structure/`, not a result). `structure` and
  `parity` now fail at once, without computing, for a block that fails (I1) or (I2): the shifted form of D is not defined for it. For
  the unmutated block nothing changes (a dev run of sections 1 to 7 gives the same output). `accel-lapse` and `alc-drop-w2` break
  (I2), so `structure` and `parity` fire for them by this rule and not by their content. They are not targets of those two controls.
  Controls already finished before this change: `disc-sign`, `no-rank`, `num-drop-w2`, `num-static`, `accel-static`; their blocks satisfy (I2).
- **Third stop, `accel-lapse` again.** With the guard in place the control passed `const_limit` (it fails there) and then did not finish
  the symbolic axis check on its rational entries within 6 min. I stopped it (`aborted_lapse_axis/`; its log already shows `entries_E`
  and `decouple` failing, but it is not a result). `--mutate=accel-lapse` now stops after section 3, where both of its targets
  are decided, unless `--stop` is given. The output of that run says so. No other control or check changes.

