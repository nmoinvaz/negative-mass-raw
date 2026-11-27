# I255-dh610: what drifts the throat radius of family G at D = 5 (B = 0.04, 0.1, 0.2), and the expanding member A = 0.05 at X = 160

Machine: dh610-fedora (Fedora 45, 20 threads, shared with choptuik-large-d, load average 18 of 20 at the start). At most 4 processes, one thread each, `nice -n 10`.
Issue: https://github.com/nmoinvaz/negative-mass/issues/255 (it serves #42; follow-ups 3 and 5 of #225). Worktree `~/Source/negative-mass-i255`, branch
`wip/i255-g-drift`, base main 5ffd461. Python `~/Source/negative-mass-venv314/bin/python`. Status words as in AGENTS.md: every number below is *numerical
evidence* unless marked. No sentence here says a result is new.

This file is written in stages and says at each stage what had been run. Nothing in a stage is changed after a later stage has seen data.

## Stage 1: the prediction (written after the development runs dev_01 to dev_05 on #225's stored B = 0.1 data, before any run with B != 0.1 and before any new code)

What the development runs read (`dev/`, all from #225's `I225-dh610/runs/stall`, the pairs p*_h -/+ 1e-9, family G, B = 0.1):

- `dev_01`: the throat radius of the pair's mean, r_th(t) = 1.0105 (t = 4), 1.0502 (5), 1.0589 (6), 1.0714 (7), 1.0879 (8), 1.1078 (9), 1.1293 (10), 1.1522 (11), 1.1759 (12), 1.2000 (13)
  at D = 5, h = 0.00354; at D = 4 it falls from 1.0241 (t = 5) to 1.0029 (t = 13). The two sides of the pair differ (the unstable mode) by at most 7e-4 up to t = 12.
- `dev_02`: on the locus the ghost energy density is the equilibrium one of a static throat of that radius, rho_g = -n(n-1)/(2 r_th^2), to 4e-4 at t = 13 (ratio 1.0131 at t = 6
  falling to 1.0004). The normal field's energy density on the locus is 1e-7 or less from t = 11 (it has left). The charge flux per unit t through the locus is constant at D = 4
  (1.381 to 1.397 over t = 6 to 13) and rises from 2.46 to 3.40 at D = 5, as sqrt(n(n-1)) N_th r_th^(n-1) with N_th = dtau/dt on the locus.
- `dev_03`: the Misner-Sharp mass at fixed areal radius is constant in t from t = 12 at D = 4 and drifts at D = 5 (at R = 2 by +0.016 per unit t on the + side and +0.019 on the - side between t = 8 and 14).
- `dev_04`: the radial velocity of the throat, dr_th/dtau (local linear fit over +-0.5 in tau), fitted over t in [6.5, 12] by
  `rdot(tau) = rdot_inf + c exp(-kappa (tau - tau_0))`: D = 5, h = 0.00177: rdot_inf = +0.02602 +- 4e-5, kappa = 0.481 +- 0.004, rms residual 8.8e-5 over 107 points;
  D = 4, h = 0.005: rdot_inf = +0.0013 +- 2e-5, kappa = 0.244. So at D = 5 the throat radius is not relaxing to a static value: its velocity approaches a constant (H = d ln r_th/dtau
  is constant at 0.021 from t = 10 to 13). The pulse integrals on the initial ray, I_2 = integral of r^n (dg/ds)^2 ds = 10.081 (D = 4), 38.730 (D = 5), with g the unit Gaussian
  (centre 3, width 0.5, r from the static wormhole), and I_1 = integral of r^n dg/ds ds = -3.760, -19.945.

**Power counting (the structural claim).** The normal field is a test field at first order in B: it enters the metric and the ghost field only through its stress, which is B^2.
The ghost pulse A enters at first order, and the unstable mode's amplitude is alpha A + beta B^2 + O(A^2, A B^2, B^4), so the tuned amplitude is A* = p*_h(B) = kappa B^2 + O(B^4).
The cross term of the ghost pulse's energy with the background vanishes (the integral of dg/ds is zero), so the ghost pulse's energy is -A*^2 I_2, fourth order in B, and the net
energy the pulses leave is E_net(B) = (B^2 - A*^2) I_2. Every effect of the tuned data on the throat is therefore second order in B, with the same time dependence:

    r_th(tau; B) - 1 = B^2 g(tau) + O(B^4),   p*_h(B) = kappa B^2 + O(B^4),   rdot_th(tau; B) = B^2 g'(tau) + O(B^4).

The alternative, first order in B, gives exponent 1 in all three. At B = 0.1 the throat radius is already 0.2 above 1 at t = 13, so the O(B^4) terms are of relative size
about R(B) = r_th - 1 itself (3 % at B = 0.04, 20 % at 0.1, order 1 at 0.2). That is why the gates below are exponents, with bands that exclude exponent 1 and allow the
nonlinearity, and why B = 0.2 is a reported measurement of the nonlinearity, not a pass/fail test of the scaling.

**Predicted values** (from B = 0.1 and the scaling; D = 5; the reference values are #225's pairs at the same h, the exponent is the claim):

| quantity | B = 0.04 | B = 0.1 | B = 0.2 (linear extrapolation, reported only) |
|---|---|---|---|
| p*_h / p*_h(0.1) | 0.16 | 1 | 4 |
| r_th(tau) - 1 relative to B = 0.1 | 0.16 | 1 | 4 |
| rdot_inf (velocity the throat radius approaches) | 0.0042 | 0.0260 | 0.104 |
| transient rate kappa | 0.48, B independent | 0.481 | 0.48 |
| E_net = (B^2 - A*^2) I_2 | 0.0619 | 0.383 | 1.48 |

**What is not predicted.** The mechanism: why the velocity of the throat radius approaches a constant at D = 5 and (to 0.0013, a factor 20 smaller) at D = 4. The candidates read in
`dev_02` and `dev_03` are (i) a flux of the normal field through the locus (ruled out as the driver after t = 8: its energy density there is 1e-7), (ii) the unstable mode (ruled
out: the odd part of the pair is at most 7e-4 up to t = 12), (iii) a resolution effect (ruled out for B = 0.1: three h agree to second order), (iv) the constraint plateau of #226
(roundoff of 1e-11 against a drift of 0.02), (v) the observer (the minimum of r on a slice; planted moving throats of #225 recover r_th = 1). Not ruled out: a generalized zero mode
of the static family (a throat radius with a constant velocity, a Jordan block of the linearization), a slowly decaying tail of the ghost field in the region 2 < r < 8 (the mass at
R = 6 to 8 on the + side changes by 0.01 to 0.02 between t = 8 and 14 at D = 5), and a drift of the lapse relative to the far region. The note will say which of these the B scan
and the h scan bear on, and call the cause "not established" unless a check can fail on it.
