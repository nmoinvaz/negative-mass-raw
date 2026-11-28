# I296-mac-review: the coordinator's review of #296 (the settled-mass relation read at departure ε = 1e-2)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/296. Under review: branch `wip/i296-departure-eps`
(note d46fa83, script 97a41f4), raw `I296-mac` at 8d99ab12 (criteria 21b10fba).

## ind296.py: the two tests at ε = 1e-2 with the coordinator's reader

Written by the coordinator; imports nothing from the repository (ind283's reader with ε = 1e-2: t_dep, the member, the plateau,
ṙ_th by a quadratic fit in τ over ±0.5). M₀ = 0.223086. Fits by least squares of y = M/r_th − M₀ = a γ₁ + b γ₁² + c ṙ_th.

Criteria, written before the first run:
- K1 (T1): the fit over the nine points (#266's four B, #267's δ = 1e-7, 1e-9 … 1e-12) predicts #283's six with a largest
  |M − P| within 1e-5 of the note's 1.29e-4, beyond 6e-5.
- K2 (T2): the fit over the fifteen predicts #295's three with a largest |M − P| within 1e-5 of the note's 9.3e-5, beyond 6e-5.
- K3: at ε = 1e-3 the same code gives #283's P3 residual at W3 (+7.11e-5) and #295's largest (2.15e-6) to 2e-6.

Mutations: `eps-1e-3` (both tests at ε = 1e-3: K1 and K2's sizes change), `no-speed` (c = 0 in the fits: K1, K2).

## Results

| check | verdict | reading (`run_01.log`) |
|---|---|---|
| K1 | met | at ε = 1e-2 the nine-point fit (0.2403, 0.0517, 0.4779) predicts #283's six with residuals +4.8e-5, −1.28e-4, −2.0e-5, +4.7e-5, −1.29e-4, −3.2e-5: largest 1.293e-4 |
| K2 | met | the fifteen-point fit (0.2405, 0.0343, 0.5105) predicts #295's three with +6.7e-5, −9.30e-5, +1.2e-5: largest 9.30e-5 |
| K3 | met | at ε = 1e-3: #283's W3 +7.108e-5, #295's largest 2.14e-6 |

Mutations: `eps-1e-3` fails K1 and K2; `no-speed` fails all three. The note's subtraction of the second-order mode part (its
declared variant) was not rechecked here.

## Rerun of the runner's analysis

From a detached worktree at the branch head: `settled_mass_eps.py analyze --part=record` (exit 1, as stored) equals
`settled_mass_eps_output.txt` apart from the header.
