#!/bin/sh
# re-runs the development probes with logs kept (nice 10, one process at a time); run from this folder
PY=$HOME/Source/negative-mass/.venv/bin/python
for p in p1 p6 p7 p9 p11 p12 p13 p14 p16 p17 p18 p19 p22; do
  nice -n 10 $PY $p.py > logs/$p.log 2> logs/$p.err
  echo $? > logs/$p.rc
done
echo done > logs/ALL_DONE
