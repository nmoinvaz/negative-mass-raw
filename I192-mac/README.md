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

**A2 (2026-11-27, stage 2). Library `feat/taylor-tables` at 03e5727 (module) and 3a64b91 (tests); pull request https://github.com/nmoinvaz/multishoot/pull/79.**

- **The coordinator's ruling on the design** (approved, with): API and rule as in design.md sections 1 and 2, with the monotonicity derivation in the module doc stated
  as proved only for what it shows (`d ln(t_k / S) / d ln h = k - k_bar`); Option L (`JetSource::limit`) **not in this PR** (filed by the coordinator as its own task);
  **`last` default 4**, PE asserts that `last` 2 fails and 3 and 4 pass, the step lists recomputed by `proto_table.py` for `last` 4 before the first library run; **C6 dropped**;
  controls confirmed; design section 9 items 1 and 2 belong to stage 3 and item 6 is stale (dropped).
- **Recomputed at `last` 4 before the first library run** (`proto_table.py` default now 4; the `last` 2 script is kept as `proto_table_last2.py.txt`): the cases and controls
  `dev_14` (step lists in `proto_steps_last4.json`), PS and PH in qd `dev_15`, the PH and PS tables' step lists `dev_16` (`proto_steps_last4_ph_ps.json`), PH f64 and dd `dev_17`.
  `gen_steps_in.py` wrote the library's `tests/table_steps.in` from them (C3). **One declared target changed with `last`**: `FractionOne` on PD no longer fires C1 (f64 5.8e-15
  against 1e-12, dd 4.3e-26 against 1e-24; at `last` 2 it did), it fires C2 only; every other target is as declared. At `last` 4 every clean C1 maximum is smaller, the tightest
  being PC (4.8e-15 / 1e-12 in f64, 5.5e-28 / 1e-24 in dd).
- **First library run (`dev_18`): C1, C2 and C3 pass in every cell (f64, dd, qd; PC in od), and the PH and C5 checks did not.**
  - **PH was ill-posed** (my error in the design). The plane P[:, :2] of `y' = (M/x) y`, M = P diag(1, -2, 3, -1) P^-1, has the exponents (1, -2) among (3, -1), so it is not the
    dominant plane and rounding in the lane grows against it as x^5 over 1e-3 to 40: plane error 5.5e-1 (f64), 6.4e-9 (dd), 7.3e-41 (qd), the lane's eps times 1e23. The 90-digit
    prototype hid it. The same run with the closed-form jets and **no table** gives the same 5.4772e-1 (f64): the table was not the cause. **The problem was changed, the bars were not**:
    M = P diag(-1, -2, -3, -4) P^-1 (every mode has an infinite series, the plane is the dominant one), ln_vol = (1/2) ln 5 - 3 ln(40 / 1e-3). The prototype's PH was rerun
    with it (`dev_19` f64 and dd with the fraction sweep and controls, `dev_20` qd; the old script is `proto_table_ph_exp1_2_3_1.py.txt`). **design.md section 4's table is superseded** by:

    | lane | table steps | plane steps | (shift + step) / w max | plane steps past w | fraction 0.3 |
    |---|---|---|---|---|---|
    | f64 | 125 | 86 | 0.970 | 0 | pass |
    | dd | 158 | 90 | 1.072 | 12 | pass |
    | qd | 193 | 95 | 1.168 | 30 | pass |

    and the dd fraction sweep (0.2, 0.3, 0.5 pass, with 0, 12, 30 steps past w; **0.7 fails** the log-volume bar, 1.15e-26 against 3.8e-27, 33 past, up to 1.52 w; **1.0 fails**,
    2.2e-23, up to 1.73 w); f64 passes at every fraction up to 1 (1.2e-11 against 3.4e-11). The PH controls at the prototype: `FractionOne` dd 2.2e-23, qd 5.2e-47 (bar 3.8e-27 and
    4.7e-59), `LooseTail` dd 1.2e-22, qd 1.5e-37, both silent in f64 (1.2e-11, 5.3e-14 against 3.4e-11).
  - **C5 is not met as worded in dd and qd** (`Err(Stall)` within 1e-9 of 5 from below). The coefficient of order nb - 1 of `1/(x-5)` is `d^-nb`, and every part of a multidouble shares
    f64's range, so it leaves it at d = f64::MAX^(-1/nb): `NotFinite` at 5 - x = 5.27e-11 in dd (the overflow distance 5.31e-11) and **7.13e-6 in qd** (7.29e-6), which is also
    outside the 1e-9 of the criterion. f64 meets it (Stall at 4.99999999999999112). The prototype, in decimal arithmetic, had no overflow. I did not change C5 or the library to meet it:
    the approved API has `NotFinite` for a coefficient that is infinite. The behavior is recorded in its own test (`pole_on_the_path_wide_lanes_recorded`: `NotFinite`, order nb - 1,
    below the pole within ten times `f64::MAX^(-1/nb)`; this is a recorded result, not the criterion) and in the module's limits.
- **Second library run (`dev_21`)**: all 15 tests pass, PH 5.4e-16, 5.9e-32, 2.6e-64 (plane) and 3.6e-15, 3.0e-30, 2.5e-62 (ln_vol) against 1.1e-12, 1.2e-28, 1.5e-60 and 3.4e-11, 3.8e-27, 4.7e-59.
- **Controls** (`dev_22`, with `mutate`): every cell as declared (the `declared` function of `tests/table.rs`); 21 tests pass. `ShiftF64` fires on PP in dd and qd only (4.6e-16 against 1e-24
  and 1e-54). `Unscaled` on PS gives E = NaN (the plain test steps to xb and the reference is evaluated past nothing: inf - inf), the prototype's 1.0; both fail the bar.
- **Cross-backend** (`dev_23`): the default build's digests, embedded in the test, hold with `--features portable,mutate`.
- **Runs of record** (module at 03e5727, tests at 3a64b91, aarch64 NEON on this Mac; `+avx2,+fma` not run): `run_01` default (15 passed), `run_02` mutate (21), `run_03` portable,mutate (21),
  `run_04` portable (15), `run_05` fmt, clippy (mutate, portable+mutate, default), doc with warnings denied, all clean; the 28 digest lines of `run_01` and `run_04` are identical (`cmp`).
- **Run bookkeeping.** `dev_17` and the earlier `dev_16` ran together with others and `dev_12` has two runs (A1); `dev_13` holds PS at `last` 2. A sed edit of `proto_table.py` replaced
  its `last` default; both older scripts are kept as `.py.txt`. A pkill by name was refused by the auto-mode classifier once, correctly (stop by PID only); the process had already ended.

**A3 (2026-11-27, stage 2 review round). Library `feat/taylor-tables` at bc78792 (module) and 60d21ab (tests); CI of 3a64b91 green on every job, including `Ubuntu x86_64 AVX2` (`+avx2,+fma`), SSE2, portable, mutation controls, Windows MSVC, ARM64 and macOS: the pinned digests hold on x86.**

- CodeRabbit posted 15 findings (README 2, module 8, tests 5). Each edge case got a test **that was run on the code before the fix and failed there for its own reason** (`dev_24`: 8 failures
  of the 10 new tests; two of them first failed for the wrong reason, `Opts::new(2, ..)`'s `last` 4 and a `last` of nb that reads c_0, which no tail passes, and were corrected before the run kept):
  `default_last_fits_small_nb`, `tiny_path_is_not_a_stall` (the search returned 0 below 1e-300, so a path of 1e-300 stalled), `huge_path_ends` (`limit / fraction` overflowed to infinity and the halving
  never ended: stopped by the test's 20 s timeout), `piece_end_before_path_end` (both distances round to 2^54, the step ended at the path's end past the piece's), `hmax_bounds_the_stored_step`,
  `series_index_is_checked`, `tablejets_rejects_a_repeated_entry`, `tablejets_names_an_order_beyond_nb`. C3 got its control (`c3_fires`: a wrong count, a moved start, no record) and a missing
  record is now a violation. **Two of the new tests had wrong inputs of mine**: `huge_path_ends` used a constant series where the function is 1 + x (1e6 steps at x = 5.6e4), and the first
  `hmax` fix skipped the adjustment when the rounded endpoint equalled the stop's coordinate (the test caught it).
- Not changed: `TableJets::jets` clamping `kj` to `nb` (it would integrate a different system without saying so); it stops with a message.
- **Runs of record, second set** (module bc78792, tests 60d21ab): `run_06` default (25 passed), `run_07` mutate (31), `run_08` portable,mutate (31), `run_09` fmt, clippy (three feature sets), doc; the 28 digest
  lines of `run_06` equal `run_01`'s (`cmp`): no table changed. `run_01` to `run_05` stay as the runs of the first commits.

**A4 (2026-11-27, stage 3: the crate on the library). Written before the first stage 3 run; no bar below is changed after a run.** The coordinator's word for stage 3 came with
multishoot 5.0.0 released (crates.io; it holds #70's plane and #73's implicit module, takes multidouble 6.1.0 and multisolver 0.3.0) and #188 and #196 merged into main.

Setup. Worktree `~/Source/negative-mass-i192`, `wip/i192-taylor-tables`, fast-forwarded from 0d1d376 to main 54a6679 (nothing of mine was committed). The crate
`phase2/nonradial/taylor_polar/`. **Old pin** = multidouble ba0ad10 and multishoot a880903 (both git, `[patch.crates-io]`), multisolver 0.2.2: the tree as it is at 54a6679, built by
`s3_build.sh old old_default | old_libplane lib_plane | old_complex complex` (`dev_25` to `dev_27`, `--locked`, binaries in `target/bins/`). **New pin** = `multishoot = "=5.0.0"`, `multidouble = "6.1.0"`
from crates.io, no `[patch]`. The library's table, for the flag, is the pull request multishoot#79 at 60d21ab as a renamed optional git dependency (`multishoot_tables`); the flag waits for
a release that contains it. Python `~/Source/negative-mass/.venv/bin/python`. At most 2 processes, nice 10; a run not finished in 2 h is stopped by its PID and reported.

*Repin, the feature `lib_table` off*

- **RP1, the builds.** `cargo build --release --locked -j 2` succeeds with the new pin for the default build, `--features lib_plane` and `--features complex`, and `cargo tree --locked -e normal`
  of the default features shows no `git+` source and no `[patch]` is left in `Cargo.toml`. Every source change the repin forces is listed in the note, with the compiler's reason.
- **RP2, the records, bitwise.** For each pair (old, new) of default, `lib_plane` and `complex` binaries, `s3_records.py` runs the same commands and compares **every field of every record as a string**
  except the wall times: `star`; `d` at l = 2, 6 in f64, dd, qd (taylor_polar.py's R1 list, 17 records, D printed to 130 digits) and one od record; `planted` const and linear in f64, dd, qd; `starsteps`;
  `jtable` for l = 2 and l = 6 (J0 and J1, every entry, every step, 20 digits); `recipcheck` in f64, dd, qd, od; `tabcheck`; `jjets`; and for the complex build `dc` and `cp1`. **Met when 0 records differ in each
  pair.** A difference is a finding, not a failure of the repin: it is reported with the records and fields, the largest relative difference, and the cause if found (multidouble 6's reciprocals, #193 and
  multidouble#188, are the first candidate; `recipcheck` and the od/qd lanes show it).
  *Control:* the same comparison with `mutate=jsign` (and, on the complex pair, the same) passed to the new binary only must report differing records (exit 1).
- **RP3, the checks.** `taylor_polar.py` with the old and with the new binaries, each in its own copy of `phase2/nonradial` (the script's binary path is fixed), compared by `s3_compare.py` (every token of every
  non-`#` line as a string; only wall times and the load average are not compared; the count of replaced tokens is printed): the default mode (22 checks, TS skipped), `--rows` (l = 2, 4, 5, 6, default build),
  `--rows` with the `lib_plane` binaries (#189's plane rows), and `--complex` with the runner's references (`--ref-dir`, `--bins`). **Met when every check gives the same verdict and 0 tokens differ.** Tokens that
  differ are listed with their lines and classified by cause; the verdicts alone equal is not enough to call it met (a printed digit that moved is a difference of the integrator's bits).
  *Control:* the comparison of the new default-mode log with a log of the same binary under `--mutate=moncrief` (a check's printed numbers change) must report mismatches (exit 1).

*J's table from multishoot, the feature `lib_table` on*

- **JT1, the builds.** `--features lib_table`, `lib_table,lib_plane` and `lib_table,complex` build. The feature touches only `table.rs`'s `build_table` (DD in, DD out); `JTable`, its lookups (`jets`,
  `taylor_shift` in the crate's lane) and `to_lane` are the crate's own.
- **JT2, the step list.** The library is called with `nb` 30 (`NS`), `tail` 1e-25, **`last` 2 passed explicitly** (the library's default is 4), `fraction` 0.3, no `hmax` and no `atol`; the source's `valid_to` is the end
  of the star step; the path is [max(first star step's x0, 0.999 rmin), x1 of the last star step with x0 <= rmax]. `s3_steps.py` compares `jtable` of the default build (#186's own `build_table`) and of the `lib_table` build for
  l = 2, 3, 4, 5, 6 over [5e-4, 34.7] and l = 2 over [1.5e-3, 24.6]. **Met when, in every case, the number of steps is equal and every x0 and x1 is within 1e-9 relative of #186's** (the bar of the library's C3);
  reported (no bar): how many breakpoints are bitwise equal, the largest relative difference, and how many steps have equal coefficient strings. The step list is expected to equal #186's apart from the
  removed `h < 1e-14 b` jump; if that jump fired on these inputs the lists differ and the difference is reported with its steps.
  *Control:* `--mutate=lib_last4` (the library called with `last` 4, an option of the crate's `build_table` under the feature) must change the number of steps (exit 1 of `s3_steps.py`).
- **JT3, the checks.** The default mode on the `lib_table` binary gives the same verdicts as the default build (22 passed, 0 failed, 1 skipped, TS); `--rows` for l = 2, 4, 5, 6 gives RA2, RA4, RA5, RA6 (every
  token of the stored files as a string) and every other `--rows` check as on the default build. The tokens of the two logs are compared by `s3_compare.py`: **reported, not a bar**, since a step list that differs at the
  ulp level moves D by the table's rounding only (the stored-file tokens are the bar).
- **JT4, `wide_table` still fires.** `--mutate=wide_table` (declared targets T3 and A2) fails T3 and A2 on the `lib_table` binary as on the default build, and the step count under it is that of the star's steps
  (the library's `TableControl::Wide`, feature `mutate` of the library, on in this build).
- **JT5.** The head record of `jtable` (pattern, `nb`, `linear_defect`) is equal in the two builds; the table build time (`t_table`) is reported for both.
- **Findings carried from the design (section 9, items 1 and 2), stated in the note and not fixed in the crate's `table.rs`**: #186's `x1 = st.x1` jump for `h < 1e-14 b` (whether it fired on these inputs is
  answered by JT2) and `width_of`'s unscaled f64 products (at nb 30 and x >= 5e-4 they do not underflow; JT2 shows it).

Run files of this stage: `dev_25`+ (`devrun.sh`) and `run_10`+ (`runrec.sh`); `s3_build.sh`, `s3_compare.py`, `s3_records.py`, `s3_steps.py` are written before the first run and kept as they were.

**A5 (2026-11-27, during the RP2 runs).** `run_10_s3_records_default` (the first RP2 run, default pair) was stopped by its PID (exit 1, the log kept) after 33 minutes: the one octo-double `d` record of A4 (`d lane=od l=2 gammas=1.0`)
had used 28 CPU-minutes on the old binary alone and did not finish, so the pair would have passed the 2 h stop rule and held back every record after it. The six f64, dd and qd `d` commands before it were equal (old and new, 17 records
`d f64 l=2 .. d qd l=6`, 14 s to 38 s each). **The od `d` record is dropped from RP2** (`s3_records.py` now takes it only with `--od`; no data motivated this, the run time did): the octo-double lane is compared through
`recipcheck od` (the reciprocals, the candidate cause of any multidouble 6 difference) and `tabcheck`/`jtable` (DD), not through a determinant. The bar of RP2 is unchanged for the records that remain. Reruns are `run_11` (default),
`run_12` (lib_plane), `run_13` (complex), `run_22` (the `jsign` control), numbered by hand (`s3_run.sh`) because `runrec.sh` would take 15, which the check chains use.

**A6 (2026-11-27, the run trees).** `run_14_s3_old_default_mode` (old pin, default mode) was stopped by its PID at about 35 minutes (rc file written by hand: 143; its log is kept): the scratch copy of the script's
directory held only `phase2/nonradial`, and `background.py` puts `phase2/` on the path, so S1, S2 and S3 failed with `ModuleNotFoundError: No module named 'boson_star'`: a harness fault, not a verdict (the other 16 checks
that had run passed). The trees are now `git archive HEAD phase2` (the crate's sources left out), one per pin (`old`, `new`), each with its own `taylor_polar/target/{release,complex/release,bins}`; S1 on the old tree passes
(29 s). **The chains are renumbered**: old pin `run_23` default mode, `run_25` rows, `run_27` rows with the lib_plane binaries, `run_29` complex; new pin `run_24`, `run_26`, `run_28`, `run_30`. The first scratch trees are
kept as `trees_nophase2_unused` outside the repository and are not used.

**A7 (2026-11-27, the record runs again).** `run_11_s3_records_default` ended with exit 1 at its last command: `jjets` prints one JSON object over several lines and `s3_records.py` read it line by line (a harness fault; `run_11`'s log is kept).
Every command before it, old binary against new, was equal as strings: `d` f64, dd, qd at l = 2 and 6 (22 records), `planted` const and linear in f64, dd, qd (42 records), `starsteps` (164), `jtable` l = 2 and l = 6 (465 records each, every
coefficient of J0 and J1 at 20 digits), `recipcheck` in f64, dd, qd, od, and `tabcheck`. `run_12_s3_records_libplane`, started by the same chain, was stopped by its PID after one minute (rc 143 written by hand) so that it would not hit the same fault.
`s3_records.py` now reads `jjets` whole. The record runs are `run_31` (default), `run_32` (lib_plane), `run_33` (complex), `run_34` (the `jsign` control, must exit 1).

**A8 (2026-11-27).** `run_31_s3_records_default` (RP2, default pair): **1167 records, 0 differ** (old pin against new pin, every field as strings except times). In `run_23_s3_old_default_mode` the check **R1 reads FAIL
`raised RuntimeError: ... old_libplane d lane=dd l=2 ... exited -15`: that was my own `kill`** (a pattern for the stopped records run's children also matched R1's child process in the old tree); no check result changed. R1 is rerun alone on the old tree
as `run_35_s3_old_R1` (the same two pins are compared there, since the check reads `target/bins`), and the comparison of the default-mode logs takes R1's line from it. The other checks of `run_23` are untouched.
