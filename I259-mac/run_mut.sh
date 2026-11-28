#!/bin/bash
# run_mut.sh OUTDIR PREFIX NAME...   run `static_c1.py check|derive --mutate=NAME` for each NAME, nice 10, one after the other;
# logs OUTDIR/PREFIXNAME.log (stdout), .err, .rc. Never overwrites: an existing log is skipped.
# The derive mutations (s_q, s_pot) run `derive`, the others `check`.
OUT="$1"; PRE="$2"; shift 2
PY="$HOME/Source/negative-mass/.venv/bin/python"
cd "$HOME/Source/negative-mass-i259/notes/black_universe" || exit 1
for N in "$@"; do
  LOG="$OUT/${PRE}${N}.log"
  if [ -e "$LOG" ]; then echo "skip $N (log exists)"; continue; fi
  case "$N" in s_q|s_pot) CMD=derive;; *) CMD=check;; esac
  nice -n 10 "$PY" -u static_c1.py $CMD --mutate="$N" > "$LOG" 2> "$OUT/${PRE}${N}.err"
  echo $? > "$OUT/${PRE}${N}.rc"
done
