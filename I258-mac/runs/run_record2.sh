#!/bin/sh
# run 2 at 7b7805c: the check, the table and the new mutation; never overwrites a log
cd /Users/nathan/Source/negative-mass-i258/notes/black_universe
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
OUT=/Users/nathan/Source/negative-mass-raw/I258-mac/runs
nice -n 10 $PY full_slice.py check > $OUT/check.2.log 2> $OUT/check.2.err; echo $? > $OUT/check.2.rc
nice -n 10 $PY full_slice.py table > $OUT/table.2.log 2> $OUT/table.2.err; echo $? > $OUT/table.2.rc
nice -n 10 $PY full_slice.py check --mutate=mode_M > $OUT/mut_mode_M.log 2> $OUT/mut_mode_M.err; echo $? > $OUT/mut_mode_M.rc
echo done > $OUT/ALL_DONE2
