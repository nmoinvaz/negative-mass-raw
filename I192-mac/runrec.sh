#!/bin/zsh
# runrec.sh NAME CMD...  : the runs of record, run_NN_NAME: runs CMD at nice 10 with stdout, stderr and the exit code kept as run_NN_NAME.{log,err,rc}
# the number NN is the next free one; the command line and start time are the first lines of the log
D=$(cd "$(dirname "$0")" && pwd)
name=$1; shift
n=$(ls $D | grep -E '^run_[0-9]+_' | sed -E 's/^run_([0-9]+)_.*/\1/' | sort -n | tail -1)
n=$(printf "%02d" $(( ${n:-0} + 1 )))
b=$D/run_${n}_${name}
{ echo "# $(date '+%Y-%m-%d %H:%M:%S') cwd=$PWD"; echo "# cmd: $*"; } > $b.log
RAYON_NUM_THREADS=2 nice -n 10 "$@" >> $b.log 2> $b.err
echo $? > $b.rc
echo "$b rc=$(cat $b.rc)"
