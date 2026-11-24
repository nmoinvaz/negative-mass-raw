#!/bin/bash
# Final run of record: checks, then every control, as one process at nice 10. Usage: run_final.sh NN
# stdout goes to notes/warp/conical_limit_output.txt (and a copy run_NN.log); stderr to run_NN.err; exit code to run_NN.rc.
NN=${1:-01}
RAW=/home/nathan/Source/negative-mass-raw/I159-rpi5
NR=/home/nathan/Source/negative-mass-i159
PY=/home/nathan/Source/negative-mass-venv314/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd "$NR" || exit 2
/usr/bin/time -v -o "$RAW/run_$NN.time" "$PY" notes/warp/conical_limit.py --logdir="$RAW" \
  > "$RAW/run_$NN.log" 2> "$RAW/run_$NN.err"
echo $? > "$RAW/run_$NN.rc"
cp "$RAW/run_$NN.log" notes/warp/conical_limit_output.txt
