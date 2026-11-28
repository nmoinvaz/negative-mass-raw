#!/bin/bash
# run_main.sh OUTDIR: derive, check, table of static_c1.py at the code commit in OUTDIR/INFO.txt; logs OUTDIR/{derive,check,table}.log .err .rc. An existing log is not overwritten.
OUT="$1"
PY="$HOME/Source/negative-mass/.venv/bin/python"
cd "$HOME/Source/negative-mass-i259/notes/black_universe" || exit 1
for C in derive check table; do
  [ -e "$OUT/$C.log" ] && { echo "skip $C"; continue; }
  nice -n 10 "$PY" -u static_c1.py $C > "$OUT/$C.log" 2> "$OUT/$C.err"
  echo $? > "$OUT/$C.rc"
done
