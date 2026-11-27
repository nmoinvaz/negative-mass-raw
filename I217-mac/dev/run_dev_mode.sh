#!/bin/bash
# dev_12 .. dev_19 of I217-mac: mode-family bisections, one process, nice 10, one thread. Started by negative-mass-mac-i217 for the design note.
export NUMBA_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=1
cd /Users/nathan/Source/negative-mass-i217/notes/black_universe
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
RAW=/Users/nathan/Source/negative-mass-raw/I217-mac/dev
run() { n=$1; shift; nice -n 10 /usr/bin/time -l $PY evolve_dev_runs.py "$@" > $RAW/dev_${n}.log 2> $RAW/dev_${n}.err; echo "rc=$?" >> $RAW/dev_${n}.log; }
run 12_mode_m03_h02  mode -0.3 0.0 0.02  40 1e-4
run 13_mode_m03_h01  mode -0.3 0.0 0.01  40 1e-4
run 14_mode_m03_h005 mode -0.3 0.0 0.005 40 1e-4
run 15_mode_m15_h02  mode -1.5 1.0 0.02  50 1e-4
run 16_mode_m15_h01  mode -1.5 1.0 0.01  50 1e-4
run 17_mode_m15_h005 mode -1.5 1.0 0.005 50 1e-4
run 18_mode_m15_rc2  mode -1.5 2.0 0.01  50 1e-4
run 19_mode_m15_rc06 mode -1.5 0.6 0.01  50 1e-4
echo done > $RAW/run_dev_mode.done
