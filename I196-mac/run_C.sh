#!/bin/bash
# the checks, their controls (each run alone, expected exit 1) and the report, on the runs of record in jsonl/
cd /Users/nathan/Source/negative-mass-i196/phase2/nonradial || exit 1
RAW=/Users/nathan/Source/negative-mass-raw/I196-mac
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
CK="$PY taylor_drift.py check --dir=$RAW/jsonl --steps=$RAW/crate_star_steps.jsonl --jtable=$RAW/crate_jtable_l5.jsonl --raw=/Users/nathan/Source/negative-mass-raw"
$RAW/runrec.sh C_checks bash -c "$CK"
for m in "ident_atol IDENT" "cs_order CS" "rm_cut RMX" "cj_shift CJ" "rep_variant REP" "ref_tol REF" "cls_swap CLS" "pln_sign PLN0" "drop_cell COMPLETE"; do
  set -- $m
  $RAW/runrec.sh ctl_$1 bash -c "$CK --only=$2 --mutate=$1"
done
$RAW/runrec.sh D_report $PY taylor_drift.py report --dir=$RAW/jsonl
$RAW/runrec.sh E_jround $PY taylor_drift.py jround --gammas=1000,3000 --n=40
