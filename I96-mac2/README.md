# I96-mac2: the coordinator's review of #96's thin-wall tanh spectrum (σR = 8 and 16)

Machine: macOS (the coordinator's Mac, 32 GiB), Python 3.14, numpy 2.5.4, at nice 10 with at most 2 processes, one
thread each. Issue: https://github.com/nmoinvaz/negative-mass/issues/96. Reviewed branch `wip/i96-thin` at 71a183f;
raw `I96-win` 7940b1e, `I96-dh610` 68abc50, `I96-mac` a477e61, `I96-rpi5` 921d262. (`I96-mac` holds the coordinator's
earlier box probes for the same issue.)

## Independent check `ind96.py` (criteria written before its first run)

ind96 drives #94's B-spline solver `notes/warp/tanh_spectrum_check.py` (`--part=solve --solver=arpack`) and compares
its sector spectra with #96's. That solver shares with `tanh_spectrum.py` the formulation (Galerkin compression of
S⁻¹M in Ḣ¹) and the profile; not the basis, coordinates, sector reduction or solver (its docstring). ind96's own code
only reads the npz files and compares.

Cases: σR = 8 and 16, m = ½ and 21/2, B-spline discretisations A and B at their defaults, `--floor=0.08`.

| id | criterion |
|---|---|
| G1 | the B-spline v_c is within 1e-6 of #96's: 1.562434 (σR = 8), 0.985030 (σR = 16) |
| G2 | at each case, the B-spline's A and B agree on the leading \|μ\|v_c to 1e-4 relative |
| G3 | at each case, the B-spline A's leading and second \|μ\|v_c (next distinct modulus) are within 1e-4 relative of #96's §7 tables: σR = 8, m = ½: 0.29951080, 0.224930; m = 21/2: 0.102782, 0.093657. σR = 16, m = ½: 0.22508330, 0.184364; m = 21/2: 0.102918, 0.095278 |

Mutations, each must exit 1 with its target failing: `ref` (#96's values × (1 + 1e-3); G3), `sig` (σR = 8 solved at
8.1; G1 and G3), `vc` (v_c × (1 + 1e-5) in the comparison; G1).

## Results

| file | what |
|---|---|
| `rerun_sector_numbers.txt`, `rerun_sector_numbers_mut_cut.txt` | `I96-rpi5/sector_numbers.py` rerun on the Mac, and its `--mutate=cut` |
| `rerun_vc_planted_shift.txt` | `tanh_spectrum.py --part=vc,planted,shift --sigmas=8,16 --procs=1` from the branch: exit 0, 15 s |
| `rerun_mut_lscale.txt` | `--part=shift --quick --mutate=lscale`: exit 1, `shift` fails (ρ = 1.0135), on target. `rerun_mut_lscale_wrongpart.txt` is my first attempt, run on `planted`, which `lscale` does not target (exit 0) |
| `resolve_s8_m3.5.*`, `eig/`, `cmp96.py`, `cmp96.txt` | one sector re-solved: σR = 8, m = 7/2, P = 200, 160 panels, `--part=vc,tanh` from the branch |
| `ind96.py`, `ind96_run1.txt`, `ind96_mut_*.txt` | the independent check, its run and its 3 mutations |
| `vc96.py`, `vc96.txt` | v_c at 30 digits (mpmath), the cause of G1's failure |

**Recount on a second machine.** `sector_numbers.py` exits 1 on the Mac as on rpi5, but the other way round. On the
Mac it matches all 132 values of the σR = 8 log. It differs from the σR = 16 log at m = 15/2 (window of A 14 against
12, symmetry 4.0e-11 against 2.9e-11). On the Mac, np.abs(array) − abs(scalar) at the cut is −1e-17 at σR = 8,
m = 7/2 and 15/2 (rpi5: 0), and 0 at σR = 16, m = 15/2 (rpi5: −1e-17). So the count of the cut's own pair follows
the last bit of |μ| on each machine. This tests the cause #96 inferred, and it holds.

**Re-solve.** Exit 0, 349 s, maximum resident set 7.31 GiB. The sector line equals the laptop's log: window 0.0975,
24 / 28 eigenvalues in it, 0 / 0 real, 102 / 94 real below it, largest 6.5e-4, identity 0 on 145 (97 real), residual
4.4e-5. The arrays match `I96-win/eig/tanh_sigma8_m3.5.npz` to 6.9e-15 (A) and 8.7e-15 (B) of the leading modulus
over the top 60, with v_c identical.

**ind96 run 1: exit 1. G1 fails at σR = 16.**

| case | G1 v_c | G2 A vs B | G3 lead, next vs #96 |
|---|---|---|---|
| σR = 8, m = ½ | 1.5624337, pass | 1.7e-7 | 2.7e-7, 7.9e-6 |
| σR = 8, m = 21/2 | pass | 1.4e-6 | 5.5e-6, 2.3e-5 |
| σR = 16, m = ½ | 0.9850202, **fail** | 4.3e-7 | 1.0e-5, 3.4e-5 |
| σR = 16, m = 21/2 | **fail** | 2.0e-6 | 1.7e-5, 4.6e-5 |

The cause is the checker's v_c, not #96's. vc96.py gives v_c = 0.985029856 at σR = 16 (#96: 0.985030) and
1.562433742 at σR = 8. `tanh_spectrum_check.py` integrates with 400 Gauss–Legendre points on [0, 15], about two points
across the σR = 16 wall, and is 9.7e-6 low there. Divided by v_c, the σR = 16 leading |μ| agree to 4e-7. The
failure stays recorded.

**Mutations:** `ref`, exit 1, G3 fails; `sig`, exit 1, G1 and G3 fail; `vc`, exit 1, G1 fails. All on target.
