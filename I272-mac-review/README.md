# I272-mac-review: the coordinator's review of #272 (the Ellis wormhole's linear spectrum beyond its unstable mode)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/272. Under review: branch
`wip/i272-ellis-spectrum` at 6373c3c (driver adc4c02), raw `I272-mac` at 938fccbf (criteria ddea1184).

## ind272.py: an independent time-domain check of the linear response

Written by the coordinator; imports nothing from the repository. It solves Y_tt = D Y, D Y = Y'' − p Y' + q Y with p and q as
the note states them (p = 2r₀''/r₀' + n r₀'/r₀, q = n r₀'²/r₀² + r₀''/r₀, r₀'' = (n−1) r₀^{1−2n}, r₀(0) = 1), on a staggered grid
with Y even at the throat and Dirichlet at l = 75, by velocity Verlet (the note: RK4 and a one-sided outer row). The growing
mode is removed each step with the discrete operator's right and left eigenvectors. Data: Y = 0, Y_t = exp(−((l − 3)/0.5)²/2),
P = ∫ Y₁ Y_t(0)/(r₀'² r₀ⁿ) dl. Series are Richardson combinations of h = 0.01 and 0.005.

Shared with the runner's code: the formula of D (the note's), the data and the definition of P. Not shared: the integrator,
the outer boundary, the eigen-solve, the throat extrapolation code and the rate estimate. The formula of D is anchored by K1
against #195's W², which is independent of #272.

Criteria, written before the first run:
- K1: the discrete operator's positive eigenvalue, Richardson over h = 0.01, 0.005, equals #195's W² (1.397052433715 at
  D = 4, 2.984958930278 at D = 5; `notes/wormhole_largeD/w2_output.txt`) within 1e-5 relative.
- K2 (D = 4): P within 1e-3 relative of 0.4577; Y(t, 0) within 1 % of the note's 0.4323, 0.4403, 0.4451, 0.4494, 0.4530,
  0.4547 at t = 8, 10, 12, 15, 20, 25; the local rate −d ln v/dt within 5 % of 0.283, 0.245, 0.216, 0.182, 0.144, 0.119.
- K3 (D = 4, the power law): rate × t at t = 15, 20, 25 within 10 % of 2.74, 2.89, 2.97, and rising by less than 15 % from
  t = 15 to 25 (an exponential's rises by 67 %).
- K4 (D = 5): P within 1e-3 relative of 0.1036; Y(t, 0) within 2 % of 0.4088, 0.4687, 0.5258, 0.6077, 0.7367, 0.8592 at the
  same t; v/P within 5 % of 0.282 at t = 10 and 0.242 at t = 20.

Mutations, each must fail at least the named checks: `wrong-n` (n + 1 in p's second term: K1), `no-proj` (the growing mode
kept: K2, K4), `width` (width 1.0 in place of 0.5: K2's Y values).

## Results

| check | verdict | reading (`run_01.log`) |
|---|---|---|
| K1 | met | W² relative 5.7e-9 (D = 4), 2.5e-8 (D = 5) from #195's |
| K2 | met | P 0.45773; Y(t, 0) within 9.8e-5; local rate within 3.5e-3 (0.2825, 0.2448, 0.2155, 0.1824, 0.1443, 0.1186) |
| K3 | met | rate × t = 2.735, 2.886, 2.965 at t = 15, 20, 25; rise 8.4 % (an exponential: 67 %) |
| K4 | met | P 0.10362; Y(t, 0) within 1.0e-4; v/P = 0.2815, 0.2421 at t = 10, 20 |

Mutations: `wrong-n` fails K1 to K4; `no-proj` fails K2, K3, K4; `width` fails K2 and K4.

## Rerun of the runner's driver

From a detached worktree at 6373c3c, with `w2_crate` built there (`rerun2_build.log`): `ellis_spectrum.py run`, exit 1 as stored,
`rerun2_full.log`. Apart from timings it equals `I272-mac/runs/run_01_full.log` except the header's commit (adc4c02 there, the
branch head 6373c3c here; the driver file is the same). The first attempt (`rerun_full.log`) stopped at the planted and spectrum
stages because the crate was not built in the review tree; it is kept.
