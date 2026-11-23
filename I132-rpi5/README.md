# I132-rpi5: logs of the enclosure of F + r f' at the tanh wall's T1 root for every sigma R_b (#132)

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/132

## Code and environment

Code: worktree `~/Source/negative-mass-i132` on branch `wip/i132-tanh-bound`, started at main 51ced6d. New files only:
`notes/warp/he_tanh_bound.py`, `notes/warp/he_tanh_bound_output.txt`, `notes/warp/he_tanh_bound.md`.
Python: `~/Source/negative-mass-venv314/bin/python` (3.14.10, sympy 1.14.0, mpmath 1.3.0). Every run is `nice -n 10` with
`OMP_NUM_THREADS=1`, one process at a time. A run longer than a few minutes is a systemd user unit `nm-i132-<step>` with
`RuntimeMaxSec=10800`, started by `run_step.sh`, which writes `<step>.log`, `<step>.time` (wall seconds, peak rss in KB)
and `done/<step>.rc`. Memory is reported only and is never a stop condition. Nothing of choptuik-large-d is touched.

## What is computed

The profile f = [tanh sigma (r + R_b) - tanh sigma (r - R_b)] / (2 tanh sigma R_b) in y = sigma r and p = sigma R_b is
f = cosh^2 p / [cosh (y + p) cosh (y - p)]. With w = 2 y and C = cosh 2p the root condition (r f')' = 0 is linear in C,
P(w) + C Q(w) = 0, and at a root F + r f' = T(w) / (Q (cosh w + C)^2) with T = A Q - P B. The script proves the sign of
T by hand-checkable identities (route 1) and, independently of that algebra, covers p in [0, 100] by interval arithmetic
on the profile's own jets (route 2): per p cell, no root for y in (0, y_a] and y >= y_t, the roots enclosed by a sign
change, unique by the sign of the y-derivative of (r f')'/f, and F + r f' and r f' bounded on the enclosure.

## Steps

| step | what | log | stop condition |
|---|---|---|---|
| 2 | `he_tanh_bound.py --pilot`: identity, jets, reduction, planted profile, the pilot cell p in [0, 0.01] | `step2.log` | not finished in 3 h wall: stop and report what finished |
| 3 | `he_tanh_bound.py --no-controls`: all checks, the full cover of p in [0, 100], the large-p evaluation | `step3.log` | not finished in 3 h wall: stop and report what finished |
| 4 | every `--mutate=NAME`, each must exit 1 and fail exactly its targets below | `mutate_<name>.log` | none |
| 5 | `he_tanh_bound.py > notes/warp/he_tanh_bound_output.txt`, must exit 0 | `final.log` | 3 h wall |

## Pass criteria, written before the runs

- `identity`: f in tanh form equals the cosh form and (1 + C)/(cosh 2y + C) as exact rational identities in e^y and e^p;
  numeric agreement at 3 points to 1e-40; L1 = -(tanh(y+p) + tanh(y-p)) = -sinh 2y/(cosh(y+p) cosh(y-p)).
- `jets`: the interval evaluators of the tanh and planted profiles (f, L1, L2, L3, Psi, Psi_y, E, r f') enclose
  mpmath's `diff` of the definition at 4 points, p = 0 included, to 1e-25.
- `reduction`: exact in sympy: Psi (cosh w + C)^2 = -2 (P + C Q); E (cosh w + C)^2 = A + C B; Q (A + C B) - B (P + C Q)
  = T; T = -w sinh w (cosh w - 1) m(w) with m = w (cosh w + 2) - 3 sinh w; the Taylor coefficients of m are
  2 (k - 1)/(2k + 1)! at w^(2k+1), checked to k = 40. By hand the coefficients are positive for k >= 2, so m > 0.
- `planted`: f = sech^2(r)/10 through `cell_proof`, the same code as the cover: a root is enclosed with F + r f' > 0 and
  r f' < 0 on the enclosure, inside [0.894, 0.896] for F + r f' (#101: 0.8946).
- `cover`: cells tile [0, 100] with no gap; in each cell (0, y_a] and [y_t, infinity) are excluded, the leaves tile
  [y_a, y_t], the roots are enclosed with a sign change and are unique, r f' < 0 and F + r f' <= -0.05 on every
  candidate leaf; the closed-form root and F + r f' at the cell's three p values (ends and middle) lie in the enclosure.
- `large_p`: at p = 100, 1000, 10^4 the exact root of the closed form is enclosed by bisection, F + r f' < 0 there and
  in (-p/2 + 1/2, -p/2 + 1/2 + 1/(4p)).
- `sup`: the closed form at C = 1 (p -> 0) gives w_0 = 2.0191131 (y_0 = 1.00955655) and F + r f' = -0.05367560306 enclosed to 30 digits (a 40-digit evaluation made while designing, not a run of the script).

## Controls: targets and predictions, written before the first control run and not changed

`--mutate=NAME` runs the whole script with the change. The checks that fail must be exactly the targets.

| control | what it changes | targets |
|---|---|---|
| `shift` | adds 0.06 to F + r f' in the cover's evaluation of E | `cover` |
| `identity-break` | the cosh form of the profile has cosh p for cosh^2 p in the numerator | `identity`, `jets`, `cover` |
| `no-tail` | drops the r -> infinity exclusion, so every cell has a gap (y_t, infinity) | `cover`, `planted` |
| `no-small` | drops the r -> 0 exclusion, so every cell has a gap (0, y_a] | `cover`, `planted` |
| `cell-gap` | removes one cell from the tiling of p | `cover` |
| `jets-typo` | 2 L2 becomes L2 in Psi_y (Psi_y only grows, so the cover still proves uniqueness) | `jets` |
| `proof-typo` | the coefficient 2 (k - 1) of m's Taylor series becomes 2 k - 1 | `reduction` |
| `factor-typo` | the factor (cosh w - 1) of T becomes (cosh w + 1) | `reduction` |
| `planted-eps` | the planted epsilon 1/10 becomes 1, so F + r f' = -0.054 at its root | `planted` |
| `asym-typo` | the asymptote -p/2 + 1/2 becomes -p/2 + 1 | `large_p` |

A control that fires on other checks than its targets, or on fewer, is reported as a result and not adjusted.

## Run notes

- First launch of step 2 (`aborted/step2.log`, header only): stopped by me after 2 min 20 s. The exact identity check built
  nested derivatives of the profile without simplifying between them, and did not finish. With a `cancel` after each
  derivative the five exact checks take about 7 s. No result came from that run.
- Second launch (`aborted/step2_first_run_reduction_k0.log`): `reduction` failed on its Taylor-coefficient line. My
  expected formula 2 (k - 1)/(2k + 1)! for the coefficient of w^(2k+1) in m(w) = w cosh w + 2 w - 3 sinh w does not hold at
  k = 0, where the extra 2 w gives 1 - 3 + 2 = 0, not -2. The mathematical claim is unchanged (the coefficients are 0 at
  k = 0 and 1 and positive from k = 2). The check now tests the formula for 1 <= k <= 40 and the value 0 at k = 0, and
  the control `proof-typo` still fails it. Every other check passed in that run.
- The README's `sup` line first had w_0 and F + r f' from a rough estimate (2.0189 and -0.053684). Corrected before any
  run to the 40-digit evaluation made while designing (2.0191131 and -0.05367560306).
