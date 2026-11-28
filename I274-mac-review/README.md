# I274-mac-review: the coordinator's review of #274 (the polar winding boxes recounted with the crate)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/274. Under review: branch
`wip/i274-crate-recount` at 6f91397, raw `I274-mac` at 0d49255d.

## ind274.py: the crate's |D| against the stored scipy caches, point by point

Written by the coordinator; imports nothing from the repository. For each of the 35 record files `I274-mac/jsonl_rec/*.jsonl`
(the crate's evaluations, f64) it finds, among the winding2 caches of `I126-rpi5/cache` and `I117-rpi5/cache` with the same
l, the one holding all its points, by its own search. It then compares |D| of the crate (`d_f64`) with |D| of the cache at
every point. The phase strip is a pure phase, so the modulus needs none of the counter's or the driver's code.

Shared with the runner's code: the crate's output files and the stored caches. Not shared: the box-to-cache mapping, the
point matching, the comparison.

Criteria, written before the first run:
- K1: each of the 35 files has all its points in exactly one cache of its l (matched to 1e-12 in s), and no point is outside it.
- K2: | |D_crate| / |D_cache| − 1 | ≤ 1e-6 at every point of every box (the caches were made at rtol 1e-8; #188 measured
  6e-10 at l = 2).

Mutations: `scale` (crate modulus × (1 + 1e-5): K2), `extra` (a point at s + 1e-3 added to each file: K1).
