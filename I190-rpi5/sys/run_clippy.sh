#!/bin/bash
export PATH=$HOME/.cargo/bin:$PATH
RAW=$HOME/Source/negative-mass-raw/I190-rpi5
NAME=$1; FEAT=$2
cd $HOME/Source/negative-mass-i190-libs/multishoot || exit 3
{
  echo "# $NAME: $(date -u +%FT%TZ) clippy --all-targets --features $FEAT -- -D warnings; load $(cut -d' ' -f1-3 /proc/loadavg)"
  cargo clippy -j 2 --all-targets --features "$FEAT" -- -D warnings 2>&1
  echo "exit $?"
} > $RAW/$NAME.log 2>&1
tail -1 $RAW/$NAME.log | sed 's/exit //' > $RAW/$NAME.rc
