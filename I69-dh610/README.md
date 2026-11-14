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
  records where the Lipschitz certificate needed a midpoint (none were needed), and a `summary` record. The log is the
  same run printed. Script commit 7058016 (the three largest runs) and 583f3f3 (the rest, which differ only in how
  `scan_resolved` counts uncertified intervals).
- `conv-<sigma R>-L<L>-N160.jsonl` and `.log`: s_min at v/v_c = 4, 7, 10 on the N = 160 grid of the larger box, for the
  convergence of the N = 128 columns (`--part=points`, commit 9d23de0).
- `pilot-L16-N128.log`: a two-point pilot of the largest scan, for time and memory before the queue started.
- `planted-truth.log`: the planted-truth checks of the final script (commit 59aeb22), run before the scans in
  `planted-truth-first-run.log` (commit f0f02a2) with the same results; the final one also prints the mean-free s_min.
- `controls-first-run.log`: the first run of every mutation control (commit 7058016). `conj` and `lipbig` did not fire;
  `controls-conj-lipbig-rerun.log` is their rerun after the fixes. `controls-half.log`, `controls-rest.log` and
  `controls-gridperturb.log` are the final control runs (commit 3c670b4).
- `table.log`: the merged tables and the table checks (`--part=table`), the source of the tables in the repository.

The tables in the repository's `notes/warp/zero_modes_output.txt` come from `python notes/warp/zero_modes.py
--part=table --raw=../negative-mass-raw/I69-dh610`.
