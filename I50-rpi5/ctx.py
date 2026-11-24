"""usage: python -I ctx.py FILE REGEX [WIDTH=250] [MAX=6]: print up to MAX matches of REGEX with WIDTH chars each side (whitespace collapsed)."""
import re, sys
t = re.sub(r'\s+', ' ', open(sys.argv[1], encoding='utf-8', errors='replace').read())
w = int(sys.argv[3]) if len(sys.argv) > 3 else 250
mx = int(sys.argv[4]) if len(sys.argv) > 4 else 6
n = 0
for m in re.finditer(sys.argv[2], t, re.I):
    print('...' + t[max(0, m.start() - w): m.end() + w] + '...\n')
    n += 1
    if n >= mx: break
print('matches shown:', n, 'of', len(re.findall(sys.argv[2], t, re.I)))
