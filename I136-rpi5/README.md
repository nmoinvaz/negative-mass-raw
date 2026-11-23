# I136-rpi5: independent exact-rational interval review of #133's Type III count (#136)

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/136

## Code and environment

Worktree `~/Source/negative-mass-i136` on `wip/i136-type3-review` (main ccd0326). New files only:
`notes/warp/review_he_type3_count.py`, its `_output.txt` and `notes/warp/review_he_type3_count.md`.
Python `~/Source/negative-mass-venv314/bin/python` (3.14.10, sympy 1.14.0, mpmath 1.3.0). One process at a time,
`nice -n 10`, `OMP_NUM_THREADS=1`. A run longer than a few minutes is a systemd user unit `nm-i136-<step>` with
`RuntimeMaxSec=7200` (the 2 h stop condition), started by `run_step.sh`, which writes `<step>.log`, `<step>.time` and
`done/<step>.rc`. Memory is reported only; nothing stops a run over memory. Nothing of choptuik-large-d is touched.

## Independence: what is and is not shared with #133

Not opened, imported or run: `he_type3_count.py`, `he_type3.py`, any other script or output file of `notes/warp/`; no
raw `I133-*` or `I102-*` logs; no mpmath `iv`; no python-flint. These stay closed until step 7.

Shared with #133 (typed from text): the frame table of `he_type3.md` section 1 (the six entries R00, R0x, R0rho, Rxx,
Rxrho, Rrhorho, M = eta R with eta = diag(-1, 1, 1), the printed c2 and E1), the tanh profile and the definition
(phi, A', B') = (v F, v r f', v r^2 f'') of `he_type3.md` section 5, and the statement of `he_type3_count.md` (walls,
ranges, counts, radii; its w and T values and the w of the other roots are used only as targets to compare with).

Two slips, disclosed here and on the issue:
1. My auto-memory held a handover summary of #133's method when this session started (reduction to (v, C, z) with
   z = 2 sigma r, C = cosh 2 sigma R_b; the weight form in (phi, A' + 2 phi, B' - A'); a z^9 dominance at large z). I
   re-derived the cosh form of the profile and every formula below before use, and checked each by an exact identity,
   but the idea of the two end bounds comes from that summary.
2. I opened lines 1 to 25 of the raw `I133-rpi5/README.md` while looking for a README format. It restates the same
   reduction. Nothing in the script was changed after reading it.

## What is computed

- f = (1 + C)/(cosh z + C), z = 2 sigma r, C = cosh 2 sigma R_b (exact identity with the tanh form, check `profile`).
  phi = v (cosh z - 1)/D, A' = v z f_z, B' = v z^2 f_zz, D = cosh z + C.
- E1, E2 are the coefficients of the characteristic polynomial of M, E1 = c2^2 - 3 c1, E2 = 27 c0 - c2^3, in
  (w; phi, A', B') with (X, gamma, y) = (A'^2, A', B' - A') (the weight scaling at u = 1). P = Res_w(E1, E2)/
  ((27/256) phi^3 (A' - B')^3), by sympy, then checked against an exact Sylvester determinant in Fractions.
- A Type III point of the wall is a common root (z, w) of E1, E2 with 0 < w < 1 and T != 0, T proportional to A' + B'.
  A common root forces Res = 0, so z is a root of P or of y = B' - A' (phi > 0). The proof is a count of those roots.
- Interval arithmetic: `fractions.Fraction` endpoints, outward rounding to a 160-bit grid after every operation (320 bits
  for root refinement and Krawczyk). exp is enclosed by a Taylor sum of degree N with remainder 2|y|^N/N! after
  halving the argument k times (|y| <= 1/2) and k interval squarings; cosh and sinh from exp(+-x); dual numbers give
  derivative enclosures. "Last place" = the spacing of the 160-bit grid at the endpoint (`ulp`); a computed exp
  enclosure is 1 or 2 spacings wide, so narrowing it by one ulp at each end empties it or leaves a point.
- mpmath at point precision (`mp`, not `iv`) is only a reference: tanh-form P and y (sympy derivatives of the tanh
  profile) and candidate starting points of the Krawczyk boxes. No result rests on it alone.

## Acceptance criteria (each can fail)

| # | criterion | check |
|---|---|---|
| 1 | own exp, cosh, sinh enclosures contain mpmath's 120-digit values on 300 random x in [-70, 70], are at most 2 ulp wide, and satisfy exp(x) exp(-x) containing 1, cosh^2 - sinh^2 containing 1 | `exp` |
| 2 | tanh form = (1 + C)/(cosh z + C) and f_z, f_zz closed forms (exact, sympy); (phi, A', B') and T from the tanh definition inside the enclosures at 2 x 12 radii | `profile` |
| 3 | c2 and E1 from the frame table equal the printed ones; 17 and 42 terms; E2 a cubic form with 10 terms; P has 167 terms, total degrees 10..18, irreducible, Res = (27/256) phi^3 (A' - B')^3 P; the table of P equals an exact Sylvester determinant at 6 rational points | `frame` |
| 4 | planted A: g = prod (cosh z - c_i) with 7 known roots in [1/4, 40] incl. a pair 1e-5 apart (2 more outside): exactly 7 root leaves, each holding exactly one known root, leaves tile, none open. Planted B: P_pl, E1_pl, E2_pl with 5 known common roots (a pair 1e-5 apart, one with T = 0, one with w = 7/2): 5 root leaves, 5 Krawczyk boxes, admissible set exactly [z = 3, 659/49, 5] | `planted` |
| 5 | (0, 1/4]: P = z^24 G with G > 0 and y = z^4 Delta with Delta < 0, series with remainders; weight-24 part of P in (phi, psi, delta) is 774144 phi^8 delta^2 and no lower weight exists | `small_z:le`, `small_z:rodal` |
| 6 | [z_t, oo): P = (tau z)^9 S with S > 0 (lower bound > 0 over all s = 1/z in (0, 1/z_t]), y > 0; the identity is exact | `tail:le`, `tail:rodal` |
| 7 | [1/4, z_t]: every leaf excludes a root or holds exactly one, leaves tile; P has 4 roots at Le (z_t = 40) and 6 at Rodal (z_t = 60), y has 1 at each; root enclosures contain the tanh-form root; leaf signs agree with the tanh-form sign | `cover:le`, `cover:rodal` |
| 8 | at each root of P: Krawczyk boxes in (z, w), all other common roots with |w| <= 1e4 excluded; 3 admissible points per wall (0 < w < 1, T != 0, T proven nonzero on the box) with r within 1e-9 of the statement's radii (and w within 1e-6, T within 1e-4); the other roots have their common root at w = 58.459 (Le), 4.1007, 8.7173, 1.0300 (Rodal) within 1e-3 | `points:le`, `points:rodal` |
| 9 | at y's root (r = 0.99211, 4.99374 within 5e-6): no common root of E1, E2 with |w| <= 1e4 | `spurious:le`, `spurious:rodal` |

A check that fails is a result. No threshold changes after data. The script exits 1 if any check fails.

## Planted problem (frozen before the first run)

A. `g(z) = prod (cosh z - c_i)`, c_i = rational (10^-30 grid) of cosh(zeta_i) for zeta = 0.9, 2.3, 2.30001, 7.5, 12, 25,
39.9 (inside [1/4, 40]) and 0.2, 41 (outside). Exact count by rational comparison of the c_i with my enclosures of
cosh(1/4) and cosh(40): 7. Root pair 2.3 and 2.30001: separation 1.000e-5. Run through the same `Cover` (same Iv, Du,
exp/cosh/sinh code, same leaf rules) over [1/4, 40]. `planted-double` multiplies g by (cosh z - c_0)^2, c_0 = cosh 5.5.

B. u1 = 3/10 + (z - 3)/100, u2 = 7/2 + (z - 7)/50, v1 = u1 - (z - 3), v2 = u2 - (z - 7)/2, v3 = u1 - (z - 5)(z - 5 - 1e-5);
E1_pl = (w - u1)(w - u2), E2_pl = (w - v1)(w - v2)(w - v3), P_pl = prod_{i,j} (u_i - v_j), T_pl = z - 5 - 1e-5.
Exact roots of P_pl in [1/4, 40]: z = 3 (w = 3/10), 659/49 (w = u1), 5 (w = 8/25), 5 + 1e-5 (T = 0), 7 (w = 7/2); the
other three factors have no root there. Expected admissible: z = 3, 659/49, 5. Same `Cover`, `refine_root`, `krawczyk`,
`common_roots` as for the walls.

## Controls (targets frozen before any run)

`--mutate=NAME` runs the listed checks with the change and must exit non-zero. "Must fire" = those checks print FAIL. A
control passes if every must-fire check fails. Other checks that also fail are reported, not counted for or against.

| mutation | change | checks run | must fire | expected silent |
|---|---|---|---|---|
| `sigma` | sigma -> sigma + 1e-3 at both walls (C and r = z/(2 sigma) use it) | all 14 | `points:le`, `points:rodal` (radii off by about 1e-6 > 1e-9) | `exp`, `profile`, `frame`, `planted`, `small_z:*`, `tail:*` (hold for any sigma); `spurious:*` and `cover:*` (shift about 1e-6 < 5e-6; counts unchanged) |
| `drop-P-term` | the term 4 phi^3 B'^9 removed from P's table | all 14 | `frame` (166 terms, Sylvester), `small_z:le`, `small_z:rodal` (weight-24 part gains 2048 phi^12), `tail:le`, `tail:rodal` (S(s=0) = 0), `points:le` | `exp`, `profile`, `planted`; `cover:*` not a target (the tanh-form reference uses the same table) |
| `exp-ulp` | each exp endpoint narrowed inward by one ulp | all 14 | `exp` | every check that builds C raises ValueError (inverted interval) and fails; not a target |
| `frame-typo` | R_x,rho = cs (X + phi y/2) instead of cs (X - phi y/2) | `frame`, `planted`, `cover:le` | `frame` (E1 differs from the printed one) | `planted`, `cover:le` need not fire |
| `tail-zt` | the tail bound starts at z = 4 instead of z_t | `tail:le`, `tail:rodal` | both (tau_t is huge, S not positive) | the exact identity parts pass |
| `small-z-range` | the small-z range is (0, 20] (Le), (0, 45] (Rodal), past the first roots of P and y | `small_z:le`, `small_z:rodal` | both | the algebra parts pass |
| `drop-leaf` | one leaf removed from the cover of P and of y | `cover:le` | `cover:le` (tiling) | |
| `krawczyk-shift` | the Krawczyk box is centred 20 half-widths from the zero | `planted`, `points:le` | `planted` (part B), `points:le` | `planted` part A |
| `w-range` | admissible window 0 < w < 100 instead of 0 < w < 1 | `points:le`, `points:rodal` | both (4 and 6 admissible instead of 3) | |
| `spurious-on-P-root` | the no-common-root test is run at the first root of P | `spurious:le`, `spurious:rodal` | both (a common root exists there) | |
| `planted-double` | g gets a factor (cosh z - c_0)^2 | `planted` | `planted` (an open leaf) | |
| `profile-typo` | the constant 2 of B' typed as 3 in the code of (phi, A', B') | `profile` | `profile` (the tanh-definition comparison) | the exact identity items of `profile` use closed forms typed separately and stay silent |
| `printed-typo` | the printed E1 coefficient (phi^2 - 3) gamma^2 typed as (phi^2 - 2) gamma^2 in the comparison | `frame` | `frame` (E1 minus printed is not 0) | everything else is built from the frame table and is unchanged |

The last two rows were added after the first batch of 11 controls, because `profile` had no control that fires it and
`frame-typo` fired through a construction error instead of the printed-E1 comparison. In the second revision of the script
(next to the two new hooks) a quotient that is not a polynomial is reported by `frame` instead of raised in the
construction, so `frame-typo` now reaches the E1 comparison. The first batch and the first full run are kept in `batch1/`
(script `3c7df24`); the final full run and all 13 controls are rerun on the second revision.

## Run plan

1. This README, then `make_index`, commit, pull `--no-rebase`, push.
2. `frame`, `profile`, `exp`, `planted` (E1, E2, P from the frame table, planted problem). Post, revise the ETA.
3. Le: `small_z:le`, `tail:le`, `cover:le`, `points:le`, `spurious:le`. Post.
4. Rodal: the same. Post.
5. The 11 controls above. Post.
6. `python3 notes/warp/review_he_type3_count.py > notes/warp/review_he_type3_count_output.txt`, exit 0.
7. Only then open `he_type3_count.py`, `he_type3.py` and their outputs; compare; write the note.

Estimate (before measuring): 3 to 5 h. The first trial cover (scratch, not logged) of P over [1/4, 40] at Le took 2 min.

## Run notes
- step2 (`exp`, `profile`, `frame`, `planted`): the first run (`step2_first_planted_unsorted.log`) failed `planted` part B
  because my expected list of known roots was not sorted by z (659/49 was paired with the root at 5). The criterion
  (admissible set exactly z = 3, 659/49, 5) was not changed; only the pairing. Rerun `step2.log`: 4 checks pass, 5 s, 71 MB.
- step3_le: the first run (`step3_le_first.log`) passed `small_z:le`, `tail:le`, `cover:le`, `spurious:le` and raised a
  TypeError in `points:le` (mpmath candidates were not converted to Fractions, a bug in the script). Fixed
  (`fr_of_mp`), `cover:le,points:le,spurious:le` rerun in `step3_le.log`: pass, 147 s, 75 MB.
- step4_rodal (`small_z:rodal`, `tail:rodal`, `cover:rodal`, `points:rodal`, `spurious:rodal`): pass on the first run, 250 s, 6 roots of P, 1 of y.
- First launch of the controls queue (`systemd-run ... ./controls.sh`) did nothing: the unit starts in `~`, so the relative
  path was not found, no log was written. Relaunched with absolute paths. No control ran twice.
- step5 (controls, script `3c7df24`, one process at a time): `controls_table.md` (made by `controls_table.py` from the logs and
  the targets frozen above). All 11 exit 1 and every frozen target fired. Mispredictions in the "expected silent" columns
  and in the stated mechanism, left as they are:
  - `sigma`: `spurious:le` also fired. I expected a shift of about 1e-6; the y root moved to r = 0.99211696 (statement
    0.99211), a difference 7e-6 above the 5e-6 tolerance of that check. The radii of the P roots moved by 1.5e-7 to 3e-5.
  - `exp-ulp`: only `exp` is a target and it fired. I wrote that every check building C would raise a ValueError.
    Actually `profile`, `frame`, `small_z:*` and `tail:*` stayed silent: cosh and sinh are sums of two exp enclosures
    that are rounded outward again, which absorbs a one-ulp inward move at the sizes involved, and those checks have
    wide margins. `planted`, `cover:*`, `points:*` and `spurious:*` raised ValueError (empty interval).
  - `frame-typo`: `frame` fired, but through a sympy PolynomialError while building P (with the typo the resultant is no
    longer divisible by (27/256) phi^3 (A' - B')^3), not through the E1-against-printed comparison, which was never reached.
  - `drop-P-term`: `cover:le` stayed silent (P still has 4 roots, at other radii), `cover:rodal` fired (4 roots, not 6).
  - `spurious-on-P-root`: fired through `complete False` (no candidate is given, so the real common root at the first root
    of P is not covered), not through a found box.
- Second revision of the script, b2c4ac7 (adds `profile-typo` and `printed-typo`, reports a non-polynomial P from `frame`, guards the
  exp squaring): the final full run (`step6.time`, output `final_output.txt`, the repository's `review_he_type3_count_output.txt`: 14 checks
  pass, 397.6 s, rss 92 MB, exit 0, identical to the first full run `batch1/step6_first_final_output.txt` except the timing lines) and all
  13 controls were rerun on it: `controls_table.md`. Every control exits 1 and every frozen target fired. `frame-typo` now fires `frame`
  through the E1-against-printed comparison (E1 minus printed is 6 phi A^2 w (w - 1)(A - B)) before the P quotient fails. `profile-typo`
  fires `profile` (38 misses of the tanh comparison) and `printed-typo` fires `frame` (E1 minus printed is -A'^2). The two mispredictions
  of the first batch (`sigma` also fires `spurious:le`; `exp-ulp` leaves `profile`, `frame`, `small_z`, `tail` silent) are unchanged.
  The script is frozen at b2c4ac7 from here on (coordinator, step 7).
- step7: `run_compare.sh` runs `notes/warp/review_he_type3_count_compare.py` (opens #133's files on purpose) and its two controls.
