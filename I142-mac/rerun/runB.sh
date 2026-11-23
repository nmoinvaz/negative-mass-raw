#!/bin/bash
cd /private/tmp/claude-501/-Users-nathan-Source-negative-mass/27911ca3-2259-460a-98f6-94387039554a/scratchpad/wt142/phase2/dg_proof
export OMP_NUM_THREADS=1 CTRL_LOGDIR=/private/tmp/claude-501/-Users-nathan-Source-negative-mass/27911ca3-2259-460a-98f6-94387039554a/scratchpad/r142/controls_logs
t0=$SECONDS; nice -n 10 /Users/nathan/Source/negative-mass/.venv/bin/python -u review_lemma_a3_controls.py > /private/tmp/claude-501/-Users-nathan-Source-negative-mass/27911ca3-2259-460a-98f6-94387039554a/scratchpad/r142/rerun_controls.txt 2> /private/tmp/claude-501/-Users-nathan-Source-negative-mass/27911ca3-2259-460a-98f6-94387039554a/scratchpad/r142/rerun_controls.err; echo "controls rc=$? s=$((SECONDS-t0))" >> /private/tmp/claude-501/-Users-nathan-Source-negative-mass/27911ca3-2259-460a-98f6-94387039554a/scratchpad/r142/runB.log
echo done >> /private/tmp/claude-501/-Users-nathan-Source-negative-mass/27911ca3-2259-460a-98f6-94387039554a/scratchpad/r142/runB.log
