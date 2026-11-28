#!/bin/bash
# runs of record: derive, check (cold cache), table; one process, nice 10. usage: run_main.sh ABSOLUTE_OUT_DIR
OUT="$1"
PY=$HOME/Source/negative-mass/.venv/bin/python
SCRIPT=$HOME/Source/negative-mass-i302/notes/black_universe/horizon_basis.py
CACHE=$HOME/Source/negative-mass-raw/I302-mac/cache
mkdir -p "$OUT"
cd $HOME/Source/negative-mass-i302/notes/black_universe
for sub in derive check table; do
  /usr/bin/time -l nice -n 10 "$PY" "$SCRIPT" $sub --cache=$CACHE > "$OUT/$sub.log" 2> "$OUT/$sub.err"
  echo $? > "$OUT/$sub.rc"
done
echo done > "$OUT/ALLDONE"
