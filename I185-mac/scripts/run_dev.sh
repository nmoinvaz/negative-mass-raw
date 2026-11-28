#!/bin/zsh
# dev logs of #185: all checks, then each mutation on its target checks. Usage: run_dev.sh WT RAW   (WT = worktree, RAW = this folder)
WT=$1; RAW=$2
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
cd $WT || exit 2
n=1
run() {  # name, args...
  name=$1; shift
  out=$RAW/dev/dev_$(printf %02d $n)_$name
  nice -n 10 $PY notes/warp/conical_eta0.py "$@" > $out.log 2> $out.err; echo $? > $out.rc
  n=$((n+1))
}
run checks --no-controls
run red-factor --mutate=red-factor --only=reduction
run bal-weight --mutate=bal-weight --only=planted
run n-c33 --mutate=n-c33 --only=table,kappa_symbolic
run ift-sq --mutate=ift-sq --only=ift_row1
run floor-sign --mutate=floor-sign --only=floor15
run iia-sign --mutate=iia-sign --only=iia_exists
run cross-root --mutate=cross-root --only=kappa_cross
run retrace-root --mutate=retrace-root --only=kappa_retrace
echo done > $RAW/dev/dev_done
