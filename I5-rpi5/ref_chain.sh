#!/bin/bash
# usage: ref_chain.sh l gmax a1 a2 -- the real-gamma refinement to level 2 and its controls, in one job
# (they share one cache csv, so they must not overlap).  Exits with the main run's status.
l=$1; gmax=$2; a1=$3; a2=$4
R="$PY -u $NR/refine_gamma.py -1 0.7603 $l 1e-3 $gmax 100 2 --out=$RAW"
$R --procs=1; rc=$?;                                      echo "== main rc=$rc (0 expected)"
$R --plant=$a1,$a2 --check=0; echo "== planted pair rc=$? (0 expected)"
$R --plant=$a1,$a2 --check=0 --mutate=coarse; echo "== planted pair, mutate=coarse rc=$? (1 expected)"
$R --check=0 --mutate=pair;   echo "== mutate=pair rc=$? (1 expected)"
$R --check=1 --mutate=stale;  echo "== mutate=stale rc=$? (1 expected)"
exit $rc
