#!/bin/bash
# the cheap controls, one devrun each: NAME CHECK
cd /Users/nathan/Source/negative-mass-i196/phase2/nonradial
CK="/Users/nathan/Source/negative-mass/.venv/bin/python taylor_drift.py check --dir=/Users/nathan/Source/negative-mass-raw/I196-mac/dev_jsonl --crate-dir=/Users/nathan/Source/negative-mass-raw/I196-mac/dev_jsonl/crate --steps=/Users/nathan/Source/negative-mass-raw/I196-mac/crate_star_steps.jsonl"
for m in "ident_atol IDENT" "cs_order CS" "rm_cut RMX" "cls_swap CLS" "drop_cell COMPLETE"; do
  set -- $m
  /Users/nathan/Source/negative-mass-raw/I196-mac/devrun.sh ctl_$1 bash -c "$CK --only=$2 --synthetic --mutate=$1"
done
