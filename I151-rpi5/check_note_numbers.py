#!/usr/bin/env python3
"""Every number the note notes/ellis_efold.md quotes from a run must appear in notes/ellis_efold_output.txt (or, for the control
numbers, in the mutated run's log). Exit 1 if one does not."""
import os, re, sys
NOTE = os.path.expanduser("~/Source/negative-mass-i151/notes")
RAW = os.path.dirname(os.path.abspath(__file__))
out = open(os.path.join(NOTE, "ellis_efold_output.txt")).read()
md = open(os.path.join(NOTE, "ellis_efold.md")).read()
pot = open(os.path.join(RAW, "mut_potential.log")).read()
checks = [  # (what, string in the note, regex that must match in the source text)
    ("beta(1/2)", "1.875127511869", r"beta_A = 1\.875127511869", out),
    ("T(1/2)", "0.75835715", r"T = 0\.75835715\b", out),
    ("tau_SN", "5.1308", r"= 5\.1308\d", out),
    ("T(0)", "0.846045", r"T = 0\.846045\b", out),
    ("beta2(0)", "1.39705243", r"beta\^2 = 1\.39705243 ", out),
    ("-0.006 %", "0.006 %", r"-0\.006 %", out),
    ("SN26 measured T", "0.75676, 0.77302", r"T = 0\.75676 .*T = 0\.77302", out),
    ("SN26 pct", "−0.211 %", r"\(-0\.211 %", out),
    ("SN26 pct", "+1.933 %", r"\(\+1\.933 %", out),
    ("table worst", "worst 0.00048", r"worst \|T - printed\| = 0\.00048", out),
    ("L1", "1e-26", r"worst residual 1\.29e-26", out),
    ("D1 A", "3.5e-13", r"A \(rtol 1e-13 -> 1e-11, L \+10\) 3\.5e-13", out),
    ("D1 B", "7.4e-12", r"B \(N 3000 -> 6000, L \+10\) 7\.4e-12", out),
    ("D1 C", "2.1e-13", r"C \(r/dist 0\.5 -> 0\.3, 0\.7; L 25 -> 30\) 2\.1e-13", out),
    ("A-B", "5.8e-13", r"gamma_1 = 0\.5: A against B, rel 5\.75e-13", out),
    ("A-C", "1.0e-13", r"gamma_1 = 0\.5: C beta = .* rel to A 1\.04e-13", out),
    ("error bar", "5.6e-12", r"error bar of T from the spreads: 5\.6e-12", out),
    ("46 checks", "46 checks", r"checks: 46 run, failed ids: \[\]", out),
    ("potential T", "T = 0.8657", r"T = 0\.865706", pot),
    ("potential b2", "β² = 1.3343", r"beta\^2 = 1\.33431593", pot),
]
bad = 0
for what, mdstr, rx, src in checks:
    ok_md = mdstr in md
    ok_src = re.search(rx, src) is not None
    print(("ok  " if ok_md and ok_src else "BAD ") + f"{what}: note has {mdstr!r}: {ok_md}; source matches: {ok_src}")
    bad += not (ok_md and ok_src)
sys.exit(1 if bad else 0)
