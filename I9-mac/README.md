# I9-mac: pilots of #9's low-ω recheck on the Mac

Machine: the Mac (Apple M5), run by negative-mass-coordinator. Issue: https://github.com/nmoinvaz/negative-mass/issues/9

Code: negative-mass at 835262d (`lowscan.py` with its `nneg` argument), from `phase2/radial`, in a Python 3.14.5 venv
with requirements.txt's packages (numpy 2.5.4, scipy 1.18.1), BLAS threads at 1, nice 10. Each log starts and ends with
its UTC time.

- `repro_N3.log`: `lowscan.py 1 3 16` reproduces low_p.txt's N = 3 row, and `lowscan.py 1 3 80` reproduces
  low_recheck_p.txt's, both to the printed digits. 52 s and 90 s.
- `pilot_N42.6.log`: `lowscan.py 1 42.6 160 160`, the most compact canonical star at the densest grid, 7 min 52 s.
  Roots 4.03972e-05, 1.80151e-03, 4.70273e-03. low_p.txt's 16-point row lists 1.40273e-02 as the third root.
- A dense `scipy.linalg.eig(a, b)` of random matrices took 3.4 s at size 1000, 40 s at 2200 and 64 s at 2400, which
  sizes fd_check.py (n = 550) and complex_check.py (n = 600).
