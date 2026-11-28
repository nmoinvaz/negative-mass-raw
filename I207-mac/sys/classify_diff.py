#!/usr/bin/env python3
"""classify_diff.py BASE_LOG RUN_LOG

The gated log lines of `compare_outputs.py` (unchanged, imported), sorted into three kinds (the third is declared below) before anything is read from them:
 (i)  zero-token: the lines are equal once the token `0.0e+00` is replaced by the comparator's own error token `<err>` on both
      sides. The comparator turns every number in scientific notation with an exponent of -6 or smaller into `<err>` (an error,
      a bar, a residual) and leaves an exact zero as it is, so an error that is exactly 0.0e+00 in one run and rounding-sized in
      the other is a difference to it. These are error-sized numbers; they are listed.
 (ii) every other difference: a label, a count, a class, a kind, an eta* printed to 10 digits, a pass or fail, a line count.
Prints the counts and every line of both kinds. Exit 1 if there is a line of kind (ii).

A third kind, declared from the baseline's lines before any run of record, is (iii) fitted exponent: the lines are equal once
the fitted exponent and its ratio to 2/(eta*^2 + 4) are masked, in the two places the baseline prints them: the closing line of
the scan summary ("measured exponent ... worst relative difference X") and the `dd_qd` note ("double-double X (R) F->0;
quad-double X (R) F->0"). The exponent is what the feature changes (the old fit was off by up to 6% in the O8 regime), so it
is listed, not gated; the eta*, the kinds and every other number on those lines stay compared."""
import difflib, os, re, sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import compare_outputs as co  # noqa: E402  (the comparator of #190, unchanged)


MASKS = [
    (re.compile(r"(measured exponent against 2/\(eta\*\^2 \+ 4\): worst relative difference )\S+"), r"\1<fit>"),
    (re.compile(r"(double-double |quad-double )\S+ \(\S+\)"), r"\1<fit> (<fit>)"),
]


def mask(s):
    for rx, to in MASKS:
        s = rx.sub(to, s)
    return s


def main():
    la, lb = co.log_lines(sys.argv[1]), co.log_lines(sys.argv[2])
    zero = lambda s: s.replace("0.0e+00", "<err>")  # noqa: E731
    z, o, f = [], [], []
    notes = []
    if len(la) != len(lb):
        notes.append(f"line counts differ: {len(la)} against {len(lb)} (lines are aligned by difflib before they are paired)")
    # the lines are aligned first: an inserted or deleted line (a longer list in a NOTE) must not shift every line after it
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        if tag == "replace" and i2 - i1 == j2 - j1:
            for k in range(i2 - i1):
                x, y = la[i1 + k], lb[j1 + k]
                if zero(x) == zero(y):
                    z.append((i1 + k, x, y))
                elif zero(mask(x)) == zero(mask(y)):
                    f.append((i1 + k, x, y))
                else:
                    o.append((i1 + k, x, y))
        else:
            for k in range(i1, i2):
                o.append((k, la[k], "(deleted)"))
            for k in range(j1, j2):
                o.append((i1, "(inserted)", lb[k]))
    print(f"lines {len(la)} against {len(lb)}; differing lines: {len(z) + len(f) + len(o)}; (i) zero-token {len(z)}; "
          f"(iii) fitted exponent {len(f)}; (ii) other {len(o)}")
    for t in notes:
        print(f"note: {t}")
    for k, name in ((z, "(i) zero-token"), (f, "(iii) fitted exponent"), (o, "(ii) other")):
        for t in k:
            print(f"{name} line {t[0]}:\n  base {t[1][:700]}\n  run  {t[2][:700]}")
    sys.exit(1 if o else 0)


main()
