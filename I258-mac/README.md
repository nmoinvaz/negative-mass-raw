# I258-mac: design note and development probes for a compactly supported datum on a full slice of the c = −1 black universe (#258)

Machine: the coordinator's Mac (Apple M5, macOS, shared), runner `negative-mass-mac-i258`.
Issue: https://github.com/nmoinvaz/negative-mass/issues/258
Code of record (stage 2): `notes/black_universe/full_slice.py` on branch `wip/i258-full-slice` of nmoinvaz/negative-mass.

- `design.md`: the stage-1 design for review. Criteria, bars and mutations are declared there before any run of record.
- `probe/`: development probes (scratch scripts, not code of record), `probe/logs/` their logs (`pN.log`, `pN.err`, `pN.rc`).
  `probe/run_logs.sh` reruns the logged set, one process at a time at nice 10; `p23` was run by hand with its log.
  The probes import `horizon_sector.py` and `linear.py` read-only from `~/Source/negative-mass-i258/notes/black_universe`
  (main at 3b3358c) and run with `~/Source/negative-mass/.venv/bin/python`.
- Stage 2 will add `runs/` with the logs of record.
