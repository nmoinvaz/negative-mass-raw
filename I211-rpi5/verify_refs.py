#!/usr/bin/env python3
"""Verifies each reference of the #211 reading against INSPIRE (title, authors, journal, DOI, arXiv id) and the arXiv API
(title, authors, version dates, journal_ref). Writes verify/<key>.json and prints a table. Network only; no paper is run.

    verify_refs.py [outdir]
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

OUT = sys.argv[1] if len(sys.argv) > 1 else "verify"
UA = "negative-mass-literature-check/1.0"
# key -> (arxiv id or None, INSPIRE query for refs without an arXiv id)
REFS = {
    "SH02": ("gr-qc/0205041", None),
    "GGS09b": ("0806.1370", None),
    "BF06": ("gr-qc/0511109", None),
    "BKZ12": ("1205.2224", None),
    "BMD07": ("gr-qc/0611022", None),
    "BBS12": ("1208.4619", None),
    "FMM89": (None, "j Phys.Lett.B,216,272"),
    "FMM90": (None, "j Phys.Rev.D,41,383"),
    "Smo92": (None, "j Class.Quant.Grav.,9,173"),
    "Smo06": ("hep-th/0612185", None),
    "SV19": ("1812.07114", None),
    "BW22": ("2112.13198", None),
    "LRSSV21": ("2009.12057", None),
    "PPS25": ("2410.17150", None),
    "EB01": ("hep-th/0103019", None),
    "BHR21": ("2105.07166", None),
    "Pop10": ("0902.1994", None),
    "Pop16": ("1410.3881", None),
    "Hay06": ("gr-qc/0506126", None),
    "Hay99": ("gr-qc/9805019", None),
    "FGG90": (None, "j Nucl.Phys.B,339,417"),
    "OY18": ("1601.03929", None),
    "CAMB20": ("1909.07129", None),
    "Dym19": (None, "a Dymnikova and t Universes inside a black hole with the de Sitter interior"),
    "MSOF23": ("2304.12018", None),
    "CK21": ("2106.14761", None),
    "BCHM25": ("2412.02742", None),
}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read()


def inspire(q):
    fields = "control_number,titles,authors.full_name,publication_info,dois,arxiv_eprints,citation_count,texkeys"
    url = "https://inspirehep.net/api/literature?" + urllib.parse.urlencode({"q": q, "fields": fields, "size": 3})
    d = json.loads(get(url))
    return d["hits"]["total"], [h["metadata"] for h in d["hits"]["hits"]]


def arxiv(aid):
    url = "https://export.arxiv.org/api/query?id_list=" + urllib.parse.quote(aid)
    ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
    e = ET.fromstring(get(url)).find("a:entry", ns)
    if e is None:
        return None
    t = lambda p: (e.find(p, ns).text or "").strip() if e.find(p, ns) is not None else None  # noqa: E731
    return {"title": " ".join(t("a:title").split()), "published": t("a:published"), "updated": t("a:updated"),
            "authors": [a.find("a:name", ns).text for a in e.findall("a:author", ns)],
            "journal_ref": t("x:journal_ref"), "doi": t("x:doi"), "id": t("a:id")}


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = []
    only = os.environ.get("ONLY")
    for key, (aid, q) in REFS.items():
        if only and key not in only.split(","):
            continue
        rec = {"key": key}
        try:
            total, hits = inspire(f"arxiv:{aid}" if aid else q)
            rec["inspire_total"] = total
            rec["inspire"] = hits[0] if hits else None
            if aid:
                time.sleep(3)
                rec["arxiv"] = arxiv(aid)
        except Exception as ex:  # a failed lookup is recorded, not hidden
            rec["error"] = repr(ex)
        json.dump(rec, open(f"{OUT}/{key}.json", "w"), indent=1, ensure_ascii=False)
        i = rec.get("inspire") or {}
        pi = (i.get("publication_info") or [{}])[0]
        a = rec.get("arxiv") or {}
        rows.append((key, aid or "-", (i.get("titles") or [{}])[0].get("title", "?")[:60],
                     (i.get("authors") or [{}])[0].get("full_name", "?"),
                     f'{pi.get("journal_title", "-")} {pi.get("journal_volume", "")} {pi.get("artid") or pi.get("page_start", "")} ({pi.get("year", "")})',
                     (i.get("dois") or [{}])[0].get("value", "-"), a.get("updated", "-")[:10] if a else "-",
                     rec.get("error", "")))
        time.sleep(3)
    for r in rows:
        print(" | ".join(str(x) for x in r))


main()
