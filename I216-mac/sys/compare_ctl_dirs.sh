#!/bin/bash
# usage: compare_ctl_dirs.sh BASE_DIR RUN_DIR   the comparator on every ctl_*.log pair (each control's own log), and the exit codes of the .rc files
here=$(cd "$(dirname "$0")" && pwd)
n=0; bad=0; rcdiff=0
for f in "$1"/ctl_*.log; do
  b=$(basename "$f"); [ -e "$2/$b" ] || { echo "missing in run: $b"; bad=$((bad+1)); continue; }
  n=$((n+1))
  python3 "$here/compare_outputs.py" "$f" "$2/$b" > /tmp/cmp_ctl_$$.txt || { bad=$((bad+1)); echo "== $b"; head -6 /tmp/cmp_ctl_$$.txt | cut -c1-300; }
  r=${b%.log}.rc
  [ "$(cat "$1/$r" 2>/dev/null)" = "$(cat "$2/$r" 2>/dev/null)" ] || { rcdiff=$((rcdiff+1)); echo "exit code differs: $r"; }
done
echo "control logs compared: $n; with gated differences or missing: $bad; exit codes that differ: $rcdiff"
exit $((bad + rcdiff > 0))
