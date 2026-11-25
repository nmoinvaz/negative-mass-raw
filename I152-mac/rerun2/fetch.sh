#!/bin/bash
# usage: fetch.sh DIR URL OUTNAME   ; downloads URL into new directory DIR/OUTNAME, logs status, size, sha256
set -u
dir=$1; url=$2; out=$3
mkdir -p "$dir"
f="$dir/$out"
code=$(curl -sL -A "generic-client/1.0" -o "$f" -w '%{http_code} %{content_type} %{size_download}' --max-time 120 "$url")
sum=$(sha256sum "$f" | cut -d' ' -f1)
echo "$(date -u +%FT%TZ) | $code | $url | $f | sha256 $sum" | tee -a "$(dirname "$0")/fetch.log"
sleep 3
