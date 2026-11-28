import json, re, sys
pats = sys.argv[1]
files = sys.argv[2:]
seen = {}
for fn in files:
    for r in json.load(open(fn)):
        t = r["titles"][0]["title"]
        ab = " ".join(a["value"] for a in r.get("abstracts", []))
        txt = t + " " + ab
        if re.search(pats, txt, re.I):
            seen.setdefault(r["_id"], (r, fn))
for k, (r, fn) in sorted(seen.items(), key=lambda kv: kv[1][0].get("earliest_date", "")):
    e = (r.get("arxiv_eprints") or [{}])[0].get("value", "-")
    print(k, e, r.get("earliest_date", "-")[:7], r.get("citation_count"), r["titles"][0]["title"][:100], "|", fn.split("cit_")[1][:-5])
print(len(seen), "hits")
