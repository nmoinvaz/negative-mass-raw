#!/bin/bash
# usage: pair.sh B BISDIR   the pair p*_h -/+ 1e-10 at (B, h = 0.0025) on the triangle X = 70, run1.sh's WAITFOR inside the run: the bisection's summary.json for B = 0.2 (this task's), PART2_DECLARED for B = 0.15 (#325's bisection is done).
RAW=${RAW:-$HOME/Source/negative-mass-raw/I326-dh610}
B=$1; BIS=$2
H=0.0025
if [ "$B" = "0.2" ]; then W=$BIS/D6_B${B}_h${H}/summary.json; else W=$RAW/PART2_DECLARED; fi
WAITFOR=$W $RAW/scripts/run1.sh runs/pair_B${B}_d1e-10_hk1 7200 @PY@ drift_b6_long.py pair --B=$B --hk=1 --delta=1e-10 --bis=$BIS --tcap=70 --out=@RAW@/runs/stall_drift
