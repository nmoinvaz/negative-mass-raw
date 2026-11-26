#!/bin/bash
# runrec.sh NAME CMD...: a run of record. Keeps stdout, stderr, exit code, /usr/bin/time -v (memory, reported only) and
# the machine's load at the start as RAW/NAME.{log,err,rc,time,env}; refuses to overwrite.
set -u
d=$(dirname "$(readlink -f "$0")")
n=$1; shift
for e in log err rc time env; do [ -e "$d/$n.$e" ] && { echo "refusing to overwrite $d/$n.$e" >&2; exit 2; }; done
{ date -Is; uptime; echo "host $(hostname) cores $(nproc)"; echo "cmd $*"; } >"$d/$n.env"
/usr/bin/time -v -o "$d/$n.time" "$@" >"$d/$n.log" 2>"$d/$n.err"
echo $? >"$d/$n.rc"
