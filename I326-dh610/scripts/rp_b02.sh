#!/bin/bash
# RP controls at B = 0.2 (stored points of I228-dh610): the two ends of the final bracket, then the points at 5.9e-11 and 2.4e-11 from p*.
S=$HOME/Source/negative-mass-raw/I326-dh610/scripts/rp.sh
$S B0.2_lo 0.2 1 0.07681202535021378 45.938959806737024
$S B0.2_hi 0.2 1 0.07681202535718415 57.917348680037136
$S B0.2_p5e-11 0.2 1 0.07681202541294717 51.355397750625976
$S B0.2_m2e-11 0.2 1 0.07681202532930265 37.190281156506465
