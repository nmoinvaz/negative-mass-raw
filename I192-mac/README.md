# I192-mac: design and development runs for multishoot's Taylor tables of coefficient functions along a path

Machine: mac, the coordinator's Mac (Apple M5, macOS), shared with other sessions; runner negative-mass-mac-i192 (Claude Code, Sonnet 5.5,
account claude-me2). Issue: https://github.com/nmoinvaz/negative-mass/issues/192
Code: worktree `~/Source/negative-mass-i192`, branch `wip/i192-taylor-tables` (from main 0d1d376); pushes:
`git push origin HEAD:refs/heads/wip/i192-taylor-tables`. Library clone `~/Source/negative-mass-i192-libs/multishoot` (main f929163, 4.2.0,
multidouble 6.1.0, multisolver 0.3.0), feature branch `feat/taylor-tables`. Rust 1.94.0 (aarch64-apple-darwin).
Written before the first development run. `dev_NN_*` are development runs (made with `devrun.sh`: stdout, stderr and exit code kept);
`run_NN_*` will be the runs of record. Amendments are numbered and dated at the end; a number below that came from a development run says so.

Stage 1 only so far: `design.md` (posted on the issue) states the API and the checks. No library code is written before the coordinator
approves it. The development runs below are **prototypes outside the library** (a scratch Rust program and a Python/mpmath script, both in
this folder) that exist to put numbers in the design: the effect of each control, and the answer to the question of whether `locate` or a
tail test cuts a step.

## What is being designed

`multishoot::table`: the Taylor series of F coefficient functions about the start of each of a path's steps, each step cut by the width at
which the *stored* functions' own series have converged, and a lookup that shifts a step's series to any point inside it. It is #186's
`table.rs` (`width_of`, `build_table`, `JTable::jets`) with the problem taken out. The caller supplies the series of its functions at a
point (`SeriesSource`); the library knows nothing of J, stars or the polar problem.

The step rule (from #186, stated here so the criteria below can refer to it): with `nb` coefficients `c_k` of a function about the step
start b, `t_k(h) = |c_k| h^k` and `S(h) = sum_k t_k(h)`, the width `w` of the step is the largest h (found by bisection, IEEE operations
only) at which, for **every** stored function, `t_k(h) <= tail * S(h)` for the last `last` orders (k = nb - last .. nb - 1); the step is
`min(fraction * w, valid_to - b, hmax, rest of the path)`. #186's values: nb = 30, tail = 1e-25, last = 2, fraction = 0.3.

## Planted problems (all rational functions: coefficients about any point and values in closed form, in the lane)

Common: lanes f64 (nb 20, tail 1e-13), dd (nb 30, tail 1e-25), qd (nb 60, tail 1e-55), od one smoke case (nb 100, tail 1e-115);
`last` 2, `fraction` 0.3. The reference is the function's closed form in the lane (a quotient or a power by repeated multiplication) and
the exact coefficients by their recurrences; it shares no code with the table.

| case | functions | path | source |
|---|---|---|---|
| **PA** poles behind a long-step source | `1/x^2`, `1/x`, `1/(30-x)` | 1e-3 to 25 | analytic; `valid_to` = next multiple of 6 (pieces as long as 6, the way a numerically known background has long steps) |
| **PB** a piece boundary the series cannot cross | `1/(30-x) + 3 (x-5)_+^2` | 0 to 20 | jets about x < 5 are those of `1/(30-x)` (the ramp's are zero), `valid_to` = 5 for x < 5; jets about x >= 5 include the ramp |
| **PC** a conjugate pair ahead | `1/((x-12)^2 + 0.04)` | 10 to 14 | analytic, no `valid_to` |
| **PD** no singularity, the width set by nb | `(1 + x/4)^40` (degree 40 > nb) | 0 to 3 | analytic |
| **PE** the last-two blind spot | `1/(1-x^3)` | 0 to 0.9, `hmax` 0.5 | analytic; the first step's series is in x^3, so c_28 = c_29 = 0 |
| **PF** backward path | PA's functions | 25 to 1e-3 | analytic; the pole is ahead |
| **PG** a singularity on the path | `1/(x-5)` | 0 to 10 | analytic |
| **PH** the plane stepper through the table | `J(x) = M / x`, M = P diag(1, -2, 3, -1) P^-1 (P integer, unimodular), k = 2, the plane P[:, :2] | 1e-3 to 40 | the table of `1/x`, `Plane::advance` (#189) with its default `Plan` (tol 100 eps, kt = `Plan::optimal_kt`, kj = kt, nb = kt + 12, tail = eps_lane); exact: the plane stays span P[:, :2] and ln_vol = (1 + (-2)) ln(40/1e-3) + the starting basis' term |

### Pass criteria (written now; none is changed after a run)

- **C1, the jets.** For every step i, every function f, x0 = s_i + t len_i (t in 0, 1/4, 1/2, 3/4, 1) and
  h = u max(0, min(0.7 w_i, V_i - x0)) (u in 0, 1/4, 1/2, 3/4, 1; w_i the step's width as the table reports it, V_i the source's `valid_to`
  at s_i, so a step that crosses it is sampled at its value there), with `jets` = the table's series for f shifted to x0:
  `E = |sum_k jets_k h^k - f(x0 + h)| / sum_k |jets_k| |h|^k <= 10 tail` of the lane. (At fraction 0.3 the reach |x0 - s_i| + h stays within w_i,
  where the last two terms are at most `tail` of the sum, so the polynomial's error is a few `tail`; 10 tail is that with a factor 3 to 4.)
  PB's reference is the piecewise function, so a step across x = 5 fails it. PE under `last` 2 is **expected to fail C1** (a recorded
  limitation) and under `last` 3 to pass; it runs in dd (nb 30) and qd (nb 60) only, where nb - 2 and nb - 1 are not multiples of 3 (in f64,
  nb 20, c_18 is not zero and the rule is not blind).
- **C2, the structure.** Steps are contiguous (end_i == start_(i+1) bitwise), the first starts at xa and the last ends at xb bitwise, every
  step has the path's direction, no step ends past `valid_to` of its start, `len_i <= fraction w_i (1 + 1e-12)` always, and
  `len_i >= fraction w_i (1 - 1e-6)` unless cut by `valid_to`, `hmax` or xb. The test recomputes `w_i` from the stored series by its own
  bisection (it shares the rule's definition, not the library's code).
- **C3, an independent step list.** The Python/mpmath prototype (50 digits, its own coefficients and bisection) gives each case's step count
  and breakpoints; the library's must have the same count and breakpoints within 1e-9 relative (dd lane; PA, PB, PC, PD, PF).
- **C4, PH.** The plane error (Frobenius norm of (I - Pi) Y, as #189) at most 1e4 eps_lane and the log-volume error at most
  1e4 eps_lane max(1, |reference|), in f64, dd and qd (bars as #189's). If PH fails at the defaults it is reported with the number, and
  the default `fraction` or the design (a consumer-side step limit, below) is revised, not the bar.
- **C5, errors.** PG returns `Err(Stall)` with x within 1e-9 of 5 (before 5); the same input with the pole moved to 15 returns Ok (the
  check's input broken once). A series with a NaN coefficient returns `Err(NotFinite)` naming the function and order.

### Controls (declared by name now; **their targets, the checks each must fail, are declared after a development run of each**)

In the library (feature `mutate`, a `TableControl` set on the build options): `Wide` (a step runs to `valid_to` or `hmax`, ignoring the
width: #186's `wide_table`); `FractionOne` (fraction 1); `NoShift` (the lookup does not shift: #186's `shift_off`); `LooseTail` (tail 1e-5);
`IgnoreValidTo` (steps cross `valid_to`); `ShiftF64` (the shift's delta formed in f64 and widened, where it must be the exact difference in
the lane). In the test, a wrong input and no hook: `ref_scale` (the reference function times 1 + 1e-4), `pole_off_path` (C5's).

## Development runs (stage 1)

- **D1, `locate` or a tail test** (scratch Rust, `exp_locate/`, multisolver =0.3.0 from crates.io). Coefficient sets, all c_0 .. c_29 about
  u = 0 with the radius 1 unless stated: S1 1/(1-u); S2 1/(1-u)^2; S3 1/(1-u)^3; S4 (1-u)^(1/2); S5 conjugate pair at e^(+-0.6i)
  (c_k = sin((k+1) 0.6) / sin 0.6); S6 the same at angle 0.05; S7 e^u (c_k = 1/k!) and S7b e^(10 u); S8 1/(1-u^3); S9 1/(1-u^2);
  S10 1/(1-u) + 1/(1+u/1.2) (two real singularities, 1 and -1.2); S11 1/x^2 about x0 = 1e-3 (radius 1e-3, coefficients up to 1e90).
  Output per set: the tail test's width (nb 30, tail 1e-25, last 2, and last 4; search cap 100 radii), width/radius, and `locate`'s kind, |s|, bar, exponent, time.
  **Decision rule, set now.** The table's rule is the tail test, because a table needs the width at which the *truncated* stored series has
  converged, which for an entire function (S7) is finite while its radius is infinite. `locate` is added as a guard only if it resolves S8
  (kind Real, |s| - 1 within its bar) where the tail test with last 2 is blind; and it replaces nothing. The measured time of one `locate`
  against one width evaluation is reported.
- **D2, the table prototype** (`proto_table.py`, mpmath, 50 digits): the rule and the lookup on PA to PH; per case the step count, the
  steps' ratios, C1's largest E per case, and the effect of each control (largest E, the check it would fail). PH uses a Python port of the
  plane stepper (Taylor recursion, modified Gram-Schmidt twice) at 50 digits, and reports the largest ratio (shift + step)/w seen.
- Threads: one process at a time, nice 10, `cargo build -j 2`; a run not finished in 2 h is stopped by its PID and reported.

## Amendments

**A1 (2026-11-27, after dev_01 to dev_14; stage 1 only, no library code yet).** The bars C1 to C5 are unchanged. Additions and findings:

- **Two cases added** (before any library run): **PP**, a polynomial `1 + 2x + 3x^2 - x^4` on [0.1, 3] (one step: its tail is zero, so the width is the search
  cap; the start 0.1 is not dyadic, so a shift by the f64 difference of x0 and the start is not the exact difference where x0 > 2 start), and **PS**, `1/(1 + 1e5 x)` on
  [0, 1] in qd (nb 60: c_58 = 1e290 and h^58 underflows in plain f64, so the rule must scale by powers of two). Controls added with them: `Unscaled` (the
  plain f64 test) with PS.
- **`ShiftF64` is a no-op on PA, PB, PC, PD, PF** (dev_04, dev_05: E equals the clean E to every printed digit in all three lanes): x0 and the step start are f64 numbers
  within a factor 2 of each other, so their f64 difference is exact (Sterbenz), and from 0 it is exact. A control that cannot change what its target reads is not a
  control; it is declared for **PP in dd and qd only** (E 4.6e-16 against bars 1e-24 and 1e-54), silent in f64 by design.
- **The OD smoke case is PC, not PA** (nb 100 at x0 = 1e-3 puts c_99 at 1e305, at the edge of f64's range).
- **Controls' computed effects** are in `design.md`, from `dev_04` (PA, PB, PC, PD, controls), `dev_05` (PD, PE, PF, PG, PP), `dev_09` to `dev_12` (PH), `dev_13` (PS).
- Observed margins of the clean runs, for the record (the bars were not moved): max E / bar = 1/220 (PA f64), 1/530 (PA dd), 1/700 (PA qd), 1/21 (PC f64),
  1/39 (PC dd), 1/36 (PC qd); the tightest of all is PC, the conjugate pair.
- **Run bookkeeping.** `dev_06_proto_ph_killed.log.txt`: the first PH run (f64, dd, qd and the control `wide`) was stopped by its PID after 10 min with no output (stdout
  buffered; with the control `wide` the planner's steps collapse and the plane does not finish), the run keeps no result; PH then got a 3000-plane-step cap (counted as a
  failure) and `-u`. `dev_11_proto_ph_controls_qd` holds the qd *baseline* only (its name is wrong; the controls are `dev_12_proto_ph_controls_qd2`). `dev_12_*` has two
  runs started together that took the same number.
- **PH, the consumer's reach** (`dev_07`, `dev_08`, `dev_09`, `dev_11`): at fraction 0.3 PH passes in f64, dd and qd, and the plane's steps reach past the table's width
  w in dd (6 of 90 steps, up to 1.03 w) and qd (22 of 95, up to 1.13 w). At dd, fraction 0.5 passes (25 steps past, up to 1.25 w), 0.7 and 1.0 **fail** the log-volume
  bar (1.0e-26 and 1.0e-23 against 1.2e-27). Reported, not tuned.
- **C6 (optional, proposed after D1; not yet part of any run).** An independent estimate of the radius: `multisolver::locate` on a step's series in dd, the ratio
  width / |s| of every step of PA's `1/x` and PC with a resolved singularity within [0.09, 0.17] (D1's resolved sets lie in [0.104, 0.160] at nb 30, tail 1e-25, last 2).
