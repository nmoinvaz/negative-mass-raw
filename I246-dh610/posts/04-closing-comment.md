**Result.** Family S settles at M_AH = 0.14587 a² (r_AH = 0.5401 a) at D = 5 and 0.10792 a³ (r_AH = 0.5996 a) at D = 6, E/E_throat = 0.292 and 0.216 (D = 4: 0.446); [ST17]'s E_f is the static throat's own energy, which the horizon's mass at its first trapped cell matches to 2 % (0.984, 0.980) and the settled mass does not. Family G settles higher (0.2640 a², 0.8629 a³ at δ = 1e-8: +0.118 and +0.754 over S, against +0.0125 at D = 4) and depends strongly on δ (0.2350 and 0.5679 at δ = 1e-6, the same at all three h). M_AH converges at second order at three h and is not at #226's roundoff floor (noise scatter / h difference 0.003 to 0.12); the settled test fails at #41's limit e^{−f} = 1.57e6, as declared, and passes at 4.0e8. All numbers are *numerical evidence*; the one conjecture (G follows its stall member) is untested.

| acceptance | verdict | numbers |
|---|---|---|
| planted Tangherlini recovered at second order | **met** | max \|M − M_exact\| at the finest h 3.2e-6, 3.3e-6 (D = 5, S-like, G-like), 3.3e-6, 5.8e-6 (D = 6); orders 1.88 to 2.08 over four h; bar 3e-4 M_exact |
| M_AH(x⁺) second order at three h up to a declared limit | **met** | orders 1.92 to 2.13, three windows, both δ, four cases, at e^{−f} = 4.0e8 (RC6) and at #41's 1.57e6 (RC6a) |
| settled at the limit (RC8, #41's bars) | met at 4.0e8; **not met at 1.57e6** (RC8a, all four) | flux 5e-7 to 1.1e-6 at 4.0e8; 1.2e-5 to 7.2e-5 at 1.57e6 (bar 1e-5), plateau change up to 3.9e-4 (bar 1e-4); the end values differ by ≤ 4e-6 between the limits |
| settled values against [ST17]'s rows in one unit | **done** | E = (D − 2)V_{D−2} M, V = unit-ball volumes: static throat π, 2π, π² = 3.14, 6.28, 9.87; settled E = 1.83, 3.32 (D = 5 S, G), 2.13, 17.0 (D = 6); their printed A₄ is twice V₄ |
| G against S per D, with the δ dependence | **done**, G differs | \|G − S\| 0.118 > bar 0.029 (D = 5), 0.754 > 0.297 (D = 6); δ = 1e-8 against 1e-6: +2.89e-2 (12 %), +2.95e-1 (52 %) |

**What ran** (code `settled_mass_d56.py` at 0c52443, #41's chain unchanged except K = 28, dxp = 14 by the coordinator's ruling): 80 runs of record, all exit 0 (24 main, 8 prefix runs showing the K = 20, 24 series are bit-identical prefixes, 48 ulp-noise runs); p*ₕ of G at D = 6, h = 0.00125 bisected here (0.01069693394962485, 44 runs, 2569 s; #228 can reuse it); analysis of record exit 1 with 69 counted checks and 4 failed (RC8a ×4, declared); 26 of 26 mutated analyses exit 0 (the failed set equals the declared one). Interruptions (reboot, suspend) were rerun from the same queue and code; every partial log is kept.
- Raw: negative-mass-raw `I246-dh610` at 085c3667 (README = declaration at 726241f9 + results; `runs/`, `mut/`, `posts/`, `figures/settled_mass_d56.svg`).
- Branch `wip/i246-settled-mass-d56` at 5b3517b: `settled_mass_d56.py`, `settled_mass_d56_output.txt`, `settled_mass_d56.md` (tables M_AH(t) per D and family, the [ST17] comparison, proposed text for `settled_mass.md`, `critical_ghost.md` §1.3 and Paper V's placeholder).

**Failed or disagrees.** (1) RC8a, four cases (above). (2) The declaration counted 72 checks and the analysis counts 69: PL1 to PL3 pass but are printed by #253's helper outside the count. (3) [ST17]'s printed A₄ = π² gives E_throat = 19.7 at n = 6 against their 9.87; the table needs π²/2 (unchanged from #41). (4) p*ₕ of #40's G at D = 5, h = 0.00707 has hi − lo = 2.9e-12 (RC1's bar 1e-11, declared). (5) The G-against-S bar includes G's physical δ dependence, as #253; the verdict holds by 4 and 2.5 against it and by 1500 and 370 against the h terms alone.

**Recommended tasks.**
1. G's settled mass against δ (1e-12 to 1e-4) and the stall member's size at departure at D = 5, 6 (#255, #267): the δ dependence is 50 (D = 5) and 500 (D = 6) times D = 4's; acceptance: M_settled one function of the member's radius at departure for six δ.
2. [ST17]'s own pulse (c₁ = 0.25, 0.5; c₂ = 16, c₃ = 0.7) through the chain at n = 5, 6: their x_H⁻ within 5 %, E at x⁺ = 5 against formation.
3. The roundoff floor at h/2 and h/4 (own p*ₕ): the ratio rises 4 to 6 per halving and is 0.05 to 0.12 at the finest h; acceptance: ratio ≥ 1 measured and the order reported there.
4. Count PL1 to PL3 in the driver's exit code (72 against 69) and rerun the analysis.
5. The settled mass beyond K = 28 and the event horizon at D = 5, 6 (#247).

Left open for review; `running` removed.
