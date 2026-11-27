#!/bin/sh
# runs of record of cminus1_mode.py (code commit 2f0eea2): worker 1 = derive, check, table, then the mutation runs of $1; worker 2 = the mutation runs of $2.
# usage: run_all.sh W1 "derive check table mut:j_sign ..." ; the arguments are item lists. Logs, errors and exit codes in this directory.
cd "$(dirname "$0")"
PY=~/Source/negative-mass/.venv/bin/python
SC=~/Source/negative-mass-i262/notes/black_universe/cminus1_mode.py
for item in $1; do
  case "$item" in
    derive|check|table)
      nice -n 10 $PY $SC $item > $item.log 2> $item.err; echo $? > $item.rc ;;
    mut:*)
      m=${item#mut:}
      : > mut_$m.log; : > mut_$m.err
      case "$m" in
        sym_pw|sym_gauge) cmds="derive" ;;
        j_sign|j_g1) cmds="derive check" ;;
        *) cmds="check" ;;
      esac
      rc=0
      for c in $cmds; do
        nice -n 10 $PY $SC $c --mutate=$m >> mut_$m.log 2>> mut_$m.err; r=$?; [ $r -ne 0 ] && rc=$r
      done
      echo $rc > mut_$m.rc ;;
  esac
done
echo done > worker_$2.done
