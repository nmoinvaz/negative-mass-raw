# I114-mac: coordinator's timing pilot for #114's two rtol 1e-12 evaluations

Machine: the coordinator's Mac (Apple M5, macOS, Python 3.14.7, the repo's venv), one thread, nice 10.
Issue: https://github.com/nmoinvaz/negative-mass/issues/114

`pilot_rate.py` (run from phase2/nonradial at main 51ced6d) carries the true regular plane from r0 at rtol 1e-8 to 12
positions spread over [r0, r_m], then times 8 chunks of PolarProblem._integrate_plane's loop body at the target rtol
from each, and prints n chunks times the mean time per chunk (the interior integration, almost all of an evaluation).

| case | rtol | n chunks | mean per chunk (Mac) | estimate (Mac) | #4's laptop time |
|---|---|---|---|---|---|
| l = 4, gamma = 3000 | 1e-10 | 36163 | 14.1 ms | 508 s | 2288 s |
| l = 4, gamma = 3000 | 1e-12 | 36163 | 109 ms | 3957 s | 17168 s |
| l = 5, gamma = 6000 | 1e-12 | 72326 | 291 ms | 21049 s | stopped at 18129 s |
| l = 6, gamma = 12000 | 1e-12 | 144652 | 509 ms | 73616 s | stopped at 22599 s |

Calibration at l = 4: the pilot's rtol 1e-12 / 1e-10 ratio is 7.8 against #4's 7.5, and the laptop is 4.5 times slower
than the Mac at rtol 1e-10 (4.34 at rtol 1e-12). Laptop estimates: about 25 h at l = 5 and 89 h at l = 6. The cost per
chunk at rtol 1e-12 rises from about 15 ms near r0 to 0.9 s (l = 5) and 1.2 s (l = 6) near r_m.
