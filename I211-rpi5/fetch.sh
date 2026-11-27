#!/bin/bash
# Downloads each arXiv paper's PDF and abs page into its own directory under $DEST, and converts the PDF to text.
# Papers are data: nothing downloaded is executed or built. Usage: fetch.sh <arxiv-id>...
DEST="${DEST:-$HOME/Source/negative-mass-i211-papers}"
for id in "$@"; do
  d="$DEST/$(echo "$id" | tr '/' '_')"
  mkdir -p "$d"
  [ -s "$d/paper.pdf" ] || curl -sS -L -m 120 -o "$d/paper.pdf" "https://arxiv.org/pdf/$id"
  [ -s "$d/abs.html" ] || curl -sS -L -m 60 -o "$d/abs.html" "https://arxiv.org/abs/$id"
  [ -s "$d/paper.txt" ] || pdftotext -layout "$d/paper.pdf" "$d/paper.txt"
  [ -s "$d/flow.txt" ] || pdftotext "$d/paper.pdf" "$d/flow.txt"
  printf '%s  %s bytes pdf, %s lines text, %s\n' "$id" "$(stat -c %s "$d/paper.pdf")" "$(wc -l < "$d/paper.txt")" "$(file -b "$d/paper.pdf" | cut -c1-20)"
  sleep 4
done
