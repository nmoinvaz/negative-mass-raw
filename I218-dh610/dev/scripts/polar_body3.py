

# ------------------------------------------------------------------------------------------------ report
ROOT_AGREE = 1e-6                                               # relative, M-AdS rates R1 against R2
PROBE_TOL = 1e-6                                                # relative, polar determinants at PROBES, R1 against R2
MONO_TOL = 1e-6                                                 # relative imaginary part of Y after the throat arc (no logarithm)


def load(d, pattern):
    rows = {}
    for fn in glob.glob(d + "/" + pattern):
        o = json.load(open(fn))
        rows.setdefault((o.get("ell"), o["c"]), {})[o["res"]] = o
    return rows


def report_command(d):
    ok_all = True
    rows = load(d, "polar_l*_*.json")
    for ell in (2, 1):
        print("Polar l = %d, real W in [%g, %g] (units 1/b), shooting; n = sign changes + 2 (flagged dips)" % (ell, W_LO, W_HI))
        print("%8s %10s %9s | %-3s %-3s | %-5s %-12s | %-24s %s" % ("c", "rho_h", "kappa", "nR1", "nR2", "dips", "max|dD|/|D|", "min|D| R1, R2", "status"))
        for (e, c) in sorted(rows):
            if e != ell:
                continue
            r1, r2 = rows[(e, c)].get("R1"), rows[(e, c)].get("R2")
            n1 = r1["n_roots"] if r1 else None
            n2 = r2["n_roots"] if r2 else None
            rel = max((abs(r1["probes"][k] - r2["probes"][k]) / max(abs(r1["probes"][k]), abs(r2["probes"][k])) for k in r1["probes"]), default=0.0) if r1 and r2 else float("nan")
            nd = sum(len(x["dips"]) for x in (r1, r2) if x)
            ok = r1 is not None and r2 is not None and n1 == n2 and rel <= PROBE_TOL
            ok_all &= ok
            ref = r2 or r1
            print("%8g %10s %9s | %-3s %-3s | %-5d %-12.2e | %-10.2e %-12.2e %s" % (
                c, "-" if ref["rh"] is None else "%.6f" % ref["rh"], "-" if ref["A1"] is None else "%.6f" % (ref["A1"] / 2), n1, n2, nd, rel,
                r1["D_absmin"] if r1 else float("nan"), r2["D_absmin"] if r2 else float("nan"), "ok" if ok else "FAIL"))
        print()
    mrows = {}
    for fn in glob.glob(d + "/mads_*_R*.json"):
        o = json.load(open(fn))
        mrows.setdefault(o["c"], {})[o["res"]] = o
    print("M-AdS wormholes, radial modes, Dirichlet at the AdS end, W in [%g, %g]" % (W_LO, W_HI))
    print("%8s | %-3s %-3s | %-18s %-18s | %-10s %-10s %s" % ("c", "nR1", "nR2", "W R1", "W R2", "R1 v R2", "monodromy", "status"))
    for c in sorted(mrows):
        r1, r2 = mrows[c].get("R1"), mrows[c].get("R2")
        w1 = [x["W"] for x in r1["roots"]] if r1 else []
        w2 = [x["W"] for x in r2["roots"]] if r2 else []
        rel = max([abs(a - b) / b for a, b in zip(w1, w2)] or [0.0])
        mono = max(x["monodromy_imag_max"] for x in (r1, r2) if x)
        ok = r1 is not None and r2 is not None and len(w1) == len(w2) and rel <= ROOT_AGREE and mono <= MONO_TOL
        ok_all &= ok
        print("%8g | %-3s %-3s | %-18s %-18s | %-10.1e %-10.1e %s" % (c, len(w1), len(w2), ",".join("%.10f" % w for w in w1) or "none", ",".join("%.10f" % w for w in w2) or "none", rel, mono, "ok" if ok else "FAIL"))
    return ok_all


# ------------------------------------------------------------------------------------------------ controls
# kind: count = the count of the control member must differ from the unmutated count; planted/spectral = the command must exit 1 with a FAIL line of the target
CONTROLS = [
    ("L_sign", "count", ("l2", -0.3)), ("hz_out", "count", ("l2", -1.5)), ("rmax", "count", ("l1", -0.3)), ("g1_wrong", "count", ("l1", -1.5)),
    ("scan_range", "count", ("mads", 0.5)), ("ads_bc", "specmads", "S6 spectral"), ("qnm_L", "planted", "P2 Ellis polar l = 2"),
    ("l1_pot", "planted", "P3a Ellis polar l = 1"), ("spec_sign", "spectral", "S6 spectral"),
]


def run_json(args):
    r = subprocess.run([sys.executable, __file__] + args, capture_output=True, text=True)
    return json.loads(r.stdout[r.stdout.index("{"):])


def controls_command():
    ok_all = True
    import tempfile
    for m, kind, tgt in CONTROLS:
        if kind == "count":
            sector, c = tgt
            args = {"l1": ["count", "1", str(c)], "l2": ["count", "2", str(c)], "mads": ["mads", str(c)]}[sector] + ["--res=R1"]
            base = run_json(args)
            mut = run_json(args + ["--mutate=" + m])
            fired = mut["n_roots"] != base["n_roots"]
            detail = f"{sector} c = {c}: n = {mut['n_roots']} against {base['n_roots']} unmutated"
            ret = 0
        else:
            if kind == "planted":
                r = subprocess.run([sys.executable, __file__, "planted", "--mutate=" + m], capture_output=True, text=True)
            elif kind == "specmads":                         # the shooting with the control, the spectral check without it
                tmp = tempfile.mkdtemp(prefix="nm_i218_ctl_")
                open(tmp + "/mads_0.5_R2.json", "w").write(json.dumps(run_json(["mads", "0.5", "--res=R1", "--mutate=" + m]) | {"res": "R2"}))
                r = subprocess.run([sys.executable, __file__, "spectral", tmp], capture_output=True, text=True)
            else:
                tmp = tempfile.mkdtemp(prefix="nm_i218_ctl_")
                open(tmp + "/mads_0.5_R2.json", "w").write(json.dumps(count_mads(0.5, "R1") | {"res": "R2"}))
                r = subprocess.run([sys.executable, __file__, "spectral", tmp, "--mutate=" + m], capture_output=True, text=True)
            txt = r.stdout + r.stderr
            fired = r.returncode == 1 and any(tgt in l and l.startswith("FAIL") for l in txt.splitlines())
            detail = "; ".join(l[:150] for l in txt.splitlines() if l.startswith("FAIL"))[:300]
            ret = r.returncode
        print(("fires   " if fired else "SILENT  ") + f"--mutate={m} (target {tgt}): exit {ret}; {detail}", flush=True)
        ok_all &= fired
    return ok_all
