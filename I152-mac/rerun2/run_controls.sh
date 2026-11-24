#!/bin/bash
# Runs check_quotes.py plain (must exit 0) and with each mutation (must exit 1), and jovera_check.py likewise.
# usage: bash run_controls.sh   (from this folder). Logs go to controls/. Exits non-zero if any control behaves wrongly.
cd "$(dirname "$0")" || exit 2
mkdir -p controls
bad=0
run() { # name expected_rc cmd...
  local name=$1 want=$2; shift 2
  nice -n 10 "$@" > "controls/$name.log" 2>&1; local rc=$?
  if [ "$rc" -eq "$want" ]; then echo "ok    $name rc=$rc: $(tail -1 controls/$name.log)"; else echo "WRONG $name rc=$rc want $want"; bad=1; fi
}
run check_plain 0 python3 -I check_quotes.py
for m in quote pdf cite dangling sha number absent cell quoted bullet; do run check_$m 1 python3 -I check_quotes.py --mutate=$m; done
run jovera_plain 0 python3 -I jovera_check.py
for m in G1 p0 exponent lam; do run jovera_$m 1 python3 -I jovera_check.py --mutate=$m; done
exit $bad
