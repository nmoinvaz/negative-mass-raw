#!/bin/sh
# development runs of the declared mutations of cminus1_mode.py check (one process, nice 10)
cd "$(dirname "$0")"
for m in eq_P cf_R2 cf_k cf_xsign inf_P beta_g1 s_g1 s_kappa dwdc_K pslq_plant j_sign j_g1; do
  nice -n 10 ~/Source/negative-mass/.venv/bin/python ~/Source/negative-mass-i262/notes/black_universe/cminus1_mode.py check --mutate=$m > dev15_check_$m.log 2> dev15_check_$m.err
  echo "$m rc=$?" >> dev15_loop.rc
done
echo done >> dev15_loop.rc
