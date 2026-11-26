#!/bin/zsh
# run_lib.sh: the runs of record of multishoot's plane tests and of its full suite, on the default backend (aarch64 NEON) and with
# --features portable; one process at a time, nice 10, 2 threads. Output: run_NN_<name>.{log,err,rc} in this folder.
D=$(cd "$(dirname "$0")" && pwd)
CL=/Users/nathan/Source/negative-mass-i189-libs/multishoot
n=${1:-17}
run() {  # run NAME CMD...
  name=$1; shift
  b=$D/run_$(printf "%02d" $n)_$name
  { echo "# $(date '+%Y-%m-%d %H:%M:%S') cwd=$CL load $(uptime | sed 's/.*load averages: //')"; echo "# multishoot $(git -C $CL rev-parse --short HEAD)"; echo "# cmd: $*"; } > $b.log
  ( cd $CL && RAYON_NUM_THREADS=2 nice -n 10 timeout 3600 /usr/bin/time -l "$@" >> $b.log 2> $b.err )
  echo $? > $b.rc
  echo "$(date '+%H:%M:%S') $b rc=$(cat $b.rc)" >> $D/run_lib.progress
  n=$((n+1))
}
run plane_default_mutate cargo test --release -j 2 --features mutate --test plane -- --test-threads=2 --nocapture
run plane_portable_mutate cargo test --release -j 2 --features portable,mutate --test plane -- --test-threads=2 --nocapture
run plane_default cargo test --release -j 2 --test plane -- --test-threads=2 --nocapture
run suite_default_mutate cargo test --release -j 2 --features mutate -- --test-threads=2
run suite_portable_mutate cargo test --release -j 2 --features portable,mutate -- --test-threads=2
run fmt_clippy zsh -c 'cargo fmt --check && cargo clippy --all-targets --features mutate -- -D warnings && cargo clippy --all-targets --features portable,mutate -- -D warnings && cargo clippy --all-targets -- -D warnings && echo ALL CLEAN'
