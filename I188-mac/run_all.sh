#!/bin/zsh
# the runs of record of #188, two queues of one process each (at most two processes); numbers are fixed so that runs.txt orders the output
# usage: run_all.sh A | B | env ; the scipy references run_01 ... run_04 were made earlier by ref_chain.sh (and run_01 by hand)
D=$(cd "$(dirname "$0")" && pwd)
PY=$HOME/Source/negative-mass/.venv/bin/python
NR=$HOME/Source/negative-mass-i188/phase2/nonradial
RAW=$HOME/Source/negative-mass-raw
TP="$PY -u taylor_polar.py"
cd $NR
C="--complex --raw=$RAW --ref-dir=$D/ref --jsonl-dir=$D/jsonl_rec"
rec() { n=$1; shift; RUN_N=$n $D/runrec.sh "$@"; }
case $1 in
env)
  {
    echo "# code: $(git -C $NR rev-parse HEAD) branch $(git -C $NR rev-parse --abbrev-ref HEAD)"
    echo "# rustc: $(rustc --version); cargo: $(cargo --version)"
    echo "# python: $($PY --version 2>&1); numpy $($PY -c 'import numpy; print(numpy.__version__)'), scipy $($PY -c 'import scipy; print(scipy.__version__)'), mpmath $($PY -c 'import mpmath; print(mpmath.__version__)')"
    echo "# machine: $(sysctl -n machdep.cpu.brand_string), $(sysctl -n hw.ncpu) cores, $(uname -sr)"
    echo "# binaries (sha256), built in $NR/taylor_polar/target/bins:"
    (cd $NR/taylor_polar/target/bins && shasum -a 256 *) | sed 's/^/#   /'
    echo "# old_default and old_libplane: main 0d1d376 built before any edit (default, and --features lib_plane); new_*: this branch's head, default, --features complex, --features lib_plane"
  } > $D/run_00_env.log ;;
A)
  rec 5  R1_real_lanes_old_new ${=TP} ${=C} --only=R1
  rec 6  R2_complex_at_real_s ${=TP} ${=C} --only=R2
  rec 7  P1C_planted_complex_plane ${=TP} ${=C} --only=P1C
  rec 8  W0_counter_port_stored ${=TP} ${=C} --only=W0
  rec 12 L1C_lanes ${=TP} ${=C} --only=L1C
  rec 13 CXZ_planted_determinant ${=TP} ${=C} --only=CXZ
  rec 14 X1_box_b1_vs_scipy ${=TP} ${=C} --only=X1
  rec 15 X1b_box_b6_vs_scipy ${=TP} ${=C} --only=X1b
  rec 16 XR_Rs_independence ${=TP} ${=C} --only=XR
  rec 17 TC_time_per_D ${=TP} ${=C} --only=TC
  rec 18 tc_big_Rs $PY $D/tc_big_rs.py
  n=30
  for m in r1_ulp cx_recip_general bilinear redot f_scaled cx_mul_sign strip_off conj_s rs_shift strip_sign lowsum; do
    rec $n ctl_$m ${=TP} ${=C} --mutate=$m; n=$((n+1))
  done ;;
B)
  rec 9  CX2_counts_crate_evaluator ${=TP} ${=C} --only=CX2
  rec 10 XRc_counts_two_Rs ${=TP} ${=C} --only=XRc
  rec 11 default_mode_186_checks ${=TP}
  n=50
  for m in jsign moncrief swapcols mext0 star_eps shift_off reverse wrongdouble misplant onesided; do
    rec $n ctl_$m ${=TP} ${=C} --mutate=$m; n=$((n+1))
  done ;;
esac
