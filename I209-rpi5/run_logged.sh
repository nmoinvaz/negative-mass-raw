#!/bin/bash
# run_logged.sh LOG CMD... : run CMD in the cwd with /usr/bin/time -v, append stdout and stderr to LOG, end LOG with "exit=<code>"
log="$1"; shift
{ echo "# start $(date -Is) cwd=$PWD cmd=$*"; /usr/bin/time -v "$@"; echo "exit=$?"; echo "# end $(date -Is)"; } >> "$log" 2>&1
