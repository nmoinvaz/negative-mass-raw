# I253-mac-review: the coordinator's review of #253 (family G's settled black-hole mass)

Machine: the coordinator's Mac (Apple M5, macOS), nice 10, one process. Issue: https://github.com/nmoinvaz/negative-mass/issues/253.
Branch `wip/i253-g-settled-mass` at 9579bcf (worktree `negative-mass-r253`, detached), raw `I253-rpi5` at a31d31d. Python
`~/Source/negative-mass/.venv/bin/python`.

## Criteria, written before any run

- **R1.** `settled_mass_g.py analyze --raw=<raw>/I253-rpi5/runs` gives the 19 verdicts of `analyze_record.log`: 17 pass, RC7 and RNR fail.
  Pass: the same verdict set and the same numbers.
- **R2.** The jobs h = 0.005 at δ = 1e-8 and δ = 1e-6, rerun here with the stored p*ₕ. Pass: each settled M_AH at the limit equals
  rpi5's to 5e-5. #41's machine-to-machine difference was 1.6e-5 to 2e-5.
- **R3.** The δ dependence, the issue's new finding. Pass: on this machine M(1e-8) − M(1e-6) has rpi5's sign and lies within
  [0.8, 1.25] times rpi5's value. A physical dependence survives a change of machine; a roundoff artefact of the size of R2's
  difference would not.
- **R4, a reading, not a pass/fail check.** δ = 1e-12 lies below #40's roundoff floor of p*ₕ at D = 4 (series jitter below
  |p − p*ₕ| ≈ 1e-11, `threshold.md`, "Roundoff floor"). The scan's value there is compared with that floor, and its weight in the
  "rises at 1e-12" statement is judged.

No independent code: the coordinator's own march (`ind41`, I41-mac-review) is the symmetric half domain and cannot run the
one-sided family G, and a uniform grid cannot reach the settled value (#41's review).

## Results

| check | result | verdict |
|---|---|---|
| R1 | first run (`rerun_analyze.log`) passed `--raw=…/runs`, the coordinator's slip; every job load failed. Second run (`rerun_analyze_2.log`, `--raw=…/I253-rpi5`): the 19 verdicts and numbers of `analyze_record.log`, except TRK's roundoff-level 2.8e-14 against 2.3e-14 (bar 1e-12) | pass |
| R2 | h = 0.005: plateau 0.23554817 against 0.23554835 (δ = 1e-8, −1.9e-7); 0.23498116 against 0.23498196 (δ = 1e-6, −8.1e-7) | pass (bar 5e-5) |
| R3 | M(1e-8) − M(1e-6): +5.6701e-4 here, +5.6639e-4 on rpi5, ratio 1.0011 | pass |
| R4 | δ = 1e-12 is at #40's roundoff floor; its h = 0.01 and 0.005 values agree to 4.1e-5 (1.4e-5 at larger δ). The rise per decade grows smoothly from 1e-6 (2.2e-4) to 1e-11 (5.5e-4), so the trend does not rest on the 1e-12 point | reading |

`compare_jobs.txt` has R2 and R3; the job logs and series are in `runs/` and `job_*.log`.
