#!/usr/bin/env python3
"""arxiv_q.py NAME 'SEARCH_QUERY' OUTDIR: arXiv API query, saves the Atom XML and logs totalResults to OUTDIR/queries.tsv."""
import datetime, re, sys, time, urllib.parse, urllib.request
name, q, outdir = sys.argv[1:4]
url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode({"search_query": q, "max_results": 100, "sortBy": "submittedDate", "sortOrder": "descending"})
for k in range(5):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "negative-mass-literature-reader/1.0"})
        data = urllib.request.urlopen(req, timeout=60).read().decode()
        break
    except Exception as e:
        print("retry", k, e, file=sys.stderr); time.sleep(5 * (k + 1))
else:
    raise SystemExit("failed")
open(f"{outdir}/arxiv_{name}.xml", "w").write(data)
tot = re.search(r"<opensearch:totalResults[^>]*>(\d+)<", data).group(1)
open(f"{outdir}/queries.tsv", "a").write(f"arxiv_{name}\t{q}\t{tot}\t{data.count('<entry>')}\t{datetime.date.today()}\n")
print(name, tot)
time.sleep(4)
