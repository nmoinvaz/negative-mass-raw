# I283-mac-review: the coordinator's review of #283 (G's settled mass on a second route to its member, blind)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/283. Under review: branch
`wip/i283-second-route` at 79fbafa, raw `I283-mac` at 4df36dd4 (criteria 77a21028).

## ind283.py: an independent reading of the six route points

Written by the coordinator; imports nothing from the repository. From `I283-mac/runs/R_*/h0.005` (W: xc 3, w 1; C: xc 4,
w 0.5) and #266's `I266-mac/runs/{O,G_B*}/h0.005` it computes, with its own code:
- t_dep: the pair's odd part (r_b − r_a)/2 over the mean, first crossing of 1e-3 at t ≥ 6, linear in t;
- the member at departure: r_th and s_m of the two stored slices that bracket t_dep, linear in t, γ₁ = s/√(1 − s²);
- the plateau: mean of M over the cells with x⁺ ≥ max x⁺ − 1;
- ṙ_th: a quadratic least-squares fit of the pair's mean r against the pair's mean τ over |τ − τ_dep| ≤ 0.5, its derivative
  at τ_dep (the runner's: local linear fits over ± 0.5 on a thinned grid, interpolated in t; a different estimator);
- P2 with (M₀, a, b) fitted here over #266's four B (as ind267 did), P3 with (0.2300, 0.2724, 0.7835) from #267's output.

Shared: the runs, the stored slices and #225's fit (s_m). Not shared: everything listed above.

Criteria, written before the first run:
- K1: t_dep within 1e-3, γ₁ within 1e-5, r_th within 1e-6, M within 2e-6 of the note's table for W1–W3, C1–C3.
- K2: M − P2 within 3e-6 of the note's six values, and all six beyond 6e-5 in size.
- K3: this ṙ_th within 3e-6 of the note's; M − P3 within 5e-6 of the note's six values. Reported either way: whether W3 still
  exceeds 6e-5 with this estimator.
- K4 (SEP): r_th minus family B's at the same γ₁ (linear interpolation over B = 0, 0.025, 0.05, 0.1, 0.125) has the note's sign
  at all six and its size within 15 %.

Mutations: `eps-1e-2` (departure at 1e-2: K1), `no-speed` (c = 0 in P3: K3), `swap` (W and C exchanged: K1).

## Results

| check | verdict | reading (`run_01.log`) |
|---|---|---|
| K1 | met | t_dep 4.7e-4, γ₁ 5.0e-7, r_th 4.7e-7, M 4.7e-7 from the note's table |
| K2 | met | M − P2 within 4.6e-7 of the note's; smallest \|M − P2\| 6.47e-5 (C1), so P2 fails at all six |
| K3 | met | this ṙ_th (quadratic fit in τ) within 3.9e-7 of the note's; M − P3 within 2.3e-7. W3: M − P3 = +7.090e-5, beyond 6e-5 with this estimator too |
| K4 | met | SEP sign and size within 15 % at 6 of 6 |

Mutations: `eps-1e-2` and `swap` fail all four; `no-speed` fails K3 only.

## Rerun of the runner's code

From a detached worktree at 79fbafa: the W3 point at h = 0.005 (`job` and `member`, rc 0, 0) gives a chain, locus, member rows
and t_dep bitwise equal to the runner's. `analyze` (exit 1, as declared) equals the branch's `settled_mass_route_output.txt`
apart from the timing (`stored_output_79fbafa.txt`). The raw folder's `analyze_record.log` is an earlier analysis that printed
ṙ_th to two digits; the numbers are the same.
