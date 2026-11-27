#!/bin/bash
# waits for N1 (6 cases), then freezes run_B.sh, stops its child and it by PID, and starts run_B2.sh through runrec.sh (amendment A2)
RAW=/Users/nathan/Source/negative-mass-raw/I196-mac
until [ "$(cat $RAW/jsonl/scipy_N1.jsonl 2>/dev/null | wc -l)" -ge 6 ]; do sleep 3; done
B=$(pgrep -f "^bash $RAW/run_B.sh" | head -1)
echo "$(date) N1 done; B = $B"
kill -STOP $B
for c in $(pgrep -P $B); do echo "killing child $c"; kill $c; done
kill -KILL $B
sleep 2
$RAW/runrec.sh B2_noiserow_noise_P1_extras bash $RAW/run_B2.sh
