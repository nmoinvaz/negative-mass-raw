#!/bin/bash
# step 5: the final run (stdout to the repository's output file) and then the final controls
RAW=/home/nathan/Source/negative-mass-raw/I143-rpi5
D=/home/nathan/Source/negative-mass-i143/phase2/dg_proof
PY=/home/nathan/Source/negative-mass-venv314/bin/python
cd $D
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
start=$(date +%s)
timeout 3600 /usr/bin/time -v -o $RAW/final.rss $PY -I $D/zerilli_derivation.py > $D/zerilli_derivation_output.txt 2> $RAW/final.err
echo $? > $RAW/final.rc
echo $(( $(date +%s) - start )) > $RAW/final.time
cp $D/zerilli_derivation_output.txt $RAW/final_output.txt
start=$(date +%s)
CTRL_LOGDIR=$RAW/controls_logs timeout 7200 /usr/bin/time -v -o $RAW/controls.rss $PY $D/zerilli_derivation_controls.py > $D/zerilli_derivation_controls_output.txt 2> $RAW/controls.err
echo $? > $RAW/controls.rc
echo $(( $(date +%s) - start )) > $RAW/controls.time
cp $D/zerilli_derivation_controls_output.txt $RAW/controls_output.txt
