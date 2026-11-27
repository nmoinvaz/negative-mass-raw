

# ------------------------------------------------------------------------------------------------ driver
def main():
    global MUT
    argv = [a for a in sys.argv[1:] if not a.startswith("--mutate=")]
    for a in sys.argv[1:]:
        if a.startswith("--mutate="):
            MUT |= set(a.split("=", 1)[1].split(","))
    opts = {a.split("=")[0]: a.split("=", 1)[1] for a in argv if a.startswith("--") and "=" in a}
    pos = [a for a in argv if not a.startswith("--")]
    cmd = pos[0] if pos else None
    if cmd == "planted":
        sys.exit(0 if planted_command() else 1)
    if cmd == "count":
        o = count_polar(int(pos[1]), float(pos[2]), opts.get("--res", "R2"))
        s = json.dumps(o, indent=1)
        if "--out" in opts:
            open(opts["--out"], "w").write(s)
        print(s)
        return
    if cmd == "mads":
        o = count_mads(float(pos[1]), opts.get("--res", "R2"))
        s = json.dumps(o, indent=1)
        if "--out" in opts:
            open(opts["--out"], "w").write(s)
        print(s)
        return
    if cmd == "spectral":
        sys.exit(0 if spectral_command(pos[1]) else 1)
    if cmd == "report":
        sys.exit(0 if report_command(pos[1]) else 1)
    if cmd == "controls":
        sys.exit(0 if controls_command() else 1)
    raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
