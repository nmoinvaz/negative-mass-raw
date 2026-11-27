#!/bin/bash
# The coordinator's rerun of #194's run_13_final (the driver over the stage logs of record), nice 10, 2 Rayon threads.
R=$HOME/Source/negative-mass-raw
OUT=$R/I194-mac-review/rerun_run_13_final.log
[ -e "$OUT" ] && { echo "$OUT exists; not overwriting"; exit 3; }
cd $HOME/Source/negative-mass-r194/phase2/radial || exit 2
export RAYON_NUM_THREADS=2 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
RAW=../../../negative-mass-raw/I194-mac
/usr/bin/time -l nice -n 10 $HOME/Source/negative-mass/.venv/bin/python taylor_radial.py \
  --arc-log=$RAW/run_09_arc.jsonl,$RAW/run_05_stepA.jsonl,$RAW/run_10_stepB.jsonl,$RAW/run_07_stepC.jsonl \
  --supp-log=$RAW/run_11_stepS.jsonl > "$OUT" 2> "${OUT%.log}.err"
echo "rc=$?" >> "$OUT"
