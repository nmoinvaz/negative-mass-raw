#!/bin/bash
# usage: build_arm.sh NAME ARM [cargo build args...]
# builds notes/warp/conical_global in the worktree into $TD/ARM (release, -j 2, nice 10); log NAME.log, rc NAME.rc in RAW
. "$(dirname "$0")/env.sh"
NAME=$1; ARM=$2; shift 2
[ -e "$RAW/$NAME.log" ] && { echo "refusing to overwrite $NAME.log" >&2; exit 2; }
mkdir -p "$TD/$ARM"
{
  echo "# $NAME: $(date -u +%FT%TZ) machine $(hostname -s) load $(sysctl -n vm.loadavg | tr -d '{}') threads 2 nice 10"
  echo "# worktree $(git -C $WT rev-parse --short HEAD), $(git -C $WT status --porcelain $CR | wc -l | tr -d ' ') changed paths under the crate; target $TD/$ARM; args $*"
  cd "$CR" || exit 3
  CARGO_TARGET_DIR="$TD/$ARM" nice -n 10 cargo build --release -j 2 "$@" 2>&1
  rc=$?
  echo "exit $rc"
  echo $rc > "$RAW/$NAME.rc"
} > "$RAW/$NAME.log" 2>&1
