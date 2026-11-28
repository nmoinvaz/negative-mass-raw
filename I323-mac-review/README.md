# I323-mac-review: the coordinator's review of #323 (the departure ε scanned for the 24 settled-mass members)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/323. Under review: branch `wip/i323-eps-scan`
(23ca1e5), raw `I323-mac` at c71d21ff.

Rerun: `rerun_analyze.txt` (`settled_mass_eps_scan.py analyze`, exit 1, 26 outcome checks fail as stored) equals the output of
record apart from the header.

`ind323.py` uses the coordinator's reader of `I317-mac-review/ind317.py` and imports nothing from the repository. At
ε = 1e-3, 2e-3, 5e-3 and 1e-2 it subtracts B = 0's reading at the same ε (V3), refits y = M/r_th − M₀ = aγ₁ + bγ₁² + cṙ_th
(M₀ = 0.223086) over the fifteen (#323's set, with δ = 1e-12) and over the fourteen (#317's set, without it), and predicts N1–N3,
X1–X3, Y1–Y3. Run from this folder: `python3 ind323.py OUTPUT [--mutate=no-sub|one-eps]`, OUTPUT = `settled_mass_eps_scan_output.txt`.

## Criteria (written 2026-11-28 before the first run)

- **K1.** Over the fifteen, X1–X3 at each ε are within 1e-5 of #323's REF-V3 row, and X2, X3 are beyond 6e-5 at every ε.
- **K2.** Over the fifteen, N1–N3 and Y1–Y3 are within 6e-5 at all four ε (#323's NOEXIT).
- **K3.** Over the fourteen at ε = 1e-2, X1–X3 are within 1e-5 of #317's +3.35e-5, +7.32e-5, +7.73e-5 (the two runners' procedures
  differ only in e12). The fourteen's X residuals at the other ε are reported.

## Mutations (each must fire the named check)

- `no-sub`: V3's subtraction dropped → K1.
- `one-eps`: every ε read at 1e-3 → K1.

## Run 1 (2026-11-28)

`ind323_run1.txt`: a parse error before any check (my regular expression read the note's markdown table, not the output's row
format). Fixed in the parser only; no criterion changed. Run 2 is the first run of the checks.

## Result (run 2)

3 of 3 pass; `no-sub` and `one-eps` fire. Reported, not gated: over the fourteen (no e12) X2 and X3 fall steadily with ε,
+1.77e-4, +1.31e-4, +9.67e-5, +7.35e-5 and +1.44e-4, +1.22e-4, +9.99e-5, +7.78e-5 at 1e-3, 2e-3, 5e-3, 1e-2, while over the
fifteen they are flat (+2.14e-4 … +1.03e-4 and +1.99e-4 … +1.68e-4). #323's "X's miss does not follow ε" holds for its fit set,
which includes e12 (the pair at the roundoff floor whose mean carries a first-order mode, #318). X2 and X3 stay beyond 6e-5 at
every ε under both sets.
