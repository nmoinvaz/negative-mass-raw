"""check_quotes.py NOTE OUTPUT [OTHER...]: every scientific number d.ddd e-xx and every decimal with >= 5 digits in NOTE must occur in OUTPUT (or in the OTHER files, the notes it quotes);
exponents are compared with two digits (e-9 = e-09). Prints the numbers not found."""
import re, sys
def norm(t):
    return re.sub(r"e([-+]?)(\d)(?!\d)", lambda m: f"e{m.group(1) or '+'}0{m.group(2)}", t.replace("−", "-"))
note = open(sys.argv[1]).read()
hay = norm(open(sys.argv[2]).read())
for f in sys.argv[3:]:
    hay += "\n" + norm(open(f).read())
nums = set(re.findall(r"\d\.\d+e[-+]?\d+", note.replace("−", "-"))) | set(re.findall(r"\b\d\.\d{5,}\b", note))
bad = []
for n in sorted(nums):
    nn = norm(n)
    if nn not in hay:
        bad.append(n)
print(f"{len(nums)} numbers, {len(bad)} not found")
for n in bad:
    print("  ", n)
