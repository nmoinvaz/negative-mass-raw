# I216-mac-review: the coordinator's rerun of #216 (conical_global on the multishoot 5.0.0 release)

Machine: the coordinator's Mac (Apple M5, macOS), nice 10, shared and loaded. Issue:
https://github.com/nmoinvaz/negative-mass/issues/216

Code: negative-mass main at 62ebb47 (the merge of `wip/i216-conical-release` at ab7c76c), in a detached worktree
`~/Source/negative-mass-r216`. Runner's raw folder: `I216-mac` at 27a08c14.

## Criteria

Written after the run started and before its output was read. The run is the runner's own script, so these are a
reproduction check, not an independent one; what the two share is the whole crate and script.

- R1: `python3 notes/warp/conical_global.py` (the scripts build the crate) exits 0 with 17 of 17 checks and 13 of 13
  controls on target.
- R2: #216's comparator (`I216-mac/sys/compare_run.py`, which runs #190's `compare_outputs.py` unchanged) finds 0 gated
  differences against #190's baseline `I190-rpi5/run_11_base_global.log`.
- R3: the same comparator finds 0 gated differences against the runner's one-path run `I216-mac/run_20_single_global.log`.

## Runs

- `rerun_01_global.log`: R1.
- `cmp_rerun_01_vs_baseline.txt`, `cmp_rerun_01_vs_run_20.txt`: R2, R3.

## Results

| criterion | verdict | reading |
|---|---|---|
| R1 | met | 17 `[PASS]`, 0 `[FAIL]`, 13 `[FIRED]`, "controls: all fired on target only". The script's exit code was not captured (the run was started without an rc file); the log is complete |
| R2 | met | 126 lines compared, 0 gated differences; 4 of 95 error-sized numbers differ as printed, the same 4 as the runner's `cmp_run_20_vs_baseline.txt` |
| R3 | met | 126 lines, 0 gated differences, 0 error-sized numbers differ: the rerun equals the runner's one-path run as printed |

The comparator's own ability to fail is #216's `compare_selftest.py` (6 of 6 mutations fire); it was not rerun here.
