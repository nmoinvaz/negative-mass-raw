#!/bin/sh
# runs of record: usage runrec.sh base | runrec.sh NAME...   (logs are never overwritten: the next free _run<N> is used)
cd "$(dirname "$0")" || exit 1
PY=~/Source/negative-mass/.venv/bin/python
SCRIPT=~/Source/negative-mass-i269/notes/black_universe/exact_mode.py
next() { n=1; while [ -e "$1_run$n.log" ]; do n=$((n+1)); done; echo $n; }
run() { # run TAG ARGS...
  tag=$1; shift; n=$(next "$tag")
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 10 "$PY" "$SCRIPT" "$@" > "${tag}_run$n.log" 2>&1
  echo "rc=$?" >> "${tag}_run$n.log"; echo "${tag}_run$n"
}
if [ "$1" = base ]; then
  run derive derive; run check check
else
  for m in "$@"; do
    d=$(run "m_${m}_derive" derive --mutate=$m); k=$(run "m_${m}_check" check --mutate=$m)
    cat "$d.log" "$k.log" > "m_${m}.log"      # the union of the fired sets is read from m_<name>.log
  done
fi
