#!/bin/bash
# Rerun the coordinator's review of #114 on the Mac. Run from this folder: ./review.sh [--mutate=diff]
# Needs the negative-mass checkout at ../../negative-mass (for git archive) and its .venv.
# --mutate=diff alters one time in the exported l = 5 output before the comparison, which must then fail.
set -u
MUT=${1:-}
HERE=$(cd "$(dirname "$0")" && pwd)
CODE=f7b8e10                                     # tip of wip/i114-convergence-cap under review
PY=${PY:-$HERE/../../negative-mass/.venv/bin/python}
W=$(mktemp -d)                                   # scratch: exported code and copies of the partial files
mkdir -p "$W/src" "$W/part" "$W/ctl_cap" "$W/ctl_nocap"
git -C "$HERE/../../negative-mass" archive "$CODE" phase2 | tar -x -C "$W/src"
cp "$HERE"/../I114-win/convergence_l{5,6}_w0.7603.partial.csv "$W/part/"
cd "$W/src/phase2/nonradial" || exit 1
if [ "$MUT" = --mutate=diff ]; then             # planted failure
  sed -i '' 's/(107868s)/(107869s)/' convergence_l5_output.txt; fi
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NPROC=1
G=0.001,0.03,0.3,1,3,10,40,137,300,1000
PARTIAL_DIR=$W/part CAP_S=129600 GAMS=$G,6000 "$PY" -u convergence.py 5 > "$HERE/regen5.txt"; echo "regen5 exit $?"
PARTIAL_DIR=$W/part CAP_S=432000 GAMS=$G,12000 "$PY" -u convergence.py 6 > "$HERE/regen6.txt"; echo "regen6 exit $?"
PARTIAL_DIR=$W/ctl_cap CAP_S=4 GAMS=0.001,40 "$PY" -u convergence.py 2 > "$HERE/ctl_cap.txt"; echo "ctl_cap exit $?"
NPROC=6 PARTIAL_DIR=$W/ctl_nocap CAP_S=4 GAMS=0.001,40 "$PY" -u convergence.py 2 --mutate=nocap > "$HERE/ctl_nocap.txt"
echo "ctl_nocap exit $?"
fail=0
for l in 5 6; do                                 # regenerated outputs against the committed ones
  if diff "$HERE/regen$l.txt" "$W/src/phase2/nonradial/convergence_l${l}_output.txt" > /dev/null; then
    echo "l=$l output identical"; else echo "l=$l output DIFFERS"; fail=1; fi
done
for l in 5 6; do                                 # the regeneration must not touch the stored results
  cmp -s "$W/part/convergence_l${l}_w0.7603.partial.csv" "$HERE/../I114-win/convergence_l${l}_w0.7603.partial.csv" \
    && echo "l=$l partial file unchanged" || { echo "l=$l partial file CHANGED"; fail=1; }
done
c=$(grep -c "not completed" "$HERE/ctl_cap.txt"); n=$(grep -c "not completed" "$HERE/ctl_nocap.txt")
r40=$(grep "^gamma=      40" "$HERE/ctl_cap.txt" | grep -o "not completed" | wc -l | tr -d ' ')
echo "ctl_cap rows marked: $c (gamma = 40 marks: $r40), ctl_nocap rows marked: $n"
[ "$c" = 1 ] && [ "$r40" = 6 ] && [ "$n" = 0 ] || fail=1
echo "W=$W"
[ $fail = 0 ] && echo PASS || echo FAIL
exit $fail
