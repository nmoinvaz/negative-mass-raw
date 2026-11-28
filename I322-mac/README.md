# I322-mac: criteria, development runs and runs of record for #322, the remainder Y_rem of smooth c = −1 data at fixed ρ

Machine: the coordinator's Mac (Apple M5), runner `negative-mass-mac-i322`, worktree `~/Source/negative-mass-i322` on `wip/i322-remainder`, at most 2 processes, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/322. Script: `notes/black_universe/remainder.py` (imports `horizon_sector.py`, `horizon_basis.py`, `full_slice.py`, `static_c1.py`, `linear.py` read-only).
Python: `~/Source/negative-mass/.venv/bin/python`. Written before the runs of record (`runs/`); development runs are in `dev/` (probes `p0`–`p8`, `d1`–`d7`, `devcheck.py`, logs `logs/`, mutation development logs `mut/`).

## Question

#302 left open whether `Y_rem = Y − (c₁R + c₂VR + c₂′UR)` of smooth data decays, so that the late growth at fixed ρ is `c₂e^{κv}R`. The issue's acceptance: Y_rem's rate at three fixed ρ with its error at two h;
a planted Y_rem with a known rate recovered through the same fit; say whether the late growth is `c₂e^{κv}R`.

## What the development found, which shapes the checks

Class G, A0, A1R, A1L (three h, V up to 24): Y_rem does not decay. At fixed ρ it grows as V = e^{κv}, with a coefficient that is a function of ρ times c₂ and the same for every class,
`Y_rem/(c₂VR) → Q(ρ)`, Q = −0.57 (Π = 0.5), −0.73 (Π = 1), +0.30 (Π = −0.1). #262 has the second solution Y_b = Y_ref J of the equation at W = κ, with
`J(ρ) = ∫₀^ρ 2K r e^{−2H}/(A R²) dr`, and the solution that is outgoing at infinity `Y_∞ = Y_ref (1 − J/I₀)`, I₀ = J(∞) = 1.0149036099284089. The prediction `Q = −J(ρ)/I₀` (−0.57371, −0.73271, +0.29606) matches the
measured Q to 4e-4 or better in the four classes. What is left after subtracting `c₂V R Q(ρ)` is V-independent at fixed ρ and has the profile of the solution f₀ of the W = 0 equation that vanishes at the horizon (the free
coefficient y₁₁ of a VU term of D6): y₁ = bR/f₀(ρ) equal at the three Π to 2 % or better. So the late growth at fixed ρ is `c₂e^{κv}Y_∞(ρ)`, not `c₂e^{κv}R`; the checks below test that, with the closed form of #262 as the
prediction (shared with the solver: A(ρ), R(ρ), the map ρ(Π), κ; not shared: the characteristic evolution).

## Method

1. **Streaming march** (`march_stream`): `hs._cellK` of #248, two columns in memory, over V ∈ [−0.1, 24], U ∈ [−2, 0.06], restricted to the past set Π ≥ −0.30 (the interior ends at Π = −0.37). Kept: the five nodes
   U = −2h … 2h of every column (the future horizon), 8-node windows around each fixed-Π curve, and 5 columns at S (or at the horizon crossings of the planted modes). Same cells as `hs.march_K` (the horizon line agrees to 3e-15,
   the windows exactly; dev `p1`).
2. **Y_rem at fixed ρ.** Y/R at the nodes (Y = δr − (ρR/√2)δφ), the residual `Y/R − (c₁ + c₂V + c₂′U)` with (c₁, c₂, c₂′) read at S by #302's 4th-order slice functionals, 8-point Lagrange interpolation in U to `U* = −Π/V`.
   Fixed ρ is fixed Π: Π = −0.1 (ρ = −0.3114, inside the horizon, from V = 1.8), 0.5 (ρ = 0.6819), 1 (ρ = 1.0000). Π = 2 is also stored. R(ρ) is constant on a curve, so `Y_rem = R × series`.
3. **Richardson** `(4 w(h/2) − w(h))/3` pointwise on common nodes, for the pairs (h = 0.00125, 0.000625) and (0.000625, 0.0003125); R2 is the second.
4. **Fits** over V ∈ [8, 24] (v from 3.3 to 5.0): (i) `ln|Y_rem| = α ln V + const` (rate = ακ); (ii) `Y_rem/R = aV + b + d/V`.
5. **Prediction** from #262: `Q = −J/I₀` by DOP853 (H, J) from |ρ| = 1e-4 with the series start; `f₀` by DOP853 from |ρ| = 1e-4 at W = 0.
6. **Independent readout** on H⁺ (no fixed-Π window): `∂_U Y(V, 0) = ∂_U δr + (G₀V/√2)δφ` from five nodes across U = 0, fitted as `AV² + BV + C`; the prediction is A = c₂G₀/I₀.

Error bars are not enclosures: the rate error is the larger of the change between the two Richardson pairs, the change between the two finest raw h, and the standard error of the log fit.
"Relative" is divided by the stated scale.

## Checks and bars (declared before the runs of record)

Data: the eight classes of #302 (A0, A1R, A1L, L, G, Lm, Rb, Gb), class R of #248 (a pulse on the ray U = −2 only; c₂ = 0), and four random data (seed 3221: corner constants and pulses on both rays, amplitudes ≤ 1e-3, #302's `_rand_spec`),
each at h = 0.00125, 0.000625, 0.0003125 on V ∈ [−0.1, 24], U ∈ [−2, 0.06]; the exact modes of #302 at the same three h on V ∈ [0.05, 24] (growing) and U ∈ [−2, −0.05] (decaying).

| id | what | bar |
|---|---|---|
| K1a | I₀ = ∫ 2K r e^{−2H}/(A R²) dr by DOP853 against #262's 1.0149036099284089 | 1e-8 relative |
| K1b | Y_ref = R e^{κx} and Y_b = Y_ref J solve #262's equation at W = κ, ρ = −0.8 … 5 | residual / size of terms ≤ 1e-9 |
| K1c | Y_∞/Y_ref = 1 − J/I₀ ≤ 1e-6 at ρ = 20 (outgoing) | 1e-6 |
| P1 | planted zero: the exact growing mode, Y_rem/R over \|c₂\|V on V ∈ [8, 24], Π = −0.1, 0.5, 1 | falls by 3.5 to 4.5 per halving of h; ≤ 1e-5 after Richardson (0.000625, 0.0003125) |
| P2 | planted rates: (a) growing mode with 99 % of c₂ subtracted (α = 1, a/c₂ = 0.01); (b) decaying mode with c₂′UR left in (α = −1, amplitude \|c₂′\|Π); same series, same fits, Richardson of the two finest h | α ± 1e-3; a/c₂ ± 0.5 % of 0.01; amplitude ± 1e-3 |
| P3 | planted array-level remainders ε Π V^α added at the nodes of the exact growing mode, α = 2, 1, 0, −1 (2e-4 at V = 16, Π = 1) | α ± 1e-3; amplitude ± 1e-3 |
| D1 | data with \|c₂\| ≥ 1e-4: `Y_rem/R = aV + b + d/V` on [8, 24]; a/c₂ against Q = −J/I₀ at Π = −0.1, 0.5, 1 (Richardson of the two finest h) | \|a/c₂ − Q\| ≤ 2e-3; change from the pair (0.00125, 0.000625) ≤ 1e-3; window exponent α of \|Y_rem\| in [0.85, 1.02] with one sign |
| D2 | the same data: y₁ = bR/f₀(ρ), f₀ the W = 0 solution that vanishes at the horizon | spread over mean of the three Π ≤ 0.10 |
| D3 | the transverse slope ∂_U Y(V, 0) on H⁺ (no fixed-Π window): `AV² + BV + C` on [8, 24]; A against c₂G₀/I₀ | \|A/(c₂G₀/I₀) − 1\| ≤ 1e-2 |
| D4 | data with \|c₂\| < 1e-4 (R, Rb: the truncation seed only): window exponent of \|Y_rem\| at the three Π; y₁ spread | α ≤ 0.3 (growth at κ is 1); spread ≤ 0.10 |

The rate of Y_rem is ακ, with α the window exponent (`ln|Y_rem|` against `ln V`, V = e^{κv}). Its error is the largest of: the change between the two Richardson pairs, the change between the two finest raw h, the standard error of the log fit.
**What the checks say in the issue's terms:** D1 says the late growth at fixed ρ is `c₂e^{κv}Y_∞(ρ)` and not `c₂e^{κv}R(ρ)`. They also say Y_rem does not decay: it carries the growth at rate κ with the coefficient Q(ρ)c₂, and a V-independent part. If D1 failed on all
data with a/c₂ near 0, Y_rem would decay or grow slower than κ, #302's reading.

## Planted cases (known answers, run before the real data)

| case | known answer | where |
|---|---|---|
| exact growing mode of #302 (β = 2e-3) | Y_rem = 0 | P1 |
| growing mode, 99 % of c₂ subtracted | Y_rem/R = 0.01 c₂ V, α = 1 | P2a |
| decaying mode, c₂′UR not subtracted | Y_rem/R = c₂′U* = −c₂′Π/V, α = −1 | P2b |
| ε Π V^α added at the nodes | α, εΠ | P3 |
| #262's quadrature | I₀ = 1.0149036099284089, ODE residual | K1 |

## Mutations (each has a `--mutate=` and a declared fired set; the effects below were computed in development runs `dev/mut_*`, before this file was committed)

`derive` has K1a to K1c; `check` has P1 to P3 and D1 to D4. A mutation changes a reading, a fit or the prediction, never an evolution (the cache of evolved readouts is shared).

| mutation | what it breaks | declared to fire | effect in development |
|---|---|---|---|
| `k_W` | W = 1.01κ in #262's equation | K1b | residual of Y_ref 6.5e-3 (bar 1e-9) |
| `k_J` | e^{+2H} for e^{−2H} in J | K1a, K1b, K1c | I₀ = 2e217; Y_b residual 0.5; 1 − J(20)/I₀ = 1 |
| `no_c2` | the c₂VR term not subtracted | P1, P2, P3, D1 | P1: Y_rem/(c₂V) = 1.000 (bar 1e-5); P2a: a/c₂ = 1.000 (0.01); D1: \|a/c₂ − Q\| = 1.0 |
| `c2_sign` | c₂ → −c₂ | P1, P2, P3, D1 | P1: 2.000; D1: 2.0 |
| `no_c1` | the c₁R term not subtracted | D2 | y₁ of A0: −1.8e-2, 2.0e-3, 3.6e-4 (spread 3.8); the exact modes have c₁ ≈ 1e-9 and do not fire |
| `c2p_V` | c₂′V subtracted for c₂′U | D1, D4 | D1: A0 5.0e-2, A1R 2.9e-2, A1L 8.7e-2; D4: Rb α = 0.94 … 1.02 against ≤ 0.3 |
| `pi_off` | the curve Π·1.05 read for Π | P2, P3, D1 | P2b amplitude ratio 1.050; P3 1.050; D1 1.8e-2 (bar 2e-3) |
| `interp_near` | nearest node instead of the 8-point Lagrange interpolation | P1, P2, D1, D2 | P1 Richardson 1.9e-4 (bar 1e-5); D1 pair change 2.3e-2; D2 spread 0.3 … 2 |
| `fit_semilog` | fit ln\|y\| against V, not ln V | P2, P3, D1 | P2a α = 0.066 for 1; P3 α = 0.132 for 2; D1 α = 0.065 (bar 0.85 …) |
| `J_sign` | Q_pred = +J/I₀ | D1 | \|a/c₂ − Q\| = 1.5 |
| `plant_alpha` | the planted α shifted by 0.1 | P3 | P3 reads α + 0.1 (bar 1e-3) |
| `hp_sign` | the sign of the d_U δr stencil | D3 | A/(c₂G₀/I₀) = 4.03 (A0), −0.49 (G) against 1 ± 1e-2 (two coarser h) |
| `g_nophi` | the (G₀V/√2)δφ term of d_U Y dropped | D3 | −1.51 (A0), 0.75 (G) |
| `f0_W` | f₀ solved at W = 0.3 instead of 0 | D2, D4 | y₁ spread 0.50 … 0.55 (bar 0.10) |

Blind spots, kept: `no_c1` does not fire P1 to P3 or D1 (the exact modes carry c₁ ≈ 1e-9, and a constant does not change a/c₂); `interp_near` is invisible to P3 (the planted amplitude is 1e-4 of the signal's leading term, the error 1e-3 relative);
`c2_sign` and `no_c2` are not separated by any check. The D1 window exponent does not fire `pi_off` (a different Π changes the amplitude, not the exponent).

## What differs from the first plan (changes after development)

- The three fixed-ρ curves are fixed by Π (−0.1, 0.5, 1): the interior curve starts at V = 1.8 and the interior corner Π = −0.3 caps the rectangle (the interior ends at Π = −0.37).
- The planted cases: the issue asks for a planted Y_rem with a known rate. The solver cannot be given a planted Y_b mode (no exact full field solution known), so the planted rates come from the exact growing and decaying modes of #302 with a known part left in the remainder (P2),
  and from known functions added at the nodes (P3); the first plan (a planted ε V^α in the evolved data) is P3, now on the exact mode so that the background is the truncation floor.
- The static-piece check D2, the horizon readout D3 and the c₂ = 0 check D4 were added after the first four classes had been read; the bars of D2 (spread 0.10), D3 (1e-2) and D4 (α ≤ 0.3) were set from the dev values (≤ 4.1e-2, 1.3e-3, 0.095).
- Class R of #248 was added for D4; the random data (seed 3221) were evolved in development only to read their size.

## Runs of record

Code of record: `notes/black_universe/remainder.py` at commit 50e1d53 of `wip/i322-remainder`. Declared here, executed after this file is committed: `run_main.sh OUT` runs `warm` in two processes (A0, A1R, A1L, L, G, R, exact_g | Lm, Rb, Gb, rand0 … rand3, exact_d;
three h each, about 280 s per item), then `derive`, `check`, `table` and `dump OUT/series` in one process; `run_mut.sh OUT PREFIX` runs the 14 mutations on the cache (`k_W`, `k_J` with `derive`, the other twelve with `check`); `remainder.py mutations OUT PREFIX` compares
the fired sets with the declared ones. `cache/` (the readouts of the evolved rectangles, 0.9 GB) stays on the Mac and is not committed; `warm` regenerates it in about 35 min, and `runs/series/series_<name>.npz` holds the Richardson series of every datum.
Stop condition: a single run not finished in 2 h of wall time is stopped and reported (the pilot of the hardest case, A0 at h = 0.0003125, took 213 s in development). Nothing stops on memory. Logs are numbered, never overwritten.

## Results of record (added after the runs; the criteria above are unchanged)

`runs/r1` (code 50e1d53): `warmA` 1837 s and `warmB` 2045 s (two processes, exit 0), `derive` 3 of 3 (8 s), `check` 7 of 7 (9 s, 1.2 GB peak), `table`, `dump` (exit 0); `mut/` 14 mutation runs (all exit 1 as a fired check does), `mutations.log`: 14 of 14 fired sets equal the declared ones.
The first report of `mutations` ran while the last two mutation runs were unfinished (g_nophi, f0_W then showed as different or missing); it was rerun after `mut_ALLDONE`.
Result: Y_rem grows at κ with a/c₂ = −J/I₀ to 4.3e-4 for the 11 data with c₂ ≠ 0; the independent horizon readout gives A/(c₂G₀/I₀) = 0.99918 … 1.00006; c₂ = 0 data (R, Rb) do not grow (α = −0.07 … +0.10). Note: `notes/black_universe/remainder.md`.
Counts: the 11 data with c₂ ≠ 0 are A0, A1R, A1L, L, G, Lm, Gb and rand0 … rand3 (an earlier comment on the issue said 12).
`runs/r1/series/series_<name>.npz` are the Richardson series; the cache of readouts (0.9 GB) stays on the Mac.
