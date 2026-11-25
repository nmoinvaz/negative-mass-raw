# I174-mac: Lean build logs for #58's minimal split

Machine: macOS (the coordinator's Mac, arm64), Lean and Mathlib v4.34.1 (Mathlib's prebuilt cache).
Issue: https://github.com/nmoinvaz/negative-mass/issues/174. Source: `lean/NegativeMass/MinimalSplit.lean` of the
repository.

## Criteria (written before the first build)

| id | criterion |
|---|---|
| B | `lake build` exits 0 with no warning (`warningAsError = true` makes a `sorry` fail) |
| X | `lake env lean scripts/Axioms.lean` lists only `propext`, `Classical.choice` and `Quot.sound` for `split_lower`, `split_attained`, `minimal_split` and `minimal_split_R3` |
| M | `python3 scripts/mutate.py` exits 0: both baselines compile, and each of the nine controls is rejected, the five of #134 and these four |

| control | change | why it is false |
|---|---|---|
| `split-58` | `split_attained` with #58's first formula, μ₋ = max(0, (‖J‖ − μ)/2) | where −μ > ‖J‖, every split has μ₋ ≥ −μ, above that value |
| `lower-nohalf` | `split_lower` with (‖J‖ − μ) in place of (‖J‖ − μ)/2 | μ = 0, ‖J‖ = 1 has the split μ₋ = 1/2 |
| `sum-plus` | μ₋ + ‖J₋‖ = max(0, ‖J‖ + μ) | μ = 1, J = 0 forces μ₋ = 0 and J₋ = 0, so the sum is 0, not 1 |
| `least-58` | `minimal_split` with #58's first formula as the least element | as `split-58` |

## Results

Source at bb56a4e. All three criteria pass.

| file | what |
|---|---|
| `build_run1.log` | first build, exit 1: two warnings, which `warningAsError` makes errors (an unused `NormedSpace` instance in `split_lower`, and the deprecated `push_neg`). The statements did not change in the fix |
| `build_run2.log` | **B**: second build, exit 0, no warning |
| `axioms.txt` | **X**: all eight theorems, the four of #134 and the four of this issue, depend on `propext`, `Classical.choice` and `Quot.sound` only |
| `mutate.txt` | **M**: exit 0; both baselines compile and all nine controls fire (five rejected with "Type mismatch", three with a failed `rewrite`, one with `linarith`, as printed) |

The controls fail where the proof no longer fits the changed statement. That each changed statement is false is the
hand argument in the table above, not something the build shows.
