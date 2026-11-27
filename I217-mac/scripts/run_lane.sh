#!/bin/bash
# Runs of record of #217, one lane (one process). Usage: run_lane.sh A|B. Thread budget: at most two lanes at once, nice 10, one thread each; 2 h stop per job.
# A log or a job directory that exists is never overwritten: the lane stops.
export NUMBA_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=1
cd /Users/nathan/Source/negative-mass-i217/notes/black_universe
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
R=/Users/nathan/Source/negative-mass-raw/I217-mac/runs
job() {                                      # job NAME ARGS...
  name=$1; shift
  if [ -e "$R/$name" ] || [ -e "$R/$name.log" ]; then echo "exists: $name" >&2; exit 2; fi
  nice -n 10 /usr/bin/time -l gtimeout 7200 $PY evolve.py job "$@" --out="$R/$name" > "$R/$name.log" 2> "$R/$name.err"
  echo "rc=$?" >> "$R/$name.log"
}
case $1 in
A)
  for h in 0.02 0.01 0.005 0.0025; do job c-1.5_h$h --c=-1.5 --h=$h; done
  for h in 0.01 0.005; do job O_c-1.5_h$h --c=-1.5 --h=$h --family=pulse; done ;;
B)
  for h in 0.02 0.01 0.005 0.0025; do job c-0.3_h$h --c=-0.3 --h=$h; done
  for h in 0.02 0.01 0.005 0.0025; do job c-1_h$h --c=-1 --h=$h; done
  for h in 0.01 0.005; do job O_c-0.3_h$h --c=-0.3 --h=$h --family=pulse; done ;;
esac
echo "lane $1 done" > "$R/lane_$1.done"
