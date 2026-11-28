#!/bin/bash
# s3_run.sh NUM NAME CMD...: a run of record run_NUM_NAME.{log,err,rc} at nice 10 (the number is given, not looked up: two runs can start together).
# S3_TREE names the tree whose binaries the command uses; their md5 are the first lines of the log. A run not finished in 2 h is stopped (exit 124).
D=$(cd "$(dirname "$0")" && pwd)
num=$1; name=$2; shift 2
b=$D/run_${num}_${name}
if [ -e "$b.log" ]; then echo "$b.log exists: never overwrite a log"; exit 3; fi
{
  echo "# $(date '+%Y-%m-%d %H:%M:%S') cwd=$PWD host=$(hostname -s) load=$(uptime | sed 's/.*load averages*: //')"
  echo "# cmd: $*"
  if [ -n "$S3_TREE" ]; then
    for f in release/taylor_polar complex/release/taylor_polar; do
      p=$S3_TREE/phase2/nonradial/taylor_polar/target/$f
      [ -e "$p" ] && echo "# binary $f: $(md5 -q $p)"
    done
  fi
} > $b.log
RAYON_NUM_THREADS=2 nice -n 10 gtimeout 7200 "$@" >> $b.log 2> $b.err
echo $? > $b.rc
echo "$b rc=$(cat $b.rc)"
