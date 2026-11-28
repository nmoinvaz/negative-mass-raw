# I246-mac-review: the coordinator's review of #246 (the settled threshold mass at D = 5 and 6)

Coordinator's Mac, nice 10. Issue: https://github.com/nmoinvaz/negative-mass/issues/246. Under review: branch
`wip/i246-settled-mass-d56` at 5b3517b (driver 0c52443), raw `I246-dh610` at 085c3667 (declaration 726241f9).

## ind246.py: the settled values from the raw series

Written by the coordinator; imports nothing from the repository. From `I246-dh610/runs/D{5,6}_{S,G}_k{0,1,2}_d1e-{8,6}/series.npz`
(k = 0, 1, 2 the three h, coarse to fine; the series end at e^{−f} = 4.0e8) it computes with its own code:
- the plateau: mean of M over the cells with x⁺ ≥ max x⁺ − 1;
- Richardson (4 M₂ − M₁)/3 and the observed order log₂((M₀ − M₁)/(M₁ − M₂)) (h ratio 2);
- E/E_throat = M/(½ a^{n−1}) with a = 1, from E = (D − 2) V_{D−2} M and V_k = π^{k/2}/Γ(k/2 + 1) for both;
- the prefix property: the K = 20 and K = 24 series against the first cells of K = 28's.

Shared with the runner's code: the series. Not shared: everything above.

Criteria, written before the first run:
- K1: the finest-h plateaus within 2e-6 of the note's: D5 S 0.145859, D5 G 0.263924, D6 S 0.107793, D6 G 0.862180
  (δ = 1e-8); D5 G 0.234978, D6 G 0.567448 (δ = 1e-6).
- K2: the Richardson values within 5e-6 of the note's 0.145866, 0.263951, 0.107920, 0.862862 (δ = 1e-8), and the observed
  order in [1.5, 2.5] for both S cases.
- K3: E/E_throat from the Richardson values equals 0.2917 (D = 5) and 0.2158 (D = 6) to the four printed digits.
- K4: the K = 20 and K = 24 series of D5 S and D5 G are bit-identical prefixes of the K = 28 series.

Mutations: `last-half` (plateau over the last 0.5: K1 if it moves the value by 2e-6, reported either way), `order1`
(Richardson as 2 M₂ − M₁: K2), `ball` (V_k with π^{k/2}/Γ(k/2): K3).
