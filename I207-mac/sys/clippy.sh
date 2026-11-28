#!/bin/bash
# usage: clippy.sh NAME CRATE_DIR TARGET_SUBDIR [cargo args...]   cargo clippy --all-targets -D warnings on a crate directory (log NAME.log, rc NAME.rc in RAW)
. "$(dirname "$0")/env.sh"
NAME=$1; DIR=$2; TS=$3; shift 3
[ -e "$RAW/$NAME.log" ] && { echo "refusing to overwrite $NAME.log" >&2; exit 2; }
{
  echo "# $NAME: $(date -u +%FT%TZ) machine $(hostname -s) load $(sysctl -n vm.loadavg | tr -d '{}') threads 2 nice 10; $(cargo clippy --version)"
  echo "# crate dir $DIR; target $TD/$TS; args $*"
  cd "$DIR" || exit 3
  CARGO_TARGET_DIR="$TD/$TS" nice -n 10 cargo clippy --all-targets -j 2 "$@" -- -D warnings 2>&1
  rc=$?
  echo "exit $rc"
  echo $rc > "$RAW/$NAME.rc"
} > "$RAW/$NAME.log" 2>&1
