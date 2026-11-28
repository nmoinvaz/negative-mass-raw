#!/bin/bash
# run_one.sh BASE [TIMEOUT_S]: Singular on BASE.sing at nice 10, one thread, with a stop (default 3600 s).
# Writes BASE.out, .err, .time (/usr/bin/time -v) and BASE.rc. Refuses to overwrite: a rerun uses a new BASE.
set -u
base="$1"; to="${2:-3600}"
for x in out err time rc; do [ -e "$base.$x" ] && { echo "refusing: $base.$x exists" >&2; exit 2; }; done
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
nice -n 10 /usr/bin/time -v -o "$base.time" timeout "$to" /usr/bin/Singular -q "$base.sing" > "$base.out" 2> "$base.err" < /dev/null
echo $? > "$base.rc"
