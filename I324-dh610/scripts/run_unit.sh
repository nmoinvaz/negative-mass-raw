#!/usr/bin/env bash
# usage: run_unit.sh <dir> <name> <command words...>
# Starts the command as a transient systemd user unit nm-i324-<name> (nice 10, one thread, 2 h limit); writes <dir>/<name>.{log,err,rc,time,start}.
# Refuses to overwrite a log: a rerun needs a new name (_run2, ...).
set -u
dir="$(realpath -m "$1")"; name="$2"; shift 2
mkdir -p "$dir"
if [ -e "$dir/$name.log" ] || [ -e "$dir/$name.rc" ]; then echo "refusing to overwrite $dir/$name.*" >&2; exit 2; fi
date -Is > "$dir/$name.start"
systemd-run --user --unit="nm-i324-$name" --collect --property=Nice=10 --working-directory="$HOME/Source/negative-mass-i324/notes/wormhole_evolution" \
  --setenv=NUMBA_NUM_THREADS=1 --setenv=OMP_NUM_THREADS=1 --setenv=PYTHONUNBUFFERED=1 \
  bash -c 'd="$1"; n="$2"; shift 2; /usr/bin/time -v -o "$d/$n.time" timeout --signal=TERM --kill-after=60 7200 "$@" > "$d/$n.log" 2> "$d/$n.err"; echo $? > "$d/$n.rc"' _ "$dir" "$name" "$@"
