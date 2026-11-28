#!/bin/sh
# usage: runx.sh TAG ARGS...  -> runs the worktree's exact_mode.py ARGS at nice 10, one thread; log TAG_run<N>.log (N = next free number)
cd "$(dirname "$0")" || exit 1
tag=$1; shift
n=1
while [ -e "${tag}_run$n.log" ]; do n=$((n+1)); done
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 10 ~/Source/negative-mass/.venv/bin/python ~/Source/negative-mass-i269/notes/black_universe/exact_mode.py "$@" > "${tag}_run$n.log" 2>&1
echo "rc=$?" >> "${tag}_run$n.log"
