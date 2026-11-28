#!/usr/bin/env python3
"""check_cargo.py CARGO_TOML [CARGO_LOCK]: criterion C3. Every dependency of Cargo.toml is named by an exact released version
("=x.y.z", alone or as `version`), with no git, path, rev, branch or tag key and no absolute path anywhere in the file; in
Cargo.lock every package but the crate itself has a registry source and none has a git source. Exits 1 if any fails.
Mutation: the Cargo.toml of main 1b44c49 (a git pin to eaf55a8) must fail (check_cargo_mutation_01.log)."""
import re, sys, tomllib

bad = []
t = tomllib.load(open(sys.argv[1], "rb"))
txt = open(sys.argv[1]).read()
for name, v in t.get("dependencies", {}).items():
    ver = v if isinstance(v, str) else v.get("version", "")
    if not re.fullmatch(r"=\d+\.\d+\.\d+", ver):
        bad.append(f"{name}: version {ver!r} is not an exact release")
    if isinstance(v, dict):
        for k in ("git", "path", "rev", "branch", "tag"):
            if k in v:
                bad.append(f"{name}: key {k}")
if re.search(r"(/Users/|/home/|[A-Za-z]:\\\\)", txt):
    bad.append("an absolute path in Cargo.toml")
if len(sys.argv) > 2:
    lock = tomllib.load(open(sys.argv[2], "rb"))
    for p in lock.get("package", []):
        s = p.get("source", "")
        if s.startswith("git+"):
            bad.append(f"lock: {p['name']} from a git source")
        elif p["name"] != t["package"]["name"] and not s.startswith("registry+"):
            bad.append(f"lock: {p['name']} has no registry source")
    print("lock packages:", ", ".join(f"{p['name']} {p['version']}" for p in lock["package"] if p["name"] in t.get("dependencies", {})))
print("deps:", {k: (v if isinstance(v, str) else v) for k, v in t.get("dependencies", {}).items()})
print("C3:", "NOT MET: " + "; ".join(bad) if bad else "met")
sys.exit(1 if bad else 0)
