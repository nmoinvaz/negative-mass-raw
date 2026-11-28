#!/usr/bin/env python3
"""verify_refs.py IDLIST PAPERSROOT OUT.tsv: INSPIRE record (title, authors, journal, DOI, citations) and the arXiv stamp of the
downloaded PDF (pypdf page-1 text, the line 'arXiv:ID vN [cat] date') for each arXiv id."""
import json, os, re, sys, time, urllib.parse, urllib.request
from pypdf import PdfReader
ids = [l.split()[0] for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")]
root, out = sys.argv[2:4]
F = "control_number,titles,authors.full_name,publication_info,dois,arxiv_eprints,citation_count"
with open(out, "w") as o:
    o.write("arxiv_id\tarxiv_stamp\tinspire_recid\ttitle\tfirst_author(n)\tjournal\tdoi\n")
    for i in ids:
        stamp = "-"
        p = os.path.join(root, i.replace("/", "_"), "paper.pdf")
        if os.path.exists(p):
            try:
                t = PdfReader(p).pages[0].extract_text()
                m = re.search(r"arXiv:\s*[\w./-]+v\d+\s*\[[^\]]+\]\s*\d+\s+\w+\s+\d{4}", t)
                stamp = re.sub(r"\s+", " ", m.group(0)) if m else "no stamp in page 1 text"
            except Exception as e:  # noqa: BLE001
                stamp = "pypdf failed"
        url = "https://inspirehep.net/api/literature?" + urllib.parse.urlencode({"q": "arxiv:" + i, "fields": F, "size": 1})
        row = [i, stamp, "-", "NOT FOUND", "-", "-", "-"]
        for k in range(4):
            try:
                d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "negative-mass-literature-reader/1.0"}), timeout=60))
                if d["hits"]["hits"]:
                    h = d["hits"]["hits"][0]; m = h["metadata"]
                    pi = m.get("publication_info", [{}])[0]
                    jr = f'{pi.get("journal_title","")} {pi.get("journal_volume","")} {pi.get("artid", pi.get("page_start",""))} ({pi.get("year","")})'.strip()
                    au = m.get("authors", [{}])
                    row = [i, stamp, h["id"], m["titles"][0]["title"], f'{au[0].get("full_name","")} ({len(au)})', jr, (m.get("dois") or [{}])[0].get("value", "-")]
                break
            except Exception as e:  # noqa: BLE001
                time.sleep(3 * (k + 1))
        o.write("\t".join(row) + "\n"); o.flush(); time.sleep(0.4)
