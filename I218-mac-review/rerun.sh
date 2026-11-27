#!/bin/bash
# The coordinator's partial rerun of #218, one process, nice 10.
R=$HOME/Source/negative-mass-raw/I218-mac-review
cd $HOME/Source/negative-mass-r218/notes/black_universe || exit 2
PY=$HOME/Source/negative-mass/.venv/bin/python
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
mkdir -p $R/rerun
run() { tag=$1; shift; [ -e $R/rerun/$tag.log ] && return; /usr/bin/time -l nice -n 10 $PY "$@" > $R/rerun/$tag.log 2> $R/rerun/$tag.err; echo "rc=$?" >> $R/rerun/$tag.log; }
run derive_check polar_derive.py check
run planted polar.py planted
run count_2_-0.3 polar.py count 2 -0.3 --res=R2 --out=$R/rerun/polar_2_-0.3_R2.json
run mads_0.5 polar.py mads 0.5 --res=R2 --out=$R/rerun/mads_0.5_R2.json
echo "rerun done $(date -u +%FT%TZ)" > $R/rerun/done
