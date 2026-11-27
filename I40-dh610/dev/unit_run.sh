#!/bin/bash
# usage: unit_run.sh <logbase> <command...>   stdout -> <logbase>.log, stderr -> .err, /usr/bin/time -v -> .time, exit code -> .rc
base=$1; shift
echo "start $(date -Is) load $(cut -d' ' -f1-3 /proc/loadavg) host $(hostname)" > "$base.start"
/usr/bin/time -v -o "$base.time" "$@" > "$base.log" 2> "$base.err"
echo "rc=$?" > "$base.rc"
