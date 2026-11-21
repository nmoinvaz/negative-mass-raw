# I124-rpi5: logs and caches of #124's counts of the zeros of Z(r_m; s), the poles of D, in #115's nine boxes (phantom star, l = 4, 5, 6)

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/124

## Code and environment

Code: worktree `~/Source/negative-mass-i124` on branch `wip/i124-zeros-l456` at b4c3a0a, `phase2/nonradial/zerilli_zeros.py`
and `collect_i121.py`, unmodified, run from `phase2/nonradial`.

Python: `~/Source/negative-mass-venv314/bin/python`, Python 3.14.10, numpy 2.5.4, scipy 1.18.1. Every run is
`nice -n 10` with `OMP_NUM_THREADS=1` and `OPENBLAS_NUM_THREADS=1` (the script is single-threaded), detached with
`setsid nohup`. At most two processes at a time, and a second one starts only while the 15-minute load average is below 4.
Memory is reported, never a stop condition.

## What is counted

`zerilli_zeros.py` counts the zeros of the decaying Zerilli solution Z(r_m; s) in a box, the poles of D's Zerilli column.
The phantom star has ω = 0.7603, M_ext = −0.014580. The nine boxes are #115's, planted zero as in #115:

| job | box | planted |
|---|---|---|
| `rep_l<L>` | stored box, Re s ∈ [0.1, 2], \|Im s\| ≤ 2.5 | 0.3 + 1.76i and its conjugate |
| `s1_l<L>` | strip, Re s ∈ [0.03, 0.1], \|Im s\| ≤ 2.5 | 0.04 + 0.25i and its conjugate |
| `n1_l<L>` | Re s ∈ [10⁻⁴, 0.1], \|Im s\| ≤ 0.23 | 0.0005 + 0.12i and its conjugate |

for L = 4, 5, 6. The four controls are on #121's stored box (l = 2): `flat` must end "all checks passed"; `mut_reverse`,
`mut_nonorm` and `mut_lshift` must each end "FAILED:", on `plant`, `holo` and `column` respectively.

## Files

- `jobs.txt`: the 13 lines `job|arguments` of `python collect_i121.py --jobs --only=3a`. Job `<job>` runs as
  `python -u zerilli_zeros.py <arguments> --cachedir=<this folder>/cache`, with stdout and stderr in `<job>.log`.
- `controls.txt`, `pilot.txt` (`n1_l6`, the largest R_z, about 1.6×10⁶) and `boxes.txt` (the other eight): the order of the
  jobs, one name per line. Controls first, then the pilot alone with a 1 h stop, then the eight boxes.
- `launch_I124.sh LISTFILE`: queue worker. Exit status of each job in `done/<job>.rc`, start and end times in `queue.log`.
  `start_second.sh LISTFILE` starts a second worker once the 15-minute load is below 4. `memwatch.sh` writes `memwatch.log`
  (load, available memory, cpu and rss of this task's processes; reports only).
- `cache/`: the per-evaluation caches (`zerilli_zeros_cache_<tag>.pkl`), restart-safe.
- `<job>.log`: the script's output. The collector reads these.

`python collect_i121.py <this folder> --only=3a > i124_zeros_output.txt` in `phase2/nonradial` builds the table of RESULTS.md
§5.3. Its `--mutate=box` and `--mutate=control` logs (`collect_mutate_box.log`, `collect_mutate_control.log`) are here too.
