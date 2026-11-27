# I226-mac-review: the coordinator's review of #226 (the constraint plateau is roundoff carried along the rays)

Machine: the coordinator's Mac (Apple M5, macOS, arm64), nice 10, at most 2 processes. Issue:
https://github.com/nmoinvaz/negative-mass/issues/226. Branch `wip/i226-constraint-plateau` at 576b859 (worktree
`negative-mass-r226`, detached), raw `I226-rpi5` at 6af8b9c (merge aef97cc).

Python: `~/Source/negative-mass/.venv/bin/python` (numpy, numba). On this Mac `np.longdouble` is float64 (`finfo.nmant` = 52),
so the runner's binary128 engine cannot be rerun here: a `dtype="f16"` job on macOS runs in float64 without saying so.

## Criteria, written before any run

**Rerun (R).** From the worktree's `notes/wormhole_evolution`:

- R1: `constraint_plateau.py analyze --raw=<raw>/I226-rpi5/runs` prints the same verdict lines as `I226-rpi5`'s analysis of
  record (`make_output.sh`'s output, `constraint_plateau_output.txt` on the branch). Pass: the same PASS/FAIL set and the same numbers.
- R2: two float64 row-engine jobs rerun here, `st_D6_k0` (static, h = 0.005, truncation-dominated) and `sm_D6_k2` (family S at
  p*ₕ − 1e-8, h = 0.00125, where the runner says roundoff is 2.1 times truncation). Pass for R2a: `st_D6_k0`'s max equals the
  stored one to 1e-8 relative. R2b is a measurement, not a pass/fail check: `sm_D6_k2`'s max on this Mac against the stored one. If the
  plateau is roundoff, a different libm may move it at the percent level, while the truncation-dominated job should not move.
- R3: `constraint_plateau.py controls` here. K3 (binary128 against float64) is vacuous on this machine and is reported as such.

**Independent check (`ind226.py`).** The coordinator's own double-null march (the half-domain scheme of
`notes/wormhole_evolution/threshold_check.py`, which shares no code with `dn.py`), with its own ray data (RK4 at h/16 of the
background and constraint ODEs), its own C₊₊ = r₊₊ + f₊ r₊ − (r/n) φ₊² by centered differences along a row, its own noise injection
(relative uniform noise in r of a·2⁻⁵², a node at a time, as it is computed) and its own derivation of the noise model:

a step d at node (i', j') of the scheme N = E + W − S + h²F is a step in the quadrant above it, so it puts ±d/h² into C₊₊ at
columns i' − 1 and i' of every later row; C₊₊ rⁿ⁻¹ is constant along x⁻ (∂₋C₊₊ = −(n − 1)(r₋/r) C₊₊, #40), so with Var d = (a ε r)²/3,

  rms ΔC₊₊(i, j) = √(2/3) · a ε / h² · r(i, j)^−(n−1) · (Σ_{j' < j} r(i, j')^{2n})^{1/2}.

Shared with the code under test: the Ellis family (the static member) and the slab's definition t ≤ T_c. Nothing else.

| check | what | pass |
|---|---|---|
| K0 | static, D = 6, h = 0.005, t ≤ 4: max \|C₊₊\| | below 1e-3 (the runner's static max is 7.8e-5) |
| K1 | the response to injected noise: the same evolution with and without noise (a = 256, one seed), ΔC = C(a) − C(0) node by node; rms ΔC over the band 0.5 ≤ l ≤ 2, 3.5 ≤ t ≤ 4, against the model's rms over the same nodes; D = 5 at h = 0.0025/√2, D = 6 at h = 0.00125 | ratio in [0.7, 1.4] in both |
| K2 | linearity: rms ΔC at a = 1024 over that at a = 256, same nodes, D = 6, h = 0.00125 | in [3.8, 4.2] |
| K3 | the plateau in an independent code: static, D = 6, float64, no injected noise, t ≤ 4, max \|C₊₊\| (rows i ≥ j + 1) at h = 0.005, 0.0025, 0.00125, 0.000625 | the first ratio in [3.364, 4.757]; the last below 3.364 |

Mutations (`--mutate=`), each with the check it must fail:

- `csign`: + (r/n) φ₊² in C₊₊. K0 must fail (C is then O(φ₊² r/n), of order 0.1 at the throat, not O(h²)).
- `model-exp`: the model's amplification r^−n and r^{2n+2} in place of r^−(n−1) and r^{2n}. K1 must fail.
- `noise-sq`: Var d taken as (a ε r)² in the model (no 1/3). K1 must fail: the model grows by √3, so the ratio falls by 1/√3 and
  leaves [0.7, 1.4] if the true ratio is below 1.21.

K3 is a prediction, not a check that needs a control: it can fail in either direction (an out-of-band first ratio, or no plateau at
the extension h).
