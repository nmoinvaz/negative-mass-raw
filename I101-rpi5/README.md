# I101-rpi5: logs of the independent review of #72's Type I set on D = 0 off the equator (#101)

Machine: rpi5 (rpi5-ubuntu, Raspberry Pi 5, aarch64, 4 cores, 8 GB, shared with choptuik-large-d).

Issue: https://github.com/nmoinvaz/negative-mass/issues/101

## Code and environment

Code: worktree `~/Source/negative-mass-i101` on branch `wip/i101-review-surface`, started at main 43bfed0. New files only:
`notes/warp/review_he_surface.md`, `notes/warp/review_he_surface_{lib,ricci,typeI,points}.py` and their `_output.txt`.
Python: `~/Source/negative-mass-venv314/bin/python` (sympy 1.14.0, mpmath 1.3.0). Every run is `nice -n 10` with
`OMP_NUM_THREADS=1`, one process at a time; a run longer than a few minutes is a systemd user unit `nm-i101-<step>` that
writes its exit code to `done/<step>.rc`. Memory is reported only and is never a stop condition. Nothing of
choptuik-large-d is touched.

Independence. The reviewer read `he_surface.md`, `he_type.md`, and the issue texts and comments of #72 and #64. The reviewer
did not open `he_surface.py`, `he_type.py`, `review_he_derive.py`, `phantom_source.py`, their outputs, or raw `I72-*`,
`I71-*`, `I64-*`. One slip: #72's closing comment embeds the coordinator's `rev72.py` and the first print of that comment
showed it. The reviewer's routes below were written from the metric and from the claims, not from it.

## What is computed

Frame: at t = 0 the orthonormal frame (n, d_x, d_y, d_z) with n = d_t - w d_x of the comoving metric
-dt^2 + (dx + w dt)^2 + dy^2 + dz^2, w = v (1 - f(r)), at the point r (c, s, 0). Ricci from the second-order jet of w
with independent symbols (coordinate route, own Christoffel and Ricci code), the frame components from it, and the 3x3 block
M = eta R on (n, d_x, d_y). The rotated frame (n, r^, theta^) is built from these only to compare with the identities of
he_surface.md. The cofactor certificates are found in the unrotated frame by linear algebra over Q at random exact points,
and are then verified as polynomial identities modulo c^2 + s^2 = 1.

## Steps

| step | what | log | stop condition |
|---|---|---|---|
| 2 | `review_he_surface_ricci.py --no-controls`: planted types, the Ricci tensor against 50-digit second differences of the lab-frame metric, the frame table, equator and axis | `step2.log` | none |
| 3 | `review_he_surface_typeI.py --no-controls`, `review_he_surface_points.py --no-controls`: T1, T2, T3, the two identities, the certificates, exact points, the tanh scan, the Type III solves | `step3_typeI.log`, `step3_points.log` | any single elimination or certificate search not finished in 3 h wall: stop it and report what finished |
| 4 | every `--mutate=NAME` of the three scripts, each must exit 1 and fire on its targets | `mutate_<script>_<name>.log` | none |
| 5 | each script's full run, stdout to `notes/warp/review_he_surface_*_output.txt`, must exit 0 | `final_<script>.log` | none |

## Pass criteria, written before the runs

- `planted_types`: the own type test returns I, I, II, II, III, IV on the six planted tensors (perfect fluid, three
  distinct real roots, Jordan block plus a simple root, null dust plus pressure, 3x3 Jordan block, complex pair), each in a
  frame that is boosted and rotated with rational Lorentz matrices, and a deformed copy of each of the first five returns a
  type different from its original.
- `ricci_numeric`: all ten frame components of the Ricci tensor from the symbolic jets agree with the 50-digit second
  differences of the lab metric to 1e-30 relative to max(1, |value|), at three points, for the tanh profile; R(e_phi, .) = 0.
- `frame_table`: each of the six entries of he_surface.md section 1's table minus my frame Ricci reduces to 0 modulo
  c^2 + s^2 = 1, and R_00 + R_xx + 2 R_rho,rho = 0.
- `equator_axis`: D of my 3x3 block equals he_type.md's closed form on the equator and on the axis as a polynomial.
- `rotated_quantities`, `identity_necessity`, `D_on_T1`: the entries and identities of he_surface.md sections 1 and 2 reduce to 0
  from my frame Ricci after my own rotation.
- `cert_T1`, `cert_T2`: explicit cofactors; the identity sum(q_k m_k) = kappa (b + a u) etc. reduces to 0; a mutated cofactor
  must make it nonzero.
- `T3_multiplicity`: on T1 and T2 the characteristic polynomial is (x - lambda)^2 (x - mu) with
  mu - lambda = v^2 a u (2 r a + (1 + c^2) F), and on T1 the vector theta^ is an eigenvector.
- `exact_points`: Type I points from my own placement have D = 0 exactly, a double root, rank 1; each point failing exactly one
  of T1, T2, T3 is not Type I.
- `axis_points`: on the axis D = 0 iff v a = 0, and there M is diagonal.
- `tanh_scan`: a planted profile whose T1 and T2 set is non-empty is found non-empty by the same scan.
- `type3_tanh`, `type3_exact`: singular values of M - lambda and powers of N = M - lambda show a 3x3 Jordan block.

## Controls and their target lists, frozen before the first control run

Under `--mutate=NAME` only the control's targets run, and each target must fail, so the script exits 1.

`review_he_surface_ricci.py`

| control | what it changes | targets |
|---|---|---|
| `no-rank` | the type test returns II at every D = 0 | `planted_types` |
| `disc-sign` | D -> -D in the type test | `planted_types` |
| `mult-off` | rank is compared with n - m + 1 instead of n - m | `planted_types` |
| `drop-w2` | the lab-frame metric loses the shift's square in g_tt | `ricci_numeric` |
| `no-gamma2` | the numeric Ricci drops the Gamma Gamma terms | `ricci_numeric` |
| `table-typo` | the typed table's R_x,rho coefficient 1/2 -> 1/4 | `frame_table` |
| `eq-typo` | he_type.md's Q_eq, F + r a -> F - r a | `equator_axis` |
| `axis-typo` | he_type.md's Q_ax, (F b - a^2)^2 -> (F b + a^2)^2 | `equator_axis` |

`review_he_surface_typeI.py`

| control | what it changes | targets |
|---|---|---|
| `rot-sign` | the rotation is by -theta, r^ = (c, -s) | `rotated_quantities` |
| `tgt-ident` | 1 + v^2 F^2 -> 1 + v F^2 in the necessity identity | `identity_necessity` |
| `tgt-DT1` | 4 c^2 -> 3 c^2 in the factor of D on T1 | `D_on_T1` |
| `cof-perturb` | one cofactor of the T1 certificate gets +1 | `cert_T1` |
| `cof-drop` | one term of one cofactor of the T1 certificate is dropped | `cert_T1` |
| `cof2-perturb` | one cofactor of the T2 certificate gets +1 | `cert_T2` |
| `cof2-drop` | one term of one cofactor of the T2 certificate is dropped | `cert_T2` |
| `tgt-T3` | 1 + c^2 -> 1 + c in the T3 offset | `T3_multiplicity` |

`review_he_surface_points.py`

| control | what it changes | targets |
|---|---|---|
| `no-rank` | the type test returns II at every D = 0 | `planted_types`, `exact_points` |
| `loosen-T1` | the description of the Type I set drops T1 | `exact_points` |
| `loosen-T2` | the description drops T2 | `exact_points` |
| `loosen-T3` | the description drops T3 | `exact_points` |
| `locus-shift` | v on the Type I points is scaled by 101/100 | `exact_points` |
| `axis-typo` | the axis check expects the diagonal (-v^2 F b, -v^2 F b, 0) with the sign of b flipped | `axis_points` |
| `nf-modulus` | the modulus of Q(sqrt 113) is changed to 112 | `type3_exact` |
| `tanh-sign` | F + r f' -> F - r f' in the T2 test of the scan | `tanh_scan` |
| `type3-off` | v of each Newton solution is scaled by 1 + 1e-3 | `type3_tanh` |

## Results

Code commits on `wip/i101-review-surface` of nmoinvaz/negative-mass: 93e3a0b (step 2), 622cad8 and ce38d51 (step 3), af4e293 (the
scripts that produced the step 4b and step 5 results; the three controls lists of the scripts equal the frozen lists above),
5a2db26 (the review and the output files).

| step | command (args to the script in `notes/warp/`) | commit | exit | wall | peak rss | result |
|---|---|---|---|---|---|---|
| 2 | `review_he_surface_ricci.py --no-controls` | 93e3a0b | 0 | 1.7 s | not measured | 4 checks pass (`step2.log`) |
| 3 | `review_he_surface_typeI.py --no-controls`, `review_he_surface_points.py --no-controls` | ce38d51 | 0, 0 | 5.8 s, 1 min 50 s | not measured | 6 and 6 checks pass (`step3_typeI.log`, `step3_points.log`) |
| 3 | `review_he_surface_typeI.py --derive` | 622cad8 | 0 | 43 s | not measured | nullspace dimension 4, the typed cofactors lie in its span (`derive_T1.log`) |
| 4 | `--mutate=NAME` for 25 controls, `step4.sh`, `step4.list` | ce38d51 | all 1 | 2 to 111 s, longest `tanh-sign` | 61 MiB | 25 FIRED on exactly their frozen targets (`step4.summary`) |
| 4b | the 8 `typeI` controls again after an edit of `T3_multiplicity`, the old logs in `step4_typeI_before_T3_edit/` | af4e293 | all 1 | 3 s each | 58 MiB | 8 FIRED (`step4b.summary`) |
| 5 | the three scripts with no arguments, `final.sh`, stdout to `notes/warp/review_he_surface_*_output.txt` | af4e293 | 0, 0, 0 | 5.1 s, 10.3 s, 3 min 41 s | 58, 60, 62 MiB | 4 + 6 + 6 checks pass, 8 + 8 + 9 controls fire (`final_*.time`, `final_*.err` empty) |

The controls, each of which must fail its frozen target list and exit 1, are in `step4.summary`, `step4b.summary` and the
`mutate_<script>_<control>.log` files. The `.time` lines were taken with `/usr/bin/time -f "%e %M"` (seconds, KiB).

