#!/bin/bash
# s3_queue1b.sh: slot 1's runs after the old-pin chain: run_35 (R1 alone on the old tree), run_48 and run_49 (the step lists of the library at 75d1e1e and the lib_last4
# control), run_50 (the step counts under wide_table), run_42 (new-pin rows with the lib_plane binary, in a copy of the new tree, so slot 2's queue does not need it).
D=$(cd "$(dirname "$0")" && pwd)
SCR=/private/tmp/claude-501/-Users-nathan-Source-negative-mass-i192/49af8a24-a787-474c-b774-7b29bee02e53/scratchpad
RAW=$HOME/Source/negative-mass-raw
PY=$HOME/Source/negative-mass/.venv/bin/python
B=$HOME/Source/negative-mass-i192/phase2/nonradial/taylor_polar/target/bins
while [ ! -e $D/run_29_s3_old_complex.rc ]; do sleep 20; done
O=$SCR/trees/old; N2=$SCR/trees/new2
S3_TREE=$O $D/s3_run.sh 35 s3_old_R1 $PY $O/phase2/nonradial/taylor_polar.py --only=R1 --raw=$RAW
$D/s3_run.sh 48 s3_steps_default_vs_libtable_main $PY $D/s3_steps.py $B/new_default $B/new_libtable_main
$D/s3_run.sh 49 s3_steps_ctl_lib_last4_main $PY $D/s3_steps.py --mutate=lib_last4 $B/new_default $B/new_libtable_main
$D/s3_run.sh 50 s3_wide_count $PY $D/s3_wide_count.py $B/new_default $B/new_libtable_main
S3_TREE=$N2 $D/s3_run.sh 42 s3_new_rows_libplane $PY $N2/phase2/nonradial/taylor_polar.py --rows --raw=$RAW --jsonl-dir=$D/s3_jsonl/new_rows_libplane
