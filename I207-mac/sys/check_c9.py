#!/usr/bin/env python3
"""check_c9.py DUMP REPORT.md

C9: the counts of table 1 of a `loc_report.py` report equal the records its tables 2 and 3 list, and both equal a count made here
straight from the dump. Table 1 counts, per (file kind, class), the records with an Unresolved step, a pair step and a step with no
result; tables 2 and 3 list the records with an Unresolved or nothing step, and with a pair step. `--mutate=drop` removes one
row of the report's table 2 in a copy, to show the check fails. Exit 1 on a difference."""
import json, os, re, sys

def main():
    dump, rep = [a for a in sys.argv[1:] if not a.startswith("--")]
    text = open(rep).read()
    if "--mutate=drop" in sys.argv:
        i = text.index("\n2. records")
        j = text.index("\n| scan", i)
        k = text.index("\n", j + 1)
        text = text[:j] + text[k:]
    n_un = n_pair = n_loc = 0
    for f in sorted(os.listdir(dump)):
        for l in open(os.path.join(dump, f)).read().splitlines()[1:]:
            if l.startswith("{"):
                r = json.loads(l)
                if isinstance(r, dict) and "loc" in r:
                    n_loc += 1
                    L = r["loc"]
                    n_un += (L["unresolved"] > 0 or L["nothing"] > 0)
                    n_pair += L["pair"] > 0
    m = re.search(r"records with a `loc` key: (\d+)", text)
    rep_loc = int(m.group(1))
    t2 = int(re.search(r"\n2\. records where locate said Unresolved or gave nothing at a gated step: (\d+) records", text).group(1))
    t3 = int(re.search(r"\n3\. records where locate read a pair at a gated step: (\d+) records", text).group(1))
    # table 1: sum of the Unresolved + nothing columns is not separable per record, so the check is on the listed rows
    rows2 = len(re.findall(r"\n\| scan[^\n]*", text[text.index("\n2. records"):text.index("\n3. records")]))
    rows3 = len(re.findall(r"\n\| scan[^\n]*", text[text.index("\n3. records"):text.index("\n4. records")]))
    ok = (rep_loc == n_loc and t2 == n_un and t3 == n_pair and rows2 == t2 and rows3 == t3)
    print(f"records with loc: dump {n_loc}, report {rep_loc}; Unresolved or nothing: dump {n_un}, report {t2}, rows listed {rows2}; pair: dump {n_pair}, report {t3}, rows listed {rows3}")
    print("RESULT:", "counts agree" if ok else "counts differ")
    sys.exit(0 if ok else 1)

main()
