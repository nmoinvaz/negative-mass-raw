import re, sys
fn = sys.argv[1]
txt = open(fn).read().split("%%EndProlog")[1]
lines = txt.splitlines()
# find curve starts: lines of form "<x> <y> M" with x ~ 1176..1300 after the key legend; print key legend labels and colors
cur = None; curves = []; color = None; path = None
for ln in lines:
    ln = ln.strip()
    m = re.match(r"^(LT\d|LTb|LTa|LCb|LC\d)", ln)
    if m: color = m.group(1)
    m = re.match(r"^(-?\d+) (-?\d+) M$", ln)
    if m:
        if path: curves.append((color, path))
        x, y = int(m.group(1)), int(m.group(2)); path = [(x, y)]; cur = (x, y); continue
    if path is None: continue
    m = re.match(r"^(-?\d+) (-?\d+) ([VR])$", ln)
    if m:
        dx, dy = int(m.group(1)), int(m.group(2)); cur = (cur[0] + dx, cur[1] + dy)
        if m.group(3) == "V": path.append(cur)
        continue
    m = re.match(r"^(-?\d+) (-?\d+) L$", ln)
    if m:
        cur = (int(m.group(1)), int(m.group(2))); path.append(cur); continue
if path: curves.append((color, path))
x0, xs = int(sys.argv[2]), float(sys.argv[3])
y0, ys = 768, float(sys.argv[4])
for color, p in curves:
    if len(p) < 5: continue
    print(color, len(p), "first points (M, y):", [(round((a - x0) / xs, 4), round((b - y0) / ys, 4)) for a, b in p[:3]], "last:", (round((p[-1][0] - x0) / xs, 3), round((p[-1][1] - y0) / ys, 3)))
