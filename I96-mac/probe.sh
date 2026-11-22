cd /private/tmp/claude-501/-Users-nathan-Source-negative-mass/27911ca3-2259-460a-98f6-94387039554a/scratchpad/wt96
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
for a in "64 1" "128 2"; do set -- $a
  /usr/bin/time -l nice -n 10 /Users/nathan/Source/negative-mass/.venv/bin/python -u notes/warp/frank_loss.py --part=krylov --sigmas=8 --Ns=$1 --L=$2 --vs=0.5 > /private/tmp/claude-501/-Users-nathan-Source-negative-mass/27911ca3-2259-460a-98f6-94387039554a/scratchpad/r96/box-s8-L$2-N$1.log 2>&1; echo "exit $?" >> /private/tmp/claude-501/-Users-nathan-Source-negative-mass/27911ca3-2259-460a-98f6-94387039554a/scratchpad/r96/box-s8-L$2-N$1.log
done
