#!/bin/bash
# rerun_lib.sh: the PR's library suite at eaf55a8 on this Mac, default then portable (as the Pi's run_36, run_37)
here=$(cd "$(dirname "$0")" && pwd)
cd /Users/nathan/Source/negative-mass-r190/multishoot || exit 2
for v in "default mutate" "portable portable,mutate"; do
  set -- $v
  n=rerun_lib_$1
  [ -e "$here/$n.log" ] && { echo "refusing to overwrite $n.log" >&2; exit 2; }
  { echo "# $n: $(date -u +%FT%TZ) $(uptime) multishoot $(git rev-parse --short HEAD)"
    CARGO_TARGET_DIR=/Users/nathan/Source/negative-mass-r190/target-$1 nice -n 10 cargo test --release -j 2 --features "$2" \
      --lib --test implicit --test taylor --test taylor_order --test plane -- --nocapture --test-threads=2 2>&1
    echo "exit $?"; } > "$here/$n.log" 2>&1
done
