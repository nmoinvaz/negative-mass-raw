# I10-rpi5: phantom family continued beyond α₀ = 1.5, to where the solver stops

Machine: rpi5 (Raspberry Pi 5, 4 cores, aarch64, 8 GB), one process at a time, `nice -n 10`, `OMP_NUM_THREADS=1`.
Issue: https://github.com/nmoinvaz/negative-mass/issues/10

Code: `phase2/radial/` of nmoinvaz/negative-mass on branch `wip/i10-phantom-family` (base main 3981eca).
Python 3.14.10 from `negative-mass-venv314` (pinned requirements.txt). Run from `phase2/radial/`, with `$R` this folder.

| file | what |
|---|---|
| `fold_rerun_m.log`, `fold_rerun_p.log` | `fold_scan.py -1 0.5 40` and `fold_scan.py 1 0.33 43`, the stored ranges rerun |
| `follow.jsonl`, `follow.log`, `follow_ckpt.npz` | `phantom_follow.py --alpha-start 1.1 --alpha-stop 20 --out $R/follow.jsonl --ckpt-path $R/follow_ckpt.npz --snap-dir $R/snap --targets 1.10,1.15,1.17,1.20,1.25,1.30,1.40,1.50,1.60,1.80,2.00,2.50,3.00,3.50,3.90,4.00,4.015`, one JSON line per star, the last line is the stop record |
| `snap/star_a<alpha_c>.npz` | BVP mesh and solution at the target alpha_c, restart data for the scripts below |
| `modes.jsonl`, `modes.log` | `phantom_modes.py $R/snap $R/modes.jsonl --alphas 1.1,1.2,1.5,2.0,2.5,3.0,3.5,3.9,4.0,4.015` |
| `modes_dense.jsonl`, `modes_dense.log`, `modes_grids.log` | the same on 3.0 and 4.0 with `--nneg 48 --npos 64`, and `phantom_modes.py --grids modes.jsonl modes_dense.jsonl` |
| `converge.json`, `converge.log` | `phantom_converge.py $R/snap $R/converge.json --alphas 1.5,2.5,3.5,4.0,4.015` |
| `converge_mutate.log`, `converge_mutate_matching.json`, `converge_selftest.log` | `--mutate=matching` on 1.5 (must fail), `--selftest` |
| `fd.json`, `fd.log`, `fd_selftest.log` | `phantom_fd.py $R/snap $R/modes.jsonl $R/fd.json --alphas 2.0,3.0` (written with the first F1 criterion, rejudged by `--rejudge-json`), and `--selftest --snap $R/snap` |
| `stop.json`, `stop.log`, `stop_mutate_fit.*`, `stop_mutate_wkb.*` | `phantom_stop.py $R/follow.jsonl $R/follow_ckpt.npz $R/snap $R/stop.json`, with `--mutate=fit` and `--mutate=wkb` |
