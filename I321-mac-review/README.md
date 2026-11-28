# I321-mac-review: the coordinator's review of #321 (the log of the c = −1 growing mode at S, rederived)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/321. Under review: branch `wip/i321-log-at-S`
(code b1ef08e, note e5b3d83), raw `I321-mac` at 694efe0b.

#321 is itself the independent rederivation of #302's result, so this review reruns it and reads the argument; it has no
independent script. `log_at_S.py` imports only sys, time, os, re, mpmath and sympy (checked by grep).

| run | result |
|---|---|
| `rerun_derive.txt` | `log_at_S.py derive`, exit 0, 4 of 4 |
| `rerun_series.txt` | `log_at_S.py series`, exit 0, 8 of 8 |
| `rerun_check.txt` | `log_at_S.py check`, exit 0, 6 of 6 |

Every check line equals `log_at_S_output.txt` of the branch; only the timings differ.
