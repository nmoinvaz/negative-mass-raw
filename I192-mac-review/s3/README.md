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

## Results

| criterion | verdict | reading |
|---|---|---|
| S1 | met | both builds rc 0 (`b1_default.rc`, `b2_libtable.rc`); `tree_default.txt` names multishoot v5.0.0 and no git source |
| S2 | met | `s3_steps.py` exit 0, every case equal (464, 389 steps); the six files of `steps_out/` are byte-equal to `I192-mac/s3_steps_out/` (`steps_cmp.txt`) |
| S3 | met except R1 | 21 passed, 0 failed, 2 skipped (R1, TS), 1315 s. Every verdict equals `run_44`'s except R1, which is SKIPPED here: it compares the old-pin and new-pin binaries (`target/bins/old_default`, `new_default`), which this tree does not have. R1's content is the runner's RP2 (3532 records, 0 differ), not rerun here |
