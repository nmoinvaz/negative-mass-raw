#!/bin/bash
# usage: analyze.sh RUN BASELINE_LOG [BASELINE_DUMP RUN_DUMP]
#   RUN: the run's stem, e.g. run_06_on_ctl. Writes cmp_<RUN>.txt (compare_run.py), classify_<RUN>.txt, eta_<RUN>.txt (C4 at 1e-10),
#   loc_<RUN>.md (loc_report.py, with the baseline's classes) in RAW, and prints the one-line summaries.
here=$(cd "$(dirname "$0")" && pwd); . "$here/env.sh"
R=$1; BL=$2; BD=$3; RD=$4
cd "$RAW"
if [ -n "$BD" ]; then python3 "$here/compare_run.py" "$BL" "$R.log" "$BD" "$RD" > "cmp_$R.txt" 2>&1; else python3 "$here/compare_run.py" "$BL" "$R.log" > "cmp_$R.txt" 2>&1; fi
python3 "$here/classify_diff.py" "$BL" "$R.log" > "classify_$R.txt" 2>&1
echo "== $R: $(grep -E '^log lines compared' cmp_$R.txt)"; grep -E "^dump:" "cmp_$R.txt" | cut -c1-330
echo "   classify: $(head -1 classify_$R.txt)"
if [ -n "$BD" ]; then
  python3 "$here/compare_eta.py" "$BD" "$RD" 1e-10 > "eta_$R.txt" 2>&1; echo "   eta* (C4, 1e-10): $(sed -n 1,3p eta_$R.txt | tr '\n' ' ' | cut -c1-420) $(grep RESULT eta_$R.txt)"
  if [ -n "$(ls $RD | head -1)" ]; then python3 "$here/loc_report.py" "$RD" "$BD" > "loc_$R.md" 2>&1; sed -n 1p "loc_$R.md"; fi
fi
