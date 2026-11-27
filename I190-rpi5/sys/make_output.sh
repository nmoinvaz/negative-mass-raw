#!/bin/bash
# writes notes/warp/implicit_taylor_lib_output.txt from the raw folder's logs (run from anywhere)
RAW=$HOME/Source/negative-mass-raw/I190-rpi5
OUT=$HOME/Source/negative-mass-i190/notes/warp/implicit_taylor_lib_output.txt
{
echo "== planted checks of tests/implicit.rs, final library run (run_20_default.log; multishoot 6bfd9b1's src, rebased as eaf55a8: digests equal, run_36 and run_37) =="
cat $RAW/summary_run_20.md
echo
echo "== planted values that moved between dev_04 (plain Cauchy sums) and run_20 (accumulators): cells that changed by more than a factor 3 =="
cat $RAW/summary_dev04_to_run20_changes.md
echo
echo "== the rebased branch, default and portable (run_36, run_37): result and digest lines =="
grep -E "^test result|^digest" $RAW/run_36_rebased_default.log
echo "-- portable"
grep -E "^test result|^digest" $RAW/run_37_rebased_portable.log
echo
echo "== the feature switch: the runs of record (arm_table.md) =="
cat $RAW/arm_table.md
echo
echo "== comparator (sys/compare_outputs.py), base against on =="
for p in "run_11_base_global.log run_32_on_global.log" "run_09_base_loglog.log run_30_on_loglog.log"; do echo "-- $p"; python3 $RAW/sys/compare_outputs.py $(for f in $p; do echo $RAW/$f; done); done
echo "-- offgrid ctl base against on (run_06, run_31), against on at the rebased head (run_42), against off (run_35)"
python3 $RAW/sys/compare_outputs.py $RAW/run_06_base_offgrid_ctl.log $RAW/run_31_on_offgrid_ctl.log $RAW/dump_base_ctl $RAW/dump_on_ctl3
python3 $RAW/sys/compare_outputs.py $RAW/run_06_base_offgrid_ctl.log $RAW/run_42_on_offgrid_ctl_r2.log $RAW/dump_base_ctl $RAW/dump_on_ctl_r2
python3 $RAW/sys/compare_outputs.py $RAW/run_06_base_offgrid_ctl.log $RAW/run_35_off_offgrid_ctl.log $RAW/dump_base_ctl $RAW/dump_off_ctl2
echo
echo "== the superseded feature-on runs, kept: run_07 (offgrid ctl) and run_10 (loglog) at multishoot ff24b6b =="
grep -E "^checks:|^\[FAIL\]" $RAW/run_10_on_loglog.log | cut -c1-300
echo
echo "== the plant_scale diagnosis (dev_08, dev_09) =="
cat $RAW/dev_08_plant_scale_diag.log $RAW/dev_09_plant_scale_diag_accumulator.log
} > $OUT 2>&1
wc -l $OUT
