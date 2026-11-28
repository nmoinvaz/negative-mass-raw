#!/bin/bash
# planted_family_output.txt of the repository: the check of record, then the mutations' fired sets; run from I277-mac/runs
OUTF=${1:-planted_family_output.txt}
{
  echo "# planted_family.py check: the run of record (negative-mass-raw I277-mac/runs/check_none.log, exit code $(cat check_none.rc))"
  cat check_none.log
  echo
  echo "# planted_family.py mutations: fired sets of the twelve mutated runs (I277-mac/runs/check_<name>.log, all exit code 1) against the declared ones"
  cat mutations.log
  echo
  echo "# effects of the mutations (from I277-mac/runs/check_<name>.log): sup|r - lam R| at c = -1.5, beta = -0.05, h = 0.00125, and the v* errors at the five h"
  for m in beta_sign kh kf rate gauge_frozen th_coef vterm_sign vterm_coef Vp_sign V_sign_f eps_sign vfit_K; do
    sup=$(grep -E "^  run c = -1.5, beta = -0.05, h = 0.00125" check_$m.log | sed -E 's/.*sup\|dr\| ([0-9.e+-]+) at.*/\1/')
    v1=$(grep -E "^  c = -1.5, beta = -0.05: v\* = " check_$m.log | sed -E 's/.*errors ([^;]*);.*/\1/')
    v2=$(grep -E "^  c = -1.0, beta = -0.05: v\* = " check_$m.log | sed -E 's/.*errors ([^;]*);.*/\1/')
    echo "$m: sup|dr| $sup; v* errors c = -1.5: $v1; c = -1: $v2"
  done
  echo
  echo "# planted_family.py rays: reported diagnostic (I277-mac/runs/rays.log; added after the runs of record, commit c883a16; the final script's check reproduces check_none.log: final_check_none.log)"
  cat rays.log
} > "$OUTF"
