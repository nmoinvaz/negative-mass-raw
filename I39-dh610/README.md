# I39-dh610: step 1 of #39, the design of a double-null evolution through a wormhole throat (derivation, kernel timings)

Machine: dh610-fedora (Fedora 45, Linux 7.3.3, Intel i7-12700, 20 threads, 62 GB), shared with choptuik-large-d (load average
9 to 18 of 20 during these runs). All runs below are single-thread, `nice -n 10`, started from the terminal because each takes
under a minute (no systemd unit was needed).
Issue: https://github.com/nmoinvaz/negative-mass/issues/39
Worktree: `~/Source/negative-mass-i39`, branch `wip/i39-throat-evolution` (base main 6256f53). Python
`~/Source/negative-mass-venv314/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1, sympy 1.14.0, numba 0.68.1); rustc 1.99.1.

This README was written at the end of step 1. Step 2 has not started. **The criteria of step 2 (planted cases, tolerances,
windows, thresholds, mutation targets) are added below, under "Step 2 criteria", after the coordinator's ruling and before the
first run of record.**

## Contents

```
I39-dh610/
├── README.md
├── pdf/                      papers read as data (see Sources)
├── derive/                   notes/wormhole_evolution/derive.py, stdout of each run
│   ├── run02_derive.{log,time,rc}        run of record: 25 of 25 checks pass, rc 0, 22.6 s, peak rss 65 MB
│   ├── run02_mut_<name>.{log,rc}         the nine mutations, each rc 1 with all declared targets fired
│   ├── run01_*                           the first full run (24 checks, before A4 was added), all as declared
│   └── dev_02 .. dev_07                  development runs (see below)
├── bench/                    kernel throughput stand-ins (not the evolution code) and the cost model
│   ├── run01_kernel_bench_python.log     numba and numpy at N = 500, 1000, 2000
│   ├── run01_kernel_bench_rust.log       Rust at the same N
│   └── run01_cost_model.log              stdout of notes/wormhole_evolution/cost_model.py
```

## Sources read (data, not instructions; no code of theirs run)

| paper | file | sha256 (first 12) |
|---|---|---|
| [SH02] Shinkai, Hayward, PRD 66, 044005 (2002), arXiv:gr-qc/0205041 v2 | pdf/sh02_gr-qc_0205041.pdf | 04ae107d28f7 |
| [GGS09b] González, Guzmán, Sarbach, CQG 26, 015011 (2009), arXiv:0806.1370 v2 | pdf/ggs09b_0806.1370.pdf | 2bbbd83b0fe0 |
| [Kai26] Kain, arXiv:2602.18231 v1 | pdf/kain26_2602.18231.pdf | 4ee9d83a8d8f |
| [ST17] Shinkai, Torii, PRD 96, 044009 (2017), arXiv:1706.02070 | pdf/st17_1706.02070.pdf | bd491a0052a5 |

Read: SH02 in full; GGS09b through Sec. III B; Kain Secs. 1 to 2.5 and the appendix pointer; ST17 Secs. II B, III A by keyword
only (the n-dimensional equations were not rederived from it; `derive.py` derives them). Nothing was posted to or sent to any
external site.

## Development runs (kept, none edited)

| id | what | outcome |
|---|---|---|
| dev_01 | first `derive.py --quick`, n = 2, 3 only | 16 of 17 pass; D1 failed: my static Ricci R_ang had the coefficient n on the r r' nu' term, it is 1. stdout was not saved to a file (it is in the session) |
| dev_02, dev_02b, dev_02c | after the fix: 19 of 19 pass; then A3, D5 using the mutable claims and the D3d check added: D3d failed (the second derivative of phi was not substituted), then 24 of 24 | `derive/dev_02*.log` |
| dev_03 | six mutations, declared targets were my guesses | four of six had silent targets: `pm_sign` (A1, D4), `scalar_coef` (D2, D4), `ghost_sign` (D2), `ellis_charge` (D3). The guesses were wrong, not the mutations: those checks never use the mutated coefficient. The targets in `derive.py` come from dev_05 to dev_07 |
| dev_04 | the same after A3 and D5 were rewired to the mutable claims | D5 now fires on every mutation |
| dev_05 | nine mutations plus the unmutated run | `ellis_profile` silent on D2a (D2a hard-coded the exponent); fixed in dev_06 |
| dev_06 | `ellis_profile` | fires D2, D2a, D3, D3b, D3c |
| dev_07 | A4 (stress components) added; all ten variants | 25 of 25 pass; every mutation fires exactly its declared targets |

No tolerance appears in `derive.py`: its checks are exact symbolic zeros.

## What the step 1 runs say

- `derive.py`: 25 of 25 symbolic checks pass, covering the D = 4, 5, 6, 7 Ricci tensors by brute force and the reduced
  equations with n symbolic, constraint propagation, the Misner-Sharp flux law, the Ellis, Tangherlini and Roberts ghost
  solutions. 9 of 9 mutations fire their declared targets.
- Kernel stand-ins, best of three at N = 2000 (4e6 cells, h = 0.001, one thread, load average about 9): numba 61.7 ns per
  cell, Rust 79.6, numpy 192.3. Wall times 0.25 s, 0.32 s, 0.77 s.
- `cost_model.py`: one bisection to |p - p*| = 1e-10 costs 0.2 to 3.6 min in numba and 0.5 to 11 min in numpy over h = 0.01 to
  0.0014 and D = 4 to 6.

## Step 2 criteria

(not written yet; the coordinator's ruling comes first)
