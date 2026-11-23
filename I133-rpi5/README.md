# I133-rpi5: logs of the rigorous count of the tanh wall's Type III points at Le's and Rodal's speeds (#133)

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/133

## Code and environment

Code: worktree `~/Source/negative-mass-i133` on branch `wip/i133-type3-count`, started at main f9e5102. New files only:
`notes/warp/he_type3_count.py`, `notes/warp/he_type3_count_output.txt`, `notes/warp/he_type3_count.md`.
Python: `~/Source/negative-mass-venv314/bin/python` (3.14.10, sympy 1.14.0, mpmath 1.3.0). Every run is `nice -n 10` with
`OMP_NUM_THREADS=1`, one process at a time. A run longer than a few minutes is a systemd user unit `nm-i133-<step>`
with `RuntimeMaxSec=10800` (the 3 h stop condition), started by `run_step.sh`, which writes `<step>.log`, `<step>.time`
(wall seconds, peak rss in KB) and `done/<step>.rc`. Memory is reported only and is never a stop condition. Nothing of
choptuik-large-d is touched.

Before this README: exploratory prototypes of the interval cover (scratch files outside the repository, no logs kept)
found, at 40 digits, 4 root leaves at Le over z in [0.5, 40] (733 leaves, 115 s) and 6 at Rodal over [0.5, 70]
(2103 leaves, 320 s), at the radii of he_type3.md. No result of this task rests on them; the script re-derives all of it.

## What is computed

At a fixed speed, with z = 2 sigma r, eps = e^-z and C = cosh 2 sigma R_b, the tanh profile is f = (1 + C)/(cosh z + C)
and (phi, A', B') = (v F, v r f', v r^2 f'') are rational in (eps, z). The Type III points are the common roots (r, w = c^2)
of E1 and E2 of he_type3.md with 0 < w < 1 and T != 0. Their radii are roots of P(phi, A', B') (the irreducible factor of
the resultant in w, 167 terms) or of the spurious factor y = B' - A' (phi > 0 for r > 0). The script

- covers z in [z_s, z_t] by interval arithmetic (mpmath `iv`, 50 digits, own forward-mode derivative) on g = P/t^9 with
  t = -A' > 0, and on the spurious factor, with exclusion by enclosure, uniqueness by a sign-definite derivative;
- proves P != 0 and y != 0 on (0, z_s] by the weighted expansion P = 774144 phi^8 delta^2 + (higher weight) in
  phi = z^2 Phi, psi = A' + 2 phi = z^4 Psi, delta = B' - A' = z^4 Delta, with series enclosures of Phi, Psi, Delta;
- proves P > 0 and y > 0 on [z_t, infinity) by dominance of the z^9 coefficient of the lowest (A', B') degree part;
- at each root cell finds every common root (z, w) with w in [0, 1] (and in a wide diagnostic range) by interval
  bisection and Krawczyk, and decides w in (0, 1) and T != 0 by enclosure;
- runs the same cover and classification on a planted problem with a known number of admissible roots (exact Sturm
  count in sympy), a close pair and roots with w outside (0, 1) or T = 0 among them.

## Steps

| step | what | log | stop condition |
|---|---|---|---|
| 2 | `he_type3_count.py --checks=identity,tables,planted,small_z,tail_z --no-controls`, then the pilot `--checks=cover,spurious,points --walls=Le --no-controls` | `step2.log`, `step2_pilot.log` | not finished in 3 h wall: stop and report what finished |
| 3 | `he_type3_count.py --no-controls`: all checks at both walls | `step3.log` | not finished in 3 h wall |
| 4 | every `--mutate=NAME`, each must exit 1 and fail exactly its targets below | `mutate_<name>.log` | 3 h wall each |
| 5 | `he_type3_count.py > notes/warp/he_type3_count_output.txt`, must exit 0 | `final.log` | 3 h wall |

## Pass criteria, written before the runs

- `identity`: the cosh form f = (1 + C)/(cosh z + C) and the (eps, z) forms of phi, A', B' agree with the tanh form of
  he_type3.jets_mp at 4 radii per wall to 1e-40, the interval jets enclose them, the forward derivatives enclose mp.diff
  of the tanh form, and the series of Phi, Psi, Delta agree with the closed forms at z = 0.1, 0.2.
- `tables`: he_type3's P times (27/256) phi^3 (A' - B')^3 equals the resultant of E1, E2 in w exactly (sympy), and equals
  an independent Sylvester determinant in exact fractions at 5 rational points; every P term has (A', B') degree 9 to
  15; the weighted expansion in (phi, psi, delta) has minimum weight 24 with leading part 774144 phi^8 delta^2.
- `planted`: the cover finds exactly the roots of the planted P (count from a sympy Sturm sequence, close pair of
  separation 1e-5 included), the classification returns the admissible points predicted by exact evaluation of the
  planted forms (w in (0, 1), T != 0), the roots with w outside (0, 1) and with T = 0 are rejected, and the planted tail
  is proved.
- `small_z`: at both walls the enclosure of G = P/z^24 over (0, z_s] excludes 0 and the enclosure of Delta excludes 0.
- `tail_z`: at both walls the dominance bound L > 0 for P and the positivity bound for y hold on [z_t, infinity).
- `cover`: the leaves tile [z_s, z_t] without a gap; each is excluded or holds exactly one root of g; the roots counted
  by the cover are the sign changes of the tanh-form P (mp, 60 digits) at the leaf ends; no unresolved leaf.
- `spurious`: the same for y; at each y-root no common root of E1 and E2 with w in [0, 1].
- `points`: at each P-root cell every common root with w in [0, 1] is isolated by Krawczyk; the admissible points (w in
  (0, 1), T != 0) are exactly 3 at Le and 3 at Rodal, with radii within 5e-7 of the table of he_type3.md section 5
  (0.990568, 1.023933, 1.094662; 4.714485, 5.071066, 5.103381), and the other P-roots (1 at Le, 3 at Rodal) have their
  common root with w outside [0, 1] (w = 58.459; 4.1007, 8.7173, 1.0300 from he_type3_output.txt) or none.
- `cross`: each admissible radius and cos(theta) lies within 1e-11 of the 12-digit values of he_type3_output.txt.
- `assembly`: `small_z`, `tail_z`, `cover`, `spurious` all pass, so the three ranges tile (0, infinity).

## Controls: targets and predictions, written before the first control run and not changed

`--mutate=NAME` runs the whole script with the change. The checks that fail must be exactly the targets.

| control | what it changes | targets |
|---|---|---|
| `sigma-1e-3` | sigma + 1e-3 at both walls (C and the radii; v fixed) | `points`, `cross` |
| `drop-P-term` | the first term of P's table is dropped wherever P is used | `tables`, `small_z`, `points`, `cross`, `assembly` |
| `no-tail-large` | the proof on [z_t, infinity) is removed | `tail_z`, `planted`, `assembly` |
| `no-tail-small` | the proof on (0, z_s] is removed | `small_z`, `assembly` |
| `cell-gap` | one leaf is removed from the tiling of each wall's cover | `cover`, `assembly` |
| `eps-typo` | D = 1 + 2 C eps + eps^2 becomes 1 + C eps + eps^2 in the jets | `identity`, `cover`, `spurious`, `points`, `cross`, `assembly` |
| `T-off` | the T != 0 condition is dropped from admissibility | `planted` |
| `w-range` | admissible w in (0, 1) becomes (-10^4, 10^4) | `planted`, `points` |
| `krawczyk-nocorr` | the Krawczyk operator drops its (I - Y J)(X - m) term | `planted`, `points` |
| `double-root` | the planted close pair becomes a double root | `planted` |
| `skip-y` | the roots of the spurious factor y are not classified | `planted`, `spurious`, `assembly` |

A control that fires on other checks than its targets, or on fewer, is reported as a result and not adjusted.

## Run notes

- Before any control run, the `eps-typo` row was changed from a~ = (1 - eps^2)/D^2 -> (1 + eps^2)/D^2 to D = 1 + 2 C eps + eps^2
  -> 1 + C eps + eps^2, with the same targets. Reason, from analysis and not from a run: the first typo changes every jet by a
  relative eps^2 (1e-14 at Le's wall, 1e-35 at Rodal's), so only `identity` would see it. The second moves the wall by ln 2.
- The Le pilot (`step2_pilot.log`, commit of the script 'warp: add he_type3_count.py ...') ran `--checks=cover,spurious,points,cross
  --walls=Le`, one check more than the README's step 2 (`cross`); it took 49 s, not hours.
- Step 4 was started once (commit 01acf50) and stopped by me after `sigma-1e-3` had begun, before any control result was read
  (`aborted/`). Reason: three changes to the script that every control must see. (1) The planted problem now also has a spurious
  factor: P_pl omits the factor z - 11/5 that a planted y_pl carries, so one admissible point sits at a root of y_pl, and the new
  control `skip-y` (row added above, before any control ran) must lose it. (2) `tables` checks the resultant identity exactly on
  three random lines as well as at five points. (3) `cover` and `spurious` also check the tanh-form sign at the midpoint of each
  excluded leaf, and `--dump-cells` exists. Step 4 and step 5 run on the commit after these changes.
- The step 3 log (`step3.log`) is from commit e154b77, before those changes; it is kept as the first full run.
- Pilot (`step2_pilot.log`): run on the working tree just before e154b77.
