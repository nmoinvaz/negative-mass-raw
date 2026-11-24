| mutation, run | rc | wall | must fail (README) | failed | state; verdict | failed although predicted not to | other failed (not predicted either way) |
|---|---|---|---|---|---|---|---|
| `potential` run1 | 1 | 2:18.76 | G0, G2, G3, G4, G5, G6 | G0, G2, G3, G4, G6, G5 | complete; fired | - | - |
| `printedW` run1 | 1 | 2:11.14 | W1, G1, G2, G3, G4, G5 | W1, G1, G2, G3, G4, G6, G5 | complete; fired | - | G6 |
| `matrix` run1 | 1 | 2:17.08 | P-B, G1, G0 | P-B, G1, G0, G7, D1 | complete; fired | - | G7, D1 |
| `planted` run1 | 1 | 2:13.20 | P-A, P-B | P-A, P-B | complete; fired | - | - |
| `xmap` run1 | 1 | 6:04.44 | P-A, G1, G2, G3, G4, G5 | P-A, G1, G2, G3, G4, G6 | crashed; SILENT on G5 | - | G6 |
| `xmap` run2 | 1 | 8:21.47 | P-A, G1, G2, G3, G4, G5 | P-A, G1, G2, G3, G4, G6, G5, G7, D1 | complete; fired | - | G6, G7, D1 |
| `units` run1 | 1 | 2:17.26 | U1 | U1 | complete; fired | - | - |
| `tfactor` run1 | 1 | 2:17.27 | U2, G3, G4, G5, G6 | U2, G3, G4, G6, G5 | complete; fired | - | - |
| `count` run1 | 1 | 4:19.08 | G7 | G7 | complete; fired | - | - |
| `domain` run1 | 1 | 0:41.88 | D1, G0, G1 | P-A, P-B, G1, G0, G2 | crashed; SILENT on D1 | - | P-A, P-B, G2 |
| `domain` run2 | 1 | 0:53.09 | D1, G0, G1 | P-A, P-B, G1, G0, G2, G5, G7, D1 | complete; fired | - | P-A, P-B, G2, G5, G7 |
| `deltaphi` run1 | 1 | 2:09.69 | L1, G2 | L1, G2, D1 | complete; fired | - | D1 |
| `cpath` run1 | 143 | ? | P-C, G2 | - | stopped by me (hung); SILENT on P-C, G2 | - | - |
| `cpath` run2 | 143 | ? | P-C, G2 | P-C | stopped by me (hung); SILENT on G2 | - | - |
| `cpath` run3 | 1 | 1:42.46 | P-C, G2 | P-C, G2 | complete; fired | - | - |
| `background` run1 | 1 | 2:15.83 | S1 | S1 | complete; fired | - | - |
