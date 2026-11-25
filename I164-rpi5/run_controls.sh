#!/bin/bash
# Runs check_quotes.py and recompute_jc.py plain (must exit 0) and with each --mutate= (must exit 1).
# usage: bash run_controls.sh   (from any directory). Logs go to controls/. Exits non-zero if any control behaves wrongly.
# Exit code 3 of a plain run means a check could not run (no pdftotext and no pdftext/ cache, or no sympy): reported as
# NOT RUN, and a mutation that exits 0 is reported as SILENT.
cd "$(dirname "$0")" || exit 2
PY=${PY:-python3}
mkdir -p controls
bad=0
run() { # name expected_rc cmd...
  local name=$1 want=$2; shift 2
  nice -n 10 "$@" > "controls/$name.log" 2>&1; local rc=$?
  if [ "$rc" -eq "$want" ]; then echo "ok      $name rc=$rc: $(tail -1 controls/$name.log)"
  elif [ "$rc" -eq 0 ]; then echo "SILENT  $name rc=0, want $want"; bad=1
  elif [ "$rc" -eq 3 ]; then echo "NOT RUN $name rc=3: $(tail -1 controls/$name.log)"; bad=1
  else echo "WRONG   $name rc=$rc want $want"; bad=1; fi
}
run check_plain 0 $PY -I check_quotes.py
for m in quote pdf cite dangling sha number absent cell quoted bullet entry loc lacks also; do run check_$m 1 $PY -I check_quotes.py --mutate=$m; done
run recompute_plain 0 $PY -I recompute_jc.py
for m in delta cross area w table; do run recompute_$m 1 $PY -I recompute_jc.py --mutate=$m; done
exit $bad
