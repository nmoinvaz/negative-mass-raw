#!/bin/bash
cd /private/tmp/claude-501/-Users-nathan-Source-negative-mass/27911ca3-2259-460a-98f6-94387039554a/scratchpad/wt142/phase2/dg_proof
export OMP_NUM_THREADS=1
for s in a3 ends dg61 l6 l4 v; do
  t0=$SECONDS; nice -n 10 /Users/nathan/Source/negative-mass/.venv/bin/python -u review_lemma_a3_$s.py > /private/tmp/claude-501/-Users-nathan-Source-negative-mass/27911ca3-2259-460a-98f6-94387039554a/scratchpad/r142/rerun_$s.txt 2> /private/tmp/claude-501/-Users-nathan-Source-negative-mass/27911ca3-2259-460a-98f6-94387039554a/scratchpad/r142/rerun_$s.err; echo "$s rc=$? s=$((SECONDS-t0))" >> /private/tmp/claude-501/-Users-nathan-Source-negative-mass/27911ca3-2259-460a-98f6-94387039554a/scratchpad/r142/runA.log
done
echo done >> /private/tmp/claude-501/-Users-nathan-Source-negative-mass/27911ca3-2259-460a-98f6-94387039554a/scratchpad/r142/runA.log
