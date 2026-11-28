#!/usr/bin/env python3
"""Download every INSPIRE hit of a query into one JSON file, and log the query and its hit count.

usage: inspire_fetch.py NAME 'QUERY' OUTDIR
Writes OUTDIR/NAME.json (list of records) and appends 'NAME<TAB>QUERY<TAB>hits<TAB>date' to OUTDIR/queries.tsv.
"""
import datetime
import json
import sys
import time
import urllib.parse
import urllib.request

FIELDS = ("control_number,titles,arxiv_eprints,authors.full_name,abstracts,citation_count,publication_info,dois,"
          "preprint_date,earliest_date")
UA = "negative-mass-literature-reader/1.0"


def get(url):
    for k in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as f:
                return json.load(f)
        except Exception as e:  # noqa: BLE001
            print("retry", k, e, file=sys.stderr)
            time.sleep(3 * (k + 1))
    raise SystemExit("failed: " + url)


def main():
    name, query, outdir = sys.argv[1:4]
    size = 100
    url = ("https://inspirehep.net/api/literature?" +
           urllib.parse.urlencode({"q": query, "size": size, "page": 1, "fields": FIELDS, "sort": "mostrecent"}))
    recs = []
    total = None
    while url:
        d = get(url)
        total = d["hits"]["total"]
        for h in d["hits"]["hits"]:
            m = h["metadata"]
            m["_id"] = h["id"]
            recs.append(m)
        url = d.get("links", {}).get("next")
        time.sleep(0.5)
    with open(f"{outdir}/{name}.json", "w") as f:
        json.dump(recs, f, indent=1)
    with open(f"{outdir}/queries.tsv", "a") as f:
        f.write(f"{name}\t{query}\t{total}\t{len(recs)}\t{datetime.date.today()}\n")
    print(name, total, len(recs))


main()
