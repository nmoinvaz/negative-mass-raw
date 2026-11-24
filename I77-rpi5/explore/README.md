# explore/: scratch scripts of the arbitrary-profile ideal step (C5, not decided)

Scripts only, written while building three_scalars.py. None is a claim. Findings, all unverified by the final script:

- Orbit-space metric h = R_ab theta^a theta^b on (t, r, theta); at a fixed theta_0 the numerators of det(h)^2 Ric(h) are
  polynomials in (r, W0..W4), linear in W4 (e7.py, e8.py, e16.py). At theta_0 = pi/2 they have 78, 66, 87 and 42 terms.
- W4-free combinations E1, E2, E3 at the equator (e11.py); resultants in W3 are polynomials in (W0, W1, W2) of degree
  (12, 18, 7) and (14, 24, 10) (e12.py).
- A Groebner basis of the equator numerators (e9.py, over Q) and of the equator system with its flow derivatives
  (e13.py, modulo a prime) did not finish in 20 min and was killed. A numerical search (e14.py, e14b.py, e15.py) found
  solutions only at b -> 0 or on Phi = 0 (the equator rank-2 locus); this is not a proof.
- A frame-based FracField computation of Ric(h) (e2-style, not kept) did not finish in 10 min.
