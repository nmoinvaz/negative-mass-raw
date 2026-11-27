#!/bin/bash
# I206-mac: the runs of record, at the clone's head commit, one process group at a time (nice 10, -j 2, RAYON_NUM_THREADS=2).
# usage: run_records.sh   (logs run_NN_*.log and .rc in the raw folder; the clone must be clean)
CLONE=$HOME/Source/negative-mass-i206-libs/multisolver
RAW=$HOME/Source/negative-mass-raw/I206-mac
SP=/private/tmp/claude-501/-Users-nathan-Source-negative-mass-i206-libs-multisolver/84294958-42d6-4032-9618-1096d90926ff/scratchpad
export RAYON_NUM_THREADS=2
cd "$CLONE" || exit 1
{ git rev-parse HEAD; git status --short; } > "$RAW/run_00_commit.txt"
step() { # name, command...
  local name=$1; shift
  date -u +%FT%TZ > "$RAW/$name.started"
  ( time "$@" ) > "$RAW/$name.log" 2>&1
  echo $? > "$RAW/$name.rc"
  date -u +%FT%TZ > "$RAW/$name.finished"
}
step run_01_locate_default   nice -n 10 cargo test --release -j 2 --test locate -- --nocapture
step run_01b_unit_doc_default bash -c "nice -n 10 cargo test --release -j 2 --lib locate:: && nice -n 10 cargo test --release -j 2 --doc locate"
step run_02_locate_portable  nice -n 10 cargo test --release -j 2 --features portable --test locate -- --nocapture
step run_02b_unit_doc_portable bash -c "nice -n 10 cargo test --release -j 2 --features portable --lib locate:: && nice -n 10 cargo test --release -j 2 --features portable --doc locate"
"$RAW/sys/run_explore.sh" run_03_explore_new_grid 0.2,0.3,0.4,0.5,0.6,0.7,0.8
step run_04_build_explore_rust bash -c "cd $RAW/sys/explore_rust && CARGO_TARGET_DIR=$SP/explore_rust_target nice -n 10 cargo build --release -j 2"
step run_04_explore_rust nice -n 10 "$SP/explore_rust_target/release/explore_rust" "$RAW/run_03_explore_new_grid_s1_series.txt" "$RAW/run_03_explore_new_grid_s2_series.txt"
step run_05_report nice -n 10 cargo test --release -j 2 --test locate late_windows_report -- --ignored --nocapture --test-threads 1
step run_06_d6_grids nice -n 10 cargo test --release -j 2 --test locate d6_grid_report -- --ignored --nocapture
step run_07_weak_sweep nice -n 10 cargo test --release -j 2 --test locate weak_sweep -- --ignored --nocapture --test-threads 1
step run_08_fmt cargo fmt --check
step run_08_clippy_default  env CARGO_TARGET_DIR="$SP/clippy_target" nice -n 10 cargo clippy --all-targets -j 2 -- -D warnings
step run_08_clippy_portable env CARGO_TARGET_DIR="$SP/clippy_target" nice -n 10 cargo clippy --all-targets -j 2 --features portable -- -D warnings
step run_08_doc env CARGO_TARGET_DIR="$SP/clippy_target" RUSTDOCFLAGS="-D warnings" cargo doc --no-deps --features portable -j 2
date -u +%FT%TZ > "$RAW/run_99_all.finished"
