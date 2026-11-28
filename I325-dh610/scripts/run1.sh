#!/bin/bash
# usage: run1.sh DIR TIMEOUT_S CMD...   one run in the worktree's notes/wormhole_evolution, as I228's lane.sh ran a RUN line, for one command.
#   DIR is relative to RAW. Writes DIR/job.{start,log,err,time,rc}. A DIR that already has job.rc is not rerun; a DIR without job.rc (a dead run) is renamed DIR.partialN first.
#   Nothing is overwritten. @RAW@ and @PY@ in CMD are substituted. A dependency (a path that must exist first) is given as WAITFOR=<path> in the environment and is waited for
#   inside the run, so that no other lane can start it before the dependency exists.
RAW=${RAW:-$HOME/Source/negative-mass-raw/I325-dh610}
WT=$HOME/Source/negative-mass-i325/notes/wormhole_evolution
PY=$HOME/Source/negative-mass-venv314/bin/python
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
dir=$RAW/$1; to=$2; shift 2
args=()
for a in "$@"; do a=${a//@RAW@/$RAW}; a=${a//@PY@/$PY}; args+=("$a"); done
if [ -e "$dir/job.rc" ]; then echo "$dir already has a result; not rerun" >&2; exit 0; fi
if [ -d "$dir" ] && [ -n "$(ls -A "$dir" 2>/dev/null)" ]; then
  k=1; while [ -e "$dir.partial$k" ]; do k=$((k+1)); done; mv "$dir" "$dir.partial$k"
fi
mkdir -p "$dir"
if [ -n "$WAITFOR" ]; then
  while [ ! -e "$WAITFOR" ]; do sleep 30; done
fi
echo "start $(date -Is) load $(cut -d' ' -f1-3 /proc/loadavg) host $(hostname) cmd: ${args[*]}" > "$dir/job.start"
( cd "$WT" && exec /usr/bin/time -v -o "$dir/job.time" timeout --signal=TERM --kill-after=60 "$to" "${args[@]}" > "$dir/job.log" 2> "$dir/job.err" )
echo "rc=$?" > "$dir/job.rc"
