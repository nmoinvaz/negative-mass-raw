# I314-mac-review: the coordinator's review of #314 (re-reading #305's route with independent estimators)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/314. Under review: branch
`wip/i314-speed-estimators` at 3856bda, raw `I314-mac` at efa73020 (the Y amendment d59c7d6c, before Y was read).

| run | result |
|---|---|
| `rerun_analyze.log` | `settled_mass_speed.py analyze` exit 1 (9 gating checks fail, as stored); equal to `settled_mass_speed_output.txt` apart from the header |

The independent reading is the coordinator's own: `I305-mac-review/ind305.py` reads ṙ_th by a quadratic fit in τ over ±0.5 (an
estimator #314 does not use) and found M − P4 = +9.00e-5, +2.13e-4, +1.98e-4 at X1–X3, the same miss. With #314's three estimators and
three member weightings, that is eight readings that leave the miss beyond the bar.
