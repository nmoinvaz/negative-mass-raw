from math import isqrt
# rational points on y^2 = x^3 + k as (a/d^2, b/d^3): b^2 = a^3 + k d^6
for k in (432, -432, 16, -16):
    pts = []
    for d in range(1, 13):
        for a in range(-60 * d * d, 60 * d * d):
            v = a**3 + k * d**6
            if v >= 0:
                b = isqrt(v)
                if b * b == v: pts.append((a, b, d))
    print(k, pts[:12])
