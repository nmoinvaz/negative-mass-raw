#!/bin/bash
# usage: run_checks.sh TAG [suite]   (TAG names the logs: TAG_fmt.log, TAG_clippy_*.log, TAG_test_*.log)
# fmt, clippy (mutate; portable,mutate; none) and, with "suite", the full suite with mutate and portable,mutate.
# Two threads at nice 10. Logs are never overwritten: an existing log name stops the script.
cd ~/Source/negative-mass-i190-libs/multishoot || exit 2
RAW=~/Source/negative-mass-raw/I219-mac
TAG=$1
run() { # name, command...
  local name=$1; shift
  local log=$RAW/${TAG}_${name}.log
  if [ -e "$log" ]; then echo "exists: $log" >&2; exit 3; fi
  echo "$ $*" > "$log"; git rev-parse --short HEAD >> "$log"
  nice -n 10 "$@" >> "$log" 2>&1
  echo "exit $?" >> "$log"
  tail -1 "$log" | sed "s|^|$name: |"
}
run fmt cargo fmt --check
run clippy_mutate cargo clippy -j 2 --all-targets --features mutate -- -D warnings
run clippy_portable_mutate cargo clippy -j 2 --all-targets --features portable,mutate -- -D warnings
run clippy_none cargo clippy -j 2 --all-targets -- -D warnings
if [ "$2" = suite ]; then
  run test_mutate cargo test --release -j 2 --features mutate -- --nocapture --test-threads=2
  run test_portable_mutate cargo test --release -j 2 --features portable,mutate -- --nocapture --test-threads=2
fi
