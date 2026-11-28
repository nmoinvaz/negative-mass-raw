#!/bin/bash
# runs of record: warm (two processes), derive, check, table; nice 10. usage: run_main.sh ABSOLUTE_OUT_DIR
OUT="$1"
PY=$HOME/Source/negative-mass/.venv/bin/python
SCRIPT=$HOME/Source/negative-mass-i322/notes/black_universe/remainder.py
CACHE=$HOME/Source/negative-mass-raw/I322-mac/cache
mkdir -p "$OUT" "$CACHE"
cd $HOME/Source/negative-mass-i322/notes/black_universe
( nice -n 10 "$PY" "$SCRIPT" warm --cache=$CACHE --items=A0,A1R,A1L,L,G,R,exact_g > "$OUT/warmA.log" 2> "$OUT/warmA.err"; echo $? > "$OUT/warmA.rc" ) &
( nice -n 10 "$PY" "$SCRIPT" warm --cache=$CACHE --items=Lm,Rb,Gb,rand0,rand1,rand2,rand3,exact_d > "$OUT/warmB.log" 2> "$OUT/warmB.err"; echo $? > "$OUT/warmB.rc" ) &
wait
for sub in derive check table; do
  /usr/bin/time -l nice -n 10 "$PY" "$SCRIPT" $sub --cache=$CACHE > "$OUT/$sub.log" 2> "$OUT/$sub.err"
  echo $? > "$OUT/$sub.rc"
done
/usr/bin/time -l nice -n 10 "$PY" "$SCRIPT" dump "$OUT/series" --cache=$CACHE > "$OUT/dump.log" 2> "$OUT/dump.err"
echo $? > "$OUT/dump.rc"
echo done > "$OUT/ALLDONE"
