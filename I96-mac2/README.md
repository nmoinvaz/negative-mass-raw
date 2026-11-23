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
