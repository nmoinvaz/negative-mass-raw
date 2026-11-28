#!/bin/zsh
# runrec.sh NAME CMD...  : runs CMD detached-safe at nice 10 with stdout, stderr (/usr/bin/time -l) and the exit code kept as run_NN_NAME.{log,err,rc}
# NN is the next free number; the command line, start time and load average are the first lines of the log
D=$(cd "$(dirname "$0")" && pwd)
name=$1; shift
n=$(ls $D | grep -E '^run_[0-9]+_' | sed -E 's/^run_([0-9]+)_.*/\1/' | sort -n | tail -1)
n=$(printf "%02d" ${RUN_N:-$(( ${n:-0} + 1 ))})
b=$D/run_${n}_${name}
{ echo "# $(date '+%Y-%m-%d %H:%M:%S') cwd=$PWD load=$(uptime | sed 's/.*load averages*: //')"; echo "# cmd: $*"; } > $b.log
RAYON_NUM_THREADS=2 /usr/bin/time -l nice -n 10 "$@" >> $b.log 2> $b.err
echo $? > $b.rc
echo "$b rc=$(cat $b.rc)"
