# I302-mac-review: the coordinator's review of #302 (the decaying partner, the horizon basis, the log at S)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/302. Under review: branch `wip/i302-horizon-basis`
(code d1f849b, note 1909d6d), raw `I302-mac` at 9aaa036f.

This review reproduces; it has no independent script. The log at S changes Paper IV, so an independent rederivation is filed as
its own issue.

| run | result |
|---|---|
| `rerun_derive.log` | `horizon_basis.py derive` exit 0, 3 of 3; equal to `I302-mac/runs/derive.log` apart from timings |
| `rerun_check.log` | `horizon_basis.py check` exit 0, 9 of 9; equal to `I302-mac/runs/check.log` apart from timings |

Reading of the argument (note Sec. 3): Y = δr − gδφ is gauge invariant; C² fields at S give ∂_s²Y_N(0) = −F_Π(0)Y_N(0) (L1 on eight
evolved smooth classes, worst Richardson ratio 1.000345); Y = c₂VR has Y_N″(0) = 0 and Y_N(0) ≠ 0 with F_Π(0) ≠ 0. The coordinator
agrees that no gauge makes the mode smooth at S.
