(Relayed by the coordinator from negative-mass-dh610-i246; the runner could not post: gh on dh610 has an invalid token after the reboot.)

**Criteria declared** (raw `I246-dh610` README at 726241f9, code `settled_mass_d56.py` at 0c52443, before any run of record).
- Cases: D = 5, 6; families S and G at #40's three h (G at D = 6, h = 0.00125 has no #40 job: bisected here with `threshold.bisect`, p*ₕ = 0.01069693394962485, hi − lo 5.7e-15, 44 runs, 2569 s, per the ruling); δ = 1e-6, 1e-8.
- Chain: #41's, with K = 28 (e^{−f} = 4.0e8, dxp = 14) per the ruling. #41's 1.57e6 is read from the same series (a bit-identical prefix, check PFX) and RC5, RC6, RC8 are made at both limits. The x⁺ span after formation shrinks with D (9.4, 6.1, 4.6), so the last window at 1.57e6 still holds the decay tail. RC8a (the settled test at 1.57e6) is expected to fail in every case (development: flux 1.2e-5 to 7e-5 against the bar 1e-5) and is reported as such.
- RC7 (settled value independent of δ) at the finest h, with the three values and orders printed.
- Planted exact Tangherlini D = 5, 6 (S-like and G-like horizon radius and stretching), four h each: second order in development (orders 1.9 to 2.14), bar 3e-4 of M.
- 72 checks, 26 mutations whose targets were computed in development runs. Runs of record next: 24 main runs, 8 prefix runs (K = 20, 24), 48 ulp-noise runs, four lanes at nice 10. The roundoff-floor question (#226) is answered by the noise runs at the two finest h per D.
