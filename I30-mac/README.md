# I30-mac: ghost-sector winding counts at D = 10, 12 and 20.04, and the other parity sector's zero refined on Im μ = ω

Machine: macOS 27.0.1, Apple M5 (10 cores, 32 GB), the coordinator's Mac, shared with other sessions. Issue:
https://github.com/nmoinvaz/negative-mass/issues/30. Branch `wip/i30-ghost-counts` (worktree `~/Source/negative-mass-i30`,
cut at a3578f4). Written 2026-11-26 before the first run of record. Stop condition: a single count still running after
3 h of wall time is stopped and reported with what it had. Memory is reported only; nothing is stopped over it.

Everything here follows notes/wormhole_next.md §1.3 and §6. The three states are counted as step 2 counted D = 5–7 and
D = 52–67: boxes B0, U0 and full, from just right of the real-axis zero to Re μ ≈ 6.2–6.7, |Im μ| < 1.5ω, each with a
planted pair inside B0.

## Environment (choptuik-large-d, read-only)

| item | value |
|---|---|
| CLD checkout | `~/Source/choptuik-large-d`, branch main, `git log -1`: `5fcadda2 Delta tables: the form-S direct solve at D 50000 (#1088)` |
| `git status --short hp` | empty (no uncommitted change in hp/) at 2026-11-26 08:40 |
| Python | CLD's `.venv`, 3.13.15; hpkernel 0.1.0, numpy 2.5.4, mpmath 1.3.0 |
| kernel | `hp/modecount_cx/build/modecount_cx.cpython-313-darwin.so`, built Nov 8 14:06, sha1 `3b1a9a22…c8a75d5` |
| scripts | `hp/modecount_test.py` (Oct 27), `hp/modecount_test_axis.py` (Oct 26), `hp/modecount_common.py` (Nov 9, with the series gate of #265/#270), `hp/modecount_wind.py` |

The kernel is **not** the build of §1.3 and §6 (the 2026-10-25 `.so`, hpkernel of 2026-10-28), and `modecount_common.py`
now carries #441's series gate, which step 2 did not run under. Two kinds of control compare this environment with step
2's: the real-axis zeros re-found here against the stored ones (E1), and the on-line zeros at D = 16.76 and 20.04
re-found against §6.2's (C5). The launcher logs CLD's commit, `git status --short hp` and the kernel's sha1 before every
job, so a change under a running queue shows in the logs.

Shared with CLD, so not independent of it: the states, the hpkernel/`modecount_cx` determinant `test_det`, and the
boxes' sampler (`modecount_wind.count`). The planted pair tests the winding code and the box geometry, not the
determinant. No independent determinant exists here (CLD #646 is open).

## States and the gate

#441's gate (both series pass SERIES_TAIL at the start and at the solution) is not waived. `setup()` passed on all
three on 2026-11-26 (read-only, 1 thread):

| state | D | M | K | ω | \|F\| | series tail, centre (ratio at x) | series tail, horizon (ratio at u) | sha1 |
|---|---|---|---|---|---|---|---|---|
| `up_D10.0000.npz` | 10 | 48 | 10 | 2.492260 | 6.5e-31 | 2.2e-71 (0.094 at 0.02) | 7.7e-43 (0.385 at 0.3) | `7bcfbff9…` |
| `up_D12.0000.npz` | 12 | 48 | 10 | 2.629841 | 8.1e-31 | 1.2e-71 (0.087 at 0.02) | 1.1e-44 (0.371 at 0.3) | `a7954aeb…` |
| `up2_D20.0437.npz` | 20.043653 | 32 | 8 | 2.976205 | 1.9e-29 | 9.0e-56 (0.204 at 0.1) | 4.1e-53 (0.303 at 0.3) | `38611ecd…` |

All in `~/Source/choptuik-large-d/hp/data/states`. The control state of C5, `up2_D16.7600.npz` (M 32), has sha1
`dd12c232…`.

## Real-axis zeros and left edges

The real-axis zero μ is each state's least-damped real zero of det M_ψ, from notes/wormhole_next/ghost_mu.jsonl (§1.3,
`ghost_mu.py`, tags below). No record is missing. E1 re-finds each in this environment (`ghost_mu.py`, window below).

| D | tag in ghost_mu.jsonl | μ (stored) | E1 window (h) |
|---|---|---|---|
| 10 | D10_M48_m1 | −0.6761242034294794 | −0.76 … −0.60 (0.04) |
| 12 | D12_M48_m1 | −0.7345316442034706 | −0.82 … −0.66 (0.04) |
| 20.04 | D20.04_M32_m1 | −0.8743130935432717 | −0.96 … −0.80 (0.04) |

aLL is `pick_edges.py`'s (the rule of step 2: in (μ + 0.02, μ + 0.08), farthest from the real parts of the candidate
poles with |Im| < 4.5ω), run on 2026-11-26 on the stored μ and before any count:

| D | aLL | right of μ | nearest pole real part | y1 = ω/2 | y2 = 1.5ω |
|---|---|---|---|---|---|
| 10 | −0.5961 | 0.0800 | −0.7616 (0.1655 away) | 1.246130 | 3.738390 |
| 12 | −0.7145 | 0.0200 | −0.6314 (0.0832 away) | 1.314920 | 3.944761 |
| 20.04 | −0.7943 | 0.0800 | −1.0415 (0.2472 away) | 1.488102 | 4.464307 |

aL and aR are CLD's defaults (`far(0.08, 0.3, …)`, `far(6.0, 6.7, …)`), a1 and a2 are not used.

## Boxes

With `--boxes=B0,U0,full` (the same boxes as step 2's D 5–7, 52, 60 and 67):

| box | region | expected zeros inside |
|---|---|---|
| B0 | aLL < Re < aL, \|Im\| < ω/2 | μ = 0 (divided out) |
| U0 | aLL < Re < aL, ω/2 < Im < 1.5ω | none |
| full | aL < Re < aR, \|Im\| < 1.5ω | none |

Sampling is CLD's default: h0 0.4, tol π/4, alias rule π/2, hmin 1e-4, `--resolve=any`. A box is resolved when every
step is ≤ π/4, every interval meets the alias rule and no verification half mismatched.

## Planted pairs

One pair (μ_p, μ̄_p) per D, inside B0 and away from every edge by at least 0.14 (both planted runs share the plain
run's evaluation cache):

| D | planted pair | distance to aLL | distance to the box's Im edges |
|---|---|---|---|
| 10 | −0.45 ± 0.6i | 0.146 | 0.646 |
| 12 | −0.55 ± 0.7i | 0.165 | 0.615 |
| 20.04 | −0.65 ± 0.8i | 0.144 | 0.688 |

## The other parity sector

The line Im μ = ω, `modecount_test_axis.py STATE --s=1`. §6.2's scan, `--lo=-1.6 --hi=-0.02 --h=0.05`
(notes/wormhole_next/axis_s1.jsonl, 2026-11-06), found one phase jump at D = 10 and 12, in (−1.05, −1.00), and a
refinement that ended at (−1.2936263734, Im/ω 0.999583) at D = 10 and (−1.3247896060, 0.999684) at D = 12. Both points
lie 0.3 from the interval and off the line.

**Hypothesis, stated before the runs.** Those points are not zeros. Their ln|g| (−991.89 at D = 10, −1101.14 at
D = 12) equals the line's smooth trend, interpolated from the neighbouring samples at the same Re (−991.89 and
−1101.14), where a zero would sit tens of units below. The script refines with `mpmath.findroot(solver="secant",
tol=1e-24, maxsteps=40, verify=False)` from the pair (cell midpoint, cell midpoint + 0.25h + 0.001i) on
g = exp(ln g − ref). The secant is free in the complex plane (the 0.001i offset), ln|g| rises with slope ≈ 110 per unit
Re, and with `verify=False` it returns its 40th iterate unchecked. §6.2's zeros run from −0.9969 (D = 8.25) to −1.0033
(D = 16.76), so at D = 10 and 12 the zero probably lies near the right end of the cell, up to 0.025 from the start. The
converged cases started 0.0197 or less from their zeros. The hypothesis is that the start was too far.

**Procedure (the script and the state unchanged, only the grid is finer, so the secant starts nearer):**

| rung | command (from `hp/`) | role |
|---|---|---|
| 0 | `modecount_test_axis.py STATE --s=1 --lo=-1.05 --hi=-1.00 --h=0.05` | the old start (cell (−1.05, −1.00), the same secant pair) at D = 10, 12 |
| 1 | `… --lo=-1.05 --hi=-1.00 --h=0.005` | the record: a 0.005 cell, start within 0.0025 |
| 2 | `… --lo=-1.05 --hi=-1.00 --h=0.002` | only if a rung-1 zero fails C4 (below); rung 1's failure is reported as a failure |
| c | `… --lo=-1.04 --hi=-1.00 --h=0.005` | the controls at D = 16.76 (`up2_D16.7600.npz`) and 20.04 |

Rung 0 is a control, not a record: C4's test must fire on it if it reproduces §6.2. If it does not fire (the old start
now works), that is reported as silent.

## Criteria (each coded as worded in `step3_table.py`; each can fail)

| id | criterion |
|---|---|
| E1 | each real-axis zero re-found here equals the stored one to 1e-9. A miss stops the work and is reported (aLL may no longer lie right of the zero) |
| C1 | every plain box (B0, U0, full) at each D is resolved and has winding of g equal to 0 |
| C2 | the planted run at each D is resolved, its B0 winding is the plain B0 winding + 2, and U0 and full equal their plain values; the pair lies inside B0 |
| C3 | §6.2's scans at D = 10 and 12 (axis_s1.jsonl) show exactly one phase jump, in (−1.05, −1.00), below the real-axis zero |
| C4 | at D = 10 and 12 the rung-1 record (a) has exactly one phase jump, in one 0.005 cell inside (−1.05, −1.00); (b) its refined zero has \|Im/ω − 1\| < 1e-5; (c) the zero's Re lies in that cell; (d) ln\|g\| at the zero is at least 10 below the lower of the cell's two end samples, so it is a zero and not an unconverged iterate |
| C5 | at D = 16.76 and 20.04 the control meets C4's (a)–(d) in its window (−1.04, −1.00) and its Re agrees with §6.2's (−1.0033192791907342, −1.0026635066001466) to 1e-8 |
| X1 | informative, no pass condition: rung 0 at D = 10 and 12, and whether C4's tests fire on it |

The on-line threshold 1e-5 is step2_table.py's. A failed criterion is reported as not met, not reworded.

## Mutations of `step3_table.py` (`--mutate=NAME`, and `--selftest` for all)

Each must make the table exit 1 with exactly its target failing.

| mutation | change | target |
|---|---|---|
| `mu` | the stored real-axis zeros shifted by 1e-6 (row added at 16:50 UTC, after the queues started and before any table was run) | E1 |
| `winding` | one plain box winding +1 | C1 |
| `noplant` | a planted record replaced by its plain one | C2 |
| `realzero` | the real-axis zero in C3 set to −1.2 (below the jump) | C3 |
| `offline` | rung-1 zero's Im shifted by 1e-3 ω | C4 |
| `trend` | rung-1 zero's ln\|g\| set to the trend | C4 |
| `old` | the rung-1 record replaced by §6.2's | C4 |
| `ctrl` | the control's reference shifted by 1e-6 | C5 |

## Jobs

`notes/wormhole_next/step3.sh` (queues A and B), two jobs at once, `--threads=2`, nice 10, `caffeinate -is`, each job
under `gtimeout 10800`. A job whose log ends in `exit 0` is skipped on restart; `modecount_test.py` reuses
`counts/*_raw.jsonl`. Logs are in `logs/`, never overwritten: a rerun gets a number suffix.

| queue | jobs in order |
|---|---|
| A | mu_D10, cnt_D10, cnt_D10_plant, mu_D20.04, cnt_D20.04, cnt_D20.04_plant |
| B | mu_D12, cnt_D12, cnt_D12_plant, ax0_D10, ax0_D12, ax_D10, ax_D12, axc_D16.76, axc_D20.04 |

Files: `counts/` (modecount_test_results.jsonl, `*_raw.jsonl` caches, `*_evals.jsonl`), `ghost_mu3.jsonl` (E1),
`axis_s1.jsonl` (rungs and controls), `logs/`, `step3_table.log` (the final table).

## Runs

Launched 2026-11-26 16:45 UTC by `nohup caffeinate -is bash notes/wormhole_next/step3.sh A` and `… B` (PIDs in
`logs/pids.txt`), at 2 threads each. The effective nice was 15, not 10: the launching shell was at nice 5, then
`nice -n 10`. All 15 jobs exited 0, the last at 17:01 UTC (16 min of wall time; no job was stopped, rerun or restarted).
Every job log records one environment line: CLD `5fcadda2`, `git status --short hp` empty, kernel sha1 `3b1a9a221956`. At
the end CLD was at the same commit with `hp/` clean and the same kernel.

| job | exit | UTC | note |
|---|---|---|---|
| E1: `D10_M48_m1_i30`, `D12_M48_m1_i30`, `D20.04_M32_m1_i30` | 0 | 16:46, 16:46, 16:53 | 16 evaluations each; zeros equal the stored ones to 1.4e-13, 5.9e-13, 1.8e-12 |
| `cnt_D10`, `cnt_D10_plant` | 0, 0 | 16:51, 16:52 | 84 determinants (plain), 108 with the planted run |
| `cnt_D12`, `cnt_D12_plant` | 0, 0 | 16:51, 16:53 | 92, 117 |
| `cnt_D20.04`, `cnt_D20.04_plant` | 0, 0 | 16:54, 16:55 | 92, 112 |
| `ax0_D10`, `ax0_D12` (rung 0) | 0, 0 | 16:56, 16:58 | the secant ends at (−1.2928, Im/ω − 1 = −4.1e-4) and (−1.3250, −3.2e-4) |
| `ax_D10`, `ax_D12` (rung 1) | 0, 0 | 16:59, 17:00 | zeros −1.0016613614 and −1.0033895309, both on the line |
| `axc_D16.76`, `axc_D20.04` | 0, 0 | 17:01, 17:01 | −1.0033192792 and −1.0026635066, equal to §6.2's |

Rung 2 was not needed and was not run (`step3.sh R2`). Results: `step3_table.log` (15 checks, all PASS, exit 0) and
`step3_selftest.log` (every mutation fails exactly its target, exit 0), both from `python3 step3_table.py [--selftest]`
run in `notes/wormhole_next/` of the worktree. Counts are in `counts/modecount_test_results.jsonl`, the lines in
`axis_s1.jsonl`, E1 in `ghost_mu3.jsonl`.

**Differences from what this README predicted.**
- Rung 0 does not reproduce §6.2's two points bit for bit, only to 8e-4 in Re and 5e-6 in Im/ω (D = 10), 2e-4 and 5e-7
  (D = 12). The README said it would if the secant is deterministic, but the script multiplies out only the poles within
  `lo − 2 < Re p < hi + 2` of the window, so the narrower window changes g and with it the secant's path. The behaviour is
  the same: both runs leave the line by 3–4e-4 ω and land 0.3 to the left of the cell. §6.2's points have ln|g| on the
  line's own trend (0.002 and 0.004 off, from its full scan); a rung-0 record samples only the cell, so that is not
  computed for rung 0. X1 is informative and has no pass condition; its "reproduces to 1e-6" label reads "does not reproduce", and the
  differences are printed beside it.
- The `mu` mutation row was added to the table above after the queues started and before any table was run.
