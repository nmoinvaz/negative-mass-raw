#!/bin/sh
# runs of record of notes/black_universe/full_slice.py at 4f31b3f; nice 10, one process at a time; never overwrites a log
cd /Users/nathan/Source/negative-mass-i258/notes/black_universe
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
OUT=/Users/nathan/Source/negative-mass-raw/I258-mac/runs
nice -n 10 $PY full_slice.py check > $OUT/check.log 2> $OUT/check.err; echo $? > $OUT/check.rc
nice -n 10 $PY full_slice.py table > $OUT/table.log 2> $OUT/table.err; echo $? > $OUT/table.rc
for m in H_P H_eps M_phi M_F fn_aT fn_sign l1_sign l1_noquad dm_noT mass_off odd_off asym_S left_mass kg_eps; do
  nice -n 10 $PY full_slice.py check --mutate=$m > $OUT/mut_$m.log 2> $OUT/mut_$m.err; echo $? > $OUT/mut_$m.rc
done
echo done > $OUT/ALL_DONE
