#!/bin/bash
# The review's rerun of #253: analysis of the stored runs, then the two h = 0.005 jobs (one process, nice 10).
WT=$HOME/Source/negative-mass-r253/notes/wormhole_evolution
RAW=$HOME/Source/negative-mass-raw/I253-rpi5
OUT=$HOME/Source/negative-mass-raw/I253-mac-review
PY=$HOME/Source/negative-mass/.venv/bin/python
cd "$WT" || exit 2
export NUMBA_NUM_THREADS=1
nice -n 10 $PY -u settled_mass_g.py analyze --raw=$RAW/runs > $OUT/rerun_analyze.log 2>&1; echo "analyze rc=$?" >> $OUT/rerun.rc
for d in 1e-08 1e-06; do
  mkdir -p $OUT/runs
  /usr/bin/time -l nice -n 10 $PY -u settled_mass_g.py job --h=0.005 --delta=$d --out=$OUT/runs/h0.005_d$d --pstar=$RAW/runs > $OUT/job_h0.005_d$d.log 2> $OUT/job_h0.005_d$d.err
  echo "job $d rc=$?" >> $OUT/rerun.rc
done
