#!/bin/bash
# usage: demo_old.sh LOG FILE OLD NEW TESTFILTER [features]
# Puts the pre-fix text back (NEW replaced by OLD, exactly once) in FILE of the multishoot clone, runs the tests that match
# TESTFILTER of tests/implicit.rs, logs to RAW/LOG, and restores FILE. The test must FAIL on the old text: that is the
# demonstration that the control can fire. Never overwrites a log.
cd ~/Source/negative-mass-i190-libs/multishoot || exit 2
RAW=~/Source/negative-mass-raw/I219-mac
LOG=$RAW/$1; FILE=$2; FIX=$3; OLD=$4; FILTER=$5; FEAT=${6:-mutate}
[ -e "$LOG" ] && { echo "exists: $LOG" >&2; exit 3; }
BAK=$(mktemp -d)/orig; cp "$FILE" "$BAK"
python3 - "$FILE" "$FIX" "$OLD" <<'EOF' || { cp "$BAK" "$FILE"; exit 4; }
import sys
p, fix, old = sys.argv[1:4]
s = open(p).read()
assert s.count(fix) == 1, "fix text not found exactly once"
open(p, 'w').write(s.replace(fix, old))
EOF
{ echo "# $FILE: the fixed text replaced by the pre-fix text; the tests must fail"; echo "--- fixed text"; echo "$FIX"; echo "--- pre-fix text"; echo "$OLD"; echo "---"; } > "$LOG"
nice -n 10 cargo test --release -j 2 --features "$FEAT" --test implicit "$FILTER" -- --nocapture --test-threads=2 >> "$LOG" 2>&1
echo "exit $?" >> "$LOG"
cp "$BAK" "$FILE"
git diff --stat -- "$FILE" | tail -1
tail -1 "$LOG"
