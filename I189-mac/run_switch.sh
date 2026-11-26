#!/bin/zsh
# run_switch.sh: the runs of record of the crate switch (X2, X3), the feature off then on for each, one process at a time, nice 10,
# RAYON_NUM_THREADS=2. Output: run_NN_<name>_<off|on>.{log,err,rc} in this folder; a run over 1 h is stopped by timeout (its own child).
D=$(cd "$(dirname "$0")" && pwd)
NR=/Users/nathan/Source/negative-mass-i189/phase2/nonradial
BINS=$NR/taylor_polar/target/bins
BIN=$NR/taylor_polar/target/release/taylor_polar
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
n=${1:-1}
run() {  # run NAME ARGS...
  name=$1; shift
  for side in off on; do
    cp $BINS/$side $BIN
    b=$D/run_$(printf "%02d" $n)_${name}_$side
    mkdir -p $D/jsonl_$side
    { echo "# $(date '+%Y-%m-%d %H:%M:%S') cwd=$NR load $(uptime | sed 's/.*load averages: //')"; echo "# side: $side ($(md5 -q $BIN))"; echo "# cmd: $PY taylor_polar.py $* --jsonl-dir=$D/jsonl_$side"; } > $b.log
    ( cd $NR && RAYON_NUM_THREADS=2 nice -n 10 timeout 3600 /usr/bin/time -l $PY taylor_polar.py "$@" --jsonl-dir=$D/jsonl_$side >> $b.log 2> $b.err )
    echo $? > $b.rc
    echo "$(date '+%H:%M:%S') $b rc=$(cat $b.rc)" >> $D/run_switch.progress
    n=$((n+1))
  done
}
runp() {  # runp NAME ARGS...: as run, without the jsonl directory
  name=$1; shift
  for side in off on; do
    cp $BINS/$side $BIN
    b=$D/run_$(printf "%02d" $n)_${name}_$side
    { echo "# $(date '+%Y-%m-%d %H:%M:%S') cwd=$NR load $(uptime | sed 's/.*load averages: //')"; echo "# side: $side ($(md5 -q $BIN))"; echo "# cmd: $PY taylor_polar.py $*"; } > $b.log
    ( cd $NR && RAYON_NUM_THREADS=2 nice -n 10 timeout 3600 /usr/bin/time -l $PY taylor_polar.py "$@" >> $b.log 2> $b.err )
    echo $? > $b.rc
    echo "$(date '+%H:%M:%S') $b rc=$(cat $b.rc)" >> $D/run_switch.progress
    n=$((n+1))
  done
}
run planted_rm --rows --only=QP,RP,RM
run rows_l2 --rows --only=RA2,RX
run rows_l3 --rows --only= --print-rows=3
run rows_l4 --rows --only=RA4
run rows_l5_cap5 --rows --only=RA5,CAP5,CAP5s
run rows_l6_cap6 --rows --only=RA6,CAP6
runp default_mode
