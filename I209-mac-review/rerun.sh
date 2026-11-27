#!/bin/bash
# rerun.sh: #209's run of record (run_03) on this Mac, from the review worktree
here=$(cd "$(dirname "$0")" && pwd)
cd /Users/nathan/Source/negative-mass-r209/notes/wormhole_largeD || exit 2
n=rerun_run_03_all_ctlsum
[ -e "$here/$n.log" ] && { echo "refusing to overwrite" >&2; exit 2; }
{ echo "# $(date -u +%FT%TZ) $(uptime)"; /usr/bin/time -l nice -n 10 /Users/nathan/Source/negative-mass/.venv/bin/python -u exchange_review.py sym exact clausen exch grid ctlsum 2>&1; echo "exit $?"; } > "$here/$n.log" 2>&1
