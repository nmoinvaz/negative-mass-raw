#!/bin/sh
# usage: run_mut_some.sh PREFIX NAME... -- runs the named controls of conical_closure.py (--skip-num), one log each
PY=$HOME/Source/negative-mass/.venv/bin/python
RAW=$HOME/Source/negative-mass-raw/I172-mac
cd $HOME/Source/negative-mass-i172/notes/warp || exit 1
p=$1; shift
for m in "$@"; do
  nice -n 10 $PY -u conical_closure.py --mutate=$m --skip-num > $RAW/${p}_$m.log 2> $RAW/${p}_$m.err
  echo $? > $RAW/${p}_$m.rc
done
echo done > $RAW/${p}_done
