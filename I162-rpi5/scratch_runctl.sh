#!/bin/bash
cd /home/nathan/Source/negative-mass-i162/notes/warp || exit 2
SC=/tmp/claude-1000/-home-nathan-Source-negative-mass-i162/52348d99-c0b3-4077-9b90-7c44e07bbaf4/scratchpad/scr1
for m in frame-nu frob-struct frob-ode sum-factor isolated-c0 each-w2 each-friction points-closed bessel-freq plant-pass plant-fail c0-sign planar-closed; do
  OMP_NUM_THREADS=1 nice -n 10 /home/nathan/Source/negative-mass-venv314/bin/python bessel_closure.py --mutate=$m > $SC/ctl_$m.log 2>&1
  echo $? > $SC/ctl_$m.rc
done
echo done > $SC/ctl_all.done
