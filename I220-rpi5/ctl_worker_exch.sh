#!/bin/bash
# ctl_worker_exch.sh PREFIX MUTATION ...: serial runs of `order6.py exch6` kept as RAW/PREFIX_MUTATION.{log,err,rc}; MUTATION "nominal" is the unmutated run
# env: PY, WT
set -u
d=$(dirname "$(readlink -f "$0")")
pre=$1; shift
for mut in "$@"; do
  args="--mutate=$mut"; [ "$mut" = nominal ] && args=""
  (cd "$WT" && "$d/devrun.sh" "${pre}_${mut}" nice -n 10 "$PY" order6.py exch6 $args)
done
