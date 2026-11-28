#!/bin/bash
# runrec.sh NAME CMD...: a run of record. Keeps stdout, stderr, exit code, /usr/bin/time -l (memory, reported only) and the machine's load
# at the start as RAW/NAME.{log,err,rc,time,env}; refuses to overwrite.
set -u
d=$(cd "$(dirname "$0")" && pwd)
n=$1; shift
for e in log err rc time env; do [ -e "$d/$n.$e" ] && { echo "refusing to overwrite $d/$n.$e" >&2; exit 2; }; done
{ date -u +%Y-%m-%dT%H:%M:%SZ; uptime; echo "host $(hostname) cores $(sysctl -n hw.ncpu)"; echo "cmd $*"; } >"$d/$n.env"
/usr/bin/time -l -o "$d/$n.time" "$@" >"$d/$n.log" 2>"$d/$n.err"
echo $? >"$d/$n.rc"
