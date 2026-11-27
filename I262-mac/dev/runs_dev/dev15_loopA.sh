#!/bin/sh
# first worker, continued: waits for the running cf_R2 process (pid 32391), then the next five
cd "$(dirname "$0")"
while kill -0 32391 2>/dev/null; do sleep 5; done
echo "cf_R2 finished" >> dev15_loop.rc
for m in cf_k cf_xsign inf_P beta_g1 s_g1; do
  nice -n 10 ~/Source/negative-mass/.venv/bin/python ~/Source/negative-mass-i262/notes/black_universe/cminus1_mode.py check --mutate=$m > dev15_check_$m.log 2> dev15_check_$m.err
  echo "$m rc=$?" >> dev15_loop.rc
done
echo doneA >> dev15_loop.rc
