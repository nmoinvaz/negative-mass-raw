# I216-mac: conical_global on released multishoot 5.0.0, then `implicit_lib` as its only path, against #190's baseline

Machine: the coordinator's Mac (Apple M5, 10 cores, macOS, arm64 NEON, shared with other agents, load average about 30 at the start).
Issue: https://github.com/nmoinvaz/negative-mass/issues/216

Written before the first run of any script. Amendments, if any, are listed at the end with their reason; nothing above them is
edited.

## Where

| what | where |
|---|---|
| worktree (the crate) | `~/Source/negative-mass-i216`, branch `wip/i216-conical-release` from main 1b44c49, crate `notes/warp/conical_global/` |
| build outputs | `~/Source/negative-mass-i216-target/<arm>` (`off1`, `on1` for step 1; `single` for step 2), copied to the crate's `target/release` by `sys/arm.sh` before a run, with their sha256 (`arm_<job>.sha256`) |
| raw | this folder: `run_NN_<what>.log` (stdout), `.err` (stderr), `.rc` (exit code), `.time` (`/usr/bin/time -l`); every rerun numbered, none overwritten |
| toolchain | rustc 1.94.0, cargo 1.94.0, clippy 0.1.94, Python 3.14.7 (`~/Source/negative-mass/.venv`) |
| libraries before | multishoot at git rev eaf55a8 (#73's PR commit), multisolver =0.2.2, multidouble =5.1.0 |
| libraries after | multishoot =5.0.0, multisolver =0.3.0, multidouble =6.1.0, all from crates.io |
| budget | at most 2 processes (`cargo -j 2`, `RAYON_NUM_THREADS=2`), `nice -n 10`, one job at a time; a job not finished in 2 h of wall time is stopped (rc 124) and reported |

## The work

1. **Step 1, repin, both paths kept.** `Cargo.toml` takes the three released versions, with no git pin; the code changes are the
   ones the new API forces (`Scalar::is_finite`, `Stop::NotFormed`, ...). Two arms are built from the same tree: `off`
   (default features: `poly.rs`'s and `hp.rs`'s own recursion and walk) and `on` (`--features implicit_lib`:
   `poly_lib.rs`, `hp_lib.rs` on `multishoot::implicit`). Each arm runs #190's three scripts.
2. **Step 2, one path.** The own recursion and walk of `poly.rs` and `hp.rs` are deleted (what other modules use stays), the
   feature is removed, and the three scripts run again on the one build.

## Criteria (each can fail)

| id | criterion |
|---|---|
| C1 | `conical_global.py` (checks and controls), `conical_loglog.py` (checks and controls) and `conical_offgrid.py --grid=ctl --no-controls --dump=DIR`, then `conical_offgrid.py --grid=ctl --controls-only --controls=n-drift,recip-dd`, exit 0 with the same pass count and every control fired on its target only, as in #190's baseline runs (17 of 17 checks and the controls of `conical_global.py`, 20 of 20 and 17 of 17 of `conical_loglog.py`, 16 of 16 of the `ctl` grid) |
| C2 | `sys/compare_outputs.py` (the comparator of #190, unchanged) finds no gated difference between each run and #190's baseline: in the logs every label, count, class, kind and eta* equal as printed after the comparator's normalization; in the `ctl` dump every class, kind, stop, tiny_kind, through, converged equal and every `xstar` equal in 10 significant digits |
| C3 | `Cargo.toml` names released versions and no git pin: `multishoot`, `multisolver`, `multidouble` with `=x.y.z` and no `git`, `path` or absolute path |
| C4 | `cargo clippy` on the crate (all targets, `-D warnings`) is clean, with the feature off and on in step 1 and on the one build in step 2 |

A difference in any eta*, class or kind is reported as not met, with its line, and the cause is not guessed. No criterion is
loosened after a run. Numbers that measure an error (a residual, a difference, a bar) are not compared as strings: the
comparator replaces every number in scientific notation with an exponent of -6 or smaller by a token, and each is held to its
own check's bar. Step counts, timings and error sizes that differ are listed (by `sys/compare_run.py`), not gated. Step 1 is
reported before step 2 starts.

## The baseline (#190, `I190-rpi5`, raw repository commit 63f0f279; feature off, multishoot 4.2.0, multisolver 0.2.2, multidouble 5.1.0, on the Raspberry Pi 5, aarch64 NEON)

| script and arguments | baseline log | baseline dump or controls | sha256 of the log |
|---|---|---|---|
| `conical_global.py` | `run_11_base_global.log` | `ctl_base_global/` (controls) | db56a7f10f9076bd... |
| `conical_loglog.py` | `run_09_base_loglog.log` | `ctl_base_loglog/` (controls) | 56d1e0d8b619b68... |
| `conical_offgrid.py --grid=ctl --no-controls --dump=DIR` | `run_06_base_offgrid_ctl.log` | `dump_base_ctl/` (79 files) | 83a5816afa0962d... |
| `conical_offgrid.py --grid=ctl --controls-only --controls=n-drift,recip-dd` | `run_33_base_offgrid_ctrl.log` | `ctl_base_offgrid/` | 9d2e8f33232a9e4... |

The Pi's baseline came from the feature-off binary of #183's code. This Mac is another operating system and libm on the same
instruction set: the Mac review of #190 (`I190-mac-review`) found the feature-on crate equal to this baseline in all 537 eta*
(largest relative difference 2.45e-15) and every class and kind.

## The comparator

`sys/compare_outputs.py` is #190's file, copied unchanged (sha256 341f60b737719ab2366664e5299b3dfc84d99a0ee7c2e5b68e98f4b584c0fa6f,
from `I190-rpi5/sys/compare_outputs.py`). Its rules are in its docstring. It is run through `sys/compare_run.py`, which imports it
unchanged (same normalization, same gate, same exit code) and adds only the listing of what the comparator does not gate (the
error-sized numbers and step counts of lines that differ), and one pairing:

- logs: `compare_run.py BASE_LOG RUN_LOG` for global, loglog and the controls run; with `BASE_DUMP RUN_DUMP` for the `ctl` run.
  `/usr/bin/time` writes to `NAME.time`, and the log has stdout only, so the log has no timing wrapper lines.
- one dump file is named by a hash of its command line, `ntable --file <absolute path>/notes/warp/conical_global/target/...`, so it
  has another name in another checkout. `compare_run.py` pairs each file of the run that the base lacks with the base file whose first
  line is equal after the absolute prefix before `notes/warp/` is replaced, prints the pairing, and compares the pair's records.
  On #190's own data (the Mac review's dump against the Pi's baseline) it pairs one file and reproduces the review's 537 eta*
  equal, largest relative difference 2.45e-15.

**The comparator can fail** (`sys/compare_selftest.py`, `selftest_01.log`): on copies of the baseline, a changed last printed
digit of an eta*, a changed class, a removed line, an eta* changed at its 10th digit, a kind and a class of a dump record each
make it exit 1 (6 of 6 mutations fire); an unchanged copy passes, and an error-sized number, an eta* changed beyond the
10th digit and a step count do not make it fire (by its rules). All 11 as expected.

## Run protocol

- `sys/build_arm.sh NAME ARM [args]`: `cargo build --release -j 2` of the worktree's crate into `~/Source/negative-mass-i216-target/ARM`.
- `sys/run_queue.sh JOBS`: one job per line `name|command`, detached with `nohup`. A job's command is
  `sys/arm.sh ARM name && cd ~/Source/negative-mass-i216 && <python> notes/warp/<script>.py ... --nobuild`.
- The scripts' own build line (`cargo build --release -j 2` in the crate, default features) is not run (`--nobuild`), so each
  arm runs the binaries built here. The scripts are not edited.
- The first run of `conical_offgrid.py` builds the series pickle `target/series_k17.pkl` (2 to 6 min); its log line is skipped by
  the comparator, as in #190.
- Timings are reported with the load at the start, 2 threads, nice 10.

## Development log and amendments

Nothing above this heading has been edited.

### S1 Step 1 (repin, both paths kept): runs 01 to 10, commit 8e081f1 of `wip/i216-conical-release`

Code changes forced by the new API (`git show 8e081f1`): `Cargo.toml` takes `multishoot =5.0.0`, `multisolver =0.3.0`, `multidouble
=6.1.0` (no git pin); `hp_lib.rs` implements `Scalar::is_finite` for the walker's scalar `W<P>` (the leading part is finite, as the
library's own `Fl<T, 1>` does) and names `Stop::NotFormed` as impossible after a successful `form` (`unreachable!`), where before a
wildcard arm would have read it as `NonFinite`. Nothing else: `poly.rs`, `hp.rs`, `poly_lib.rs`, the other modules and the three
scripts are unchanged. The `off` arm built with no change (`run_01_build_off`; two warnings of `main.rs` that were there before). The
first build of the `on` arm failed with E0046, `Scalar::is_finite` missing (`run_02_build_on_failed1`, kept); `run_02_build_on` is
the build after the change. Both arms were built from the tree of 8e081f1 (the `off` build before the edit of `hp_lib.rs`, which that
arm does not compile). The binaries' sha256 are in `arm_run_*.sha256`.

Result: C1 met and C2 met in every run, with the comparator unchanged. No eta*, class or kind differs from #190's baseline in any run.

| run | exit | checks | controls | gated differences (lines, eta*, class, kind) | error-sized numbers differing as printed | wall (s) | max RSS (MB) | load at start |
|---|---|---|---|---|---|---|---|---|
| run_03_off_offgrid_ctl | 0 | 16 passed, 0 failed | - | 0 in the log; 0 of 537 eta* differ, largest relative difference 0.00e+00 | 0 of 77 | 505 | 100 | 37.42 39.49 33.78 |
| run_04_on_offgrid_ctl | 0 | 16 passed, 0 failed | - | 0 in the log; 0 of 537 eta* differ, largest relative difference 2.45e-15 | 5 of 77 | 102 | 76 | 33.01 33.47 33.37 |
| run_05_off_offgrid_ctrl | 0 | - | 2 fired; all fired on target only | 0 in the log | 0 of 0 | 531 | 80 | 19.63 29.22 31.76 |
| run_06_on_offgrid_ctrl | 0 | - | 2 fired; all fired on target only | 0 in the log | 0 of 0 | 209 | 79 | 5.81 11.59 21.29 |
| run_07_off_loglog | 0 | 20 passed, 0 failed | 17 fired; all fired on target only | 0 in the log | 16 of 490 | 585 | 105 | 5.31 8.40 17.82 |
| run_08_on_loglog | 0 | 20 passed, 0 failed | 17 fired; all fired on target only | 0 in the log | 206 of 490 | 524 | 105 | 6.66 6.92 12.28 |
| run_09_off_global | 0 | 17 passed, 0 failed | 13 fired; all fired on target only | 0 in the log | 0 of 95 | 1403 | 188 | 12.91 9.08 10.60 |
| run_10_on_global | 0 | 17 passed, 0 failed | 13 fired; all fired on target only | 0 in the log | 4 of 95 | 1528 | 187 | 16.72 19.33 18.39 |

- The `ctl` dump: 79 files, 685 records, 2300 string fields (class, kind, stop, tiny_kind, through, converged) equal, 537 eta*
  compared. With the feature off every eta* equals the baseline's bit for bit (largest relative difference 0); with it on the largest
  relative difference is 2.45e-15, the number #190 found on the Pi and the Mac review reproduced. The records whose step count differs
  (listed, not gated): 0 off, 10 on (`cmp_run_03_vs_baseline.txt`, `cmp_run_04_vs_baseline.txt`).
- Each control's own log and exit code: 13 of `conical_global.py`, 17 of `conical_loglog.py`, 2 of `conical_offgrid.py` equal the
  baseline's with the comparator, in both arms (`cmp_ctl_dirs_step1.txt`).
- The same-machine comparison of the two arms (`cmp_run_10_vs_run_09.txt`, `cmp_run_08_vs_run_07.txt`): no gated difference.
- Error-sized numbers that differ as printed (listed, not gated; each is held to its own check's bar, and every check passes):

| run | differing of all error-sized numbers | in the checks |
|---|---|---|
| `run_04_on_offgrid_ctl` | 5 of 77 | `plant_167` 4, `recip_check` 1 (the numbers #190's on arm also gave, line for line) |
| `run_07_off_loglog` | 16 of 490 | `approach` 15, `plant_shift` 1 |
| `run_08_on_loglog` | 206 of 490 | `approach` 188, `plant_167` 4, `plant_loglog` 3, `plant_limit` 3, `n_floor` 2, `plant_scale` 2, `invariants`, `dd_qd`, `plant_shift`, `recip_check` 1 each |
| `run_10_on_global` | 4 of 95 | `plant_cubic` 4 |
| `run_03`, `run_05`, `run_06`, `run_09` | 0 | |

  The differing numbers are residuals at the double-double floor (for example `approach`, rho at eta = 1e9 and 1e12 in
  `run_07`: 1.9e-29 against 3.4e-30). Multidouble 6's reciprocals are a candidate cause in the `off` arm, whose code is
  unchanged; this was not isolated (multishoot 5.0.0 does not build against multidouble 5.1.0).
- Not run: `+avx2,+fma`, other machines, `conical_offgrid.py` without `--grid=ctl`.
