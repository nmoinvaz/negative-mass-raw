#!/bin/bash
# ctl_worker_red.sh PREFIX SCRIPT JSON MUTATION ...: serial runs of `SCRIPT reduce6 --load=JSON` under each mutation (RAW/PREFIX_MUTATION.{log,err,rc}); "nominal" is unmutated
# env: PY, WT
set -u
d=$(dirname "$(readlink -f "$0")")
pre=$1; script=$2; json=$3; shift; shift; shift
for mut in "$@"; do
  args="--mutate=$mut"; [ "$mut" = nominal ] && args=""
  (cd "$WT" && "$d/devrun.sh" "${pre}_${mut}" nice -n 10 "$PY" "$script" reduce6 --load="$d/$json" $args)
done
