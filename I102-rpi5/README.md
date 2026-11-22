# I102-rpi5: logs of the exact Type III set on D = 0 off the equator of the Alcubierre wall (#102)

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/102

## Code and environment

Code: worktree `~/Source/negative-mass-i102` on branch `wip/i102-type3`, started at main fc6014f. New files only:
`notes/warp/he_type3.py`, `notes/warp/he_type3_output.txt`, `notes/warp/he_type3.md`.
Python: `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0, mpmath 1.3.0). Every run is `nice -n 10` with
`OMP_NUM_THREADS=1`, one process at a time; a run longer than a few minutes is a systemd user unit `nm-i102-<step>` that
writes its exit code to `done/<step>.rc`. Memory is reported only and is never a stop condition. Nothing of
choptuik-large-d is touched.

Imports. `he_type3.py` imports `review_he_surface_lib.py` (#101: `ricci_jet` and `frame_block` for the frame Ricci tensor,
`sigma`, `minors`, `classify`, `rank_frac`, `QS`, `Harness`) and `he_type.he_type_exact` (#64, #103) with `he_type.tanh_jets`
for the cross-check of the profile jets. It does not import `he_surface.py` or `review_he_surface_{typeI,points}.py`.

## What is computed

Setting. Frame (n, e_x, e_rho) at the point r (c, s, 0), the 3x3 block M = eta R, characteristic polynomial
lam^3 + c2 lam^2 + c1 lam + c0, T = b + a u, Sigma(lam) = R - lam eta. A Type III point has a triple root and
rank(M - lam) = 2. Conjectured description, to be checked and certified, for v c s u != 0 and (a, b) != (0, 0):

    E1 = c2^2 - 3 c1 = 0,    E2 = 27 c0 - c2^3 = 0,    T = b + a u != 0.

Parts. (i) E1 and E2 as explicit polynomials in (v, F, a, b, u, c). (ii) Cofactor certificates: rank <= 1 at any lam forces
T = 0 (the unrotated certificate of #101), T = 0 with E1 = E2 = 0 forces rank <= 1 (so rank 2 at a triple root forces
T != 0), and 27 D + E2^2 = 27 E1 G on every point (so E1 = 0 and D = 0 give E2 = 0). (iii) Exact points of the set, in
Q and in Q(sqrt d), from a null kernel vector of R - lam eta, including the Q(sqrt 113) point of #72. (iv) Type II points
of D = 0 failing exactly one condition. (v) The curve of Type III points on the tanh wall for Le (sigma R_b = 8, v = 1/2)
and Rodal (sigma = 4, R_b = 5, v = 1), from the resultant of E1 and E2 in c^2, with the status word.

## Steps

| step | what | log | stop condition |
|---|---|---|---|
| 2 | `he_type3.py --no-controls` checks `planted_types` ... `exact_points` (planted types, the polynomials, the certificates, the description) | `step2.log` | any single elimination or certificate search not finished in 3 h wall: stop it and report what finished |
| 3 | `he_type3.py --no-controls` checks `type2_failures`, `tanh_curve` | `step3.log` | same |
| 4 | every `--mutate=NAME`, each must exit 1 and fire on exactly its frozen targets | `mutate_<name>.log` | none |
| 5 | `python3 notes/warp/he_type3.py > notes/warp/he_type3_output.txt`, must exit 0 | `final.log`, `final.time` | none |

## Pass criteria, written before the runs

- `planted_types`: the own type test (`classify`) and `he_type_exact` return III on a 3x3 Jordan block tensor (R = l m^T +
  m l^T, l null, m unit and orthogonal), II on a 2x2 Jordan block plus a simple root, II on a triple root of rank 1, I on a
  perfect fluid, each boosted and rotated by rational Lorentz matrices, and each deformed copy of the first changes type.
- `polynomials`: E1 and E2 from the frame Ricci tensor are polynomials in (v, F, a, b, u, c) after s^2 -> 1 - c^2, even in
  s; c2, c1, c0 equal the closed forms computed here from the typed R entries of he_surface.md section 1 (checked as
  polynomial identities), E1 = (p - q)^2 and E2 = (p - q)^2 (8p + q) on a double root p with third root q.
- `cert_rank`: `K1 T = sum q_k m_k(lam)` (the cofactors of #101, restated here) as a polynomial identity for symbolic lam.
- `cert_T0`: on T = 0 the characteristic polynomial is (x - lam*)[(x - lam*)(x - lam* - Theta) + K], E1 = Theta^2 - 3K and
  E2 = a polynomial in (Theta, K, lam*) up to explicit multiples of T, and the six minors at lam0 = tr M / 3 lie in
  <T, Theta, K> with explicit cofactors, all as polynomial identities modulo c^2 + s^2 = 1.
- `cert_disc`: 27 D + E2^2 = 27 E1 G as an identity in (c2, c1, c0).
- `equator_axis`: R_0rho and R_x,rho vanish at c = 0 and at s = 0, so M is block diagonal there and no triple root has
  rank 2.
- `description`: the chain of the theorem (Type III iff E1 = E2 = 0 and T != 0) written as the three implications, each
  from a named certificate, and tested at every exact point below.
- `exact_points`: at every exact point of E1 = E2 = 0 with T != 0 (the Q(sqrt 113) point of #72 and the points built
  here), `classify`, `he_type_exact` and the field rank agree: D = 0, a triple root, rank 2, Type III; N^2 != 0 and N^3 = 0.
- `type2_failures`: a Type II point of D = 0 with a triple root and rank 1 (E1 = E2 = 0, T = 0), one with a double root p
  and third root -8p and rank 2 (E2 = 0, E1 != 0, T != 0), and one generic (E1 != 0, E2 != 0, T != 0), none in the
  description, each admitted by the description loosened by dropping exactly its condition.
- `tanh_curve`: planted truth first: the same resultant code finds the exact point of a planted profile whose Type III
  point is known; then the curve of Type III points on the tanh wall at sigma R_b = 8 and 20, solved at 60 digits, each point
  checked by singular values of M - lam (two nonzero, one below 1e-45) and |N^3| < 1e-40; the points at v = 1/2 (Le) and
  v = 1 (Rodal), or the statement that the set is empty there and how that was decided. Status word: numerical evidence.

## Controls, frozen before the first control run

Each control is `he_type3.py --mutate=NAME`. It runs only its target checks and must exit 1 with every target failing. The lists
below were written before any control run and are not changed; `CONTROLS` in the script must match them name for name (checked by
`check_controls.py` in this folder).

| # | control | what it changes | targets |
|---|---|---|---|
| 1 | `no-rank` | the type test (`classify`, `he_type_exact`) calls every D = 0 tensor Type II | planted_types, exact_points, description |
| 2 | `disc-sign` | the sign of D in `classify` and `he_type_exact` | planted_types, type2_failures, description |
| 3 | `E2-typo` | E2 = 27 c0 + c2^3 | planted_types, polynomials, cert_T0, cert_disc, ray_family, exact_points |
| 4 | `E1-typo` | E1 = c2^2 - 4 c1 | planted_types, polynomials, cert_T0, cert_disc, ray_family, exact_points |
| 5 | `table-typo` | the sign of R_0x in the typed table of he_surface.md section 1 | polynomials |
| 6 | `weight-typo` | the weight of E1 under (A, B, u) -> (l A, l^2 B, l u) taken as 5 | polynomials |
| 7 | `cof-rank-perturb` | the first cofactor of the rank certificate plus 1 | cert_rank |
| 8 | `cof-rank-drop` | the cofactor of m02,12 set to 0 | cert_rank |
| 9 | `cof-g1-perturb` | the cofactor g1 of E1 plus 1 | cert_T0 |
| 10 | `cof-g2-drop` | the cofactor g2 of E2 set to 0 | cert_T0 |
| 11 | `cof-B-perturb` | the cofactor B_0 of the first minor plus 1 | cert_T0 |
| 12 | `theta-typo` | Theta with (1 + c) in place of (1 + c^2) | cert_T0 |
| 13 | `disc27` | 26 D + E2^2 in place of 27 D + E2^2 | cert_disc |
| 14 | `cof-disc-perturb` | G plus c2 | cert_disc |
| 15 | `axis-typo` | the vanishing of M[0,2], M[1,2] tested at c = 1/2 and 1/3, not at c = 0 and s = 0 | equator_axis |
| 16 | `ray-typo` | the cofactor n_X of the null ray plus 1 | ray_family, exact_points |
| 17 | `nf-radicand` | the radicand of Q(sqrt d) plus 1 when a point is built | exact_points, description |
| 18 | `phi-off` | phi shifted by 1/1000 when a point is built | exact_points, description |
| 19 | `loosen-E1` | the description without E1 = 0 | type2_failures, description |
| 20 | `loosen-E2` | the description without E2 = 0 | type2_failures, description |
| 21 | `loosen-T` | the description without T != 0 | type2_failures, description |
| 22 | `jets-sign` | the sign of f'' in the own tanh jets | tanh_jets |
| 23 | `P-term` | the first term of the shadow polynomial P dropped | tanh_planted |
| 24 | `T-filter-off` | the T != 0 test of `admit` skipped | tanh_planted |
| 25 | `tanh-off-root` | r shifted by 1e-6 before the 60-digit rank test of each point | tanh_points |
| 26 | `enclosure-shift` | the Krawczyk box moved by 20 half-widths off the root | tanh_enclosure |
| 27 | `eq-end-typo` | the equator end solved from r a + 3F = 0, not r a + 2F = 0 | tanh_curve |
