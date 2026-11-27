#!/bin/bash
# devrec_lane.sh NAME ARGS...: runs `throat_locus.py ARGS...` once (development record, dev/rec/), log dev/rec/logs/NAME.{log,time,rc}, never overwritten
PY=$HOME/Source/negative-mass-venv314/bin/python
RAW=$HOME/Source/negative-mass-raw/I225-dh610
mkdir -p $RAW/dev/rec/logs
cd $HOME/Source/negative-mass-i225/notes/wormhole_evolution
name=$1; shift
f=$RAW/dev/rec/logs/$name; i=1
while [ -e $f.log ]; do f=$RAW/dev/rec/logs/${name}_r$i; i=$((i+1)); done
/usr/bin/time -v -o $f.time nice -n 10 $PY throat_locus.py "$@" > $f.log 2>&1
echo $? > $f.rc
