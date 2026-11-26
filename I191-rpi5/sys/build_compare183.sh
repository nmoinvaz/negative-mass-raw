#!/bin/bash
# builds the comparison harness (-j 1, nice 10) into a target directory outside every repository
export PATH=$HOME/.cargo/bin:$PATH
export CARGO_TARGET_DIR=$HOME/Source/negative-mass-i191-libs/target-compare183
cd "$(dirname "$0")/compare183" || exit 1
cargo build --release -j 1
echo "exit $?"
