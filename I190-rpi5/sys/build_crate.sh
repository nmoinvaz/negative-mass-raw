#!/bin/bash
# usage: build_crate.sh NAME TARGET_DIR [cargo args...]   builds notes/warp/conical_global in the worktree (log, rc in raw)
export PATH=$HOME/.cargo/bin:$PATH
RAW=$HOME/Source/negative-mass-raw/I190-rpi5
NAME=$1; TD=$2; shift 2
cd $HOME/Source/negative-mass-i190/notes/warp/conical_global || exit 3
{
  echo "# $NAME: $(date -u +%FT%TZ) machine $(hostname) load $(cut -d' ' -f1-3 /proc/loadavg) threads 2 nice 10"
  echo "# worktree $(git rev-parse --short HEAD) $(git status --porcelain . | wc -l) modified files under the crate; target $TD; args $*"
  CARGO_TARGET_DIR=$TD /usr/bin/time -v cargo build --release -j 2 "$@" 2>&1
  rc=$?
  echo "exit $rc"
  echo $rc > $RAW/$NAME.rc
} > $RAW/$NAME.log 2>&1
