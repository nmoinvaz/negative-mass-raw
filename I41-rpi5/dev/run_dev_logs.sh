#!/bin/bash
# reruns the development scripts of dev/scripts/ against the code as committed, one log each (the originals printed to a terminal)
RAW=$(dirname "$(readlink -f "$0")")/..
PY=~/Source/negative-mass-venv314/bin/python
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1
cd $RAW/dev/scripts || exit 1
nice -n 10 $PY pilot1.py 0.02 20 1e-8 1e30 > ../pilot1_h0.02_d1e-8.log 2>&1
for nc in 120 240 480; do nice -n 10 $PY p1b.py 4 10 $nc 0.02 0.01 0.005 0.0025 > ../p1b_F4_K10_Nc$nc.log 2>&1; done
nice -n 10 $PY p2.py 480 0.02 0.01 0.005 0.0025 > ../p2_Nc480.log 2>&1
for a in "0.01 1e-8 4 10 480" "0.005 1e-8 4 10 480" "0.01 1e-8 2 11 480" "0.005 1e-8 2 11 480" "0.005 1e-8 1.5 12 480" "0.005 1e-8 1.5 12 960" "0.005 1e-8 1.0 12 480"; do
  nice -n 10 $PY real2.py $a > "../real2_$(echo $a | tr ' ' '_').log" 2>&1
done
