#!/bin/bash
# usage: queue_members.sh JOBS RESDIR   -- a worker; lines of JOBS: "id res stage". Under flock each worker takes the next line (qpos), so several
# copies share the queue. A finished JSON is never overwritten. Exit codes and times in RESDIR/status.txt.
RAW=$HOME/Source/negative-mass-raw/I223-rpi5
PY=$HOME/Source/negative-mass-venv314/bin/python
JOBS=$1; RESDIR=$RAW/$2; mkdir -p $RESDIR
cd $HOME/Source/negative-mass-i223/notes/black_universe || exit 1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
while true; do
  line=$(flock $RESDIR/queue.lock bash -c "n=\$(cat $RESDIR/qpos 2>/dev/null || echo 0); n=\$((n+1)); echo \$n > $RESDIR/qpos; sed -n \${n}p $JOBS")
  [ -z "$line" ] && break
  set -- $line; id=$1; res=$2; stage=$3
  f=$RESDIR/${id}_${res}; [ "$stage" = low ] && f=${f}_low
  [ -f $f.json ] && continue
  start=$(date +%s)
  /usr/bin/time -v nice -n 10 $PY bounce.py count $id --res=$res --stage=$stage --out=$f.json > $f.log 2>&1
  echo "$id $res $stage exit $? $(( $(date +%s) - start )) s $(date +%H:%M:%S)" >> $RESDIR/status.txt
done
