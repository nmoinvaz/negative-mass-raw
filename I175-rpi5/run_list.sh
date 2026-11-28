#!/bin/bash
# run_list.sh LISTFILE [TIMEOUT_S]: runs run_one.sh on each base path in LISTFILE, one after the other, skipping a base
# whose .rc exists. One worker = one process; start up to 3 workers on disjoint lists.
set -u
here="$(cd "$(dirname "$0")" && pwd)"
while read -r base; do
  [ -z "$base" ] && continue
  [ -e "$base.rc" ] && continue
  "$here/run_one.sh" "$base" "${2:-3600}"
done < "$1"
