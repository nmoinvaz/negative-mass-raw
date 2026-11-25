#!/usr/bin/env python3
"""Derive the unified diff of the proposed text against notes/critical_ghost.md at main dffa582 from proposal.md.

usage: python3 -I make_diff.py [--write] [--check] [--mutate=anchor|text]
  --write   replace the block between <!-- diff:begin --> and <!-- diff:end --> in proposal.md by the derived diff
  --check   exit 1 if that block differs from the derived diff, or if `patch --dry-run` does not apply it to the stored
            copy of the note (patch is skipped, with a notice, when it is not installed)
The rows of proposal.md (### Row Rn table|bullets|entry) carry an `anchor:` line, `after N | <line prefix>` or
`replace A-B | <prefix of line A>`, where N, A, B are 1-based line numbers of src/critical_ghost_dffa582.md; the prefix is
checked against that line. A table row also has `col1:` and `col3:`; its middle cell is the joined sentences. Bullets are
wrapped at 120 characters, a bullet at four spaces, an entry at two. A sentence tagged {KEEP} is existing text of the note.
"""
import difflib
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE / "src/critical_ghost_dffa582.md"
BEGIN, END = "<!-- diff:begin -->", "<!-- diff:end -->"


def parse_rows(text):
    rows, cur = [], None
    for line in text.splitlines():
        m = re.match(r"^### Row (R\d+) (table|bullets|entry)\s*$", line)
        if m:
            cur = {"id": m.group(1), "type": m.group(2), "sents": [], "meta": {}}
            rows.append(cur)
            continue
        if cur is None:
            continue
        m = re.match(r"^(anchor|col1|col3): (.*)$", line)
        if m:
            cur["meta"][m.group(1)] = m.group(2).strip()
            continue
        m = re.match(r"^- (R\d+)\.(\d+) (.+) \{([^}]*)\}\s*$", line)
        if m and m.group(1) == cur["id"]:
            cur["sents"].append((int(m.group(2)), m.group(3)))
    for r in rows:
        r["sents"] = [s for _, s in sorted(r["sents"])]
    return rows


def render(row):
    if row["type"] == "table":
        return [f"| {row['meta']['col1']} | {' '.join(row['sents'])} | {row['meta']['col3']} |"]
    ind1, ind2 = ("    - ", "      ") if row["type"] == "bullets" else ("  - ", "    ")
    out = []
    for s in row["sents"]:
        # keep "24 %" together: a line must not start with "%"
        out += [ln.replace("\x01", " ") for ln in textwrap.wrap(s.replace(" %", "\x01%"), width=120, initial_indent=ind1,
                                                                 subsequent_indent=ind2, break_long_words=False, break_on_hyphens=False)]
    return out


def derive(proposal_text, mutate=None):
    base = BASE.read_text(encoding="utf-8").split("\n")
    edits = []  # (first line index, last line index exclusive, new lines)
    for row in parse_rows(proposal_text):
        m = re.match(r"^(after|replace) (\d+)(?:-(\d+))? \| (.*)$", row["meta"].get("anchor", ""))
        if not m:
            raise SystemExit(f"{row['id']}: bad or missing anchor")
        kind, a, b, prefix = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2)), m.group(4)
        if mutate == "anchor":
            a += 1
        if not base[a - 1].startswith(prefix):
            raise SystemExit(f"{row['id']}: line {a} of the base note does not start with {prefix!r}: {base[a - 1][:60]!r}")
        if kind == "after":
            edits.append((a, a, render(row)))
        else:
            edits.append((a - 1, b, render(row)))
    if mutate == "text":
        lo, hi, lines = edits[0]
        edits[0] = (lo, hi, [lines[0] + " x"] + lines[1:])
    new = list(base)
    for lo, hi, lines in sorted(edits, reverse=True):
        new[lo:hi] = lines
    diff = difflib.unified_diff(base, new, fromfile="a/notes/critical_ghost.md", tofile="b/notes/critical_ghost.md", lineterm="")
    return "\n".join(diff) + "\n", "\n".join(new)


def block_of(text):
    i, j = text.index(BEGIN), text.index(END)
    return text[i + len(BEGIN):j].strip("\n")


def main():
    mutate = None
    for a in sys.argv[1:]:
        if a.startswith("--mutate="):
            mutate = a.split("=", 1)[1]
    p = HERE / "proposal.md"
    text = p.read_text(encoding="utf-8")
    diff, new = derive(text, mutate)
    want = "```diff\n" + diff.rstrip("\n") + "\n```"
    if "--write" in sys.argv:
        i, j = text.index(BEGIN), text.index(END)
        p.write_text(text[:i + len(BEGIN)] + "\n" + want + "\n" + text[j:], encoding="utf-8")
        print(f"wrote the diff block ({diff.count(chr(10))} lines)")
        return 0
    bad = 0
    if block_of(text) != want:
        print("FAIL C9: the diff block of proposal.md differs from the diff derived from its sentences")
        bad = 1
    if shutil.which("patch"):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "notes").mkdir()
            shutil.copy(BASE, Path(d) / "notes" / "critical_ghost.md")
            (Path(d) / "x.diff").write_text(block_of(text).split("\n", 1)[1].rsplit("\n```", 1)[0] + "\n", encoding="utf-8")
            r = subprocess.run(["patch", "-p1", "--dry-run", "-i", "x.diff"], cwd=d, capture_output=True, text=True)
            if r.returncode != 0:
                print("FAIL C9: patch --dry-run does not apply the diff:", (r.stdout + r.stderr)[:300])
                bad = 1
    else:
        print("C9 patch check skipped: patch is not installed")
    print("C9", "FAIL" if bad else "ok")
    return bad


sys.exit(main())
