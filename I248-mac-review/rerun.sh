#!/bin/bash
# The review's rerun of #248's derive, check and table on the Mac (one process, nice 10), from the review worktree.
WT=$HOME/Source/negative-mass-r248/notes/black_universe
OUT=$HOME/Source/negative-mass-raw/I248-mac-review
PY=$HOME/Source/negative-mass/.venv/bin/python
cd "$WT" || exit 2
for c in derive check table; do
  NUMBA_NUM_THREADS=1 /usr/bin/time -l nice -n 10 $PY -u horizon_sector.py $c > "$OUT/rerun_$c.log" 2> "$OUT/rerun_$c.err"
  echo "$c rc=$?" >> "$OUT/rerun.rc"
done
