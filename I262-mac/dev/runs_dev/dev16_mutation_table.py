"""dev16: the fired sets and the effects of the development mutation runs (dev15_*), as the table of the README."""
import glob, re, os, ast
rows = []
for fn in sorted(glob.glob("dev15_check_*.log") + glob.glob("dev15_derive_*.log")):
    name = re.match(r"dev15_(?:check|derive)_(.*)\.log", os.path.basename(fn)).group(1)
    kind = "check" if "_check_" in fn else "derive"
    txt = open(fn).read()
    for line in txt.splitlines():
        if line.startswith("[FAIL]"):
            cid = line.split(":")[0].replace("[FAIL] ", "")
            m = re.search(r"\((max relative difference[^)]*|[^()]*\([^()]*\)[^()]*|[^()]*)\)\s*$", line)
            det = line[line.rfind("  (") + 3:-1] if "  (" in line else ""
            rows.append((name, kind, cid, det[:220]))
for r in rows:
    print(" | ".join(r))
