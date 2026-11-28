#!/bin/sh
# second development worker: the last five mutations of dev15_loop.sh in reverse (one process, nice 10)
cd "$(dirname "$0")"
for m in j_g1 j_sign pslq_plant dwdc_K s_kappa; do
  nice -n 10 ~/Source/negative-mass/.venv/bin/python ~/Source/negative-mass-i262/notes/black_universe/cminus1_mode.py check --mutate=$m > dev15_check_$m.log 2> dev15_check_$m.err
  echo "$m rc=$?" >> dev15_loop.rc
done
echo doneB >> dev15_loop.rc
