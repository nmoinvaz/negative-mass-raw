#!/bin/bash
# development runs of the controls: each prints which checks fire
cd ~/Source/negative-mass-i272/notes/wormhole_evolution
PY=~/Source/negative-mass/.venv/bin/python
RAWD=~/Source/negative-mass-raw/I272-mac/dev
i=5
for m in "wrong_p planted" "pt_V planted" "ray_flip planted" "ecs_noscale planted" "wrong_secular zero" "pole_off zero" "no_projection time"; do
  set -- $m
  nice -n 10 $PY ellis_spectrum.py run --only=$2 --mutate=$1 > $RAWD/dev_0${i}_mut_$1.log 2> $RAWD/dev_0${i}_mut_$1.err
  echo $? > $RAWD/dev_0${i}_mut_$1.rc
  i=$((i+1))
done
