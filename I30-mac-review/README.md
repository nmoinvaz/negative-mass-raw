# I30-mac-review: the coordinator's review of #30 (independent winding check ind30)

The runner's raw folder for #30 is `I30-mac` (it ran on this Mac). Machine: macOS (the coordinator's Mac), Python 3.14.7
(`/Users/nathan/Source/negative-mass/.venv`). Issue: https://github.com/nmoinvaz/negative-mass/issues/30. Under review:
branch `wip/i30-ghost-counts` at ad00567, raw `I30-mac` at b338967. Written 2026-11-26 before the first run of
`ind30.py`.

## ind30.py: the windings recomputed from the stored evaluations

The counts are choptuik-large-d's `modecount_test.py`, whose own phase sum (`modecount_wind.count`) gives the windings
in its logs. ind30 recomputes them from the stored evaluations (`I30-mac/counts/*_evals.jsonl`: re, im, arg of det M)
with its own boundary ordering and phase unwrapping. It shares the evaluations, which are the object under test; it
shares no code with the counting. The records hold Im ≥ 0; the lower half is their reflection with the argument negated
(det M(s̄) is the conjugate of det M(s)). The boxes are those of the logs: B0 = (aLL, aL) × (−y₁, y₁), U0 = (aLL, aL) ×
(y₁, y₂), full = (aL, 6.70) × (−y₂, y₂), with the edge values read from the evaluations' most frequent coordinates.

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| W1 | For D = 10, 12, 20.04, plain and planted, and each box B0, U0, full: ind30's winding of arg det M equals the log's "winding of det M" |
| W2 | Every consecutive phase step on every box boundary is at most π/2 in absolute value (the counts' alias rule) |
| W3 | At each D, the planted run's B0 winding is the plain one + 2, and U0 and full are unchanged |

## Mutations (`--mutate=NAME`; each must make ind30 exit non-zero with exactly these criteria failing)

| mutation | change | targets |
|---|---|---|
| `orient` | the boundaries are traversed clockwise | W1, W3 |
| `alias-claim` | W2's bar is 0.1 in place of π/2 | W2 |

## Runs (filled in as they are done)
