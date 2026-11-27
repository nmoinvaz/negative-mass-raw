#!/usr/bin/env python3
"""dl.py LISTFILE OUTROOT [--src]: for each arXiv id in LISTFILE download the PDF (and with --src the e-print) into its own
new directory OUTROOT/<id with / -> _>/ ; appends 'id<TAB>file<TAB>bytes<TAB>sha256' to OUTROOT/downloads.tsv. Skips existing."""
import hashlib, os, sys, time, urllib.request
ids = [l.split()[0] for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")]
root = sys.argv[2]; src = "--src" in sys.argv
UA = {"User-Agent": "negative-mass-literature-reader/1.0"}
def get(url, dest):
    for k in range(4):
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read()
            open(dest, "wb").write(data)
            with open(os.path.join(root, "downloads.tsv"), "a") as f:
                f.write(f"{url}\t{os.path.relpath(dest, root)}\t{len(data)}\t{hashlib.sha256(data).hexdigest()}\n")
            return True
        except Exception as e:
            print("retry", url, k, e, file=sys.stderr); time.sleep(5 * (k + 1))
    print("FAILED", url); return False
for i in ids:
    d = os.path.join(root, i.replace("/", "_"))
    pdf = os.path.join(d, "paper.pdf")
    if not os.path.exists(pdf):
        os.makedirs(d, exist_ok=True)
        get(f"https://arxiv.org/pdf/{i}", pdf); time.sleep(3)
    if src and not os.path.exists(os.path.join(d, "source.tgz")):
        get(f"https://arxiv.org/e-print/{i}", os.path.join(d, "source.tgz")); time.sleep(3)
print("done", len(ids))
