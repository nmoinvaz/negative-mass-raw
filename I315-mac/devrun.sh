#!/bin/bash
# devrun.sh NAME CMD...: run CMD with stdout, stderr and exit code kept as RAW/NAME.{log,err,rc}; refuses to overwrite
set -u
d=$(cd "$(dirname "$0")" && pwd)
n=$1; shift
for e in log err rc; do [ -e "$d/$n.$e" ] && { echo "refusing to overwrite $d/$n.$e" >&2; exit 2; }; done
"$@" >"$d/$n.log" 2>"$d/$n.err"
echo $? >"$d/$n.rc"
