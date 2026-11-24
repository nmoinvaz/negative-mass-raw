#!/bin/bash
# One control at a time, nice 10, one thread. Log ctl_<name>.log, exit code ctl_<name>.rc, stderr ctl_<name>.err.
PY=/home/nathan/Source/negative-mass-venv314/bin/python
WT=/home/nathan/Source/negative-mass-i73
RAW=/home/nathan/Source/negative-mass-raw/I73-rpi5
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd "$WT" || exit 1
for m in disc-sign no-rank num-drop-w2 num-static accel-static accel-lapse alc-drop-w2 drop-accel time-lemma-sign weight-break parity-break axis-flip rest-v; do
  [ -f "$RAW/ctl_$m.rc" ] && continue
  echo "$(date +%T) start $m" >> "$RAW/controls_queue.log"
  nice -n 10 "$PY" "$WT/notes/warp/he_accel.py" --mutate=$m > "$RAW/ctl_$m.log" 2> "$RAW/ctl_$m.err"
  echo $? > "$RAW/ctl_$m.rc"
  echo "$(date +%T) end $m rc=$(cat $RAW/ctl_$m.rc)" >> "$RAW/controls_queue.log"
done
m=ps-accel-static
echo "$(date +%T) start $m" >> "$RAW/controls_queue.log"
nice -n 10 "$PY" "$WT/notes/warp/phantom_source.py" --mutate=accel-static > "$RAW/ctl_$m.log" 2> "$RAW/ctl_$m.err"
echo $? > "$RAW/ctl_$m.rc"
echo "$(date +%T) end $m rc=$(cat $RAW/ctl_$m.rc)" >> "$RAW/controls_queue.log"
echo done > "$RAW/controls_all.done"
