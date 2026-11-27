#!/bin/bash
# checks and the first four controls (each run alone, exit 1 expected) on the runs of record in jsonl/
cd /Users/nathan/Source/negative-mass-i196/phase2/nonradial || exit 1
RAW=/Users/nathan/Source/negative-mass-raw/I196-mac
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
CK="$PY taylor_drift.py check --dir=$RAW/jsonl --steps=$RAW/crate_star_steps.jsonl --jtable=$RAW/crate_jtable_l5.jsonl --raw=/Users/nathan/Source/negative-mass-raw"
$RAW/runrec.sh C_checks bash -c "$CK"
for m in "ident_atol IDENT" "cs_order CS" "rm_cut RMX" "cj_shift CJ"; do
  set -- $m
  $RAW/runrec.sh ctl_$1 bash -c "$CK --only=$2 --mutate=$1"
done
