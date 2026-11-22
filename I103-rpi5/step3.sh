#!/bin/bash
RAW=$HOME/Source/negative-mass-raw/I103-rpi5
$RAW/run_step.sh s3_nocontrols - --no-controls
$RAW/run_step.sh s3_mutate_nsimplify - --mutate=nsimplify
$RAW/run_step.sh s3_mutate_disc-sign - --mutate=disc-sign
echo 0 > $RAW/done/step3.rc
