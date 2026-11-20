# I54-rpi5: recount of the non-radial windings with the corrected step rule (stage 1 of #54)

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, 4 cores, 8 GB, aarch64, shared with choptuik-large-d).
Issue: https://github.com/nmoinvaz/negative-mass/issues/54
Code: negative-mass checkout `~/Source/negative-mass-i54`, branch `wip/i54-pole-recount` from main 8518279,
scripts in `phase2/nonradial/`.

#5 found that the first step rule of `winding2.py` can lose 2π in one step, which shifts a symmetric box's count by ±2,
the size of #7's −2 at ω = 0.85, l = 3. Stage 1 recounts the boxes of RESULTS.md §5 with the current rule, each with a
planted zero. Stage 2 (locating a pole) runs only if ω = 0.85, l = 3 still counts −2.

Boxes: Re s ∈ [0.1, 2], |Im s| ≤ 2.5, planted zero 0.3 + 1.76i (and its conjugate), `winding2.py` at rtol 10⁻⁸.

| job | star | l |
|---|---|---|
| `chk_cache` | the four caches of #7 recomputed at stored points on this machine (`check_cache_i54.py`) | 2, 3 |
| `w085_l3` | phantom ω = 0.85 (#7's −2) | 3 |
| `w085_l2` | phantom ω = 0.85 | 2 |
| `w070_l3` | phantom ω = 0.70 | 3 |
| `w070_l2` | phantom ω = 0.70 | 2 |
| `w07603_l3` | phantom ω = 0.7603 | 3 |
| `c075_l2` | canonical ω = 0.75 (eps = +1) | 2 |

The seventh row of the §5 table, phantom ω = 0.7603, l = 2, was recounted by #5 (`../I5-rpi5/rep_l2.log`) and is not
rerun here.

Python 3.14.10, numpy 2.5.4, scipy 1.18.1, sympy 1.14.0 (`~/Source/negative-mass-venv314`), `nice -n 10`,
`OMP_NUM_THREADS=1`, at most two processes, one until the 15-minute load average is below 4.

Every run is a line of `jobs.txt` (`name|command`), run by `launch_I54.sh`, with its log in `<name>.log` and its exit
status in `done/<name>.rc`. `queue.log` has the start and end times.

| files | what |
|---|---|
| `cache/` | per-evaluation caches of `winding2.py`. The four ω = 0.70 and 0.85 files start as byte copies of #7's (`../I7-win2/winding2_cache_*.pkl`, sha256 in `cache_original.sha256`) and grow as the new rule asks for more evaluations. The ω = 0.7603 (l = 3) and ω = 0.75 caches start empty. |
| `cache_original.sha256` | sha256 of the four caches as copied |
| `jobs.txt`, `launch_I54.sh` | the queue and its launcher |
| `<job>.log`, `done/`, `queue.log` | output, exit status and times of each job |
| `memwatch.log` | cpu, memory and load of the jobs, one line per minute (reports only) |
