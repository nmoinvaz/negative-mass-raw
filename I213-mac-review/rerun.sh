#!/bin/bash
# The coordinator's rerun of #213: the analysis over the runner's stored runs, then one job of record (D = 4 tuned, h = 0.02, X = 200).
R=$HOME/Source/negative-mass-raw/I213-mac-review
cd $HOME/Source/negative-mass-r213/notes/wormhole_evolution || exit 2
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
PY=$HOME/Source/negative-mass/.venv/bin/python
[ -e $R/rerun_analyze.log ] || { /usr/bin/time -l nice -n 10 $PY expansion.py analyze --raw=$HOME/Source/negative-mass-raw/I213-dh610 > $R/rerun_analyze.log 2> $R/rerun_analyze.err; echo "rc=$?" >> $R/rerun_analyze.log; }
mkdir -p $R/rerun
[ -e $R/rerun/job.log ] || { /usr/bin/time -l nice -n 10 $PY expansion.py job --kind=Sp --D=4 --h=0.02 --X=200 --out=$R/rerun > $R/rerun/job.log 2> $R/rerun/job.err; echo "rc=$?" >> $R/rerun/job.log; }
echo "rerun done $(date -u +%FT%TZ)" >> $R/rerun/job.log
