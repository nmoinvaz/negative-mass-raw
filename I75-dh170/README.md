# I75-dh170: logs and eigenvalue arrays of the Galerkin spectrum of T1 for the tanh profile, without a periodic box

Machine: dh170 (dh170-fedora, Fedora Linux, 8 cores, 31 GiB, shared with the desktop session).

Issue: https://github.com/nmoinvaz/negative-mass/issues/75

## Code and environment

Code: `~/Source/negative-mass-i75` on branch `wip/i75-tanh-spectrum` (from main 5cf960b), `notes/warp/tanh_spectrum.py`,
run from the repository root. `run.log` ran at commit a0040eb, `conv.log` and `controls.log` at a1d0578, which only adds
the `conv` part. The box runs are the unmodified `notes/warp/frank_loss.py` of the same checkout.

Python: `~/Source/negative-mass-venv314/bin/python`, Python 3.14.10, numpy 2.5.4, scipy 1.18.1, sympy 1.14.0 (the pinned
requirements.txt). Every run is at `nice -n 10` with `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1` and
`MKL_NUM_THREADS=1`, at most four processes at a time.

## Files

- `run.log`: the full default run, `python notes/warp/tanh_spectrum.py --raw=<this folder>`, which includes the symbolic,
  basis, v_c, planted and shifted-weight checks before the tanh part. About 36 min, four workers.
- `tanh_sigma<sigma R>_m<m>.npz`: all eigenvalues mu of S^-1 M (not times v_c) of one sigma R and one half-integer
  m = J_z in two discretisations, `muA` and `muB`, with `vc`. The eigenvalues of T1 are +-mu. Written by the run above.
- `conv.log`: `--part=conv`, the leading eigenvalues of m = 1/2 and 3/2 with one discretisation parameter changed.
- `controls.log`: `--controls`, the mutation controls.
- `first-run/run-before-cluster-fix.log`: the first full run, whose `real_identity` check failed in six sectors because
  its cluster tolerance paired two distinct, nearly imaginary eigenvalues. Kept as the record of that correction; its
  eigenvalues are those of `run.log` to 1e-9.
- `box-sigma4-L7.5-N96.log`, `box-sigma4-L10-N128.log`: `python notes/warp/frank_loss.py --part=krylov --sigmas=4
  --Ns=<N> --L=<L> --vs=0.5`, for the box error of #63's sigma R = 4 value. Their `identity` and `#58 Picard` checks
  compare with #58's box L = 5 and fail by design at another L.

The tables in the repository's `notes/warp/tanh_spectrum_output.txt` are `run.log`, `conv.log` and `controls.log`.
