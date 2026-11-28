# I207-mac-review: the coordinator's review of #207 (multisolver's locate in the conical walkers)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/207. Under review: branch
`wip/i207-locate-walkers` at 2701c5d, raw `I207-mac` at b28e2e69. The feature `locate_lib` is off by default, so the merge
question is whether the default build is unchanged.

Criteria, written before the first run:
- R1 (default build, feature off): `conical_offgrid.py --grid=ctl --no-controls` passes 16 of 16, and #216's comparator
  (`I216-mac/sys/compare_run.py`, #190's `compare_outputs.py` unchanged) finds 0 gated differences against #190's baseline
  `I190-rpi5/run_06_base_offgrid_ctl.log` and against #216's one-path run.
- R2 (feature on): the same command reproduces the runner's `run_06_on_ctl` with 0 gated differences, and its dump's `loc`
  records equal the runner's.
- R3: `cargo build --release` with and without the feature exits 0.

This is a reproduction with the runner's code, not an independent check. The pair reading at the 10 changed records is not
checked here; it is the runner's recommended task 1.
