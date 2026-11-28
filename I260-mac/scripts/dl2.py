#!/usr/bin/env python3
"""dl2.py LISTFILE OUTROOT: like dl.py (PDF only), two workers, requests started at least 3 s apart in total."""
import hashlib, os, sys, threading, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
ids = [l.split()[0] for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")]
root = sys.argv[2]
UA = {"User-Agent": "negative-mass-literature-reader/1.0"}
lock = threading.Lock(); last = [0.0]; wlock = threading.Lock()
def gate():
    with lock:
        w = last[0] + 3.0 - time.time()
        if w > 0: time.sleep(w)
        last[0] = time.time()
def one(i):
    d = os.path.join(root, i.replace("/", "_")); pdf = os.path.join(d, "paper.pdf")
    if os.path.exists(pdf): return
    os.makedirs(d, exist_ok=True)
    url = f"https://arxiv.org/pdf/{i}"
    for k in range(4):
        gate()
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read()
            open(pdf, "wb").write(data)
            with wlock, open(os.path.join(root, "downloads.tsv"), "a") as f:
                f.write(f"{url}\t{os.path.relpath(pdf, root)}\t{len(data)}\t{hashlib.sha256(data).hexdigest()}\n")
            return
        except Exception as e:
            print("retry", url, k, e, file=sys.stderr); time.sleep(5 * (k + 1))
    print("FAILED", url)
with ThreadPoolExecutor(2) as ex: list(ex.map(one, ids))
print("done", len(ids))
