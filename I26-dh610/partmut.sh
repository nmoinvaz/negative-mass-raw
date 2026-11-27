#!/bin/bash
# partmut.sh PREFIX SCRIPT PART:MUT...: development runs of SCRIPT PART --mutate=MUT, logs PREFIX_PART_MUT.{log,err,rc}
set -u
d=$(dirname "$(readlink -f "$0")")
prefix=$1; script=$2; shift 2
for pm in "$@"; do
  part=${pm%%:*}; m=${pm##*:}
  nice -n 10 "$d/devrun.sh" "${prefix}_${part}_${m}" nice -n 10 ~/Source/negative-mass-venv314/bin/python -u "$script" $part --mutate=$m
done
