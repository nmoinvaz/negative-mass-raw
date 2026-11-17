# I5-rpi5: polar-mode counts the l = 2, 3 scans did not cover (strip 0 < Re s < 0.1, |Im s| > 2.5, real-γ refinement)

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, 4 cores, 8 GB, aarch64, shared with choptuik-large-d).
Issue: https://github.com/nmoinvaz/negative-mass/issues/5
Code: negative-mass checkout `~/Source/negative-mass-i5`, branch `wip/i5-polar-count`, scripts in `phase2/nonradial/`.

Star: phantom, ω = 0.7603, M = −0.014580, l = 2 and 3. Python 3.14.10, numpy 2.5.4, scipy 1.18.1, sympy 1.14.0
(`~/Source/negative-mass-venv314`), `nice -n 10`, `OMP_NUM_THREADS=1`, at most two processes.

Every run is a line of `jobs.txt` (`name|command`), run by `launch_I5.sh` (two workers, `nice -n 10`), with its log in
`<name>.log` and its exit status in `done/<name>.rc`. `queue.log` has the start and end times.

| files | what |
|---|---|
| `rep_l2`, `plant_chain.sh` | the stored box Re s ∈ [0.1, 2], \|Im s\| ≤ 2.5 (l = 2) and the four mutations of the planted-zero check |
| `s1_l2`, `s1_l3`, `s2_l2` | strips Re s ∈ [0.03, 0.1] (l = 2, 3) and [0.01, 0.03] (l = 2), \|Im s\| ≤ 2.5 |
| `s3_l2`, `s3_l3` | strip Re s ∈ [0.03, 0.1], Im s ∈ [2.5, 6] |
| `h1_l2`, `h1_l3`, `h2_l2` | Re s ∈ [0.1, 2], Im s ∈ [2.5, 6] (l = 2, 3) and [6, 10] (l = 2) |
| `n1_*`, `n3_*` | below the threshold 1 − ω, right of the axis and across it |
| `t1_r40`, `t1_r80`, `t2_r40`, `t2_r80` | the thresholds 1 − ω and 1 + ω at the two outer radii |
| `cs_*`, `polish_mini.log` | Mini BS I controls (`control_winding2.py`, `polish_zero.py --mini`) |
| `ref_l2`, `ref_l3`, `refine_*.csv`, `ref_chain.sh` | real-γ refinement, the planted pair and the three mutations |
| `as_*`, `cs_axis`, `axis_scan_*.csv` | axis scan, its control fails and it is not used as evidence |
| `cache/` | per-evaluation caches of `winding2.py` and `control_winding2.py` (restart-safe) |
| `repro_*`, `plant_winding2_*`, `plant2_*`, `control_winding2_strip.log`, `control2_default.log` | earlier runs under the first step rule, kept for transparency |
| `issue_post_pending_2146.md` | the note relayed to #5 while gh was unavailable |

`python collect_i5.py <this folder>` in `phase2/nonradial/` builds the tables of RESULTS.md section 5.1.
