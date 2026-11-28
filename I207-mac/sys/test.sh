#!/bin/bash
# usage: test.sh NAME CRATE_DIR TARGET_SUBDIR [cargo args...]   cargo test --release --lib (log NAME.log, rc NAME.rc in RAW)
. "$(dirname "$0")/env.sh"
NAME=$1; DIR=$2; TS=$3; shift 3
[ -e "$RAW/$NAME.log" ] && { echo "refusing to overwrite $NAME.log" >&2; exit 2; }
{
  echo "# $NAME: $(date -u +%FT%TZ) machine $(hostname -s) load $(sysctl -n vm.loadavg | tr -d '{}') threads 2 nice 10"
  echo "# crate dir $DIR; target $TD/$TS; args $*; worktree $(git -C $WT rev-parse --short HEAD), $(git -C $WT status --porcelain $CR | wc -l | tr -d ' ') changed paths under the crate"
  cd "$DIR" || exit 3
  CARGO_TARGET_DIR="$TD/$TS" nice -n 10 cargo test --release --lib -j 2 "$@" 2>&1
  rc=$?
  echo "exit $rc"
  echo $rc > "$RAW/$NAME.rc"
} > "$RAW/$NAME.log" 2>&1
