#!/bin/bash
# usage: chain0.sh B   post hoc, h = 0.005 (hk = 0): the bisection of p*_h(B) to 1e-12, then the pairs at delta = 1e-10 and 1e-11, each by run1.sh (README part 2d)
RAW=${RAW:-$HOME/Source/negative-mass-raw/I325-dh610}
B=$1
$RAW/scripts/run1.sh runs/bisect_B${B}_hk0 7200 @PY@ g_d6.py drift bisect --D=6 --B=$B --hk=0 --out=@RAW@/runs/bisect
if [ -e "$RAW/runs/bisect/D6_B${B}_h0.005/summary.json" ]; then
  for d in 1e-10 1e-11; do
    $RAW/scripts/run1.sh runs/pair_B${B}_d${d}_hk0 7200 @PY@ g_d6.py drift stall --D=6 --B=$B --hk=0 --delta=$d --bis=@RAW@/runs/bisect --out=@RAW@/runs/stall_drift
  done
else
  echo "no summary.json for B=$B hk=0" >&2
fi
