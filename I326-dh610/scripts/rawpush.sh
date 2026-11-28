#!/bin/bash
# usage: rawpush.sh "message"   commit I326-dh610 and INDEX.md in the raw clone, pull --no-rebase, regenerate INDEX.md if it conflicts (it is generated), push; retried if another runner pushed first.
cd "$HOME/Source/negative-mass-raw" || exit 1
for k in 1 2 3 4; do
  (python3 make_index.py >/dev/null; true)
  git add I326-dh610 INDEX.md
  git commit -q -m "$1" 2>/dev/null
  if ! git pull --no-rebase -q 2>/dev/null; then
    if git status --short | grep -q '^UU INDEX.md' && [ "$(git status --short | grep -c '^UU')" = 1 ]; then
      git checkout --theirs INDEX.md; (python3 make_index.py >/dev/null; true); git add INDEX.md; git commit -q --no-edit
    else
      echo "conflict outside INDEX.md: stop"; git status --short | grep '^UU'; exit 2
    fi
  fi
  if git push -q 2>/dev/null; then echo "pushed: $(git log --oneline | head -1)"; exit 0; fi
  sleep 3
done
echo "push failed"; exit 3
