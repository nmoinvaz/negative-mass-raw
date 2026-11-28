#!/bin/bash
# s3_chain.sh TREE LABEL N1 N2 N3 N4 [BINPREFIX]: the four checks runs of one tree, one after the other, as run_N1 .. run_N4:
#   N1 default mode (#186's 22 checks), N2 --rows (default binary), N3 --rows with the lib_plane binary (#189's plane rows),
#   N4 --complex with the runner's references (--bins = the tree's target/bins, --ref-dir = I188-mac/ref).
# TREE has phase2/nonradial (a copy of the script's directory) and taylor_polar/target/{release,complex/release,bins}; BINPREFIX (default LABEL)
# names the binaries of target/bins to use (BINPREFIX_default, _libplane, _complex, _libtable...).
set -u
TREE=$1; LABEL=$2; N1=$3; N2=$4; N3=$5; N4=$6; PFX=${7:-$LABEL}
D=$(cd "$(dirname "$0")" && pwd)
RAW=$HOME/Source/negative-mass-raw
PY=$HOME/Source/negative-mass/.venv/bin/python
NR=$TREE/phase2/nonradial
T=$NR/taylor_polar/target
export S3_TREE=$TREE
cp $T/bins/${PFX}_default $T/release/taylor_polar
cp $T/bins/${PFX}_complex $T/complex/release/taylor_polar
$D/s3_run.sh $N1 s3_${LABEL}_default_mode $PY $NR/taylor_polar.py --raw=$RAW
$D/s3_run.sh $N2 s3_${LABEL}_rows $PY $NR/taylor_polar.py --rows --raw=$RAW --jsonl-dir=$D/s3_jsonl/${LABEL}_rows
cp $T/bins/${PFX}_libplane $T/release/taylor_polar
$D/s3_run.sh $N3 s3_${LABEL}_rows_libplane $PY $NR/taylor_polar.py --rows --raw=$RAW --jsonl-dir=$D/s3_jsonl/${LABEL}_rows_libplane
cp $T/bins/${PFX}_default $T/release/taylor_polar
$D/s3_run.sh $N4 s3_${LABEL}_complex $PY $NR/taylor_polar.py --complex --raw=$RAW --bins=$T/bins --ref-dir=$RAW/I188-mac/ref --jsonl-dir=$D/s3_jsonl/${LABEL}_complex
