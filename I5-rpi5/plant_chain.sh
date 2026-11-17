#!/bin/bash
# usage: plant_chain.sh <winding2 args incl. --cachedir> -- <plant re,im>: the planted-zero check, then each mutation
# (all on the cached D of the box).  Exit status: the unmutated run's, and 1 if a mutated run does not fail.
plant=$1; shift
rc0=0; bad=0
for m in none reverse wrongdouble misplant onesided; do
  echo "## mutate=$m"
  if [ $m = none ]; then $PY -u $NR/winding2.py "$@" --plant=$plant | grep -E "RESULT|PLANTED"; rc=${PIPESTATUS[0]}; rc0=$rc
  else $PY -u $NR/winding2.py "$@" --plant=$plant --mutate=$m | grep -E "RESULT|PLANTED"; rc=${PIPESTATUS[0]}; [ $rc -eq 1 ] || bad=1; fi
  echo "exit $rc"
done
[ $bad -eq 0 ] || echo "A MUTATION DID NOT FAIL"
exit $(( rc0 | bad ))
