# I291-mac-review: the coordinator's review of #291 (the power-law tail of G's throat speed at D = 4, B = 0.02)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/291. Under review: branch `wip/i291-d4-tail` at
532f56b, raw `I291-mac` at 7e3f8e35 (criteria c324b74a).

## ind291.py: the ensemble slope from the raw pairs

Written by the coordinator; imports nothing from the repository. For h = 0.01 and 0.005 it reads the eight members' pairs
(`runs/G_B0.02/h<h>/e12/member/locus.npz` and `runs_k1` … `runs_k7`), forms each member's pair mean r(τ) on the steps both runs
have, interpolates the eight onto one grid in t and averages them. The speed v = dr/dτ is the slope of a quadratic least-squares
fit over |τ − τ₀| ≤ 0.25 (the runner's: its own local estimator). Then:
- the log-log slope p of |v| against τ over [15, 18.2];
- rate × t = −t d ln|v|/dt at t = 10, 13, 16.

Shared with the runner's code: the pairs. Not shared: the averaging, the speed estimator, the fits.

Criteria, written before the first run:
- K1: p within 0.05 of the note's −2.413 (h = 0.01) and −2.304 (h = 0.005).
- K2: rate × t within 0.05 of the note's 2.11, 2.23, 2.32 at t = 10, 13, 16 (both h), and its spread over the mean below 23.1 %
  (S2's bar).
- K3: the verdict of S1 at each h with this estimator (|p + 2.9| ≤ 0.58), reported either way.

Mutations: `one-member` (member 0 alone: K1 at h = 0.005, if the note's ±0.1 to ±0.23 single-pair scatter is right),
`t-not-tau` (ln t in place of ln τ: reported), `wide` (the fit over ±1.0 in τ: reported).

## Results

| check | verdict | reading (`run_01.log`) |
|---|---|---|
| K1 | met | slope −2.4065 (h = 0.01), −2.3050 (h = 0.005); worst 0.007 from the note's |
| K2 | met | rate × t = 2.129, 2.226, 2.340 (h = 0.01) and 2.131, 2.227, 2.315 (h = 0.005); worst 0.021; spread 9.5 % (bar 23.1 %) |
| K3 | reported | S1 with this estimator: met at h = 0.01 (−2.406), not met at h = 0.005 (−2.305), as the note |

Mutations: `one-member` fails K1 and K2 (−2.357, −2.083: the note's single pairs −2.36, −2.07); `t-not-tau` and `wide` move the
slopes by at most 0.013 and fail nothing (reported, as declared).

## Rerun of the runner's analysis

From a detached worktree at 532f56b: `throat_tail.py analyze` (exit 1, as stored: S1 at h = 0.005) equals
`throat_tail_output.txt` apart from the header.
