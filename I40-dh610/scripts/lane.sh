#!/bin/bash
# usage: lane.sh LANE   one lane of the run queue (runs/queue.txt): takes the next line atomically and runs it until the queue is empty.
#   G6             the D = 6 growth control (threshold.py g6), into runs/g6
#   BARRIER g6     wait until runs/g6/job.rc exists; stop this lane if it is not rc=0
#   JOB D fam h flags    threshold.py job into runs/D<D>_<fam>_h<h:.6g>; at most 2 h (timeout), rc 124 means stopped by the limit
# Every job writes <dir>/job.{start,log,err,time,rc,lane}; /usr/bin/time -v reports the memory. Nothing is overwritten.
LANE=$1
RAW=${RAW:-$HOME/Source/negative-mass-raw/I40-dh610}
Q=$RAW/runs/queue.txt
TH=$HOME/Source/negative-mass-i40/notes/wormhole_evolution/threshold.py
PY=$HOME/Source/negative-mass-venv314/bin/python
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
run() {  # dir, command...
  local dir=$1; shift
  mkdir -p "$dir"
  if [ -e "$dir/job.rc" ]; then echo "$dir already has a result; not overwriting" >&2; return; fi
  echo "$LANE" > "$dir/job.lane"
  echo "start $(date -Is) load $(cut -d' ' -f1-3 /proc/loadavg) host $(hostname) lane $LANE" > "$dir/job.start"
  /usr/bin/time -v -o "$dir/job.time" timeout --signal=TERM --kill-after=60 7200 "$@" > "$dir/job.log" 2> "$dir/job.err"
  echo "rc=$?" > "$dir/job.rc"
}
while true; do
  line=$(flock "$Q.lock" bash -c 'head -1 "$1"; sed -i 1d "$1"' _ "$Q")
  [ -z "$line" ] && break
  set -- $line
  case $1 in
    G6) run "$RAW/runs/g6" $PY $TH g6 --out="$RAW/runs/g6" ;;
    BARRIER)
      while [ ! -e "$RAW/runs/$2/job.rc" ]; do sleep 30; done
      grep -q "rc=0" "$RAW/runs/$2/job.rc" || { echo "barrier $2 failed: lane $LANE stops" >&2; exit 3; } ;;
    JOB) D=$2; fam=$3; h=$4; shift 4
         label=$(printf '%.6g' $h)
         run "$RAW/runs/D${D}_${fam}_h${label}" $PY $TH job --D=$D --family=$fam --h=$h --out="$RAW/runs/D${D}_${fam}_h${label}" "$@" ;;
  esac
done
