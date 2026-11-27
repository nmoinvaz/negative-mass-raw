"""Shares of the non-idle samples in macOS `sample` output: top-of-stack by function, and inclusive counts on the main thread."""
import re, sys
for f in sys.argv[1:]:
    t = open(f).read().split("\n")
    i = [k for k, l in enumerate(t) if l.startswith("Sort by top of stack")][0]
    top = {}
    for l in t[i + 1:]:
        m = re.match(r"\s+(.*?)\s+\(in .*?\)\s+(\d+)\s*$", l)
        if m: top[m[1]] = top.get(m[1], 0) + int(m[2])
    idle = top.get("__psynch_cvwait", 0)
    busy = sum(top.values()) - idle
    rec = sum(v for k, v in top.items() if k.startswith("taylor_radial::bvp::recursion"))
    md = sum(v for k, v in top.items() if k.startswith("multidouble::"))
    mem = sum(v for k, v in top.items() if "malloc" in k or "free" in k or "memmove" in k or "bzero" in k)
    print(f"{f.split('/')[-1]}: busy samples {busy}, idle (cvwait) {idle}; bvp::recursion {rec/busy:.3f}, multidouble:: {md/busy:.3f}, malloc/free/memcpy {mem/busy:.3f}")
