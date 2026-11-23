# Slips and changes after exploratory runs (kept, none changed a pass criterion)

1. ends, first run: E2.6 crashed (`series(..., n=-1)` is not allowed in sympy), after E2.1-E2.5 had passed. Fixed by expanding s^4 V-hat; no criterion changed.
2. ends, second run: E2.6 FAILED: the coefficient of 1/x in V-hat(x) is exactly 0 (checked symbolically in l and numerically with mpmath at r = 1e-8 for l = 2, 3, 5),
   not -l(l+1)/4 as printed in DG09 (61). DG's printed value equals the contribution of the first two terms of the r-series only (12/r^4 and 2(l^2+l+3)/r^3);
   the O(r^-2) term l(l+1)/r^2 adds +l(l+1)/(4x). RESULTS does not use that coefficient (it uses r^4 V-hat = 12 + 2(l^2+l+3) r + O(r^2), which agrees with DG's first line of (61)).
   Handling: E2.6 moved out of the ends script into `review_lemma_a3_dg61.py` so the other checks keep a clean baseline; its comparison with the printed coefficients is kept
   unchanged and reported as DIFFERS (a printed-source difference, not a failure of RESULTS); E2.6b (the true coefficients, exact) and E2.6c (numeric) were added after seeing the data.
3. l6, first run: L6.6 FAILED for l = 17..30 ("positive roots of den: 1", the root being r_s to 12 digits). Cause: my helper `k_of` used Python float division, k = c(c+2)/6 became a float,
   and sympy `cancel` with floats left the (cr-6) factor uncancelled for l >= 17 (for l < 17 the floats happened to be exact). Fixed with `sp.Rational(1, 6) * c * (c + 2)`; all later
   runs exact. The first run's output is in `step3_l6_run1_FLOAT_K.log`. No criterion changed.
