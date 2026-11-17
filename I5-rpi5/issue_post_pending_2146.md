Progress (rpi5, 21:46, newest commit f079d57; rpi5 stalled under swap from ~19:07 to 21:44 and my jobs lost that time).

- **Finished, all windings 0 with the planted zero returned (+2 for a symmetric box, +1 for an upper box):** strip Re s ∈ [0.03, 0.1], |Im s| ≤ 2.5 (l = 2, 3); Re s ∈ [1e-4, 0.1], |Im s| ≤ 0.23 (l = 2, 3); Re s ∈ [−1e-3, 1e-4], Im s ∈ [0.01, 0.23] (l = 2, 3); Re s ∈ [0.1, 2], Im s ∈ [2.5, 6] (l = 2).
- **Running:** the Mini BS strip control (two jobs, one at the doubled outer radius). **Queued:** the same Im s ∈ [2.5, 6] box for l = 3, the real-γ refinement (l = 2, 3), the threshold boxes at two outer radii. ETA about 8 h if rpi5 does not stall again. 2 processes, ~130 MB, 3.2 GB available.

**Mini BS strip control, and why its expectation changed.** All four boxes span Re s ∈ [−2e-4, 0.1] on the Mini BS I star (l = 2, `control_winding2.py --strip`).

| box | Im s | expected before the run | expected now | counted |
|---|---|---|---|---|
| fundamental only | [0.09, 0.125] | 1 | 1 | +1.0000 |
| three zeros | [0.09, 0.14] | 1 | 3 | +3.0000 |
| above the QNM | [0.1225, 0.14] | 0 | 2 | pending |
| between QNM and next zero | [0.1225, 0.1285] | not in the first control | 0 | pending |

Before the run I expected one zero in [0.09, 0.14] and none in [0.1225, 0.14], because the published QNM (σ = 0.1195 − 5e-5 i) was the only mode I knew there, and the original control box around it held only it. The first strip run returned +3 and, after the step-rule fix, +3 and +2, so I did not trust either number until the zeros were located. `polish_zero.py --mini` runs a complex secant on the same `PolarProblem.D` from guesses at Im s = 0.1195, 0.126, 0.131, 0.136, 0.139, at rtol 1e-8 and 1e-10. It converges (|D| ≤ 1.4e-15) to s = −5.35350e-5 + 0.11951908 i (the published mode: control passes, spread of Re s over rtol 2e-15), −2.62464e-5 + 0.131605 i, −1.35809e-5 + 0.137308 i and −7.7455e-6 + 0.140372 i. Three lie inside [0.09, 0.14] and two inside [0.1225, 0.14], which is what the windings returned. The raw log is `polish_mini.log` in I5-rpi5.

What this does and does not check. The fundamental-only box and the published value are independent of the later zeros. The agreement of the box counts with the polished zeros compares two uses of the same D, so it tests the counter, not D. I changed the expectation after seeing the counts, and the control is rerun with the new expectation in all four boxes. The zeros fall toward the threshold Im s = 1 − ω = 0.1469 with |Re s| shrinking (5.4e-5, 2.6e-5, 1.4e-5, 7.7e-6), which I read as a Coulomb-tail series of the M > 0 star, but I have not tested that.
