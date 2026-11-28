#!/bin/bash
# planted_family_output.txt of the repository: the check of record, then the mutations' fired sets; run from I277-mac/runs
OUTF=${1:-planted_family_output.txt}
{
  echo "# planted_family.py check: the run of record (negative-mass-raw I277-mac/runs/check_none.log, exit code $(cat check_none.rc))"
  cat check_none.log
  echo
  echo "# planted_family.py mutations: fired sets of the twelve mutated runs (I277-mac/runs/check_<name>.log, all exit code 1) against the declared ones"
  cat mutations.log
} > "$OUTF"
