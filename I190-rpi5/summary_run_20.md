| lane | check | met (gated) | not met (gated) | met (recorded) | NOT MET (recorded) |
|---|---|---|---|---|---|
| f64 | closed_form | 15 | 0 | 0 | 3 |
| f64 | coeffs | 0 | 0 | 0 | 2 |
| f64 | crossings | 12 | 0 | 0 | 2 |
| f64 | fold | 3 | 0 | 0 | 1 |
| f64 | planner | 1 | 0 | 0 | 0 |
| f64 | step_sum | 11 | 0 | 0 | 0 |
| f64 | zero_pivot | 1 | 0 | 0 | 0 |
| dd | closed_form | 15 | 0 | 0 | 3 |
| dd | coeffs | 0 | 0 | 0 | 2 |
| dd | crossings | 12 | 0 | 0 | 2 |
| dd | fold | 4 | 0 | 0 | 0 |
| dd | planner | 1 | 0 | 0 | 0 |
| dd | step_sum | 11 | 0 | 0 | 0 |
| dd | zero_pivot | 1 | 0 | 0 | 0 |
| qd | closed_form | 15 | 0 | 0 | 3 |
| qd | coeffs | 0 | 0 | 0 | 2 |
| qd | crossings | 12 | 0 | 0 | 2 |
| qd | fold | 4 | 0 | 0 | 0 |
| qd | planner | 1 | 0 | 0 | 0 |
| qd | step_sum | 11 | 0 | 0 | 0 |
| qd | zero_pivot | 1 | 0 | 0 | 0 |
| od | closed_form | 3 | 0 | 0 | 0 |
| od | crossings | 1 | 0 | 0 | 0 |
| od | fold | 1 | 0 | 0 | 0 |
| od | step_sum | 1 | 0 | 0 | 0 |

worst gated values:
- f64: closed_form err 3.50e-14; crossings position error 7.84e-14; step_sum ratio 2.93e+04
- dd: closed_form err 4.13e-30; crossings position error 4.45e-30; step_sum ratio 7.10e+03
- qd: closed_form err 3.41e-62; crossings position error 2.82e-62; step_sum ratio 1.81e+04
- od: closed_form err 6.42e-127; crossings position error 1.87e-129; step_sum ratio 1.54e+03
digest dd 92ec461781147d77
digest f64 b124d44e9758f1a1
digest qd 75902b0bf76ced2a
