#!/bin/bash
# usage: arm.sh ARM JOB   copies the three binaries of an arm to the crate's target/release, records their sha256 in RAW
. "$(dirname "$0")/env.sh"
mkdir -p "$CR/target/release"
for b in conical_global loglog offgrid; do cp "$TD/$1/release/$b" "$CR/target/release/$b" || exit 3; done
(cd "$CR/target/release" && shasum -a 256 conical_global loglog offgrid) > "$RAW/arm_$2.sha256"
