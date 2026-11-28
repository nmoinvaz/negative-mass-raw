# I258-mac: design note and development probes for a compactly supported datum on a full slice of the c = −1 black universe (#258)

Machine: the coordinator's Mac (Apple M5, macOS, shared), runner `negative-mass-mac-i258`.
Issue: https://github.com/nmoinvaz/negative-mass/issues/258
Code of record (stage 2): `notes/black_universe/full_slice.py` on branch `wip/i258-full-slice` of nmoinvaz/negative-mass.

- `design.md`: the stage-1 design for review. Criteria, bars and mutations are declared there before any run of record.
- `probe/`: development probes (scratch scripts, not code of record), `probe/logs/` their logs (`pN.log`, `pN.err`, `pN.rc`).
  `probe/run_logs.sh` reruns the logged set, one process at a time at nice 10; `p23` was run by hand with its log.
  The probes import `horizon_sector.py` and `linear.py` read-only from `~/Source/negative-mass-i258/notes/black_universe`
  (main at 3b3358c) and run with `~/Source/negative-mass/.venv/bin/python`.
- Stage 2 will add `runs/` with the logs of record.

## Stage 2: criteria declared before the runs of record (2026-11-28)

Code `notes/black_universe/full_slice.py` at 4f31b3f (branch `wip/i258-full-slice`), `~/Source/negative-mass/.venv/bin/python`, nice 10, one process at a time.
The coordinator approved the design (comment on #258): strict compact reading, bars relative to c₂, the diamond E6 and X20 in, the three discrepancies
reported (no note text edited), O1 made a declared check, E9 (planted mode) optional.
Development run of the script (`dev1/`, before this section): reference 17 of 17, every mutation run once. Bars of the design are unchanged. Added since the design,
declared here: Q6, Q7, E9, and bars for O1; Q6 and Q7 were declared at 1e-5 and 1e-6 in the first draft and are tightened to 1e-7 and 1e-9 before any run of record
(development values 2.5e-9 and 1.9e-11).

Units: amplitude max|δφ| ≈ max|δφ_N| = 1e-3. Rich(h, h/2) = (4 c₂(h/2) − c₂(h))/3. h = 0.01, 0.005, 0.0025, 0.00125.

| id | check | bar |
|---|---|---|
| Q1 | slice ODEs reproduce exact pure-gauge δr, n (c = −1, −1.5, δF ≠ 0), relative | ≤ 1e-9 |
| Q2 | \|δm − ε/2\| on Schwarzschild scaling + gauge, s = 0.2, 1, 5, ε = 1e-3 | ≤ 1e-10 |
| Q3 | tails of datum G on 1.05 ≤ \|s\| ≤ 3e4: max \|δr\|, \|δr'\|, \|κ s n\| (right from the left start, left from the right start) | ≤ 1e-12 |
| Q4 | \|δm(s)\|, 10 ≤ \|s\| ≤ 3e4, both ends (δM_ADM) | ≤ 1e-12 |
| Q5 | \|c₂ left start − c₂ right start\|, \|c₁\| of both | ≤ 1e-12 |
| Q6 | Θ′ = μH: a′ = μQ and c′ = μE𝒱′r at s = 0.1 … 8, relative | ≤ 1e-7 |
| Q7 | Θ conserved on the homogeneous solutions, relative variation; \|Θ\| past the support at both ends | ≤ 1e-9; ≤ 1e-12 |
| E1 | planted evolution of exact pure gauge (c = −1, −1.5): error/scale at 8 fixed points at h = 0.00125; last Cauchy ratio | ≤ 3e-5; 4.0 ± 0.3 |
| E2 | c = −1.5: slice functional and Rich(0.005, 0.0025) fit against the known c₂ = −η(0)R′(ρ_h)G(ρ_h) (60-digit quadrature), relative; c = −1: \|c₂ fit\|/max\|δr\| at h = 0.0025 and last ratio | ≤ 1e-5 each; ≤ 1e-5, 4.0 ± 0.3 |
| E3 | G: horizon values linear in V, residual/max at h = 0.00125; last ratio | ≤ 1e-5; 4.0 ± 0.3 |
| E4 | G: c₂ of the slice against the evolved fit, relative, Rich(0.005, 0.0025) | ≤ 1e-6 |
| E5 | G: \|C_VV\|, \|C_UU\| of the evolved fields at 8 fixed points over the largest term, h = 0.0025; last ratio over h = 0.005, 0.0025, 0.00125 | ≤ 1e-3; 4.0 ± 0.3 |
| E6 | diamond \|s\| ≤ 0.5: c₂ (U = 0) and c₂′ (V = 0) fits against the slice, relative, Rich(0.005, 0.0025) | ≤ 1e-6 each |
| E7 | one-sided datum R: \|c₂ slice\|; \|c₂ fit\| at h = 0.00125; last ratio; max \|Y\| on \|s\| ≤ 0.5 | ≤ 1e-12; ≤ 1e-7; 4.0 ± 0.3; ≤ 1e-12 |
| O1 | two-sided datum, support 0.6 ≤ \|s\| ≤ 1.0: \|c₂ slice\|; fit against slice relative Rich(0.005, 0.0025); max \|Y\| on \|s\| ≤ 0.5; end vector | ≥ 1e-6; ≤ 1e-6; ≥ 1e-6; ≤ 1e-12 |
| E8 | X20: \|Rich(0.005, 0.0025) − slice\| absolute; min \|c₂\| | ≤ 1e-6; ≥ 1e-5 |
| E9 | planted exact growing mode Y = c₂VR on [0.3, 1.6] with M = 0: error of Y over its maximum at h = 0.00125; last ratio; max \|M\| of the data over the scale of M before the fix | ≤ 1e-5; 4.0 ± 0.3; ≤ 1e-9 |

Mutations (`check --mutate=NAME`). Every check is in scope; the declared fired set is the set of the development run, with the target check among them:

| name | declared fired set |
|---|---|
| H_P, H_eps | Q1 Q3 Q4 Q5 Q6 Q7 E3 E4 E5 E6 E7 E8 E9 O1 |
| M_phi | Q1 E3 E4 E5 E6 E7 E8 E9 O1 |
| M_F | Q1 Q3 E3 E4 E5 E6 E7 E8 E9 O1 |
| fn_aT, fn_sign | E2 E4 E6 E8 O1 |
| l1_sign | E1 E2 E4 E6 E8 E9 O1 |
| l1_noquad | E1 E2 E3 E4 E5 E6 E7 E8 E9 O1 |
| dm_noT | Q2 |
| mass_off | Q3 Q4 Q5 E3 E4 |
| odd_off | Q3 Q5 E3 E4 |
| asym_S | Q3 Q4 E3 E4 E6 |
| left_mass | Q3 Q4 Q5 Q7 E3 E4 |
| kg_eps | Q6 |
| mode_M | E9 (added at 7b7805c: E9's data with M left non-zero, declared from a development run: error 3.2e-2 at every h) |

Why the extra fires: an ODE mutation breaks the rank-1 end vector (Q3 to Q5); a datum with a tail is cut at s = 1.05 by the evolution (E3, E4); a data set with c₂ = 0
makes the relative errors of E4 and E6 degenerate. `full_slice.py mutations runs mut_` compares the stored logs with this table.

Runs of record: `runs/` (`check.log`, `mut_<name>.log`, `table.log`, `.rc`); a rerun gets a new number suffix and the old log stays.

Run 1 (`runs/check.log`, `table.log`, `mut_*.log` for the 14 mutations): code 4f31b3f. The code was then extended at 7b7805c by one mutation (`mode_M`), its declared
set and one `table` line (Θ at the left_mass datum against −c₁); the diff touches nothing else (`git diff 4f31b3f 7b7805c`). Run 2 at 7b7805c: `check.2.log`,
`table.2.log`, `mut_mode_M.log`. The 14 mutation logs of run 1 stay the logs of record for those mutations; `check.2.log` equals `check.log` apart from the time.
