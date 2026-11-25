#!/usr/bin/env python3
"""Summarize the mutated runs of notes/ellis_efold.py against the predictions of README.md section 5.

    python3 summarize_mutations.py          writes mutations_summary.md next to this file and prints it

For each mut_<name>.log: the ids of the checks that FAILed, the target ids and the 'predicted not to fail' ids from the README
table (rows whose first cell is `name`), and the verdict:
    fired    every target id failed
    SILENT   some target id did not fail (a result; the target list is not edited)
and 'mispredicted' = ids that failed although the README predicted they would not.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IDS = r"(?:U1|U2|S1|L1|W1|P-A|P-B|P-C|G[0-7]|D1)"


def readme_table():
    rows = {}
    sec = open(os.path.join(HERE, "README.md")).read().split("## 5.")[1].split("## 6.")[0]
    for line in sec.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 4 and cells[0].startswith("`"):
            name = cells[0].strip("`")
            allowed = re.sub(r"\([^)]*may fail[^)]*\)", "", cells[3])  # ids the README says 'may fail' are not predictions
            rows[name] = (re.findall(IDS, cells[2]), re.findall(IDS, allowed), cells[2], cells[3])
    return rows


def one(name, tag, target, notfail):
    suffix = "" if tag == "run1" else "_" + tag
    log = os.path.join(HERE, f"mut_{name}{suffix}.log")
    if not os.path.exists(log):
        return f"| `{name}` {tag} | not run | | {', '.join(target)} | | | | |", True
    text = open(log).read()
    failed = []
    for m in re.finditer(r"^FAIL  (" + IDS + r"):", text, re.M):
        if m.group(1) not in failed:
            failed.append(m.group(1))
    rcf = os.path.join(HERE, f"mut_{name}{suffix}.rc")
    rc = open(rcf).read().strip() if os.path.exists(rcf) else "?"
    wall = "?"
    tf = os.path.join(HERE, f"mut_{name}{suffix}.time")
    if os.path.exists(tf):
        m = re.search(r"Elapsed \(wall clock\) time.*: (\S+)", open(tf).read())
        wall = m.group(1) if m else "?"
    done = "\ncontrol " in text  # the script prints this line last, only when it ran to the end
    state = "complete" if done else ("stopped by me (hung)" if rc == "143" else "crashed")
    silent = [t for t in target if t not in failed]
    verdict = "fired" if not silent else "SILENT on " + ", ".join(silent)
    mis = [f for f in failed if f in notfail]
    other = [f for f in failed if f not in target and f not in notfail]
    row = (f"| `{name}` {tag} | {rc} | {wall} | {', '.join(target)} | {', '.join(failed) or '-'} | {state}; {verdict} | "
           f"{', '.join(mis) or '-'} | {', '.join(other) or '-'} |")
    return row, bool(silent or mis or not done)


def main():
    table = readme_table()
    out = ["| mutation, run | rc | wall | must fail (README) | failed | state; verdict | failed although predicted not to | other failed (not predicted either way) |",
           "|---|---|---|---|---|---|---|---|"]
    bad_final = 0
    for name, (target, notfail, _, _) in table.items():
        row, bad = one(name, "run1", target, notfail)
        out.append(row)
        for tag in ("run2", "run3"):
            if os.path.exists(os.path.join(HERE, f"mut_{name}_{tag}.log")):
                row2, bad2 = one(name, tag, target, notfail)
                out.append(row2)
                bad = bad2  # a rerun replaces the earlier run's verdict; all runs are listed
        bad_final += bad
    text = "\n".join(out) + "\n"
    open(os.path.join(HERE, "mutations_summary.md"), "w").write(text)
    print(text)
    print(f"{bad_final} mutation(s) silent, mispredicted, incomplete or not run (counting the latest run of each)")
    return 1 if bad_final else 0


if __name__ == "__main__":
    sys.exit(main())
