#!/bin/bash
# runrec.sh NAME CMD...: run CMD at nice 10 in the worktree's notes dir; keep stdout NAME.log, stderr NAME.err, exit code NAME.rc
# Never overwrites: refuses if NAME.log exists (number reruns).
name="$1"; shift
here="$(cd "$(dirname "$0")" && pwd)"
if [ -e "$here/$name.log" ]; then echo "exists: $name.log" >&2; exit 2; fi
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1
cd /Users/nathan/Source/negative-mass-i34/notes/wormhole_next || exit 3
start=$(date +%s)
nice -n 10 "$@" > "$here/$name.log" 2> "$here/$name.err"
rc=$?
echo "$rc" > "$here/$name.rc"
echo "# wall $(( $(date +%s) - start )) s, exit $rc" >> "$here/$name.log"
exit $rc
