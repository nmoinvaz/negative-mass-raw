#!/bin/bash
# usage: fetch.sh DIR URL OUTNAME  ; downloads URL into DIR/OUTNAME (DIR is new or empty), logs UTC time, HTTP status,
# content type, size and sha256 to fetch.log beside this script. Generic user agent. No retries, no bypass of 403/paywalls.
set -u
dir=$1; url=$2; out=$3
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$dir"
f="$dir/$out"
meta=$(curl -sL -A "generic-client/1.0" -o "$f" -w '%{http_code} %{content_type} %{size_download}' --max-time 120 "$url")
sum=$(sha256sum "$f" | cut -d' ' -f1)
echo "$(date -u +%FT%TZ) | $meta | $url | $f | sha256 $sum" | tee -a "$here/fetch.log"
sleep 3
