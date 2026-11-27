#!/bin/bash
# The coordinator's rerun of #217: check, analyze over the runner's runs, one job of record. One process, nice 10.
R=$HOME/Source/negative-mass-raw/I217-mac-review
cd $HOME/Source/negative-mass-r217/notes/black_universe || exit 2
PY=$HOME/Source/negative-mass/.venv/bin/python
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
[ -e $R/rerun_check.log ] || { nice -n 10 $PY evolve.py check > $R/rerun_check.log 2>&1; echo "rc=$?" >> $R/rerun_check.log; }
[ -e $R/rerun_analyze.log ] || { nice -n 10 $PY evolve.py analyze --raw=$HOME/Source/negative-mass-raw/I217-mac/runs > $R/rerun_analyze.log 2>&1; echo "rc=$?" >> $R/rerun_analyze.log; }
mkdir -p $R/rerun_job
[ -e $R/rerun_job/job.log ] || { /usr/bin/time -l nice -n 10 $PY evolve.py job --c=-1.5 --h=0.005 --out=$R/rerun_job/c-1.5_h0.005 > $R/rerun_job/job.log 2> $R/rerun_job/job.err; echo "rc=$?" >> $R/rerun_job/job.log; }
echo "rerun done $(date -u +%FT%TZ)" > $R/rerun_done
