#!/bin/bash
# s3_build.sh SET LABEL [FEATURES]: builds the crate of the worktree at nice 10 with -j 2 into the target dir target/SET
# (SET = old or new: one dependency build per set), then copies the binary to target/bins/LABEL and prints its md5.
#   s3_build.sh old old_default
#   s3_build.sh old old_libplane lib_plane
#   s3_build.sh old old_complex complex
# --locked: the Cargo.lock in the tree is the one built, never rewritten by the build.
set -euo pipefail
set_=$1
label=$2
features=${3:-}
crate=$HOME/Source/negative-mass-i192/phase2/nonradial/taylor_polar
cd "$crate"
export CARGO_NET_GIT_FETCH_WITH_CLI=true
args=(build --release -j "${JOBS:-2}" --locked --target-dir "target/$set_")
if [ -n "$features" ]; then args+=(--features "$features"); fi
echo "# build $label: cargo ${args[*]}  (Cargo.toml md5 $(md5 -q Cargo.toml), Cargo.lock md5 $(md5 -q Cargo.lock), HEAD $(git rev-parse --short HEAD))"
nice -n 10 cargo "${args[@]}"
mkdir -p target/bins
cp "target/$set_/release/taylor_polar" "target/bins/$label"
echo "# $label: $(md5 -q target/bins/$label)  $(ls -l target/bins/$label | awk '{print $5}') bytes"
