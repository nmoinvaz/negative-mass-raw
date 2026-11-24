#!/bin/bash
# Waits for the sweep (unit nm-i104-sweep) to finish, then runs the controls (step 5) and the final runs (step 6), one process at a time.
RAW=$HOME/Source/negative-mass-raw/I104-rpi5
DG=$HOME/Source/negative-mass-i104/phase2/dg_proof
PY=$HOME/Source/negative-mass-venv314/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd "$DG" || exit 9
until [ -f "$RAW/step4b_sweep.rc" ]; do sleep 15; done
echo "sweep rc=$(cat $RAW/step4b_sweep.rc) at $(date)" >> "$RAW/chain.log"
# step 5: controls
t0=$SECONDS
nice -n 10 $PY -u review_large_l_controls.py --logdir="$RAW/controls_logs" > review_large_l_controls_output.txt 2> "$RAW/controls_stderr.txt"
echo "review_large_l_controls.py rc=$? seconds=$((SECONDS-t0)) at $(date)" >> "$RAW/chain.log"
# step 6: final runs
for s in common roots theorem3 brackets thm_l thm_m; do
  t0=$SECONDS
  nice -n 10 $PY -u review_large_l_$s.py > review_large_l_${s}_output.txt 2> "$RAW/final_${s}_stderr.txt"
  echo "review_large_l_$s.py rc=$? seconds=$((SECONDS-t0)) at $(date)" >> "$RAW/chain.log"
done
t0=$SECONDS
nice -n 10 $PY -u review_large_l_table.py --csv="$RAW/sweep_brackets.csv" > review_large_l_table_output.txt 2> "$RAW/final_table_stderr.txt"
echo "review_large_l_table.py rc=$? seconds=$((SECONDS-t0)) at $(date)" >> "$RAW/chain.log"
cp "$RAW/step4b_sweep.log" review_large_l_sweep_output.txt
echo "sweep output copied from step4b_sweep.log (run launched 2026-11-23 01:44, rc $(cat $RAW/step4b_sweep.rc))" >> "$RAW/chain.log"
echo "chain done at $(date)" >> "$RAW/chain.log"
touch "$RAW/chain.done"
