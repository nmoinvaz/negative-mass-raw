#!/bin/bash
# old he_type_exact (main 29e395d) on the three tiny-D tensors; Irat is cut at 300 s
RAW=$HOME/Source/negative-mass-raw/I103-rpi5
cd /tmp/claude-1000/-home-nathan-Source-negative-mass-i103/5e59a2be-b4eb-48b6-bced-84f9743c2d2e/scratchpad/old_code
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
for c in Irad IVrad Irat; do
  nice -n 10 timeout 300 $HOME/Source/negative-mass-venv314/bin/python $RAW/support/probe_old_code.py /tmp/claude-1000/-home-nathan-Source-negative-mass-i103/5e59a2be-b4eb-48b6-bced-84f9743c2d2e/scratchpad/old_code $c > $RAW/s6_old_$c.log 2>&1
  echo $? > $RAW/done/s6_old_$c.rc
done
echo 0 > $RAW/done/step6.rc
