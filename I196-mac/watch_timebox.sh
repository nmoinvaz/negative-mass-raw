#!/bin/bash
# amendment A7: stops run_A.sh (after its (3000, base, rtol 1e-13) case) and run_B4.sh (after its (2000, phi, rtol 1e-12) case) by PID, then starts run_A2.sh
RAW=/Users/nathan/Source/negative-mass-raw/I196-mac
has() { python3 - "$@" <<PY
import json, sys
g, v, r = float(sys.argv[1]), sys.argv[2], float(sys.argv[3])
for l in open("$RAW/jsonl/scipy_P0.jsonl"):
    o = json.loads(l)
    if o["gamma"] == g and o["variant"] == v and o["rtol"] == r and o["status"] == "done" and o["plant"] == "sci" and o["atol"] == 1e-14 and o["extra_chunks"] == 0:
        sys.exit(0)
sys.exit(1)
PY
}
PA=$(pgrep -f "^taylor_drift_A_placeholder" | head -1)
A_PY=$1; B_PY=$2
a_done=0; b_done=0
while [ $a_done -eq 0 ] || [ $b_done -eq 0 ]; do
  if [ $a_done -eq 0 ] && has 3000 base 1e-13; then kill $A_PY; a_done=1; echo "$(date) A stopped after (3000, base, 1e-13)"; $RAW/runrec.sh A2_P0_1e-11 bash $RAW/run_A2.sh & fi
  if [ $b_done -eq 0 ] && has 2000 phi 1e-12; then kill $B_PY; b_done=1; echo "$(date) B4 stopped after (2000, phi, 1e-12)"; fi
  sleep 5
done
wait
