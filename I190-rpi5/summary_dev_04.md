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

worst gated values:
- f64: closed_form err 3.50e-14; crossings position error 7.84e-14; step_sum ratio 2.93e+04
- dd: closed_form err 4.06e-30; crossings position error 1.00e-29; step_sum ratio 2.22e+04
- qd: closed_form err 4.04e-62; crossings position error 2.50e-62; step_sum ratio 1.51e+04
digest dd a8977a5c50933054
digest f64 b124d44e9758f1a1
digest qd a97a140ad786c8d8
