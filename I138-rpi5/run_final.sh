#!/bin/bash
# step 6: final runs, one process at a time, stdout only into the repository's *_output.txt, stderr and exit codes here
RAW=$HOME/Source/negative-mass-raw/I138-rpi5
DG=$HOME/Source/negative-mass-i138/phase2/dg_proof
PY=$HOME/Source/negative-mass-venv314/bin/python
cd $DG || exit 1
: > $RAW/final.rc
for s in common signs recur zerilli l1 t1 t2; do
  nice -n 10 env OMP_NUM_THREADS=1 $PY -u review_lemma_a_$s.py > review_lemma_a_${s}_output.txt 2> $RAW/final_${s}.err
  echo "$s $?" >> $RAW/final.rc
done
rm -rf $RAW/controls_logs && mkdir -p $RAW/controls_logs
nice -n 10 env OMP_NUM_THREADS=1 $PY -u review_lemma_a_controls.py --logdir=$RAW/controls_logs > review_lemma_a_controls_output.txt 2> $RAW/final_controls.err
echo "controls $?" >> $RAW/final.rc
echo done >> $RAW/final.rc
