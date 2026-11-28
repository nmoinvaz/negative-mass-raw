#!/usr/bin/env python3
"""mut_targets.py LOGDIR: reads the `mutation NAME: fired [...]; ...; newly fired [...]` line of each LOGDIR/<name>.log (the highest-numbered rerun) and prints the MUTATIONS dict body of
settled_mass_route.py (the checks a mutation newly fails, those failing without a mutation excluded)."""
import glob, os, re, sys
out = {}
for f in sorted(glob.glob(os.path.join(sys.argv[1], "*.log"))):
    nm = os.path.basename(f)[:-4]
    if "." in nm or nm.startswith("aborted") or nm == "ana":
        continue
    lines = [l for l in open(f) if l.startswith("mutation ")]
    if not lines:
        print(f"# {nm}: no mutation line", file=sys.stderr)
        continue
    m = re.search(r"newly fired (\[[^\]]*\])", lines[-1])
    out[nm] = eval(m.group(1))
for nm in sorted(out):
    print(f'    "{nm}": {out[nm]!r},')
