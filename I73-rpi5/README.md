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
| `drop_detected` | the type labels with the acceleration terms dropped (α = 0, u = v at the same v) differ from the full ones at ≥ 1 grid point at every slice with α ≠ 0 or u ≠ v, on both walls, and the Le Type I fraction differs by ≥ 1 percentage point at ≥ 1 slice of each profile; at P1 t = 0 they are identical | `drop-accel` → `drop_detected` (the full D is the dropped one, so no label differs) |

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

## Added after the first run

(nothing yet)
