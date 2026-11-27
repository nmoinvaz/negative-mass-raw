# I202-rpi5: logs of TS13 Table I read against growth.csv and the crate

Machine: rpi5-ubuntu (4 cores, 8 GB, aarch64, Python 3.14 venv `negative-mass-venv314`). Issue:
https://github.com/nmoinvaz/negative-mass/issues/202. Code: branch `wip/i202-ts13-digits` of negative-mass, script
`notes/wormhole_largeD/ts13_digits.py`. Runner: `negative-mass-rpi5-i202`, started by the coordinator over hc.

## What is being checked

Torii and Shinkai 2013 (TS13, arXiv:1309.2058, PRD 88, 064027), Table I, the unstable mode's growth rate at D = 4 … 11.
For each D: the value as printed, its conversion to this repository's W²a², growth.csv's value, and #195's qd value in
`w2_output.txt`. Where growth.csv has digits beyond the printed ones, the source from `git log -p`.

## Plan, written before the reading

- The arXiv text is downloaded to this folder (`ts13_arxiv.pdf`, `ts13_arxiv.txt`) and read as data. No code from it runs.
- The table is copied by eye from the page image and from the text layer, and the two are compared; the copy is
  `ts13_table_I.txt`. If the journal version cannot be fetched, only the arXiv version is recorded, and that is said.
- The conversion to W²a² is stated from TS13's own definitions and checked on one row against the crate's value.
- `ts13_digits.py` holds the printed values as strings. Its check fails on a mistyped digit; `--mutate=` changes one digit.
- Pass criteria: every printed value agrees with the crate to its last printed digit (± half a unit) or the row is
  reported as a discrepancy. A mismatch is reported, not loosened.

## Files

(filled in as the run proceeds)
