#!/bin/sh
# usage: run_mut.sh ABSOLUTE_OUT PREFIX NAME...   one process each, nice 10; the log of NAME is ABSOLUTE_OUT/PREFIXNAME.log
OUT=$1
PREFIX=$2
shift 2
cd "$HOME/Source/negative-mass-i321/notes/black_universe" || exit 2
for NAME in "$@"; do
  case "$NAME" in
    eps|a2|om|gauge|gth) CMD=derive ;;
    fpi|nolog|pred|rhs|hor|s2t) CMD=series ;;
    *) CMD=check ;;
  esac
  nice -n 10 "$HOME/Source/negative-mass/.venv/bin/python" log_at_S.py $CMD "--mutate=$NAME" > "$OUT/$PREFIX$NAME.log" 2>&1
  echo "$NAME ($CMD): exit $?"
done
