# I188-mac: the Taylor crate over complex s for the polar box counts (negative-mass #188): design, development runs, runs of record

Machine: mac, the coordinator's Mac (Apple M5, 10 cores, 32 GB, macOS), shared with other sessions; runner negative-mass-mac-i188
(Claude Code, account claude-me2). Issue: https://github.com/nmoinvaz/negative-mass/issues/188
Code: worktree `~/Source/negative-mass-i188`, branch `wip/i188-complex-s` from main 0d1d376, pushed by
`git push origin HEAD:refs/heads/wip/i188-complex-s`; the runs of record are at 8b8bb4d (`run_00_env.log` has the binaries' hashes).
Library clone `~/Source/negative-mass-i188-libs/multishoot` (main f929163), branch `feat/complex-plane` (stage 3).
Python `~/Source/negative-mass/.venv/bin/python` 3.14.7, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0; rustc 1.94.0. At most two processes, nice 10.

`design.md` is the design of stage 1, approved by the coordinator with one added check (X1b). Its criteria are the criteria of the runs of
record, with the amendments below; every one was written before the first run of record. `dev_NN_*` are development runs (`devrun.sh`),
`run_NN_*` the runs of record (`runrec.sh`: log, `/usr/bin/time -l` in the `.err`, exit code in `.rc`); `runs.txt` orders them and
`assemble_output.py OUT` rebuilds `phase2/nonradial/taylor_complex_output.txt` from them.

## What was built (stage 2)

The crate `phase2/nonradial/taylor_polar/` gets the cargo feature `complex` (off by default, exclusive with `lib_plane`): `Cx<T>`
(`src/complex.rs`), `dc` and `dserve` (D at complex s, `src/cdrive.rs`), `cp1` and `czserve` (the planted systems, `src/cplanted.rs`).
Shared code changed: four trait defaults in `num.rs` (`conj`, `abs2`, `mag`, `re_f64`: the identity, `z * z`, `|x|`, `x` on the real lanes),
`gram_schmidt`'s two lines and one magnitude in `plane.rs`, nine magnitudes, one branch line and the split of `d_eval` into `d_eval` and
`d_eval_s` in `polar.rs`, the module lines in `main.rs`. `table.rs` is untouched. `taylor_polar.py --complex` runs the checks.

## Amendments to the design (each before the runs of record)

- **A1.** The crate's option for winding2's fixed R_s is `rsfix`, not `rs`: `rs` is the star's shooting start radius (`dev_22` and `dev_23`, the
  first versions of the stored-box comparison, ran with the star's start set to 404.85 and crashed; they are in `stale_dev/`).
- **A2.** **XR fails on real data.** The check as declared (the stripped D at four start radii agree to 1e-9 in modulus and phase) gives modulus 2.2e-16
  and phase 0.11 rad. The cause (`dev_xr_diag.py`, run as `run_19_xr_diag`): the phase carries tails of the exterior solution that winding2's
  strip does not remove, 1/R_s from the start vectors and the angular term and ln R_s from the mass, and both are holomorphic and zero-free at a fixed
  R_s. XR stays in the output, **not met**. The check that the counts need, **XRc** (b1 counted at rsmult 40 and 80, winding 0, planted pair 2),
  was added after the failure and passes. The control `strip_sign`, which I had given XR, now targets X1 (XR fails on the unmutated crate, so it cannot serve).
- **A3.** **L1C**, the lane check (qd against dd at three points of b1, bar 1e-20 as #186's L1), with the control `lowsum`, was added before its first run
  (the design said "f64, dd, qd at least" without a check for it).
- **A4.** W0 also reports the smallest distance of any quantity the counter compares with a threshold (0.4, 0.4, 0.1 rad) from it, on both boxes
  and with the plant: the coordinator's request (a stored phase error of 1e-6 cannot move a count unless this margin is under 1e-6).
- **A5.** The control `bilinear` first crashed (`ln` of a complex "norm", `dev_29`); under the mutation `ln` takes ln |z|, so that the control runs and
  its target reads a number. Its effect is the one in the table of the note: plane, orthonormality and the real part of the log-volume unchanged,
  the phase of the log-volume off by 2.27 rad.
- **A6.** The first launch of the runs of record (`failed_launch_1/`) ran every command with exit 127: zsh did not word-split `$TP` and `$C`. Kept, and
  rerun with the same numbers. `run_18_tc_big_Rs` was running when I stopped that queue and was stopped by its PID; its partial log is there too.
- **A7.** `dev_01`'s B12 column (the conjugate-free control) is wrong: the control's class attribute was shared with the Hermitian class; `dev_07` has the fixed
  control. `dev_08` was a third process started by mistake and stopped by its PID after 5 s (`notes_stopped.txt`).

## Files

| file | what |
|---|---|
| `design.md` | the design of stage 1 |
| `run_all.sh`, `runrec.sh`, `runs.txt`, `assemble_output.py` | the two queues of the runs of record (A, B; one process each), their recorder, the order and the assembler |
| `ref_chain.sh`, `ref/` | the scipy references: `scipy_b1_rtol1e-13.jsonl` (147 points, run_01), `scipy_b1_rtol1e-08.jsonl`, `scipy_b6_rtol1e-13.jsonl`, `scipy_b6_rtol1e-08.jsonl` (8 points each) |
| `jsonl_rec/` | the crate's evaluations of the runs of record (one JSON line each, D at lane precision), which a rerun resumes from; `jsonl/` and `jsonl_ctl/` those of the development runs |
| `tc_big_rs.py`, `dev_xr_diag.py` | the timing at large R_s and the diagnosis of XR |
| `probe_*.py`, `cxbench/`, `dev_01` ... `dev_16` | stage 1's probes (see below) |
| `dev_17` ... `dev_83` | stage 2 and 3 development runs: the first crate comparisons, the controls' effects before they were declared (`ctl_*`), the library's tests and clippy (`ms_*`) |
| `failed_launch_1/`, `stale_dev/`, `queueA.out`, `queueB.out` | the failed first launch (A6), stale development logs (A1), the queue outputs |

## Rerun

From `phase2/nonradial` of the checkout at 8b8bb4d, with this repository cloned beside it (`--raw=`, default `../../../negative-mass-raw`):
`python taylor_polar.py --complex --build`, the baselines in `taylor_polar/target/bins` (`old_default`, `old_libplane` from main 0d1d376 before any edit,
default and `--features lib_plane`; `new_default`, `new_libplane`; `new_complex` is `target/complex/release/taylor_polar`), then
`python taylor_polar.py --complex --ref-dir=<this folder>/ref [--only=X1] [--mutate=NAME]`; `--complex --list` names the checks and the controls.
The scipy references: `python taylor_polar.py --complex --scipy-ref-make=b1 --rtol=1e-13 --out=ref/scipy_b1_rtol1e-13.jsonl` (about 40 min, resumable).

## Files of stage 1 (probes)


| file | what |
|---|---|
| `design.md` | the design note posted on the issue for review |
| `probe_scipy.py`, `dev_01`, `dev_07` | winding2's D at stored points of the box: fresh rtol 1e-8 and 1e-12, Hermitian Gram–Schmidt in place of LAPACK's QR, and the conjugate-free control. `dev_01`'s B12 column is wrong (the control's class attribute was shared with the Hermitian class, so it equals H12); `dev_07` reruns three points with the fixed control |
| `probe_rtol.py`, `dev_14` | the scipy path at rtol 1e-8 … 1e-13 at three points (`dev_08` was this probe started as a third process by mistake, stopped by its PID after 5 s: `notes_stopped.txt`) |
| `probe_count.py`, `dev_09` … `dev_13` | winding2's counter ported to read a cache: the stored result, then its four mutations |
| `probe_mut_effects.py`, `dev_15` | the size of `strip_off`, `conj_s`, `rs_shift` on the stored points |
| `probe_qr_diag.py`, `dev_16` | LAPACK's complex QR has a real R diagonal |
| `dev_02` … `dev_04` | the real crate (main 0d1d376, built here) at the box's \|s\|: star data, dd and f64 times |
| `cxbench/`, `dev_05`, `dev_06` | the cost of a complex multiply-add against a real one (`dev_05`'s f64 line was optimized away: 0.0 ns; `dev_06` uses `black_box`) |

## Stage 3: the library pull request

multishoot pull request https://github.com/nmoinvaz/multishoot/pull/81 (branch `feat/complex-plane`, head 54d6fca after the review fixes; not merged, not published). The development runs are
`dev_71` to `dev_98`: the first build (`dev_71`, a borrow error), the tests (`dev_72`, `dev_73` with `mutate`, `dev_74` the existing plane tests with their digests,
`dev_75` portable), `cargo fmt` and clippy (`dev_76` to `dev_80`), the final tests after formatting on both backends (`dev_81`, `dev_82`), and the whole `cargo test --release`
on the default build (`dev_83`) and with `--features portable` (`dev_84`): all `test result: ok`; then CodeRabbit's four findings (`dev_85` to `dev_98`: the reciprocal and square root at 1e+-200, `ln_vol`'s docs, per-metric controls, tests, fmt and clippy again on both backends). The 16 digests are the same after the fixes. The 16 digests of `dev_81` and `dev_82` are equal; the real lanes'
P1, P2, P3 digests equal those in `../I189-mac/run_17*.log` (10 of 10).
