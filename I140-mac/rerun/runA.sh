#!/bin/bash
# Mac rerun of #140: retab (and its 3 mutations), the window part (and abscut), the v_c part (and nosplit), drive_part_tanh.
S=/private/tmp/claude-501/-Users-nathan-Source-negative-mass/27911ca3-2259-460a-98f6-94387039554a/scratchpad
WT=$S/wt140; OUT=$S/r140; PY=$HOME/Source/negative-mass/.venv/bin/python; RAW=$HOME/Source/negative-mass-raw/I140-rpi5
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
cd "$WT" || exit 1
run() { local name=$1; shift; local t0=$(date +%s); nice -n 10 "$PY" -X utf8 "$@" > "$OUT/$name.log" 2>&1; local rc=$?; echo "$name rc=$rc s=$(( $(date +%s) - t0 ))" >> "$OUT/runA.log"; }
run retab_mac $RAW/retab.py --tag=mac --ts=$WT/notes/warp --csv=$OUT/retab_mac.csv
for m in abscut nearcut notie; do run retab_mac_$m $RAW/retab.py --tag=mac --ts=$WT/notes/warp --mutate=$m --csv=$OUT/retab_mac_$m.csv; done
run window notes/warp/tanh_spectrum.py --part=window
run window_abscut notes/warp/tanh_spectrum.py --part=window --mutate=abscut
run vc notes/warp/tanh_spectrum_check.py --part=vc
run vc_nosplit notes/warp/tanh_spectrum_check.py --part=vc --mutate=nosplit
echo done >> "$OUT/runA.log"
