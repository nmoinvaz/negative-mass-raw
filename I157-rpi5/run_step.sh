#!/bin/bash
# usage: run_step.sh NAME CMD...   one process at nice 10, one thread; stdout+stderr to logs/NAME.log, exit code to logs/NAME.rc,
# peak resident size and times to logs/NAME.time (/usr/bin/time -v). Refuses to overwrite a log.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
N="$1"; shift
[ -e "$D/logs/$N.log" ] && { echo "logs/$N.log exists; number the rerun" >&2; exit 2; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
nice -n 10 /usr/bin/time -v -o "$D/logs/$N.time" "$@" > "$D/logs/$N.log" 2>&1
echo $? > "$D/logs/$N.rc"
