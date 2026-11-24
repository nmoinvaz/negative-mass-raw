# I96-rpi5: numbers of #96's sigma R = 8 and 16 sector runs that no log prints (recount from eig/*.npz, memwatch, P = 320 vs 340)

Machine: rpi5-ubuntu (Raspberry Pi 5, aarch64, 4 cores, shared with choptuik-large-d), one process, nice 10, one thread.
Issue: https://github.com/nmoinvaz/negative-mass/issues/96
Worktree: `~/Source/negative-mass-i96`, branch `wip/i96-thin` (base a43dd10). Python: `~/Source/negative-mass-venv314/bin/python`.

Nothing of #96's runs is recomputed. `sector_numbers.py` reads the eigenvalue arrays that the runs wrote (`eig/*.npz`), the
sector logs and dh610's `memwatch.log`, and prints what the note's section 7 quotes and no log prints. Inputs, read in
place from the sibling folders of this clone:

- `../I96-win/sectors-s8.log` and `../I96-win/eig/tanh_sigma8_m*.npz` (sigma R = 8, P = 200, N = 160),
- `../I96-dh610/sectors-s16-p340.log` and `../I96-dh610/eig/tanh_sigma16_m*.npz` (sigma R = 16, P = 340, N = 320),
- `../I96-win/eig/tanh_sigma16_m0.5.npz` (the pilot, sigma R = 16, m = 1/2, P = 320, N = 320),
- `../I96-dh610/memwatch.log`.

Run from this folder: `python -X utf8 sector_numbers.py` (add `--mutate=cut`, `--mutate=real` or `--mutate=ab` for the
controls). It writes to stdout; `sector_numbers_output.txt` is that output, `controls_output.txt` the three mutated runs.

## Checks, written before the first run

R1. Recount. From each sector's npz the script recomputes the columns that the sector logs print: the leading |mu| v_c of A
    and B, "stable to 1e-5 above" (`match_stable`), the eigenvalues in the window (A / B), the real ones in it, the real
    ones with |mu| v_c > 1e-8 (A / B), the largest of them and how many B reproduces (`persisting`). The three helpers
    are copied from `tanh_spectrum.py` (lines 531, 613, 625) with their tolerances. Pass: every value equals the log's, at
    the digits the log prints, in all 22 sectors. Fail: any value differs; the script exits 1 and names it.
R2. A and B. |rho_A - rho_B| < 1e-6 rho for the leading eigenvalue of every sector, the issue's criterion, at each sigma R.
    Exit 1 if it fails. The per-sector differences are printed.
R3. P = 320 against P = 340, sigma R = 16, m = 1/2: the leading |mu| v_c of A and of B, their absolute and relative
    differences. Data, no threshold.
R4. dh610's memory: the largest rss (the sum over tanh_spectrum.py processes, once a minute) and the lowest MemAvailable.
    Report only; nothing stops over memory.

Controls (each must make R1 or R2 fail):

- `--mutate=cut`: `match_stable` tolerance 1e-3 instead of 1e-5, so the windows and their counts move; R1 must fail.
- `--mutate=real`: the real-eigenvalue tolerance 1e-3 instead of 1e-9, so the real counts move; R1 must fail.
- `--mutate=ab`: B's eigenvalues times (1 + 2e-6); R2 must fail.

## Run

`nice -n 10 ~/Source/negative-mass-venv314/bin/python -X utf8 sector_numbers.py > sector_numbers_output.txt` (Python 3.14.10,
numpy 2.5.4, scipy 1.18.1; 0.9 s; exit 1, because R1 fails at sigma R = 8, below). `controls_output.txt` has the three mutated
runs (`--mutate=cut`, `real`, `ab`), each with exit 1 and the failures listed. `reals_check_s8_output.txt` and
`reals_check_s16_output.txt` are `../I96-win/reals_check.py 8 ../I96-win/eig` and `reals_check.py 16 ../I96-dh610/eig`
(that script takes the eig folder as its second argument), both exit 0. `sector_numbers_stderr.txt` is empty.

## Results

| check | sigma R = 8 (P = 200) | sigma R = 16 (P = 340) |
|---|---|---|
| R1 recount of the logs' columns | **FAIL**: 3 of 132 values differ, in m = 7/2 and 15/2 | pass, 132 of 132 |
| R1b the differences vanish without the cut's own eigenvalues | pass, both sectors | pass, nothing to explain |
| R2 largest relative \|A - B\| of a sector's leading \|mu\| v_c | 6.5e-10 (m = 21/2); rho: 1.4e-11 absolute | 5.3e-9 (m = 21/2); rho: 1.5e-10 absolute |

R1 at sigma R = 8. The log's window of A holds 24 eigenvalues at m = 7/2 and 16 at m = 15/2, the recount 26 and 18, and the
log's symmetry value at m = 15/2 is 3.4e-11, the recount 5.5e-11. R1 was not loosened and the script exits 1. Cause, tested
on the stored arrays: in both sectors the two eigenvalues that define the window's cut (z and its conjugate, whose |mu| v_c
is the cut) are excluded by the log and included by the recount, and with `|mu| > cut` in place of `>=` the recount
reproduces the log's 24, 16 and 3.4e-11 exactly (R1b). The script takes the cut as `abs(z)` of one numpy scalar and the
window as `np.abs(array) >= cut`; on this machine those two differ in the last bit for 309,576 of the 825,000 stored
eigenvalues (the sign at each sector's cut is in the output), so a tie of the cut's own eigenvalue is decided by rounding, and
the win laptop's rounding put it below the cut in those two sectors. That last step is inferred from the log and was not
run on win. No real eigenvalue enters or leaves a window (the real-in-window columns agree in all 22 sectors), the cuts agree
to four digits, and the note's window and real-eigenvalue conclusions do not change. The windows of sigma R = 8 hold 254 (A)
and 284 (B) eigenvalues together by the log, 258 and 284 by the recount.

R3 (sigma R = 16, m = 1/2): the leading |mu| v_c of A is 0.225083300746 at P = 320 (the pilot, I96-win) and 0.225083300767 at
P = 340 (+2.1e-11, relative 9.1e-11); of B 0.225083300303 (P = 330) and 0.225083300620 (P = 350) (+3.2e-10, relative 1.4e-9).

R4: 1631 samples from 2026-11-21T21:37:09-08:00 to 2026-11-23T00:48:27-08:00 (the file's UTC-8). Largest rss 28.67 GiB (sum
over the processes whose command line holds tanh_spectrum.py), lowest MemAvailable 19.34 GiB. The logs' own per-sector peak of
the worker is 28.39 to 28.40 GiB. Report only.

Controls. `cut` fires R1 and R1b at both sigma R, `real` fires R1 at both (36 and 33 values differ), `ab` fires R2 at both
(2.0e-6 against 1e-6). The first `real` control (real tolerance 1e-3) was inert: real eigenvalues have Im = 0 exactly and the
smallest nonzero |Im|/|mu| is 0.066 (sigma R = 8, m = 1/2) and 0.080 (sigma R = 16), so no count moved. It was replaced by 0.5
before the runs above. R1b was added after R1 failed on the data (it is not one of the checks written first).

`reals_check`: at sigma R = 16 the real eigenvalues with |mu| v_c > 1e-8 and those with |mu| > 1e-8 (the identity check's
floor, in the script's unscaled mu) are the same in all 11 sectors (74 to 76), because v_c = 0.985 < 1; at sigma R = 8
(v_c = 1.56) they differ by 1 to 6 per sector (87 against 88 at m = 1/2).
