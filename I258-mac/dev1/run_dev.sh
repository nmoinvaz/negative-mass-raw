#!/bin/sh
cd /Users/nathan/Source/negative-mass-i258/notes/black_universe
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
OUT=/private/tmp/claude-501/-Users-nathan-Source-negative-mass-i258/a3b4ef3d-a62a-4fe4-92ef-57bcaec9c565/scratchpad/dev1
nice -n 10 $PY full_slice.py check > $OUT/ref.log 2> $OUT/ref.err; echo $? > $OUT/ref.rc
for m in H_P H_eps M_phi M_F fn_aT fn_sign l1_sign l1_noquad dm_noT mass_off odd_off asym_S left_mass kg_eps; do
  nice -n 10 $PY full_slice.py check --mutate=$m > $OUT/$m.log 2> $OUT/$m.err; echo $? > $OUT/$m.rc
done
echo done > $OUT/ALL_DONE
