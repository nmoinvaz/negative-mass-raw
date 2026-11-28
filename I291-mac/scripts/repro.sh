#!/bin/bash
# repro.sh : the runs of record against the development runs, bit for bit (locus.npz, member.json, pstar summary) for every (h, k) of the development set.
RAW=$HOME/Source/negative-mass-raw/I291-mac
n=0; bad=0
for k in 0 1 2 3 4 5 6 7; do
  rd=runs; dd=dev/runs; [ $k -ne 0 ] && rd=runs_k$k && dd=dev/runs_k$k
  for h in 0.02 0.01 0.005; do
    a=$RAW/$rd/G_B0.02/h$h/e12/member/locus.npz; b=$RAW/$dd/G_B0.02/h$h/e12/member/locus.npz
    if [ -e $b ]; then n=$((n+1)); cmp -s $a $b || { bad=$((bad+1)); echo "DIFFERENT $a"; }; fi
    for f in e12/member/member.json pstar/summary.json; do      # json: equal apart from the wall-clock "secs"
      a=$RAW/$rd/G_B0.02/h$h/$f; b=$RAW/$dd/G_B0.02/h$h/$f
      if [ -e $b ]; then n=$((n+1)); python3 - "$a" "$b" <<'PY' || { bad=$((bad+1)); echo "DIFFERENT $a"; }
import json, sys
a, b = (json.load(open(p)) for p in sys.argv[1:3])
for d in (a, b):
    d.pop("secs", None)
sys.exit(0 if a == b else 1)
PY
      fi
    done
  done
done
echo "$n files compared, $bad different"
