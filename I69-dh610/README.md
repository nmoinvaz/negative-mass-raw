# I69-dh610: logs and jsonl of #69's search for real zero modes of the Alcubierre Witten operator, up to 10 v_c

Machine: dh610 (dh610-fedora, Fedora Linux, Intel Core i7-12700, 20 threads, 62 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/69

## Code and environment

Code: `~/Source/negative-mass-i69` on branch `wip/i69-zero-modes` (from main 5918f9e), `notes/warp/zero_modes.py`, run
from the repository root. The commit that wrote each file is named in the file's first line.

Python: `~/Source/negative-mass-venv314/bin/python`, Python 3.14.10, numpy 2.5.4, scipy 1.18.1, sympy 1.14.0 (the pinned
requirements.txt). Every run is one process at `nice -n 10` with `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`,
`MKL_NUM_THREADS=1`, at most four at a time.

## Files

- `scan-<sigma R>-L<L>-N<N>.jsonl` and `.log`: one s_min(v) scan per (sigma R, box L, grid N), eight in all. The jsonl
  has a `start` record, a `sample` record per v/v_c (s_min, Lanczos applications, seconds, peak memory), `bisect`
  records where the Lipschitz certificate needed a midpoint, and a `summary` record. The log is the same run printed.
- `planted-truth.log`, `controls.log`: the planted-truth checks and the mutation controls.

The tables in the repository's `notes/warp/zero_modes_output.txt` come from `python notes/warp/zero_modes.py
--part=table --raw=../negative-mass-raw/I69-dh610`.
