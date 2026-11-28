#!/bin/bash
# usage: chain.sh B HK [DELTA]   the bisection of p*_h(B, h) to 1e-12 (2 h limit), then, if it finished, the pair p*_h -/+ DELTA (default 1e-10, 2 h limit), each by run1.sh.
#   The pair waits for $RAW/PART2B_DECLARED (written when README part 2b, the mutations' computed effects, is committed) inside the run, so that the pairs of record start after the criteria.
RAW=${RAW:-$HOME/Source/negative-mass-raw/I325-dh610}
B=$1; HK=$2; DELTA=${3:-1e-10}
case $HK in 1) H=0.0025;; 2) H=0.00125;; esac
if [ ! -e "$RAW/runs/bisect/D6_B${B}_h${H}/summary.json" ] && [ "$DELTA" = 1e-10 ]; then
  $RAW/scripts/run1.sh runs/bisect_B${B}_hk${HK} 7200 @PY@ g_d6.py drift bisect --D=6 --B=$B --hk=$HK --out=@RAW@/runs/bisect
fi
if [ -e "$RAW/runs/bisect/D6_B${B}_h${H}/summary.json" ]; then
  WAITFOR=$RAW/PART2B_DECLARED $RAW/scripts/run1.sh runs/pair_B${B}_d${DELTA}_hk${HK} 7200 @PY@ g_d6.py drift stall --D=6 --B=$B --hk=$HK --delta=$DELTA --bis=@RAW@/runs/bisect --out=@RAW@/runs/stall_drift
else
  echo "no summary.json for B=$B hk=$HK: the bisection did not finish; the pair is not started" >&2
fi
