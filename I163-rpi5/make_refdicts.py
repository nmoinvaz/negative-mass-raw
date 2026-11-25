import re
def load(f):
    d={}
    for l in open(f):
        m=re.match(r"g=(\S+) beta_A=(\S+) ",l)
        if m: d[float(m.group(1))]=m.group(2)
    return d
for name,f in (("FIRST_ROW_BETA","baseline_first_row_main2455a0d.log"),("FIRST_ROW_BETA_L60","legacy_Lspread_L60.log")):
    d=load(f); print(name+" = {"+", ".join(f"{g!r}: {v}" for g,v in d.items())+"}")
