# I10-rpi5: phantom family continued beyond α₀ = 1.5, to where the solver stops

Machine: rpi5 (Raspberry Pi 5, 4 cores, aarch64, 8 GB), one process at a time, `nice -n 10`, `OMP_NUM_THREADS=1`.
Issue: https://github.com/nmoinvaz/negative-mass/issues/10

Code: `phase2/radial/` of nmoinvaz/negative-mass on branch `wip/i10-phantom-family` (base main 3981eca).
Python 3.14.10 from `negative-mass-venv314` (pinned requirements.txt).

| file | what |
|---|---|
| `fold_rerun_m.log` | `fold_scan.py -1 0.5 40` (phantom), the stored range rerun |
| `fold_rerun_p.log` | `fold_scan.py 1 0.33 43` (canonical), the stored `fold_p.txt` rerun |
| `follow.jsonl`, `follow.log`, `follow_ckpt.npz` | `phantom_follow.py --alpha-start 1.1 --alpha-stop 20 --targets ...`, one JSON line per star, the last line is the stop record |
| `snap/star_a<alpha_c>.npz` | the BVP mesh and solution of the stars at the target alpha_c, restart data for the later scripts |
| `modes.jsonl`, `modes.log` | `phantom_modes.py snap modes.jsonl --alphas ...`, sigma^2 roots of those stars |
