#!/bin/bash
# After both lanes: the code checks and their mutations, the analysis and its mutations, the naming runs, the response diagnostic. One process, nice 10.
export NUMBA_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=1
cd /Users/nathan/Source/negative-mass-i217/notes/black_universe
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
P=/Users/nathan/Source/negative-mass-raw/I217-mac
run() { name=$1; shift; if [ -e "$P/post/$name.log" ]; then echo "exists: $name" >&2; exit 2; fi
  nice -n 10 /usr/bin/time -l $PY evolve.py "$@" > "$P/post/$name.log" 2> "$P/post/$name.err"; echo "rc=$?" >> "$P/post/$name.log"; }
mkdir -p "$P/post" "$P/post/naming"
run run01_check check
for mu in th_coef vterm_sign vterm_coef Vp_sign V_sign_f numpy_pert time_unit pstar_off; do run mut_check_$mu check --mutate=$mu; done
run analysis analyze --raw=$P/runs
for mu in time_unit pstar_off; do run mut_analysis_$mu analyze --raw=$P/runs --mutate=$mu; done
for c in -0.3 -1.5 -1; do run naming_c$c name --c=$c --h=0.005 --raw=$P/runs --out=$P/post/naming; done
for c in -1.5 -1.01 -1 -0.99 -0.3; do run resp_c$c resp --c=$c --out=$P/post; done
echo done > "$P/post/post.done"
