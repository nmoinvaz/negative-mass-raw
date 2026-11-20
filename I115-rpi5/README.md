# I115-rpi5: complex-s zero counts of the phantom star at l = 4, 5, 6 (argument principle, `winding2.py`)

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, 4 cores, 8 GB, aarch64, shared with choptuik-large-d).
Issue: https://github.com/nmoinvaz/negative-mass/issues/115
Code: negative-mass checkout `~/Source/negative-mass-i115`, branch `wip/i115-complex-l456` from main 2344ed6,
scripts in `phase2/nonradial/`.

Star: phantom, ω = 0.7603, M = −0.014580, l = 4, 5, 6. `winding2.py` at rtol 1e-8, Python 3.14.10 from
`~/Source/negative-mass-venv314`, `nice -n 10`, `OMP_NUM_THREADS=1`, at most two processes.

Each winding counts zeros minus poles of D. #121 will count the poles, so no box here is covered by a pole exclusion yet.

Boxes, for each l (the pilot is `s1_l6`; planted zero in the same cached evaluations):

| job | box | planted |
|---|---|---|
| `rep_l<L>` | stored box, Re s ∈ [0.1, 2], \|Im s\| ≤ 2.5 | 0.3 + 1.76i and its conjugate |
| `s1_l<L>` | strip, Re s ∈ [0.03, 0.1], \|Im s\| ≤ 2.5 | 0.04 + 0.25i and its conjugate |
| `n1_l<L>` | below the threshold 1 − ω, Re s ∈ [10⁻⁴, 0.1], \|Im s\| ≤ 0.23 | 0.0005 + 0.12i and its conjugate |

`control` is `control_winding2.py` (Mini BS I, around the QNM and displaced) on this machine. Every run is a line of
`jobs.txt` (`name|command`), run by `launch_I115.sh` with its log in `<name>.log` and its exit status in
`done/<name>.rc`. `queue.log` has the start and end times and `memwatch.log` the load and rss, reported only.
`cache/` holds the per-evaluation caches (restart-safe).

`python collect_i115.py <this folder>` in `phase2/nonradial/` builds the table of RESULTS.md section 3a.
