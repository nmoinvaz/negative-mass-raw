#!/bin/bash
# usage: batch.sh TAG   full implicit suite with mutate (logged), then fmt and clippy in the three feature sets
cd ~/Source/negative-mass-i190-libs/multishoot || exit 2
L=~/Source/negative-mass-raw/I219-mac/$1_all_mutate.log
[ -e "$L" ] && { echo "exists: $L" >&2; exit 3; }
nice -n 10 cargo test --release -j 2 --features mutate --test implicit -- --nocapture --test-threads=2 > $L 2>&1; echo "exit $?" >> $L
grep -E "^digest|test result|^exit" $L
for f in mutate portable,mutate; do cargo clippy -j 2 --all-targets --features $f -- -D warnings 2>&1 | tail -1; done
cargo clippy -j 2 --all-targets -- -D warnings 2>&1 | tail -1
cargo fmt --check && echo fmt-ok
