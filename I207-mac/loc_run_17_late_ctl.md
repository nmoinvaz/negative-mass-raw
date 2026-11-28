records with a `loc` key: 615

1. totals (records; records with calls of locate; with an Unresolved step; with a pair step; with no result at a step; SINGULAR records whose stop step differs from the old rule's; SINGULAR records the old rule would not have stopped by then)

| file kind | class | records | with calls | Unresolved | pair | nothing | stop step differs | old rule no stop |
|---|---|---|---|---|---|---|---|---|
| conical | FLOOR | 15 | 15 | 0 | 0 | 0 | 0 | 0 |
| conical | SINGULAR | 172 | 172 | 17 | 0 | 0 | 0 | 0 |
| offgrid | FLOOR | 76 | 22 | 0 | 0 | 0 | 0 | 0 |
| offgrid | SINGULAR | 352 | 352 | 36 | 0 | 0 | 4 | 1 |

2. records where locate said Unresolved or gave nothing at a gated step: 53 records

| file command (start) | F_inf | C | class | kind | base class:kind | steps | calls | real | Unresolved | nothing | pair | old real | locate not real while old real | stop step | old stop step | eta* | old eta* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 0.25 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 599 | 213 | 171 | 42 | 0 | 0 | 171 | 0 | 462 | 462 | 0.0007153455038 | 0.0007153455038 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 0.5 | 30 | SINGULAR | F->0 | SINGULAR:F->0 | 599 | 194 | 176 | 18 | 0 | 0 | 176 | 0 | 462 | 462 | 0.001124585934 | 0.001124585934 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 0.75 | 100 | SINGULAR | F->0 | SINGULAR:F->0 | 704 | 268 | 185 | 83 | 0 | 0 | 189 | 4 | 508 | 508 | 0.0004081235124 | 0.0004081235124 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 0.75 | 300 | SINGULAR | other | SINGULAR:other | 452 | 83 | 63 | 20 | 0 | 0 | 70 | 7 | 166 | 166 | 1.157378097e-06 | 1.157378097e-06 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 1 | 300 | SINGULAR | F->0 | SINGULAR:F->0 | 692 | 236 | 187 | 49 | 0 | 0 | 187 | 0 | 495 | 495 | 0.0009548066174 | 0.0009548066175 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 1 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 796 | 422 | 255 | 107 | 0 | 0 | 266 | 11 | 499 | 499 | 4.578491649e-05 | 4.578491656e-05 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 1 | 3000 | SINGULAR | other | SINGULAR:other | 675 | 67 | 47 | 20 | 0 | 0 | 54 | 7 | 152 | 152 | 3.649447461e-06 | 3.649447461e-06 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 1.5 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 991 | 353 | 209 | 139 | 0 | 0 | 218 | 9 | 930 | 930 | 0.5442949715 | 0.5442949715 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 2 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 953 | 315 | 209 | 106 | 0 | 0 | 217 | 8 | 892 | 892 | 1.162043429 | 1.162043429 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 3 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 894 | 257 | 216 | 41 | 0 | 0 | 216 | 0 | 833 | 833 | 2.321748788 | 2.321748788 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 3 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 1172 | 524 | 270 | 175 | 0 | 0 | 279 | 9 | 1111 | 1111 | 2.381267496 | 2.381267496 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 4 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 1020 | 373 | 252 | 121 | 0 | 0 | 261 | 9 | 959 | 959 | 3.490621782 | 3.490621782 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | -0.5 | -30 | SINGULAR | F->0 | SINGULAR:F->0 | 599 | 194 | 176 | 18 | 0 | 0 | 176 | 0 | 462 | 462 | 0.001124585934 | 0.001124585934 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | -1 | -3000 | SINGULAR | other | SINGULAR:other | 675 | 67 | 47 | 20 | 0 | 0 | 54 | 7 | 152 | 152 | 3.649447461e-06 | 3.649447461e-06 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | -1 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 796 | 422 | 255 | 107 | 0 | 0 | 266 | 11 | 499 | 499 | 4.578491649e-05 | 4.578491656e-05 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | -1 | -300 | SINGULAR | F->0 | SINGULAR:F->0 | 692 | 236 | 187 | 49 | 0 | 0 | 187 | 0 | 495 | 495 | 0.0009548066174 | 0.0009548066175 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | -2 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 953 | 315 | 209 | 106 | 0 | 0 | 217 | 8 | 892 | 892 | 1.162043429 | 1.162043429 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 699 | 166 | 82 | 84 | 0 | 0 | 89 | 7 | 699 | 699 | 1.162043429 | 1.162043429 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 0 | SINGULAR | F->0 | SINGULAR:F->0 | 486 | 91 | 75 | 16 | 0 | 0 | 75 | 0 | 486 | 486 | 15.78191794 | 15.78191794 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 595 | 173 | 86 | 77 | 0 | 0 | 93 | 7 | 595 | 595 | 15.81421368 | 15.81421368 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 288 | 42 | 31 | 11 | 0 | 0 | 35 | 4 | 288 | 288 | 15.9477322 | 15.9477322 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 1000000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 417 | 27 | 26 | 1 | 0 | 0 | 27 | 1 | 417 | 417 | 1.73192683 | 1.73192683 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1259 | 409 | 94 | 57 | 0 | 0 | 100 | 6 | 1259 | 1259 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 501 | 77 | 67 | 10 | 0 | 0 | 71 | 4 | 501 | 499 | 15.96866047 | 15.96866047 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1236 | 410 | 94 | 57 | 0 | 0 | 100 | 6 | 1236 | 1236 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 479 | 77 | 67 | 10 | 0 | 0 | 71 | 4 | 479 | 477 | 15.96866047 | 15.96866047 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 1000000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 435 | 25 | 21 | 4 | 0 | 0 | 23 | 2 | 435 | 435 | 1.73192683 | 1.73192683 |
| scan --prec dd --mode conserve --fi 1.5  | 1.5 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 747 | 207 | 92 | 111 | 0 | 0 | 99 | 7 | 747 | 747 | 0.5442949715 | 0.5442949715 |
| scan --prec qd --mode conserve --fi 4.0  | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1115 | 203 | 74 | 76 | 0 | 0 | 77 | 3 | 1115 | 1115 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode conserve --fi -16. | -16 | -100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1236 | 410 | 94 | 57 | 0 | 0 | 100 | 6 | 1236 | 1236 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi -16. | -16 | -100000000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 479 | 77 | 67 | 10 | 0 | 0 | 71 | 4 | 479 | 477 | 15.96866047 | 15.96866047 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1563 | 458 | 84 | 56 | 0 | 0 | 90 | 6 | 1563 | 1563 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode conserve --fi 0.75 | 0.75 | 100 | SINGULAR | F->0 | SINGULAR:F->0 | 453 | 114 | 71 | 43 | 0 | 0 | 71 | 0 | 453 | 453 | 0.0004081235124 | 0.0004081235124 |
| scan --prec dd --mode conserve --fi 0.75 | 0.75 | 300 | SINGULAR | other | SINGULAR:other | 313 | 23 | 15 | 8 | 0 | 0 | 18 | 3 | 313 | 313 | 1.157378098e-06 | 1.157378098e-06 |
| scan --prec dd --mode conserve --fi -1.0 | -1 | -3000 | SINGULAR | other | SINGULAR:other | 330 | 23 | 20 | 3 | 0 | 0 | 22 | 2 | 330 | 330 | 3.649447456e-06 | 3.649447456e-06 |
| scan --prec dd --mode conserve --fi -1.0 | -1 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 474 | 179 | 95 | 56 | 0 | 0 | 101 | 6 | 474 | 474 | 4.578491649e-05 | 4.578491656e-05 |
| scan --prec dd --mode conserve --fi -1.0 | -1 | -300 | SINGULAR | F->0 | SINGULAR:F->0 | 444 | 94 | 71 | 23 | 0 | 0 | 71 | 0 | 444 | 444 | 0.0009548066174 | 0.0009548066175 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 710 | 184 | 90 | 94 | 0 | 0 | 97 | 7 | 710 | 710 | 3.490621782 | 3.490621782 |
| scan --prec dd --mode conserve --fi 1.0  | 1 | 300 | SINGULAR | F->0 | SINGULAR:F->0 | 444 | 94 | 71 | 23 | 0 | 0 | 71 | 0 | 444 | 444 | 0.0009548066174 | 0.0009548066175 |
| scan --prec dd --mode conserve --fi 1.0  | 1 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 474 | 179 | 95 | 56 | 0 | 0 | 101 | 6 | 474 | 474 | 4.578491649e-05 | 4.578491656e-05 |
| scan --prec dd --mode conserve --fi 1.0  | 1 | 3000 | SINGULAR | other | SINGULAR:other | 330 | 23 | 20 | 3 | 0 | 0 | 22 | 2 | 330 | 330 | 3.649447456e-06 | 3.649447456e-06 |
| scan --prec dd --mode conserve --fi 3.0  | 3 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 626 | 105 | 74 | 31 | 0 | 0 | 74 | 0 | 626 | 626 | 2.321748788 | 2.321748788 |
| scan --prec dd --mode conserve --fi 3.0  | 3 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 840 | 309 | 112 | 133 | 0 | 0 | 119 | 7 | 840 | 840 | 2.381267496 | 2.381267496 |
| scan --prec dd --mode conserve --fi -2.0 | -2 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 699 | 166 | 82 | 84 | 0 | 0 | 89 | 7 | 699 | 699 | 1.162043429 | 1.162043429 |
| scan --prec dd --mode project --fi 16.0  | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1327 | 485 | 94 | 57 | 0 | 0 | 100 | 6 | 1327 | 1327 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode project --fi 16.0  | 16 | 100000000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 479 | 77 | 67 | 10 | 0 | 0 | 71 | 4 | 479 | 477 | 15.96866047 | 15.96866047 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 100000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 314 | 51 | 36 | 15 | 0 | 0 | 42 | 6 | 314 | 314 | 3.870076593 | 3.870076593 |
| scan --prec dd --mode project --fi 4.0 - | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1738 | 582 | 84 | 56 | 0 | 0 | 90 | 6 | 1738 | 1738 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode conserve --fi 0.25 | 0.25 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 433 | 95 | 71 | 24 | 0 | 0 | 71 | 0 | 433 | 433 | 0.0007153455038 | 0.0007153455038 |
| scan --prec qd --mode conserve --fi 16.0 | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 966 | 230 | 85 | 77 | 0 | 0 | 88 | 3 | 966 | 966 | 15.86125434 | 15.86125434 |
| scan --prec qd --mode conserve --fi 16.0 | 16 | 100000000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 437 | 65 | 56 | 9 | 0 | 0 | 52 | 1 | 437 | - | 15.96866047 | - |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1588 | 457 | 84 | 56 | 0 | 0 | 90 | 6 | 1588 | 1588 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode conserve --fi -4.0 | -4 | -10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1563 | 458 | 84 | 56 | 0 | 0 | 90 | 6 | 1563 | 1563 | 3.527557745 | 3.527557745 |

3. records where locate read a pair at a gated step: 0 records


4. records whose stop is not the old rule's: 4 records

| file command (start) | F_inf | C | class | kind | base class:kind | steps | calls | real | Unresolved | nothing | pair | old real | locate not real while old real | stop step | old stop step | eta* | old eta* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 501 | 77 | 67 | 10 | 0 | 0 | 71 | 4 | 501 | 499 | 15.96866047 | 15.96866047 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 479 | 77 | 67 | 10 | 0 | 0 | 71 | 4 | 479 | 477 | 15.96866047 | 15.96866047 |
| scan --prec dd --mode conserve --fi -16. | -16 | -100000000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 479 | 77 | 67 | 10 | 0 | 0 | 71 | 4 | 479 | 477 | 15.96866047 | 15.96866047 |
| scan --prec dd --mode project --fi 16.0  | 16 | 100000000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 479 | 77 | 67 | 10 | 0 | 0 | 71 | 4 | 479 | 477 | 15.96866047 | 15.96866047 |

5. eta* against the old rule's eta* on the same steps: 523 SINGULAR records with both; largest |difference| / max(1, eta*) 1.803e-12; above 1e-12: 1; above 1e-10: 0

  1.803e-12  F_inf 4.0 C [100000.0, 0.0]  eta* 3.8700765928240757  old 3.870076592817097  [scan --prec dd --mode conserve --fi 4.0 --c -100000000.0,-10]
  7.325e-13  F_inf 16.0 C [100000.0, 0.0]  eta* 15.947732200251725  old 15.947732200240043  [scan --prec dd --mode conserve --fi 16.0 --c -100000000.0,-1]
  7.144e-13  F_inf 4.0 C [10000.0, 0.0]  eta* 3.851819411195818  old 3.8518194111930666  [scan --prec dd --mode conserve --fi 4.0 --c -100000000.0,-10]
  6.758e-13  F_inf 1.5 C [3000.0, 0.0]  eta* 1.1000625308574679  old 1.1000625308567245  [scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,-2 -3000,-1000,-300,-]
  6.645e-13  F_inf 1.5 C [3000.0, 0.0]  eta* 1.1000625308574454  old 1.1000625308567145  [scan --prec dd --mode conserve --fi 1.5 --c -3000.0,-1000.0,]
  5.236e-13  F_inf 2.0 C [3000.0, 0.0]  eta* 1.7085396460362756  old 1.708539646035381  [scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,-2 -3000,-1000,-300,-]
  5.236e-13  F_inf -2.0 C [-3000.0, 0.0]  eta* 1.7085396460362756  old 1.708539646035381  [scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,-2 -3000,-1000,-300,-]
  5.111e-13  F_inf 2.0 C [3000.0, 0.0]  eta* 1.7085396460360789  old 1.7085396460352056  [scan --prec dd --mode conserve --fi 2.0 --c -3000.0,-1000.0,]
