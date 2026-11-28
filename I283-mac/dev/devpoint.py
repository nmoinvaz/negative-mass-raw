#!/usr/bin/env python3
"""devpoint.py ROOT B XC W H [lo hi]: development. One route point at one h: bracket scan (unless lo, hi given), p*_h bisection, chain, pair, then the line of results.
run_point() is also used by devtune.py. Run with NUMBA_NUM_THREADS=1, nice 10."""
import json, os, sys, time
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i283/notes/wormhole_evolution"))
import settled_mass_route as r


def run_point(root, spec, h, bracket=None):
    base = os.path.join(root, r.tag_of("G", spec), f"h{h:g}")
    t0 = time.time()
    if bracket is None:
        lo, hi, rows = r.bracket_scan(spec, h)
        print("bracket", lo, hi, [(x["A"], x["fate"]) for x in rows], flush=True)
        if lo is None:
            return dict(spec=spec, h=h, status="no bracket")
        bracket = (lo, hi)
    r.pstar_cmd(spec, h, base + "/pstar", bracket)
    r.job_cmd(spec, h, base + "/chain", root)
    ok = r.load_point(root, spec, h)
    stalls, dm, dp = r.b.stalls(ok)
    if not stalls:
        out = dict(spec=spec, h=h, ps=ok["p"]["ps"], status=ok["i"]["status"], stall=False, gain=[dm, dp], M=r.g.summary_g(ok["s"], h)["plat1"] if len(ok["s"]["r"]) else None, secs=round(time.time() - t0))
        return out
    r.member_cmd(spec, h, base + "/member", root)
    e = r.load_point(root, spec, h)
    d = r.read_point(e)
    return dict(spec=spec, h=h, ps=e["p"]["ps"], status=e["i"]["status"], stall=True, gain=[dm, dp], M=d["M"], g1=d["mem"]["g1"], rth=d["mem"]["r_th"], tdep=d["mem"]["t_dep"], rdot=d["sp"],
                secs=round(time.time() - t0))


if __name__ == "__main__":
    root, B, xc, w, h = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
    br = (float(sys.argv[6]), float(sys.argv[7])) if len(sys.argv) >= 8 else None
    print("RESULT", json.dumps(run_point(root, (B, xc, w), h, br)), flush=True)
