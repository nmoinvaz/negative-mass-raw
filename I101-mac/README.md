# I101-mac: coordinator's review of #101 (reruns and independent check of the review of #72)

Machine: the coordinator's MacBook Air M5. Issue: https://github.com/nmoinvaz/negative-mass/issues/101

- `rerun_{ricci,typeI,points}.txt`: stdout of `python notes/warp/review_he_surface_{ricci,typeI,points}.py` from
  `wip/i101-review-surface` at 5a2db26 (Python 3.14.7, nice 10), each exit 0 and identical to the committed outputs.
  `.time`: `/usr/bin/time -l`.
- `mut_cof-perturb.txt`: `review_he_surface_typeI.py --mutate=cof-perturb`, exit 1, `cert_T1` fails.
- `ind101.py`: an independent check. The coordinate Ricci tensor of the comoving Alcubierre metric with an explicit
  quadratic profile (not a jet of the shift), exact at rational points with Pythagorean (c, s): flatness at v = 0 and
  the table identity R00 + Rxx + 2 Rrr = 0; the review's cofactor certificate as polynomials in lam at 6 points;
  he_surface.md's factorization of D on T1 at 4 points; 4 points built on T1, T2 with T3 != 0 (2 with F < 0) that are
  Type I (D = 0, double root, rank 1); a T3 = 0 point that is not. Criteria in its docstring, fixed before run 1.
  - `ind101_run1.txt`: FAIL, C3 at 2 of 4 points: the point draw gave c = 0, so v = 0, outside the claim's domain.
  - `ind101_run2.txt`: after excluding c = 0 from the draw (criteria unchanged), PASS. At both F < 0 points the
    stated -F < r a < -c^2 F and v F s^2 >= 2|c| fail, as the review's gap 1 says.
  - `ind101_mut_{cof,Rsign,T2off}.txt`: each exits 1 on its required criteria.
