#!/bin/bash
# ctl_worker.sh PREFIX NAME:MUTATION ...: serial runs of order6.py on the control grids, each kept as RAW/PREFIX_NAME.{log,err,rc} (devrun.sh); MUTATION "none" is the nominal run
# env: PY, WT (the notes/wormhole_largeD directory), EXTRA (further arguments)
set -u
d=$(dirname "$(readlink -f "$0")")
pre=$1; shift
for job in "$@"; do
  name=${job%%:*}; mut=${job#*:}
  args=""; [ "$mut" != none ] && args="--mutate=$mut"
  [ "$mut" = none ] && args="--save=$d/${pre}_${name}.json"
  (cd "$WT" && "$d/devrun.sh" "${pre}_${name}" nice -n 10 "$PY" order6.py sym evals values pslq remainder --cgrids --no-real $args --w2raw="$d/inputs_w2_growthD.txt" ${EXTRA:-})
done
