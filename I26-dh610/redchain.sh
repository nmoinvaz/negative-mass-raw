#!/bin/bash
# redchain.sh MUT...: development runs of the `reduce` part of dev_10_order4_wip.py (the copy that became order4.py), nominal first when MUT is "none"
set -u
d=$(dirname "$(readlink -f "$0")")
for m in "$@"; do
  if [ "$m" = none ]; then a=""; else a="--mutate=$m"; fi
  nice -n 10 "$d/devrun.sh" "dev_11_reduce_$m" nice -n 10 ~/Source/negative-mass-venv314/bin/python -u "$d/dev_10_order4_wip.py" reduce $a
done
