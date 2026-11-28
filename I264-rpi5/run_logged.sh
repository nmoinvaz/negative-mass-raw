#!/bin/bash
# usage: run_logged.sh NAME CMD ARGS...   stdout NAME.log, stderr NAME.err, exit code NAME.rc, load and time in NAME.env; refuses to overwrite
cd "$(dirname "$0")" || exit 2
N=$1; shift
for e in log err rc env; do [ -e "$N.$e" ] && { echo "$N.$e exists" >&2; exit 3; }; done
{ date -u +%FT%TZ; uptime; echo "cmd: $*"; } > "$N.env"
/usr/bin/time -v -o "$N.time" "$@" > "$N.log" 2> "$N.err"
echo $? > "$N.rc"
date -u +%FT%TZ >> "$N.env"
