#!/bin/bash
# The coordinator's rerun of #41: analyze over the runner's stored runs, then one job (h = 0.01, delta = 1e-6) with the runner's p*_h files.
R=$HOME/Source/negative-mass-raw/I41-mac-review
cd $HOME/Source/negative-mass-r41/notes/wormhole_evolution || exit 2
PY=$HOME/Source/negative-mass/.venv/bin/python
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
[ -e $R/rerun_analyze.log ] || { nice -n 10 $PY settled_mass.py analyze --raw=$HOME/Source/negative-mass-raw/I41-rpi5 > $R/rerun_analyze.log 2>&1; echo "rc=$?" >> $R/rerun_analyze.log; }
mkdir -p $R/rerun_job/h0.01_d1e-06
[ -e $R/rerun_job/h0.01_d1e-06/job.log ] || { nice -n 10 $PY settled_mass.py job --h=0.01 --delta=1e-6 --out=$R/rerun_job/h0.01_d1e-06 --pstar=$HOME/Source/negative-mass-raw/I41-rpi5/runs > $R/rerun_job/h0.01_d1e-06/job.log 2>&1; echo "rc=$?" >> $R/rerun_job/h0.01_d1e-06/job.log; }
echo "rerun done $(date -u +%FT%TZ)" > $R/rerun_done
