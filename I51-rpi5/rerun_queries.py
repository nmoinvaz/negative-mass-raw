#!/usr/bin/env python3
"""Rerun of the novelty check's searches for work posted after 2026-10-21 (#51).

    python3 -I rerun_queries.py [--subset=control] [--mutate=window|terms] [--out=DIR]

Sources: arXiv API (export.arxiv.org, one request per 3.2 s) and INSPIRE API (inspirehep.net). Every response is stored
unchanged in DIR/raw/ with its sha256; DIR/queries.json holds every parsed hit and DIR/queries.md the table.
Windows: NEW = posted 2026-10-21 .. now (arXiv submittedDate / INSPIRE earliest date `de`); CTRL = 2026-01-01 ..
2026-10-20, run through the same code path to plant known papers (the expectations are written below, before any run).

Controls (exit 1 if one fails; the outputs are still written):
  C1 planted positives: each query in EXPECT must return its listed arXiv ids in the CTRL window.
  C2 window edge: every NEW hit must have been posted on or after 2026-10-21 (arXiv `published`, INSPIRE `de`).
  C3 a query for a nonsense token must have 0 hits in both windows (zero counts are real zeros).
  C4 INSPIRE citation trail: refersto:recid:3195733 (all dates) must list arXiv 2610.13206.
--mutate=window  starts the NEW window at 2026-03-01 while C2 still checks 2026-10-21 (C2 must fail).
--mutate=terms   replaces a key term of each EXPECT query by a wrong one (C1 must fail).
"""
import hashlib, json, os, re, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

UA = "generic-client/1.0"
NEW_START = "2026-10-21"
CTRL_START, CTRL_END = "2026-01-01", "2026-10-20"
args = dict(a.lstrip("-").split("=", 1) if "=" in a else (a.lstrip("-"), "1") for a in sys.argv[1:])
MUT = args.get("mutate", "")
SUBSET = args.get("subset", "")
OUT = args.get("out", os.path.join(os.path.dirname(os.path.abspath(__file__)), "rerun"))
os.makedirs(os.path.join(OUT, "raw"), exist_ok=True)
NEW_QUERY_START = "2026-03-01" if MUT == "window" else NEW_START
def day_before(d):
    y, m, dd = map(int, d.split("-"))
    return (datetime(y, m, dd) - timedelta(days=1)).strftime("%Y-%m-%d")
INS_LO = day_before(NEW_QUERY_START)  # INSPIRE `de >` is exclusive
NOW = datetime.now(timezone.utc)
NOW_S = NOW.strftime("%Y-%m-%d")


def ax_date(d, end=False):
    return d.replace("-", "") + ("2359" if end else "0000")


# (qid, section, arXiv query, INSPIRE query or None, set of arXiv ids that must appear in the CTRL window)
Q = [
    ("A01", "A", 'ti:"negative mass"', 't "negative mass"', {"2608.24577", "2605.10976", "2601.22910"}),
    ("A02", "A", 'all:"negative mass" AND all:Schwarzschild AND (all:perturbation OR all:perturbations OR all:stability OR all:instability)', None, set()),
    ("A03", "A", 'all:"negative mass" AND (all:star OR all:stars) AND (all:stability OR all:nonradial OR all:"non-radial" OR all:perturbations)', None, set()),
    ("A04", "A", 'all:"naked singularity" AND (all:Zerilli OR all:"Regge-Wheeler" OR all:"gravitational perturbations")', 't "naked singularity" and (t stability or t perturbations)', set()),
    ("A05", "A", '(all:Darboux OR all:intertwining OR all:"supersymmetric quantum mechanics") AND (all:Schwarzschild OR all:Zerilli)', None, set()),
    ("A06", "A", 'all:"negative mass" AND (all:bubble OR all:"thin shell" OR all:"thin-wall") AND all:stability', None, set()),
    ("A07", "A", 'all:"S-deformation" OR (au:Dotti AND au:Gleiser)', None, set()),
    ("A08", "A", 'all:"negative mass" AND (all:Robin OR all:"boundary condition") AND (all:Schwarzschild OR all:"naked singularity")', None, set()),
    ("A09", "A", 'ti:"negative mass" AND (ti:star OR ti:stars OR ti:stability OR ti:instability OR ti:perturbations)', None, set()),
    ("A10", "A", 'all:"Penrose" AND all:"naked singularity" AND all:instability', None, set()),
    ("B01", "B", 'all:"boson star" AND (all:phantom OR all:ghost)', 't "boson star" and (t phantom or t ghost)', set()),  # run 1 planted 2603.04400 here; its abstract has no "boson star"
    ("B10", "B", 'all:ghost AND all:scalar AND (all:"neutron star" OR all:"neutron stars")', None, {"2603.04400"}),
    ("B02", "B", '(all:"negative ADM mass" OR all:"negative active mass") AND (all:scalar OR all:boson OR all:phantom)', None, {"2608.24577"}),
    ("B03", "B", '(ti:"boson star" OR ti:"boson stars") AND (all:"negative mass" OR all:"negative energy" OR all:phantom OR all:ghost)', None, set()),
    ("B04", "B", 'all:"boson star" AND (all:"negative Newton" OR all:"negative gravitational" OR all:"wrong-sign" OR all:"repulsive gravity")', None, set()),
    ("B05", "B", '(all:"Q-ball" OR all:"Q-balls") AND (all:ghost OR all:phantom) AND all:gravity', None, set()),
    ("B06", "B", 'all:"boson star" AND all:"turning point" AND all:stability', None, set()),
    ("B07", "B", '(all:phantom OR all:ghost) AND (all:soliton OR all:solitons) AND (all:"negative mass" OR all:wormhole)', None, set()),
    ("B08", "B", 'all:"Kleihaus" AND all:"boson" AND (all:phantom OR all:"negative mass")', None, set()),
    ("B09", "B", 'ti:phantom AND (ti:star OR ti:stars OR ti:soliton OR ti:ball OR ti:balls) AND all:stability', None, set()),
    ("C01", "C", 'all:"negative mass" AND (all:"post-Newtonian" OR all:"Einstein-Infeld-Hoffmann" OR all:EIH)', 't "negative mass" and (t "post-Newtonian" or t EIH)', set()),
    ("C02", "C", 'all:"negative mass" AND (all:runaway OR all:"self-acceleration" OR all:"self-accelerating" OR all:"self-accelerated")', None, set()),
    ("C03", "C", '(all:"opposite sign" OR all:"opposite signs") AND all:masses AND (all:relativistic OR all:"general relativity")', None, set()),
    ("C04", "C", 'all:"negative mass" AND (all:"two-body" OR all:"two body" OR all:binary)', None, {"2605.10976"}),
    ("C05", "C", 'all:Bondi AND all:"negative mass"', None, {"2601.22910"}),
    ("C06", "C", 'all:"Bonnor" AND (all:"negative mass" OR all:dipole OR all:"uniformly accelerated")', None, set()),
    ("C07", "C", 'all:"negative mass" AND (all:dipole OR all:"Fermi-Walker" OR all:"uniformly accelerated")', None, set()),
    ("C08", "C", 'au:Ivanov_P AND all:"opposite signs"', None, set()),
    ("C09", "C", 'all:"negative mass" AND (all:"gravitational wave" OR all:"gravitational waves") AND all:binary', None, {"2605.10976"}),
    ("D01", "D", 'all:"positive mass theorem" AND (all:"negative energy" OR all:ghost OR all:phantom OR all:"energy condition")', None, set()),
    ("D02", "D", 'all:"positive energy theorem" AND all:Witten AND (all:"energy condition" OR all:violation OR all:violating)', None, set()),
    ("D03", "D", 'all:"ADM mass" AND (all:"lower bound" OR all:"lower bounds") AND all:"scalar curvature"', None, set()),
    ("D04", "D", 'all:"Bondi mass" AND (all:ghost OR all:phantom)', None, set()),
    ("D05", "D", '(all:phantom OR all:ghost) AND all:scalar AND all:"numerical relativity"', None, {"2603.13210"}),
    ("E01", "E", 'all:Shirokov AND all:"numerical relativity"', None, {"2608.24577", "2610.13206"}),
    ("E02", "E", 'all:"negative mass" AND all:"numerical relativity"', None, {"2608.24577"}),
    ("E03", "E", 'all:binary AND all:wormhole AND all:"numerical relativity"', None, {"2610.13206"}),
    ("E04", "E", 'all:"moving puncture" AND (all:"negative mass" OR all:"naked singularity")', None, set()),
    ("Z01", "Z", 'all:xyzzyqwertyplugh', 'xyzzyqwertyplugh', set()),  # C3
]
INSP_ONLY = [
    ("I01", "A", 't "negative energy" and t "star"', set()),
    ("I02", "B", 'abstracts.value:"negative mass" and abstracts.value:"boson"', set()),  # run 1 planted 2608.24577; its abstract has neither phrase
    ("I03", "B", 'abstracts.value:"negative mass"', {"2605.10976"}),
    ("I04", "D", 't "positive mass theorem" or t "positive energy theorem"', set()),
    ("I05", "E", 'a Shirokov and t "numerical relativity"', {"2610.13206"}),
    ("I06", "A", 't "negative mass" and (t star or t stability or t perturbations)', set()),
]
# citation trails: label, recid (None = look up by arXiv id / DOI), lookup, note
TRAILS = [
    ("GHI hep-th/0409307", 660779, None), ("GD06 gr-qc/0604021", 713860, None), ("DG08 0809.3615", 797174, None),
    ("Mbarek-Paranjape 1407.1457", 1305085, None), ("Shirokov 2608.24577", 3195733, None), ("Ivanov 1204.1269", 1104736, None),
    ("Novikov+ 1807.06468", 1682851, None), ("Cao 2012 IJMPD 21 1250061", 1191325, None),
    ("Paranjape 2025 chapter", 3116840, None),
    ("Dotti 2022 2201.03640", None, "arxiv:2201.03640"), ("de Aguiar Alves+ 2408.00154", None, "arxiv:2408.00154"),
    ("Johnson+ 1910.01774", None, "arxiv:1910.01774"), ("Cardoso-Cavaglia gr-qc/0604101", None, "arxiv:gr-qc/0604101"),
    ("Giveon+ hep-th/0401209", None, "arxiv:hep-th/0401209"), ("Bernal+ 2603.04400", None, "arxiv:2603.04400"),
    ("Dzhunushaliev+ 0805.3211", None, "arxiv:0805.3211"), ("Dzhunushaliev+ 1409.6978", None, "arxiv:1409.6978"),
    ("Tamaki-Sakai 1105.1498", None, "arxiv:1105.1498"), ("Bicak-Kofron 0901.3971", None, "arxiv:0901.3971"),
    ("Trivedi-Loeb 2605.10976", None, "arxiv:2605.10976"), ("Caridi+ 2603.13210", None, "arxiv:2603.13210"),
    ("Shirokov-Nachevsky 2610.13206", None, "arxiv:2610.13206"),
]
KNOWN = """2608.24577 2610.13206 2603.04400 2408.00154 2201.03640 0809.3615 gr-qc/0604021 gr-qc/0604101 hep-th/0409307 1407.1457
1910.01774 1807.06468 1204.1269 1409.6978 0805.3211 1606.07304 2302.07889 1105.1498 2605.10976 2603.13210 2602.15058 2601.22910
2604.00071 2411.00933 1406.0841 2507.09677 2510.20305 2608.27900 2510.09506 1611.03534 1706.01447 0810.0025 hep-th/0401209
0901.3971 1408.2451 2307.05277 2509.05244 2604.24746 2508.17585 2606.23529 2503.18963 2603.28356 2412.13400 1901.01363 1304.1566""".split()

NS = {"a": "http://www.w3.org/2005/Atom", "o": "http://a9.com/-/spec/opensearch/1.1/"}
RUNS, N_RAW = [], [0]
LAST = {"arxiv": 0.0, "inspire": 0.0}


def get(url, kind):
    wait = (3.2 if kind == "arxiv" else 0.8) - (time.time() - LAST[kind])
    if wait > 0:
        time.sleep(wait)
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                body = r.read()
                code = r.status
            break
        except Exception as e:  # noqa: BLE001
            body, code = str(e).encode(), -1
            time.sleep(5 * (attempt + 1))
    LAST[kind] = time.time()
    N_RAW[0] += 1
    sha = hashlib.sha256(body).hexdigest()
    ext = "xml" if kind == "arxiv" else "json"
    name = f"{N_RAW[0]:04d}_{kind}.{ext}"
    with open(os.path.join(OUT, "raw", name), "wb") as f:
        f.write(body)
    return code, body, name, sha


def arxiv_run(qid, section, q, lo, hi, label, id_list=None):
    ents, total, start = [], None, 0
    while True:
        p = {"max_results": "100", "start": str(start), "sortBy": "submittedDate", "sortOrder": "descending"}
        if id_list:
            p["id_list"] = ",".join(id_list)
        else:
            p["search_query"] = f"({q}) AND submittedDate:[{ax_date(lo)} TO {ax_date(hi, True)}]"
        url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(p)
        code, body, name, sha = get(url, "arxiv")
        if code != 200:
            RUNS.append(dict(qid=qid, section=section, source="arxiv", window=label, query=q, url=url, http=code, raw=name, sha256=sha, total=None, hits=[]))
            return
        root = ET.fromstring(body)
        total = int(root.find("o:totalResults", NS).text)
        for e in root.findall("a:entry", NS):
            i = e.find("a:id", NS).text.split("/abs/")[1]
            ents.append(dict(
                id=re.sub(r"v\d+$", "", i), ver=int(re.search(r"v(\d+)$", i).group(1)) if re.search(r"v(\d+)$", i) else 1,
                title=re.sub(r"\s+", " ", e.find("a:title", NS).text).strip(),
                published=e.find("a:published", NS).text, updated=e.find("a:updated", NS).text,
                authors=[a.find("a:name", NS).text for a in e.findall("a:author", NS)][:4],
                summary=re.sub(r"\s+", " ", e.find("a:summary", NS).text).strip()))
        start += 100
        if start >= (total or 0) or id_list:
            break
    RUNS.append(dict(qid=qid, section=section, source="arxiv", window=label, query=q, url=url, http=code, raw=name, sha256=sha,
                     utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), total=total, hits=ents))


def inspire_run(qid, section, q, label, extra_fields="", size=100):
    p = {"q": q, "size": str(size), "sort": "mostrecent",
         "fields": "titles,arxiv_eprints,earliest_date,control_number,publication_info,dois,authors.full_name,abstracts" + extra_fields}
    url = "https://inspirehep.net/api/literature?" + urllib.parse.urlencode(p)
    hits, total = [], None
    while url:
        code, body, name, sha = get(url, "inspire")
        if code != 200:
            RUNS.append(dict(qid=qid, section=section, source="inspire", window=label, query=q, url=url, http=code, raw=name, sha256=sha, total=None, hits=[]))
            return
        j = json.loads(body)
        total = j["hits"]["total"]
        for h in j["hits"]["hits"]:
            m = h["metadata"]
            hits.append(dict(
                id=(m.get("arxiv_eprints") or [{}])[0].get("value"), recid=m.get("control_number"),
                title=(m.get("titles") or [{}])[0].get("title"), date=m.get("earliest_date"),
                authors=[a["full_name"] for a in (m.get("authors") or [])][:4],
                pub=(m.get("publication_info") or [{}])[0].get("journal_title"),
                summary=((m.get("abstracts") or [{}])[0].get("value") or "")[:600]))
        url = j.get("links", {}).get("next")
        if len(hits) >= 500:
            break
    RUNS.append(dict(qid=qid, section=section, source="inspire", window=label, query=q, url=url or "", http=code, raw=name, sha256=sha,
                     utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), total=total, hits=hits))


def mut(q):
    for a, b in (("negative", "positive"), ("phantom", "canonical"), ("Shirokov", "Smith"), ("boson", "fermion"), ("wormhole", "pulsar"), ("Bondi", "Planck"), ("ghost", "canonical"), ("neutron", "proton")):
        q = q.replace(a, b)
    return q


def lookup_recid(spec):
    code, body, name, sha = get("https://inspirehep.net/api/literature?" + urllib.parse.urlencode({"q": spec, "fields": "control_number,titles", "size": "2"}), "inspire")
    j = json.loads(body)
    if j["hits"]["total"] != 1:
        return None, None
    h = j["hits"]["hits"][0]
    return h["metadata"]["control_number"], (h["metadata"]["titles"][0]["title"])


def main():
    expect_q = [x for x in Q if x[4] or x[0] == "Z01"]
    qs = expect_q if SUBSET == "control" else Q
    for qid, sec, aq, iq, exp in qs:
        if MUT == "terms" and exp:
            aq, iq = mut(aq), (mut(iq) if iq else iq)
        arxiv_run(qid, sec, aq, NEW_QUERY_START, NOW_S, "NEW")
        arxiv_run(qid, sec, aq, CTRL_START, CTRL_END, "CTRL")
        if iq:
            inspire_run(qid, sec, f"({iq}) and de > {INS_LO}", "NEW")
            inspire_run(qid, sec, f"({iq}) and de > {day_before(CTRL_START)} and de < 2026-10-21", "CTRL")
    insp = [x for x in INSP_ONLY if x[3]] if SUBSET == "control" else INSP_ONLY
    for qid, sec, iq, exp in insp:
        iq = mut(iq) if (MUT == "terms" and exp) else iq
        inspire_run(qid, sec, f"({iq}) and de > {INS_LO}", "NEW")
        inspire_run(qid, sec, f"({iq}) and de > {day_before(CTRL_START)} and de < 2026-10-21", "CTRL")
    if SUBSET != "control":
        # revisions of known papers: version and last update, one request
        for k in range(0, len(KNOWN), 25):
            arxiv_run(f"K{k // 25 + 1:02d}", "K", "id_list", NEW_START, NOW_S, "KNOWN", id_list=KNOWN[k:k + 25])
        for label, recid, look in TRAILS:
            title = None
            if recid is None:
                recid, title = lookup_recid(look)
            if recid is None:
                RUNS.append(dict(qid="T?", section="T", source="inspire", window="TRAIL", query=label + " (recid lookup failed)", total=None, hits=[], http=0, url="", raw="", sha256=""))
                continue
            inspire_run("T:" + label, "T", f"refersto:recid:{recid} and de > {INS_LO}", "NEW")
            inspire_run("T:" + label, "T", f"refersto:recid:{recid}", "ALLTIME")
            RUNS[-1]["recid"] = RUNS[-2]["recid"] = recid
    else:
        inspire_run("T:Shirokov 2608.24577", "T", "refersto:recid:3195733", "ALLTIME")
    check()


def check():
    fails = []
    # C1
    for qid, sec, aq, iq, exp in Q:
        if not exp:
            continue
        got = {h["id"] for r in RUNS if r["qid"] == qid and r["window"] == "CTRL" and r["source"] == "arxiv" for h in r["hits"]}
        if not exp <= got:
            fails.append(f"C1 {qid}: arXiv CTRL missing {sorted(exp - got)}")
    for qid, sec, iq, exp in INSP_ONLY:
        if not exp:
            continue
        got = {h["id"] for r in RUNS if r["qid"] == qid and r["window"] == "CTRL" and r["source"] == "inspire" for h in r["hits"]}
        if r_ran(qid) and not exp <= got:
            fails.append(f"C1 {qid}: INSPIRE CTRL missing {sorted(exp - got)}")
    # C2
    for r in RUNS:
        if r["window"] != "NEW":
            continue
        for h in r["hits"]:
            d = (h.get("published") or h.get("date") or "")[:10]
            if r["source"] == "arxiv" and d < NEW_START:
                fails.append(f"C2 {r['qid']}: arXiv {h['id']} published {d} < {NEW_START}")
            if r["source"] == "inspire" and d and d < NEW_START and len(d) == 10:
                fails.append(f"C2 {r['qid']}: INSPIRE {h.get('id') or h.get('recid')} date {d} < {NEW_START}")
    # C3
    for r in RUNS:
        if r["qid"] == "Z01" and r["total"] != 0:
            fails.append(f"C3 Z01 {r['source']} {r['window']}: total {r['total']} != 0")
    # C4
    c4 = [h["id"] for r in RUNS if r["qid"] == "T:Shirokov 2608.24577" and r["window"] == "ALLTIME" for h in r["hits"]]
    if "2610.13206" not in c4:
        fails.append("C4: Shirokov citers do not list 2610.13206")
    bad = [r["qid"] + " " + r["window"] for r in RUNS if r["http"] != 200]
    if bad:
        fails.append("HTTP failures: " + ", ".join(bad))
    with open(os.path.join(OUT, "queries.json"), "w") as f:
        json.dump(dict(generated=NOW.strftime("%Y-%m-%dT%H:%MZ"), mutate=MUT, subset=SUBSET, new_start=NEW_START, runs=RUNS, control_failures=fails), f, indent=1)
    for x in fails:
        print("FAIL", x)
    print("controls:", "FAIL" if fails else "PASS", len(RUNS), "runs")
    sys.exit(1 if fails else 0)


def r_ran(qid):
    return any(r["qid"] == qid for r in RUNS)


if __name__ == "__main__":
    main()
