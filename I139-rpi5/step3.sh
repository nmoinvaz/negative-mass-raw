#!/bin/bash
# usage: step3.sh planted | real | controls
# Runs compare_brackets.py of the i139 worktree, one process at a time, nice 10. Logs and exit codes in step3/NAME.log, NAME.rc.
RAW=$HOME/Source/negative-mass-raw/I139-rpi5
WT=$HOME/Source/negative-mass-i139
PY=$HOME/Source/negative-mass-venv314/bin/python
THEIRS=$HOME/Source/negative-mass-raw/I104-rpi5/sweep_brackets.csv
OURS=$RAW/brackets_i2.csv
P=$RAW/planted
mkdir -p "$RAW/step3"
cd "$WT/phase2/dg_proof" || exit 99
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
run() { name=$1; shift; nice -n 10 "$PY" compare_brackets.py "$@" > "$RAW/step3/$name.log" 2> "$RAW/step3/$name.err"; echo $? > "$RAW/step3/$name.rc"; }
case $1 in
  planted)
    run P1 --ours=$P/ours_p1.csv --theirs=$P/theirs_a.csv --lmax=4
    run P2 --ours=$P/ours_p2.csv --theirs=$P/theirs_b.csv --lmax=3
    run P3 --ours=$P/ours_p3.csv --theirs=$P/theirs_b.csv --lmax=3
    run P4 --ours=$P/ours_p4.csv --theirs=$P/theirs_a.csv --lmax=4
    run P5 --ours=$P/ours_p5.csv --theirs=$P/theirs_a.csv --lmax=4
    run P6 --ours=$P/ours_p6.csv --theirs=$P/theirs_a.csv --lmax=4 ;;
  real)
    run real --ours=$OURS --theirs=$THEIRS ;;
  controls)
    for m in shift drop swap; do run mutate_$m --ours=$OURS --theirs=$THEIRS --mutate=$m; done ;;
  *) echo "usage: step3.sh planted | real | controls"; exit 2 ;;
esac
