#!/bin/bash
# usage: run_tests.sh NAME "FEATURES" [test args after --]   (runs in the multishoot clone, log and rc in the raw folder)
export PATH=$HOME/.cargo/bin:$PATH
RAW=$HOME/Source/negative-mass-raw/I190-rpi5
NAME=$1; FEAT=$2; shift 2
cd $HOME/Source/negative-mass-i190-libs/multishoot || exit 3
{
  echo "# $NAME: $(date -u +%FT%TZ) machine $(hostname) load $(cut -d' ' -f1-3 /proc/loadavg) threads 2 nice 10"
  echo "# multishoot $(git rev-parse --short HEAD) $(git status --porcelain | wc -l) modified files"
  /usr/bin/time -v cargo test --release -j 2 --features "$FEAT" "$@" 2>&1
  echo "exit $?"
} > $RAW/$NAME.log 2>&1
echo $? > $RAW/$NAME.rc
