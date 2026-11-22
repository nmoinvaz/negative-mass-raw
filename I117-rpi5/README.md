# I117-rpi5: logs and caches of #117's counts of four boxes beyond Re s = 2 and |Im s| = 10 with winding2.py and zerilli_zeros.py at --guard=all

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/117

## Code and environment

Code: worktree `~/Source/negative-mass-i117` on branch `wip/i117-boxes` at a05cd0b, `phase2/nonradial/winding2.py` and
`zerilli_zeros.py`, unmodified, run from `phase2/nonradial`. The collector `collect_i117.py` is written after the runs.

Python: `~/Source/negative-mass-venv314/bin/python`. Every run is `nice -n 10` with `OMP_NUM_THREADS=1` and
`OPENBLAS_NUM_THREADS=1` (both scripts are single-threaded), detached with `setsid nohup`. At most two processes at a
time, and a second one starts only while the 15-minute load average is below 4 (checked before every start by
`launch_I117.sh`). Memory is reported, never a stop condition. Nothing of choptuik-large-d is touched.

## What is counted

The phantom campaign star (ε = −1, ω = 0.7603), each box once with `winding2.py` (zeros minus poles of D) and once with
`zerilli_zeros.py` (zeros of Z(r_m; s), D's poles), same arguments, both with `--guard=all`:

| box | l | Re s | Im s | arguments after `-1 0.7603 <l>` |
|---|---|---|---|---|
| b25_l2 | 2 | [2, 5] | abs(Im s) ≤ 10 | `2.0 5.0 10.0 --plant=2.5,1.0` |
| b25_l3 | 3 | [2, 5] | abs(Im s) ≤ 10 | `2.0 5.0 10.0 --plant=2.5,1.0` |
| h2_l3 | 3 | [0.1, 2] | [6, 10] | `0.1 2.0 10.0 --y0=6.0 --plant=0.3,6.2` |
| h3_l2 | 2 | [0.1, 2] | [10, 20] | `0.1 2.0 20.0 --y0=10.0 --plant=0.3,10.5` |

The boxes and planted zeros are fixed by the task and are not moved after a count is seen. Each planted zero lies inside its
box (a pair in the symmetric boxes, one zero in the upper boxes).

## Pass criteria, written before the runs

- Every job exits 0.
- `winding2.py`: the winding is within 0.05 of an integer; the PLANTED line says PASS (the count with the factor exceeds the
  count without by the number of planted zeros inside, 2 in a symmetric box and 1 in an upper box, within 0.05, with a max
  phase step below 0.45 rad). The max phase step, min abs(D) and evaluations are reported.
- `zerilli_zeros.py`: the last line is "all checks passed" (`count`, `plant`, `holo`, `column`).
- Zeros of D = winding of D + count of Z. A nonzero count is reported with its box.
- A failed check is a result. No threshold is loosened and no box or plant moves.
- Stop condition of the pilot `w_h3_l2`: it runs alone and is stopped at 8 h (`LIMIT=28800`, exit 124), and then reported
  before anything else starts.

## Files

- `jobs.txt`: one line `job|script|arguments` per job. Job `<job>` runs as `python -u <script> <arguments>
  --cachedir=<this folder>/cache`, with stdout and stderr in `<job>.log` and its exit status in `done/<job>.rc`.
  `w_*` jobs are `winding2.py`, `z_*` jobs `zerilli_zeros.py`.
- `pilot.txt` (the pilot `w_h3_l2`), and the list files of the later stages.
- `launch_I117.sh LIST`: the gated queue worker (`LIMIT=SECONDS` is a timeout). It tests the gate before it takes a job,
  so a waiting worker holds no job. `queue.log` has the start, wait and end lines, `qpos.<list>` the next line of a list.
- `memwatch.sh` and `memwatch.log`: once a minute the load, the free memory and the cpu and rss of the task's processes. It
  reports only and stops nothing.
- `cache/`: the per-evaluation caches of the eight jobs (pickles, written in place while a job runs). No cache was copied in:
  the eight boxes are new.
