#!/bin/bash
# usage: lane.sh LANE   one lane of a queue ($Q, default RAW/queue.txt): takes the next line atomically and runs it until the queue is empty. Line formats:
#   RUN <dir-relative-to-RAW> <timeout_s> <command...>   runs the command in the worktree's notes/wormhole_evolution; @RAW@ and @PY@ are substituted;
#                                                         writes <dir>/job.{start,log,err,time,rc,lane}; a dir with job.rc is not rerun; a dir without
#                                                         job.rc (a dead run) is renamed <dir>.partialN first. Nothing is overwritten.
#   WAIT <path>                                           waits until the path exists (a dependency)
LANE=$1
RAW=${RAW:-$HOME/Source/negative-mass-raw/I228-dh610}
Q=${Q:-$RAW/queue.txt}
WT=$HOME/Source/negative-mass-i228/notes/wormhole_evolution
PY=$HOME/Source/negative-mass-venv314/bin/python
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
while true; do
  line=$(flock "$Q.lock" bash -c 'head -1 "$1"; sed -i 1d "$1"' _ "$Q")
  [ -z "$line" ] && break
  line=${line//@RAW@/$RAW}; line=${line//@PY@/$PY}
  set -- $line
  case $1 in
    WAIT) while [ ! -e "$2" ]; do sleep 30; done ;;
    RUN)
      dir=$RAW/$2; to=$3; shift 3
      if [ -e "$dir/job.rc" ]; then echo "$dir already has a result; not rerun" >&2; continue; fi
      if [ -d "$dir" ] && [ -n "$(ls -A "$dir" 2>/dev/null)" ]; then
        k=1; while [ -e "$dir.partial$k" ]; do k=$((k+1)); done; mv "$dir" "$dir.partial$k"
      fi
      mkdir -p "$dir"; echo "$LANE" > "$dir/job.lane"
      echo "start $(date -Is) load $(cut -d' ' -f1-3 /proc/loadavg) host $(hostname) lane $LANE cmd: $*" > "$dir/job.start"
      ( cd "$WT" && exec /usr/bin/time -v -o "$dir/job.time" timeout --signal=TERM --kill-after=60 "$to" "$@" > "$dir/job.log" 2> "$dir/job.err" )
      echo "rc=$?" > "$dir/job.rc" ;;
  esac
done
