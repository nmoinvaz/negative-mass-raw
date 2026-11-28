# Stage 3 review (#192): the crate on multishoot 5.0.0, J's table from multishoot behind `lib_table`

Coordinator's Mac, nice 10. Branch `wip/i192-taylor-tables` at a7a57dd, raw `I192-mac` at 2cad9bb5. A detached worktree
`~/Source/negative-mass-r192` at a7a57dd; builds with `cargo build --release -j 2` (default) and `--features lib_table`.

Criteria, written before the first run:
- S1: both builds succeed; `cargo tree` of the default build has no git source.
- S2: `s3_steps.py` (the runner's) on the two new binaries passes, and each of its six step-list files is byte-equal (`cmp`) to
  the runner's `I192-mac/s3_steps_out/`. The byte comparison is the coordinator's and shares nothing with `s3_steps.py`'s
  comparison; both share the binaries' `jtable` output.
- S3: `taylor_polar.py --raw=...` (the default mode, 23 checks) on the `lib_table` build: 22 passed, 0 failed, 1 skipped (TS),
  and every CHECK line's verdict equals `run_44`'s.
