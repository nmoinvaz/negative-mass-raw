#!/bin/bash
# Step 4: every mutation of weitzenbock_conf.py, old and new, one after the other, one log and one exit code each.
cd /home/nathan/Source/negative-mass-i99
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
RAW=/home/nathan/Source/negative-mass-raw/I99-rpi5
PY=/home/nathan/Source/negative-mass-venv314/bin/python
echo "start $(date -Is) commit $(git rev-parse --short HEAD) sha256 $(sha256sum notes/warp/weitzenbock_conf.py | cut -c1-16)" > $RAW/step4.time
NAMES=$($PY - <<'PYEOF'
import re
s = open("notes/warp/weitzenbock_conf.py").read()
i = s.index("CONTROLS = {"); j = s.index("if MUT and MUT not in CONTROLS")
print(" ".join(re.findall(r'^    "([^"]+)": \(', s[i:j], re.M)))
PYEOF
)
for m in $NAMES; do
  t0=$(date +%s)
  nice -n 10 $PY -u notes/warp/weitzenbock_conf.py --mutate=$m > $RAW/mutate_$m.log 2>&1
  rc=$?
  echo $rc > $RAW/done/mutate_$m.rc
  echo "$m exit $rc $(( $(date +%s) - t0 )) s $(grep '^control ' $RAW/mutate_$m.log | grep -o '\(FIRED\|SILENT\)$')" >> $RAW/step4.time
done
echo "end $(date -Is)" >> $RAW/step4.time
echo done > $RAW/done/step4.rc
