#!/bin/bash
# usage: arm.sh ARM JOB   copies the three binaries of an arm (base, off, on) to the crate's target/release, records their sha256
CR=$HOME/Source/negative-mass-i190/notes/warp/conical_global
T=$HOME/Source/negative-mass-i190-libs
RAW=$HOME/Source/negative-mass-raw/I190-rpi5
mkdir -p $CR/target/release
for b in conical_global loglog offgrid; do cp $T/target-crate-$1/release/$b $CR/target/release/$b || exit 3; done
(cd $CR/target/release && sha256sum conical_global loglog offgrid) > $RAW/arm_$2.sha256
