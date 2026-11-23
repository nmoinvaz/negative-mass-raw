#!/bin/bash
# step 6: final runs of the five check scripts, stdout only, one process at a time, nice 10, exit codes in final.rc
cd "$HOME/Source/negative-mass-i142/phase2/dg_proof" || exit 1
RAW="$HOME/Source/negative-mass-raw/I142-rpi5"
export OMP_NUM_THREADS=1
: > "$RAW/final.rc"
for sc in a3 ends dg61 l6 l4 v; do
  nice -n 10 "$HOME/Source/negative-mass-venv314/bin/python" -I "review_lemma_a3_$sc.py" > "review_lemma_a3_${sc}_output.txt" 2> "$RAW/final_$sc.err"
  echo "$sc $?" >> "$RAW/final.rc"
done
mkdir -p "$RAW/controls_logs_final"
CTRL_LOGDIR="$RAW/controls_logs_final" nice -n 10 "$HOME/Source/negative-mass-venv314/bin/python" -I review_lemma_a3_controls.py > review_lemma_a3_controls_output.txt 2> "$RAW/final_controls.err"
echo "controls $?" >> "$RAW/final.rc"
echo done >> "$RAW/final.rc"
