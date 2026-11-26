# Singular and series attempts (development, 2026-11-25), outputs were read from the terminal

- `gen_prol.py 2 2 al0 d prol_22.sing` then `Singular -q prol_22.sing` under `timeout 300`, nice 10: the (2,2) prolongation of E in (n; alpha, beta, gamma, delta)
  jets with t*detN*alpha - 1 added, `std` over Z/32003: no output after 300 s (killed by timeout). The first version of the script wrote `n2^2/2`, which Singular
  parses as a failed power; the corrected version has integer coefficients only (8D = h2^3 - 4 h2 P^2 - h2 Q2^2 + h2 Y2^2 + h2 Z2^2 - 2P(Y2^2 - Z2^2) + 2 Q2 Y2 Z2).
- `gen_prol_c.py 2 2` and `3 3` (case c, u = A R + B, jets A_k, B_k, R_k, iota, t*W3*R1 - 1, W3 = A1 B2 - A2 B1), `timeout 120` each: no output.
- `probe8.py`: sympy `factor_list` of E: constant 1, one factor of 376 terms, multiplicity 1, 68 s. Ranks of the X2 = 0 form: 6, 10, 9 at v = 0, 1/3, 1; 11 for symbolic v.
- `probe9.py`: exact d_F, d_G of the exponential pair: v = 0: 12, 22 (r = 59); v = 1/3: 22, 36 (r = 93).
- `probe6.py`: numerical rank of the 12 x-coefficients of case (c) on sample curves: 4 to 9 for exp/poly/trig pairs, 12 for a generic pair.
- `dev1.log`: the numerical formal-series runs.
