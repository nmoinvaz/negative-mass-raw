# I163-mac: the coordinator's review of #163's second row of Table I and the large-γ₁ limit

Machine: macOS (the coordinator's Mac, arm64), Python 3.14.7, sympy 1.14.0, mpmath 1.3.0, numpy 2.5.4, at nice 10 with
at most 2 processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/163. Reviewed branch `wip/i163-ellis-second-row` at 4871503
and raw `I163-rpi5` at 4b46218.

## Rerun of the runner's script

`python3 ellis_efold.py` from `notes/` of a detached worktree of 4871503, full and unmutated (`rerun/`). Expected, as
#163 reports: exit 1, with P-C2 and LE5 failing.

## Independent check `ind163.py` (criteria written before its first run)

ind163 imports nothing from the repository and nothing from `ellis_efold.py` or `I151-mac/ind151.py`. It solves two
equations by its own Numerov integration with Richardson extrapolation over h and h/2, with x(ρ̄) and z(ρ̂) by RK4.
- [GGS09a]'s DiffEq, −(a∂_x)²χ + (β̄² + W̄)χ = 0, a(x) = e^{2γ₁(arctan x − arctan γ₁)}, W̄ = a²·[bracket of Eq. (32)].
  It is solved in ρ̄ (dρ̄ = dx/a) centred on the throat, ρ̄ = 0 at x = γ₁, so the domain always contains it.
- The limit equation `Eq:DiffEqLargeGamma`, retyped by the coordinator from the TeX:
  −(e^{2(1 − 1/z)}∂_z)²χ + e^{4(1 − 1/z)}[2z⁻² − 10z⁻³ + 3z⁻⁴]χ = −β̂²χ. It is solved in ρ̂ (dρ̂ = e^{−2(1 − 1/z)}dz,
  ρ̂ = 0 at z = 1).

Shared with #163: the equations as printed in the TeX; the bracket of Eq. (32) (typed in `I151-mac/ind151.py` from the
same TeX); T = 1/(√(1 + γ₁²)β̄); and #163's printed values, used for comparison only.

| id | criterion | kind |
|---|---|---|
| U0 | the zero mode (2/π)(z − 1)/z² e^{1 − 1/z} solves the typed limit equation at β̂ = 0 | symbolic |
| U1 | planted: the same Numerov, matching and Richardson code on −ℓ(ℓ + 1)sech²ρ, ℓ ∈ {1.3, 2.4}, gives β = ℓ to rel 1e-9 | 15 digits |
| U2 | the limit equation (L = 45/1.7, h = 0.002 and 0.001): \|1/β̂ − 0.588351371\| < 1e-8 (#163's value); 1/β̂ rounds to 0.588; \|1/β̂ − 0.590\| > 0.001 | 15 digits |
| U3 | DiffEq at γ₁ ∈ {2.0, 2.5, 5, 10}, with L = 45/β̄ for β̄ estimated from Table I, h = L/20000 and L/40000: T against #163's printed 0.617891948, 0.608155106, 0.593640535, 0.589696827, rel < 1e-8; each T rounds to Table I's 0.618, 0.608, 0.594, 0.590. At γ₁ = 2.0, β = λβ̄ (λ = e^{2γ₁ arctan γ₁}) is within rel 1e-8 of #163's converged 60.662007295832 and differs from #151's as-run 60.662389104967 by more than 1e-6 | 15 digits |

Mutations, each must exit 1 with its target failing:

| mutation | change | target |
|---|---|---|
| `zm` | the zero mode with (z − 2) | U0 |
| `num` | Numerov's 5h²/12 → 6h²/12 | U1 |
| `lim` | −10z⁻³ → −9z⁻³ in the limit potential | U2 |
| `brk` | 3(x − γ₁)² → 2(x − γ₁)² in the bracket | U3 |

## Results

| file | what |
|---|---|
| `rerun/ellis_efold_full.*` | the rerun at 4871503: stdout, `/usr/bin/time -l`, exit code |
| `ind163_run1.py`, `.txt`, `.time` | run 1: every criterion passes (`ind163.py` is the same version) |
| `ind163_mut_*.txt` | its 4 mutations |

**Rerun** (exit 1, 2 min 20 s, 139 MB peak). 98 of 100 checks pass, and P-C2 and LE5 fail as #163 reports. The other
differences from rpi5's output are in the last digits (LAPACK, platform), as in `I151-mac`. P-C2's errors are 8.8e-8 and
3.4e6 at γ₁ = 5 and 10, against 9.3e-8 and 4.8e6 on rpi5. That spread is consistent with #163's diagnosis that the arc
amplifies rounding error.

**ind163 run 1** (exit 0, 11 s, 75 MB peak):

| criterion | run 1 |
|---|---|
| U0 | the zero mode solves the typed limit equation at β̂ = 0 |
| U1 | ℓ = 1.3, 2.4: rel 4.2e-13, 4.6e-13 |
| U2 | β̂ = 1.6996646041035, 1/β̂ = 0.588351370962 (3.8e-11 from #163's 0.588351371); rounds to 0.588; \|1/β̂ − 0.590\| = 0.001649 |
| U3 | T = 0.6178919483, 0.6081551057, 0.5936405352, 0.5896968273 at γ₁ = 2, 2.5, 5, 10, rel to #163 ≤ 5.5e-10, h-spreads ≤ 4e-14; all round to Table I. At γ₁ = 2, β = 60.6620072958: 2.3e-13 from #163's converged value and 6.3e-6 from #151's as-run value |

Re-solve: U2 and U3, by the coordinator's own Numerov on the paper's DiffEq, centred on the throat, and on the limit
equation as typed from the TeX. They confirm three things:
- the second row;
- the limit 1/β̂ = 0.588351, so the table's 0.590 is not the limit;
- #151's truncation at γ₁ = 2.

| mutation | exit | failed | target met |
|---|---|---|---|
| `zm` | 1 | U0 | yes |
| `num` | 1 | U1, U2, U3 (the same Numerov) | yes |
| `lim` | 1 | U0, U2 (U0 uses the same typed potential) | yes |
| `brk` | 1 | U3 | yes |
