# #188 design: the Taylor crate over complex s for the polar box counts

Written by negative-mass-mac-i188, stage 1. No crate code exists yet. Every number below is in a `dev_NN_*` log of this folder
(`devrun.sh` keeps command, stdout, stderr and exit code). Status of all numbers: *numerical evidence*, development runs, not
runs of record.

## Answer

Run the crate's own generic code over a pair type `Cx<T>` (re, im of any lane) that implements the crate's `Num`. The plane stepper
needs three one-line changes (Hermitian inner product, |z|², magnitudes) that are the identity on the real lanes. Gram–Schmidt
with a real positive R diagonal gives winding2's D exactly, with the phase carried by Q; the probe shows this to 3.3e-12.
The issue's 1e-9 bar cannot be applied to the stored cache values: they carry phase errors of 1e-7 to 9e-7 rad (scipy at
rtol 1e-8). The bar applies to a fresh scipy evaluation at rtol 1e-13. Three decisions are asked for at the end.

## 1. What the probes found

| probe | result |
|---|---|
| `dev_01`, `dev_07`: winding2's D at 8 stored points of the box l = 2, Re s ∈ [0.1, 2], \|Im s\| ≤ 2.5 (I126 cache, 147 points), R_s = 404.85 (kmin 0.10506) | fresh rtol 1e-8 reproduces the stored value to 3.3e-12 (modulus), 1.5e-10 (phase) at every point |
| the same at rtol 1e-12 | differs from the stored value by 3e-13 … 2e-10 (modulus) and **1.1e-7 … 8.8e-7 rad (phase)**, 0 at the two real points |
| `dev_14`: rtol 1e-8 → 1e-13 at three points | successive phase changes (0.1 + 1.76i) 5.8e-7, 5.6e-8, 6.0e-9, 6.5e-10, 7.2e-11; (2 + 2.5i) 4.0e-7, 3.7e-8, 3.8e-9, 3.7e-10, 3.7e-11; (0.1 + 0.5i) 1.0e-7, 9.2e-9, 7.6e-10, 8.0e-11, 8.9e-12. The error falls like rtol, so rtol 1e-13 is within about 1e-11 of the limit |
| Hermitian modified Gram–Schmidt (positive real R diagonal) in place of LAPACK's QR, same rtol 1e-12 | D agrees with LAPACK's to 8.9e-15 … 5.5e-13 (modulus), 1.5e-14 … 3.3e-12 (phase) at 8 points (0 in phase at the two real ones). `dev_16`: LAPACK's R diagonal is exactly real for 1000 random complex 6 × 3 matrices (1472 of 3000 entries negative), so `polar_solver._qr`'s `ph` is a sign only |
| the same with the conjugate-free inner product (control) | 8.6e-2 … 1.8 (modulus), 2.6e-2 … 2.9 rad (phase): fires. `dev_01`'s B12 column is wrong (class attribute bug, identical to H12); `dev_07` has the fixed control |
| `dev_09`–`dev_13`: winding2's `count()` ported to read values from the stored cache | reproduces the stored result: winding +0.0000, max step 0.39, min\|D\| 6.70e-04, D(x0) = −2.999e-02, D(x1) = −1.773e-03, plant +2.0000 (0.40), asks 133 (147 with the plant) of 147 cached points, none missing |
| the counter's mutations on the stored values | `reverse` −2.0000, `wrongdouble` +1.0000, `misplant` 0.0000, `onesided` +1.7195 (bar: 2 ± 0.05): each fires |
| `dev_15`: wrong inputs on the stored points | `strip_off`, `conj_s`, `rs_shift` move the phase of 145 of 147 points by more than 1e-9 rad (median 1.6 to 1.7 rad); the two real points stay |
| `dev_03`, `dev_04`: the real crate at the box's \|s\| (R_s 36 … 84), l = 2 | dd 0.083 … 0.091 s per D (interior 0.056 … 0.069 s, scalar plane 0.021 … 0.034 s, q 0.001 s); f64 0.0034 … 0.0082 s. Real D at γ = 0.1 and 2: −2.99851e-02, −1.77288e-03, equal to the stored D(x0), D(x1) |
| `dev_06`: cost of a complex multiply-add against a real one (30-term kernel) | f64 1.1×, dd 1.7×, qd 3.6× |
| scipy per D on this Mac (load 4 to 6), same box | rtol 1e-8: 1.7 … 7.5 s; rtol 1e-12: 4.6 … 22 s; rtol 1e-13: 7.6 … 26.7 s |

## 2. The complex scalar

`Cx<T: Num> { re: T, im: T }` in a new file `src/complex.rs`, behind the cargo feature `complex`. It implements `Num` for T = f64, dd,
qd, od, so every generic piece of the crate (`Ser`, `j_series`, `integrate`, `det_n`, `inv_n`, `contracting_projector`, `zerilli_q`,
`interior_q`, `JTable::to_lane`, `VacSource`) runs unchanged on a complex lane. Not multidouble's `Dc`: that is an 8-lane
complex double-double dual number of the engine, not a scalar of the four lanes. Not multishoot's `plane::Real`: real only until
the library change of stage 3.

Real embedding is exact. A `Cx` with im = 0 behaves bit for bit as its real part: `mul` is (ac − bd, ad + bc); `recip`, `sqrt` and
`ln` take the real-axis branch (`recip` = (re.recip(), 0), `sqrt` of a nonnegative real = (sqrt, 0), `ln` of a positive real =
(ln, 0)) when im = 0. So the complex lane at Im s = 0 should reproduce the real lane's bits (check R2). `ln`, `exp` and `to_f64`
of a number with im ≠ 0 panic: the R diagonal is real positive, so none is needed, and a silent drop of the imaginary part is
the failure the panics catch.

Changes to shared code (all identity on real lanes; the check R1 compares the outputs of the old and new binaries):

| where | change |
|---|---|
| `num.rs` | four trait methods with defaults: `conj` (self), `abs2` (self·self), `mag` (`to_f64().abs()`), `re_f64` (`to_f64()`) |
| `plane.rs` `gram_schmidt` | inner product `conj(y_p)·y_c`; squared norm by `abs2` |
| `plane.rs` `integrate`, `polar.rs` | `.to_f64().abs()` → `.mag()` at 9 sites (step control, two pivots, `fro`, projector change, `zerilli_q` ratios, `interior_q`); the vacuum coupling assert |
| `polar.rs` `zerilli_q` | after the start value: `if (q / gamma).re_f64() > 0 { q = -q }` (polar_solver's branch rule for complex s; never true for real γ > 0) |
| `polar.rs` `d_eval` | split into `d_eval_s(cfg, table, mext, s, \|s\|, r_s, r_far)` and a wrapper `d_eval(.., gamma)` that computes the same R_s and r_far as now and calls it |

`table.rs` is not touched: `JTable<DD>::to_lane::<Cx<DD>>` already exists and J = J0 + s²·J1 takes a complex s² from the lane. The
J tables stay real (their imaginary parts are zero); using that to halve the jet cost is an option for later, not now.
`lib_plane` and `complex` are exclusive (`compile_error!`) until the library holds a complex stepper (stage 3).

New files: `complex.rs` (the type), `cplanted.rs` (the planted systems of §6), `cdrive.rs` (the commands below). `main.rs` gets the
module lines and the commands. `taylor_polar.py` gets `--complex`, built as `cargo build --release --features complex
--target-dir target/complex`, so the default build and its 22 checks are untouched.

Commands: `dc` (list of s, one process, one star and one J table, one JSON line per s with D and q as lane strings) and `dserve`
(the same, reading `re im` lines from stdin, for the counter). Both take `rs` (the fixed R_s), `zfac`, `lane`, `l`, the star's
`pc`, `zc`.

## 3. The plane stepper over a complex lane, and the phase

The stepper is `plane::integrate` as it is, on `Cx<T>` columns. After each step, modified Gram–Schmidt twice with the
Hermitian product Σ conj(y_p) y_c; R_cc = ‖v‖ is real and positive; `ln_vol` is real and adds Σ ln R_cc. The phase of
the columns therefore lives in Q (it rotates with s and with the flow), and D = det[Q_Y | Q_Z] needs no stored phase.

This is the gauge `polar_solver` has: LAPACK's complex QR returns a real R diagonal, `ph` is a sign, and the probe shows
Hermitian Gram–Schmidt gives the same D. The coordinator's comment asks for "the QR's phase recorded in `ln_vol`". The same D
results if the phase is moved into a complex `ln_vol` and Q is put in a pivot gauge (each column's largest component real
positive); that variant adds a code path, makes Q smooth, and gives up the property below. **Decision 1** asks which to build; I
recommend the positive gauge.

The property: the complex lane at real s is the real lane's output bit for bit, because the positive gauge reduces to the real
Gram–Schmidt. The pivot gauge puts a ±1 into the complex log-volume at real s instead.

The complex log-volume of the issue's acceptance, in the positive gauge, is Λ = ln_vol + ln det(Q₀ᴴ Q), with Q₀ an orthonormal
basis of the exact plane. For a plane invariant under J (the planted case) Λ = Σ λ_j x + ln R₀-term. It needs the exact basis, so it
is a planted-case quantity; in the real problem the phase is read from det[Q_Y | Q_Z].

## 4. winding2's normalization

winding2's D (cached values) is `PolarProblem.D(s)` with these choices; the crate reproduces each:

| winding2 | crate |
|---|---|
| interior plane from fixed r0 = 1e-3 to r_m = 24.10980364018201 (grid rule, #187 `grid_rm`) | as now; r_m passed |
| scalar plane from a fixed R_s = r_m + rsmult / kmin, kmin = min Re k± over the contour (404.8501936481817 for the box) | `rs` argument, computed by the Python driver with winding2's code (`np.sqrt`, 200 points per edge) and passed as a repr, exact |
| Zerilli column (1, q/f), q the decaying Riccati value from r_far = r_m + zfac (40 + 20 l)/\|s\| + 50, start −√(s² + V), sign so that Re(q/s) < 0 | as now, `\|s\|` and the branch rule of §2; `zfac` passed |
| `D(s)` = det of the two orthonormalized planes with the phases of both QR chains | Hermitian Gram–Schmidt (§3), D at lane precision |
| the phase strip exp(−i Im[(k₊ + k₋)(R_s − r_m) + (k₊ + k₋ + s) r_m]), k± = √(1 + (s ∓ iω)²) principal, s rounded to 12 digits | applied by the Python driver in double precision to the crate's D (a unit-modulus factor of argument up to about 600 rad, error 1e-13); the crate returns the unstripped D |
| the scalar start columns 0 and 2 of the spectral projector (eig) | columns 0 and 2 of the matrix-sign projector (`contracting_projector`), the same projector |

winding2's D differs from `polar_solver.D(s)` called with its default R_s (which varies with s) by exactly the strip and the fixed
R_s; the crate matched polar_solver at real s only, where the strip is 1.

## 5. The stored box

**Primary**: `winding2_cache_eps-1_w0.7603_l2_0.1_2.0_2.5.pkl`, the `w_p7603_l2` box of #126 (the table of RESULTS.md §5, l = 2,
phantom star ε = −1, ω = 0.7603, Re s ∈ [0.1, 2], \|Im s\| ≤ 2.5). Copy: `negative-mass-raw/I126-rpi5/cache/`, 147 points (the 118 of
`I5-rpi5/cache` plus those of the `--guard=all` run, `cache_sources.sha256`). Made by `winding2.py` of branch `wip/i126-guard-all`
at e3bdadd, options `--plant=0.3,1.76 --guard=all`, rtol 1e-8 (the script's default, `RTOL` unset), Python 3.14.10, numpy 2.5.4, scipy
1.18.1 on rpi5; `dev_01` reproduces the values here to 3.3e-12. Its count: winding +0.0000, plant +2.0000.

Why this box: it is the box of the §5 table; its edge runs along Re s = 0.1, where R_s = 404.85 is large (the long scalar plane
dominates the cost, as in the strips of #116); it covers the thresholds Im s = 1 − ω = 0.2397 and 1 + ω = 1.7603 and D's phase over (−π, π]; 147 evaluations are cheap to redo in scipy (about 40 min at rtol 1e-13). It is l = 2
only: the l dependence enters through the J table (one per l), which #186 and #187 tested for l = 2 … 6, so a second box adds little
to this check.

**Second box, for the counts only**: `I117-mac/cache` and `I117-rpi5/cache` `winding2_cache_eps-1_w0.7603_l2_2.0_5.0_10.0.pkl`
(Re s ∈ [2, 5], \|Im s\| ≤ 10, 195 points, plant 2.5 + 1i; the two caches come from two machines and agree to 2.6e-10, median 6.2e-12).
It tests large \|s\| (up to 11) and a small R_s. Its count: winding +0.0000, plant +2.0000.

**The bar.** The issue says "matches the scipy path's modulus and phase to 1e-9". The stored values cannot be matched that closely
by any accurate evaluator: their phase is off by 1e-7 to 9e-7 rad (§1). So check X1 compares the crate's D (dd) at all 147 points
with a **fresh scipy D at rtol 1e-13** (same `polar_solver`, same fixed R_s, same strip), modulus ratio and phase, bar 1e-9 each at every
point. The stored values are compared too and reported without a bar, with the scipy rtol 1e-8 error it must show. **Decision 2.**

## 6. The planted zero and the count

The counter stays in Python: a copy of winding2's `count()`, `--plant` and `--y0`, `--guard`, `--nseg`, `--rsmult`, `--zfac` in
`taylor_polar.py`, with `F(s)` = the strip times the crate's D from a `dserve` process (cached in memory and in a jsonl file). The port
is checked first against the stored values alone (W0: it reproduces §1's result and asks for no missing point), so its logic is
independent of the crate.

Planted zeros, two levels:

- **CX2, the analytic factor of winding2's `--plant`**, on the crate's values: winding 0.0000 ± 0.05, plant difference 2.0000 ± 0.05, max
  phase step < 0.45, on both boxes; the set of evaluated points reported against the stored 147. A box whose count is 0 cannot see a
  sign error of D's phase (`conj_s` is silent on CX2: D̄ has winding −0 and the factor adds +2 either way). X1 catches `conj_s`; CX2
  alone does not.
- **CXZ, a planted determinant with zeros** (sign sensitive, end to end through the stepper): constant J = A_re + i A_im over 6 × 6
  Gaussian-integer entries (the rotating phase), the regular plane from 0 to L, the decaying plane inward from L + Lz, starting data
  Y₀(s) = Y₀ + p(s) [0 0 u] with p(s) = (s − s₀)(s − s̄₀), and u chosen (mpmath, 130 digits) so that Y₀ and Z₀ meet when p = 0: D(s) is
  c · p(s) up to a positive real factor, so winding = 2 for s₀ = 0.8 + 0.5i inside a box and 0 outside; `conj_s` gives −2. The reference
  D(s) comes from mpmath's `expm` (shares no code). Bar: crate D against the reference at 20 points on the contour to 1e4 ε max(1, ·)
  (the same bar as the planes), and the count equals 2.

Both are in the acceptance "a planted zero in a box is counted"; CXZ is the one that can see a wrong sign or a non-holomorphic gauge.

## 7. Criteria, each written before any run, and the controls

Bars use ε, the lane's unit roundoff (f64 1.1e-16, dd 1.2e-32, qd 1.5e-64), as multishoot's plane tests do.

| check | what | bar | `--mutate=` (target) and the effect it must have |
|---|---|---|---|
| R1 | real lanes, the old binary (main 0d1d376) against the new build, default and `lib_plane`: `d` at l = 2, 6, γ = 0.001, 1, 40, lanes f64, dd, qd; `planted` const and linear, three lanes; every field except times, as strings | all equal | `r1_ulp` (the last digit of one D in the new log changed): 1 field of the compared lines differs |
| R2 | complex lane at Im s = 0 against the real lane: the same `d` list, `dc` with s = γ, `rs` as the real run's r_s | Re D equal as strings, Im D = 0, steps equal | `cx_recip_general` (the general formula at im = 0): R2 fails, P1c and X1 pass; the number of differing digits is measured in dev |
| P1c | planted complex plane: J = P diag(24 + 7i, 8 − 3i, −8 + 5i, −24 − 11i) P⁻¹, P = the L U of multishoot's P1 (integer, cond 96), k = 2, basis P[:, :2], x = 12, lanes f64, dd, qd. Exact: Q = Q₀ diag(e^{7ix}, e^{−3ix}), ln_vol = 32 x + ½ ln 5, Λ = (32 + 4i) x + ½ ln 5 (84 and −36 rad of column phase, 48 rad total) | plane ‖(I − Π) Y‖ ≤ 1e4 ε; \|Λ − exact\| ≤ 1e4 ε max(1, \|Λ\|) (imaginary part modulo 2π); orthonormality ≤ 1e2 ε; with f = 0 the complex lane equals #189's real P1 bit for bit | `bilinear` (no conjugate): orthonormality and ln_vol fail; `redot` (real part of the coefficient only, "the phase of the projection dropped"): orthonormality and ln_vol fail, plane passes; `f_scaled` (f₂ × (1 + 1e-6) in J, not in the reference): Im Λ off by 3.6e-5; `cx_mul_sign` (re = ac + bd): all fail |
| X1 | the box of §5, 147 points, dd | modulus ratio − 1 and phase, ≤ 1e-9 at every point against scipy rtol 1e-13 | `strip_off`, `conj_s`, `rs_shift` (R_s +1, strip unchanged): 145 of 147 points off by 5e-3 … 3.1 rad (`dev_15`); the six existing D mutations (`jsign`, `moncrief`, `swapcols`, `mext0`, `star_eps`, `shift_off`) run on X1 and each must fire (measured in dev) |
| XR | stripped D at R_s = 405, 300 and 200 on 8 points | agree to 1e-9 (modulus, phase); the transient is e^(−2 Re k (R_s − r_m)) < 1e-18 | `strip_sign` (exp(+i …)): phase off by 2 Im[…] mod 2π |
| W0 | the counter port on the stored values of both boxes | stored winding, plant, max step (0.39, 0.40), no point missing | the four counter mutations (§1): each fires |
| CX2 | the counter on the crate's values, both boxes | §6 | the four counter mutations on the crate's values |
| CXZ | §6 | §6 | `conj_s` (count −2), `reverse` (−2), `misplant` (0): measured in dev before declaring |
| TC | time per D, scipy at rtol 1e-8 against the crate f64 and dd, 8 points of the box | reported | none |

A control is declared only after its dev run shows the effect on its target in the named column. #187 had two controls that did
not read what they claimed (`qint_sign`, `qstart` on RX); here each dev run prints the target's number with and without the
mutation.

## 8. Time per evaluation

| | per D at the box's points |
|---|---|
| scipy path on this Mac, rtol 1e-8 (the stored ones) | 1.7 … 7.5 s |
| scipy, rtol 1e-13 (the reference) | 7.6 … 26.7 s at 3 points; about 40 min for 147 points |
| crate, real lane, R_s 36 … 84 (`dev_03`, `dev_04`) | dd 0.083 … 0.091 s, f64 0.0034 … 0.0082 s |
| crate, complex lane, R_s 405 — **estimate**, not measured | dd 0.3 … 0.6 s, f64 0.03 … 0.06 s |

The estimate: the scalar plane's steps grow with R_s − r_m (60 → 380: 6×) and cost 1.7× (dd) and 1.1× (f64) per multiply-add in the
complex lane (`dev_06`). Against scipy at rtol 1e-8 that is about 4 … 25× in dd and 40 … 250× in f64; the measured values replace this
in stage 2 (check TC). The setup per process (star 0.005 s, J table 5 s per l, dd whatever the lane) is paid once per `dserve`.

What #116's strips need (box Re s ≈ 0.01 … 0.1, the one that took 3.7 h on rpi5): the same call with `rs` = r_m + 40/kmin, R_s of order 10³ … 10⁴.
The cost grows linearly with R_s − r_m, so a point costs about R_s/405 times a point of this box: seconds in dd, 10 s at R_s = 4000.
Whether dd or f64 holds there is not known: the decaying plane grows by e^(Re k · 4000) between normalizations (handled by the stepper)
and the phase strip's argument reaches 10⁴ rad, so its double-precision error is about 1e-12. No check covers R_s above 405 yet; XR
adds R_s = 600 at 8 points for dd, and TC reports one point at R_s ≈ 1000.

## 9. Plan, files and time

Stage 2 files: `taylor_polar/src/{complex.rs, cplanted.rs, cdrive.rs}` (new), `num.rs`, `plane.rs`, `polar.rs`, `main.rs`, `Cargo.toml` (edits, §2),
`taylor_polar.py` (`--complex`), `taylor_complex_output.txt`, a section of `taylor_polar.md`, this raw folder. Not touched: `table.rs`, `winding2.py`,
`polar_solver.py`, RESULTS.md.

Merge note for the coordinator: #192 and #196 work in the same crate. My edits to existing lines are the 9 `mag` sites, `gram_schmidt`'s two
lines, `zerilli_q`'s branch line, `d_eval`'s head and the four trait defaults; every other change is new files.

Stage 3: multishoot's `plane` module maps. `orthonormalize`, `Plane::advance` and `Plane::new` use the scalar only through `Real`'s operations and
three `to_f64()` magnitudes; a `plane::Scalar` supertrait with `conj`, `abs2`, `mag`, blanket-implemented for `Real`, and a `plane::Complex<R: Real>`
pair give the complex plane with the real lanes unchanged. The pull request goes from `~/Source/negative-mass-i188-libs/multishoot` on
`feat/complex-plane` with P1c as its planted case. Its controls and cross-backend digest follow multishoot's CLAUDE.md; `+avx2,+fma` cannot be run here.

Time: 10 … 14 h as estimated; the design stage took about 2.5 h. Stage 2: build and the dev runs of every control 4 h, scipy reference (one process) and the checks 3 h
(largely waiting), notes 1.5 h; stage 3 3 … 4 h.

## Decisions asked

1. **Gauge.** Positive real R diagonal, phase in Q, `ln_vol` real (recommended), or phase in a complex `ln_vol` with Q in a pivot gauge. Default if no answer: the first.
2. **The 1e-9 reference.** Fresh scipy at rtol 1e-13 (the stored values are off by up to 9e-7 rad), or the stored values with a bar the coordinator names. Default: the first, with the stored comparison reported.
3. **CXZ, the planted determinant** (§6, about 2 h): in the acceptance as the sign-sensitive form of "a planted zero is counted", or dropped, leaving only the analytic factor, which a box with count 0 cannot test for a sign error. Default: in.
