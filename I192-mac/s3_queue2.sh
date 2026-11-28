#!/bin/bash
# s3_queue2.sh: the second slot's runs, one after the other (run numbers in A9 of the README):
#  40 new-pin default mode, 41 new-pin rows, 44 lib_table default mode, 45 lib_table rows, 46 and 47 `--mutate=wide_table` on the new-pin and lib_table default builds,
#  43 new-pin complex, 42 new-pin rows with the lib_plane binary.
D=$(cd "$(dirname "$0")" && pwd)
SCR=/private/tmp/claude-501/-Users-nathan-Source-negative-mass-i192/49af8a24-a787-474c-b774-7b29bee02e53/scratchpad
RAW=$HOME/Source/negative-mass-raw
PY=$HOME/Source/negative-mass/.venv/bin/python
sw() { # TREE BINARY-NAME: the tree's release binary
  cp $1/phase2/nonradial/taylor_polar/target/bins/$2 $1/phase2/nonradial/taylor_polar/target/release/taylor_polar; }
nr() { echo $1/phase2/nonradial; }
N=$SCR/trees/new; L=$SCR/trees/libtable
sw $N new_default
S3_TREE=$N $D/s3_run.sh 40 s3_new_default_mode $PY $(nr $N)/taylor_polar.py --raw=$RAW
S3_TREE=$N $D/s3_run.sh 41 s3_new_rows $PY $(nr $N)/taylor_polar.py --rows --raw=$RAW --jsonl-dir=$D/s3_jsonl/new_rows
sw $L libtable_default
S3_TREE=$L $D/s3_run.sh 44 s3_libtable_default_mode $PY $(nr $L)/taylor_polar.py --raw=$RAW
S3_TREE=$L $D/s3_run.sh 45 s3_libtable_rows $PY $(nr $L)/taylor_polar.py --rows --raw=$RAW --jsonl-dir=$D/s3_jsonl/libtable_rows
S3_TREE=$N $D/s3_run.sh 46 s3_new_ctl_wide_table $PY $(nr $N)/taylor_polar.py --mutate=wide_table --raw=$RAW
S3_TREE=$L $D/s3_run.sh 47 s3_libtable_ctl_wide_table $PY $(nr $L)/taylor_polar.py --mutate=wide_table --raw=$RAW
S3_TREE=$N $D/s3_run.sh 43 s3_new_complex $PY $(nr $N)/taylor_polar.py --complex --raw=$RAW --bins=$N/phase2/nonradial/taylor_polar/target/bins --ref-dir=$RAW/I188-mac/ref --jsonl-dir=$D/s3_jsonl/new_complex
sw $N new_libplane
S3_TREE=$N $D/s3_run.sh 42 s3_new_rows_libplane $PY $(nr $N)/taylor_polar.py --rows --raw=$RAW --jsonl-dir=$D/s3_jsonl/new_rows_libplane
