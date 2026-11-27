#!/bin/bash
# ctl_worker_load.sh PREFIX JSON MUTATION ...: serial runs of `order6.py values pslq remainder --cgrids --no-real --load=JSON` under each mutation (RAW/PREFIX_MUTATION.{log,err,rc})
# env: PY, WT
set -u
d=$(dirname "$(readlink -f "$0")")
pre=$1; json=$2; shift; shift
for mut in "$@"; do
  args="--mutate=$mut"; [ "$mut" = nominal ] && args=""
  (cd "$WT" && "$d/devrun.sh" "${pre}_${mut}" nice -n 10 "$PY" order6.py values pslq remainder --cgrids --no-real --load="$d/$json" --w2raw="$d/inputs_w2_growthD.txt" $args)
done
