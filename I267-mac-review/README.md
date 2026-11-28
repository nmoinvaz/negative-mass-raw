# I267-mac-review: the coordinator's review of #267 (G's settled mass against the member at departure as δ → 0)

Machine: the coordinator's Mac (Apple M5, macOS), nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/267

Under review: branch `wip/i267-mass-vs-member` at 86b6039, raw `I267-mac` at 3f5f2b89 (criteria d534bf03).

## ind267.py: an independent reading of the raw runs

Written by the coordinator; it imports nothing from the repository. It reads `I267-mac/runs/G_B0.1/h0.005/e<e>/` and
#266's `I266-mac/runs/<member>/h0.005/` and does its own:
- departure time: from `member/locus.npz`, the odd part (r_b − r_a)/2 at the steps common to the pair, over the mean, first
  crossing of 1e-3 at t ≥ 6, linear in t between steps;
- member at departure: r_th (the pair's mean throat radius) and s_m of the two stored slices that bracket t_dep, linear in t;
  γ₁ = s/√(1 − s²);
- plateau: the plain mean of M over the cells of `chain/series.npz` with x⁺ ≥ max x⁺ − 1;
- relation: (a, b) by least squares of M/r_th − M₀ = aγ₁ + bγ₁² over #266's four B (0.025, 0.05, 0.1, 0.125), M₀ the
  plateau of #266's member O.

Shared with the runner's code: the evolution, the chain and the stored slices, and #225's `fit_asym` (the stored s_m).
Not shared: the departure time, the interpolation, the plateau mean and the fit.

Criteria, written before the first run:
- K1: the reading reproduces the note's table at δ = 1e-7 … 1e-12 (h = 0.005): t_dep within 1e-3, r_th within 1e-6,
  γ₁ within 1e-5, M within 2e-6.
- K2: (a, b, M₀) within (1e-3, 1e-2, 2e-6) of the note's (0.2027, 0.8534, 0.223086).
- K3: M − predicted at the six δ within 1e-5 of the note's column; and the largest |M − predicted| over δ = 1e-9 … 1e-12
  exceeds the declared bar 6e-5 (PRED not met is reproduced).
- K4: dM from δ = 1e-8 to 1e-12 within 1e-5 of +2.074e-3 and its predicted part within 2e-5 of +1.186e-3.
- K5 (the note's post hoc numbers): the excess dM − (M/r_th) dr_th between neighbouring decades, 1e-7 … 1e-12, has the
  ratios 0.649, 0.653, 0.669, 0.650 within 0.02.

Mutations (each must fail at least the named check): `eps-1e-2` (departure at 1e-2: K1), `b-scale` (b × 1.05 after the
fit: K3), `plat-half` (plateau over the last 0.5: K1 if the plateau moves by 2e-6, reported either way), `rth-side`
(r_th_a in place of r_th: K1).

## Results

| check | verdict | reading (`run_01.log`) |
|---|---|---|
| K1 | met | largest differences from the note's table: t_dep 4.9e-4, r_th 4.9e-7, γ₁ 4.0e-7, M 5.0e-7 |
| K2 | met | a = 0.20269, b = 0.8534, M₀ = 0.223086 |
| K3 | met | M − predicted within 4.7e-7 of the note's column; largest at 1e-9 … 1e-12 is 8.88e-4, so PRED not met is reproduced |
| K4 | met | dM = +2.0737e-3, predicted +1.1860e-3 |
| K5 | met | ratios 0.650, 0.653, 0.670, 0.650 |

Mutations: `eps-1e-2` fails all five; `b-scale` fails K3 only; `rth-side` fails K1, K2, K3; `plat-half` fails nothing:
the plateau over the last 0.5 of x⁺ differs from the one over the last 1.0 by at most 7.4e-7, inside K1's 2e-6. So the
plateau window is not tested by K1 at this bar, as the criteria allowed.

## Rerun of the runner's code

From a detached worktree at 86b6039, nice 10:
- `settled_mass_member.py job` and `member` at h = 0.005, δ = 1e-12 (`rerun_e12_h0.005/`, rc 0 and 0): the chain's
  `series.npz`, the pair's `locus.npz` and `member.json` rows and t_dep are bitwise equal to the runner's.
- `settled_mass_member.py analyze --raw=I267-mac` (`rerun_analyze.log`, rc 1, as stored: HST and PRED fail): equal to
  the stored `settled_mass_member_output.txt` (`stored_output_86b6039.txt`) except for the header's timestamp.
