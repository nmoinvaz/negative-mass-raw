#!/bin/bash
cd ~/Source/negative-mass-i272/notes/wormhole_evolution
PY=~/Source/negative-mass/.venv/bin/python
RAW=~/Source/negative-mass-raw/I272-mac/runs/mut
for m in "wrong_p planted" "pt_V planted" "ray_flip planted" "ecs_noscale planted" "wrong_secular zero" "pole_off zero" "no_projection time"; do
  set -- $m
  nice -n 10 $PY ellis_spectrum.py run --only=$2 --mutate=$1 > $RAW/mut_$1.log 2> $RAW/mut_$1.err
  echo $? > $RAW/mut_$1.rc
done
