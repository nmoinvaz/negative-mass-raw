#!/bin/bash
# usage: run_mut.sh ABSOLUTE_OUT_DIR PREFIX NAME...   (derive mutations s_*, check mutations otherwise); one process, nice 10
OUT="$1"; PREFIX="$2"; shift 2
PY=$HOME/Source/negative-mass/.venv/bin/python
SCRIPT=$HOME/Source/negative-mass-i302/notes/black_universe/horizon_basis.py
CACHE=$HOME/Source/negative-mass-raw/I302-mac/cache
mkdir -p "$OUT"
for m in "$@"; do
  case "$m" in
    s_*) sub=derive ;;
    *) sub=check ;;
  esac
  nice -n 10 "$PY" "$SCRIPT" $sub --mutate=$m --cache=$CACHE > "$OUT/${PREFIX}${m}.log" 2> "$OUT/${PREFIX}${m}.err"
  echo $? > "$OUT/${PREFIX}${m}.rc"
done
echo done > "$OUT/${PREFIX}ALLDONE"
