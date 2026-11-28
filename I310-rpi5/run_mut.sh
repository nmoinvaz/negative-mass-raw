#!/bin/bash
# usage: run_mut.sh OUTPREFIX NAME...   OUTPREFIX is an absolute path prefix (e.g. /abs/dev/d3_).
# NAME = base (check, no mutation) | <mutation> (check --mutate=<mutation>) | derive_base | derive_<mutation> (derive [--mutate=..]).
# Each run writes OUTPREFIX<NAME>.log, .err and .rc; a run whose log exists is skipped (logs are never overwritten, a rerun gets a new prefix).
NR=/home/nathan/Source/negative-mass-i310/notes/black_universe
PY=/home/nathan/Source/negative-mass-venv314/bin/python
OUT=$1; shift
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd "$NR" || exit 2
for name in "$@"; do
  if [ -e "${OUT}${name}.log" ]; then echo "skip ${name}: log exists"; continue; fi
  cmd=check; mut=$name
  case "$name" in derive_*) cmd=derive; mut=${name#derive_};; esac
  if [ "$mut" = base ]; then opt=""; else opt="--mutate=$mut"; fi
  nice -n 10 "$PY" "$NR/static_c1_all.py" $cmd $opt > "${OUT}${name}.log" 2> "${OUT}${name}.err"
  echo $? > "${OUT}${name}.rc"
done
