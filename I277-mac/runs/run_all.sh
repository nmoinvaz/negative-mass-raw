#!/bin/bash
# runs of record of #277: lane A and lane B, one process each, nice 10; from notes/black_universe of the worktree at commit 4ee1c6b
export NUMBA_NUM_THREADS=1
R=~/Source/negative-mass-raw/I277-mac/runs
PY=~/Source/negative-mass/.venv/bin/python
lane() {
  for m in "$@"; do
    if [ "$m" = none ]; then arg=""; else arg="--mutate=$m"; fi
    nice -n 10 $PY planted_family.py check $arg --out=$R > $R/check_$m.log 2> $R/check_$m.err
    echo $? > $R/check_$m.rc
  done
}
cd ~/Source/negative-mass-i277/notes/black_universe
lane none beta_sign kh kf rate gauge_frozen &
lane th_coef vterm_sign vterm_coef Vp_sign V_sign_f eps_sign vfit_K &
wait
echo done > $R/done
