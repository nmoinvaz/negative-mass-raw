"""mut_summary.py DIR PREFIX: fired sets and the detail of each fired check of the stored mutation logs DIR/PREFIX<name>.log."""
import os, re, sys
d, pre = sys.argv[1], sys.argv[2]
names = "s_q s_pot th_noF th_nophi th_asign dm_noT kappa_off jump_off xform_p xform_q mode_khat mode_dF0 fn_c1_noV fn_c1_aT fn_c1_sign law_norm".split()
for n in names:
    p = os.path.join(d, f"{pre}{n}.log")
    if not os.path.exists(p):
        print(f"{n}: no log"); continue
    fired = []
    for line in open(p):
        m = re.match(r"\[FAIL\] (\w+): .*?  \((.*)\)$", line.rstrip("\n"))
        if m:
            fired.append((m.group(1), m.group(2)))
        elif line.startswith("[FAIL]"):
            fired.append((line[7:].split(":")[0], ""))
    print(f"{n}: fired {[f for f, _ in fired]}")
    for f, det in fired:
        print(f"    {f}: {det[:420]}")
