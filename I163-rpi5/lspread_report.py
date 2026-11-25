import re,sys
def load(f):
    d={}
    for l in open(f):
        m=re.match(r"g=(\S+) beta_A=(\S+) ",l)
        if m: d[float(m.group(1))]=float(m.group(2))
    return d
b=load("baseline_first_row_main2455a0d.log"); l45=load("legacy_Lspread_L45.log"); l60=load("legacy_Lspread_L60.log")
print(f"{'g':>4} {'beta(L=30)':>20} {'rel(45-30)':>11} {'rel(60-30)':>11} {'rel(60-45)':>11}")
for g in b:
    print(f"{g:4.1f} {b[g]:20.15f} {abs(l45[g]/b[g]-1):11.2e} {abs(l60[g]/b[g]-1):11.2e} {abs(l60[g]/l45[g]-1):11.2e}")
