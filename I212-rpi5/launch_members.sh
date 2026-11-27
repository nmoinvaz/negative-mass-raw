#!/bin/bash
# usage: launch_members.sh c1 c2 ...   (runs R1 then R2 for each member; JSON and log per run, exit code in results/status.txt)
RAW=$HOME/Source/negative-mass-raw/I212-rpi5
PY=$HOME/Source/negative-mass-venv314/bin/python
cd $HOME/Source/negative-mass-i212/notes/black_universe || exit 1
for c in "$@"; do
  for res in R1 R2; do
    f=$RAW/results/member_${c}_${res}
    if [ -f $f.json ]; then continue; fi          # a finished run is never overwritten
    /usr/bin/time -v nice -n 10 $PY stability.py count $c --res=$res --out=$f.json > $f.log 2>&1
    echo "c=$c $res exit $? $(date +%H:%M:%S)" >> $RAW/results/status.txt
  done
done
