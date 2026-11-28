#!/bin/bash
# usage: pair.sh B HK DELTA   the pair p*_h -/+ DELTA at (B, HK), waiting inside its run for (1) the bisection's summary.json (this task's, or #228's for its B) and (2) the ticket
#   $RAW/tickets/pair_B<B>_d<DELTA>_hk<HK> that dispatch.sh issues once README part 2b is declared and fewer than 4 of my compute processes run.
RAW=${RAW:-$HOME/Source/negative-mass-raw/I325-dh610}
I228=$HOME/Source/negative-mass-raw/I228-dh610/runs
B=$1; HK=$2; DELTA=$3
case $HK in 1) H=0.0025;; 2) H=0.00125;; esac
BIS=""
while [ -z "$BIS" ]; do
  for d in "$RAW/runs/bisect" "$I228/bisect"; do [ -e "$d/D6_B${B}_h${H}/summary.json" ] && BIS=$d && break; done
  [ -z "$BIS" ] && sleep 30
done
mkdir -p "$RAW/tickets"
WAITFOR=$RAW/tickets/pair_B${B}_d${DELTA}_hk${HK} $RAW/scripts/run1.sh runs/pair_B${B}_d${DELTA}_hk${HK} 7200 @PY@ g_d6.py drift stall --D=6 --B=$B --hk=$HK --delta=$DELTA --bis=$BIS --out=@RAW@/runs/stall_drift
