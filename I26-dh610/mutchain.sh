#!/bin/bash
# mutchain.sh PARTS NAMEPREFIX MUT...: development runs of order4.py under each mutation, one after the other (cwd: the worktree's notes/wormhole_largeD)
set -u
d=$(dirname "$(readlink -f "$0")")
parts=$1; prefix=$2; shift 2
for m in "$@"; do
  nice -n 10 "$d/devrun.sh" "${prefix}_$m" nice -n 10 ~/Source/negative-mass-venv314/bin/python -u order4.py $parts --mutate=$m --w2raw="$d/inputs_w2_growthD.txt"
done
