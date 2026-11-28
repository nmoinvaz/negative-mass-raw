records with a `loc` key: 615

1. totals (records; records with calls of locate; with an Unresolved step; with a pair step; with no result at a step; SINGULAR records whose stop step differs from the old rule's; SINGULAR records the old rule would not have stopped by then)

| file kind | class | records | with calls | Unresolved | pair | nothing | stop step differs | old rule no stop |
|---|---|---|---|---|---|---|---|---|
| conical | FLOOR | 15 | 15 | 0 | 0 | 0 | 0 | 0 |
| conical | NONFINITE | 2 | 2 | 0 | 2 | 0 | 0 | 0 |
| conical | SINGULAR | 170 | 170 | 9 | 14 | 0 | 0 | 0 |
| offgrid | FLOOR | 76 | 22 | 0 | 0 | 0 | 0 | 0 |
| offgrid | SINGULAR | 352 | 352 | 20 | 26 | 0 | 2 | 5 |

2. records where locate said Unresolved or gave nothing at a gated step: 29 records

| file command (start) | F_inf | C | class | kind | base class:kind | steps | calls | real | Unresolved | nothing | pair | old real | locate not real while old real | stop step | old stop step | eta* | old eta* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 0.75 | 300 | SINGULAR | other | SINGULAR:other | 452 | 83 | 79 | 4 | 0 | 0 | 70 | 0 | 166 | 166 | 1.157378105e-06 | 1.157378097e-06 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 1 | 3000 | SINGULAR | other | SINGULAR:other | 675 | 67 | 64 | 3 | 0 | 0 | 54 | 0 | 152 | 152 | 3.649447454e-06 | 3.649447461e-06 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 1.5 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 991 | 353 | 182 | 18 | 0 | 88 | 218 | 36 | 930 | 930 | 0.5442949715 | 0.5442949715 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 2 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 953 | 315 | 194 | 18 | 0 | 76 | 217 | 23 | 892 | 892 | 1.162043429 | 1.162043429 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 3 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 894 | 257 | 216 | 4 | 0 | 37 | 216 | 0 | 833 | 833 | 2.321748788 | 2.321748788 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 3 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 1172 | 524 | 245 | 19 | 0 | 86 | 279 | 34 | 1111 | 1111 | 2.381267496 | 2.381267496 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 4 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 1020 | 373 | 229 | 20 | 0 | 84 | 261 | 32 | 959 | 959 | 3.490621782 | 3.490621782 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | -1 | -3000 | SINGULAR | other | SINGULAR:other | 675 | 67 | 64 | 3 | 0 | 0 | 54 | 0 | 152 | 152 | 3.649447454e-06 | 3.649447461e-06 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | -2 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 953 | 315 | 194 | 18 | 0 | 76 | 217 | 23 | 892 | 892 | 1.162043429 | 1.162043429 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 699 | 166 | 72 | 14 | 0 | 59 | 89 | 17 | 699 | 699 | 1.162043429 | 1.162043429 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 3000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1275 | 737 | 109 | 14 | 0 | 71 | 142 | 33 | 1275 | 285 | 1.201426408 | 1.708539646 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 595 | 173 | 80 | 15 | 0 | 61 | 93 | 13 | 595 | 595 | 15.81421368 | 15.81421368 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1259 | 409 | 76 | 11 | 0 | 61 | 100 | 24 | 1259 | 1259 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1236 | 410 | 76 | 11 | 0 | 61 | 100 | 24 | 1236 | 1236 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi 1.5  | 1.5 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 747 | 207 | 72 | 14 | 0 | 68 | 99 | 27 | 747 | 747 | 0.5442949715 | 0.5442949715 |
| scan --prec qd --mode conserve --fi 4.0  | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1115 | 203 | 67 | 11 | 0 | 68 | 77 | 10 | 1115 | 1115 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode conserve --fi -16. | -16 | -100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1236 | 410 | 76 | 11 | 0 | 61 | 100 | 24 | 1236 | 1236 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1563 | 458 | 75 | 10 | 0 | 52 | 90 | 15 | 1563 | 1563 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode conserve --fi 0.75 | 0.75 | 300 | SINGULAR | other | SINGULAR:other | 313 | 23 | 22 | 1 | 0 | 0 | 18 | 0 | 313 | 313 | 1.157378105e-06 | 1.157378098e-06 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 710 | 184 | 74 | 15 | 0 | 65 | 97 | 23 | 710 | 710 | 3.490621782 | 3.490621782 |
| scan --prec dd --mode conserve --fi 3.0  | 3 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 626 | 105 | 74 | 3 | 0 | 28 | 74 | 0 | 626 | 626 | 2.321748788 | 2.321748788 |
| scan --prec dd --mode conserve --fi 3.0  | 3 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 840 | 309 | 91 | 18 | 0 | 69 | 119 | 28 | 840 | 840 | 2.381267496 | 2.381267496 |
| scan --prec dd --mode conserve --fi -2.0 | -2 | -3000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1275 | 737 | 109 | 14 | 0 | 71 | 142 | 33 | 1275 | 285 | 1.201426408 | 1.708539646 |
| scan --prec dd --mode conserve --fi -2.0 | -2 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 699 | 166 | 72 | 14 | 0 | 59 | 89 | 17 | 699 | 699 | 1.162043429 | 1.162043429 |
| scan --prec dd --mode project --fi 16.0  | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1327 | 485 | 76 | 11 | 0 | 61 | 100 | 24 | 1327 | 1327 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode project --fi 4.0 - | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1738 | 582 | 75 | 10 | 0 | 52 | 90 | 15 | 1738 | 1738 | 3.527557745 | 3.527557745 |
| scan --prec qd --mode conserve --fi 16.0 | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 966 | 230 | 68 | 12 | 0 | 78 | 88 | 20 | 966 | 966 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1588 | 457 | 75 | 10 | 0 | 52 | 90 | 15 | 1588 | 1588 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode conserve --fi -4.0 | -4 | -10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1563 | 458 | 75 | 10 | 0 | 52 | 90 | 15 | 1563 | 1563 | 3.527557745 | 3.527557745 |

3. records where locate read a pair at a gated step: 42 records

| file command (start) | F_inf | C | class | kind | base class:kind | steps | calls | real | Unresolved | nothing | pair | old real | locate not real while old real | stop step | old stop step | eta* | old eta* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 0.25 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 599 | 213 | 171 | 0 | 0 | 42 | 171 | 0 | 462 | 462 | 0.0007153455038 | 0.0007153455038 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 0.5 | 30 | SINGULAR | F->0 | SINGULAR:F->0 | 599 | 194 | 176 | 0 | 0 | 18 | 176 | 0 | 462 | 462 | 0.001124585934 | 0.001124585934 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 0.75 | 100 | SINGULAR | F->0 | SINGULAR:F->0 | 704 | 268 | 185 | 0 | 0 | 83 | 189 | 4 | 508 | 508 | 0.0004081235124 | 0.0004081235124 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 1 | 300 | SINGULAR | F->0 | SINGULAR:F->0 | 692 | 236 | 187 | 0 | 0 | 49 | 187 | 0 | 495 | 495 | 0.0009548066174 | 0.0009548066175 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 1 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 796 | 422 | 228 | 0 | 0 | 161 | 266 | 38 | 499 | 499 | 4.578491649e-05 | 4.578491656e-05 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 1.5 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 991 | 353 | 182 | 18 | 0 | 88 | 218 | 36 | 930 | 930 | 0.5442949715 | 0.5442949715 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 2 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 953 | 315 | 194 | 18 | 0 | 76 | 217 | 23 | 892 | 892 | 1.162043429 | 1.162043429 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 2 | 3000 | NONFINITE |  | SINGULAR:a3->0 | 378 | 103 | 54 | 0 | 0 | 49 | 98 | 44 | 317 | 272 | - | 1.708539646 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 3 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 894 | 257 | 216 | 4 | 0 | 37 | 216 | 0 | 833 | 833 | 2.321748788 | 2.321748788 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 3 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 1172 | 524 | 245 | 19 | 0 | 86 | 279 | 34 | 1111 | 1111 | 2.381267496 | 2.381267496 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 4 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 1020 | 373 | 229 | 20 | 0 | 84 | 261 | 32 | 959 | 959 | 3.490621782 | 3.490621782 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | -0.5 | -30 | SINGULAR | F->0 | SINGULAR:F->0 | 599 | 194 | 176 | 0 | 0 | 18 | 176 | 0 | 462 | 462 | 0.001124585934 | 0.001124585934 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | -1 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 796 | 422 | 228 | 0 | 0 | 161 | 266 | 38 | 499 | 499 | 4.578491649e-05 | 4.578491656e-05 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | -1 | -300 | SINGULAR | F->0 | SINGULAR:F->0 | 692 | 236 | 187 | 0 | 0 | 49 | 187 | 0 | 495 | 495 | 0.0009548066174 | 0.0009548066175 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | -2 | -3000 | NONFINITE |  | SINGULAR:a3->0 | 378 | 103 | 54 | 0 | 0 | 49 | 98 | 44 | 317 | 272 | - | 1.708539646 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | -2 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 953 | 315 | 194 | 18 | 0 | 76 | 217 | 23 | 892 | 892 | 1.162043429 | 1.162043429 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 699 | 166 | 72 | 14 | 0 | 59 | 89 | 17 | 699 | 699 | 1.162043429 | 1.162043429 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 3000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1275 | 737 | 109 | 14 | 0 | 71 | 142 | 33 | 1275 | 285 | 1.201426408 | 1.708539646 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 0 | SINGULAR | F->0 | SINGULAR:F->0 | 486 | 91 | 75 | 0 | 0 | 16 | 75 | 0 | 486 | 486 | 15.78191794 | 15.78191794 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 595 | 173 | 80 | 15 | 0 | 61 | 93 | 13 | 595 | 595 | 15.81421368 | 15.81421368 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1259 | 409 | 76 | 11 | 0 | 61 | 100 | 24 | 1259 | 1259 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1236 | 410 | 76 | 11 | 0 | 61 | 100 | 24 | 1236 | 1236 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi 1.5  | 1.5 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 747 | 207 | 72 | 14 | 0 | 68 | 99 | 27 | 747 | 747 | 0.5442949715 | 0.5442949715 |
| scan --prec qd --mode conserve --fi 4.0  | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1115 | 203 | 67 | 11 | 0 | 68 | 77 | 10 | 1115 | 1115 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode conserve --fi -16. | -16 | -100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1236 | 410 | 76 | 11 | 0 | 61 | 100 | 24 | 1236 | 1236 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1563 | 458 | 75 | 10 | 0 | 52 | 90 | 15 | 1563 | 1563 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode conserve --fi 0.75 | 0.75 | 100 | SINGULAR | F->0 | SINGULAR:F->0 | 453 | 114 | 71 | 0 | 0 | 43 | 71 | 0 | 453 | 453 | 0.0004081235124 | 0.0004081235124 |
| scan --prec dd --mode conserve --fi -1.0 | -1 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 474 | 179 | 81 | 0 | 0 | 83 | 101 | 20 | 474 | 474 | 4.578491649e-05 | 4.578491656e-05 |
| scan --prec dd --mode conserve --fi -1.0 | -1 | -300 | SINGULAR | F->0 | SINGULAR:F->0 | 444 | 94 | 71 | 0 | 0 | 23 | 71 | 0 | 444 | 444 | 0.0009548066174 | 0.0009548066175 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 710 | 184 | 74 | 15 | 0 | 65 | 97 | 23 | 710 | 710 | 3.490621782 | 3.490621782 |
| scan --prec dd --mode conserve --fi 1.0  | 1 | 300 | SINGULAR | F->0 | SINGULAR:F->0 | 444 | 94 | 71 | 0 | 0 | 23 | 71 | 0 | 444 | 444 | 0.0009548066174 | 0.0009548066175 |
| scan --prec dd --mode conserve --fi 1.0  | 1 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 474 | 179 | 81 | 0 | 0 | 83 | 101 | 20 | 474 | 474 | 4.578491649e-05 | 4.578491656e-05 |
| scan --prec dd --mode conserve --fi 3.0  | 3 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 626 | 105 | 74 | 3 | 0 | 28 | 74 | 0 | 626 | 626 | 2.321748788 | 2.321748788 |
| scan --prec dd --mode conserve --fi 3.0  | 3 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 840 | 309 | 91 | 18 | 0 | 69 | 119 | 28 | 840 | 840 | 2.381267496 | 2.381267496 |
| scan --prec dd --mode conserve --fi -2.0 | -2 | -3000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1275 | 737 | 109 | 14 | 0 | 71 | 142 | 33 | 1275 | 285 | 1.201426408 | 1.708539646 |
| scan --prec dd --mode conserve --fi -2.0 | -2 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 699 | 166 | 72 | 14 | 0 | 59 | 89 | 17 | 699 | 699 | 1.162043429 | 1.162043429 |
| scan --prec dd --mode project --fi 16.0  | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1327 | 485 | 76 | 11 | 0 | 61 | 100 | 24 | 1327 | 1327 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode project --fi 4.0 - | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1738 | 582 | 75 | 10 | 0 | 52 | 90 | 15 | 1738 | 1738 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode conserve --fi 0.25 | 0.25 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 433 | 95 | 71 | 0 | 0 | 24 | 71 | 0 | 433 | 433 | 0.0007153455038 | 0.0007153455038 |
| scan --prec qd --mode conserve --fi 16.0 | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 966 | 230 | 68 | 12 | 0 | 78 | 88 | 20 | 966 | 966 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1588 | 457 | 75 | 10 | 0 | 52 | 90 | 15 | 1588 | 1588 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode conserve --fi -4.0 | -4 | -10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1563 | 458 | 75 | 10 | 0 | 52 | 90 | 15 | 1563 | 1563 | 3.527557745 | 3.527557745 |

4. records whose stop is not the old rule's: 4 records

| file command (start) | F_inf | C | class | kind | base class:kind | steps | calls | real | Unresolved | nothing | pair | old real | locate not real while old real | stop step | old stop step | eta* | old eta* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 2 | 3000 | NONFINITE |  | SINGULAR:a3->0 | 378 | 103 | 54 | 0 | 0 | 49 | 98 | 44 | 317 | 272 | - | 1.708539646 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | -2 | -3000 | NONFINITE |  | SINGULAR:a3->0 | 378 | 103 | 54 | 0 | 0 | 49 | 98 | 44 | 317 | 272 | - | 1.708539646 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 3000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1275 | 737 | 109 | 14 | 0 | 71 | 142 | 33 | 1275 | 285 | 1.201426408 | 1.708539646 |
| scan --prec dd --mode conserve --fi -2.0 | -2 | -3000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1275 | 737 | 109 | 14 | 0 | 71 | 142 | 33 | 1275 | 285 | 1.201426408 | 1.708539646 |

5. eta* against the old rule's eta* on the same steps: 517 SINGULAR records with both; largest |difference| / max(1, eta*) 4.221e-01; above 1e-12: 3; above 1e-10: 2

  4.221e-01  F_inf 2.0 C [3000.0, 0.0]  eta* 1.2014264075106749  old 1.7085396460352056  [scan --prec dd --mode conserve --fi 2.0 --c -3000.0,-1000.0,]
  4.221e-01  F_inf -2.0 C [-3000.0, 0.0]  eta* 1.2014264075106749  old 1.7085396460352056  [scan --prec dd --mode conserve --fi -2.0 --c -3000.0,-1000.0]
  3.136e-12  F_inf 4.0 C [100000.0, 0.0]  eta* 3.8700765928292324  old 3.870076592817097  [scan --prec dd --mode conserve --fi 4.0 --c -100000000.0,-10]
  3.079e-13  F_inf 4.0 C [10000.0, 0.0]  eta* 3.8518194111942528  old 3.8518194111930666  [scan --prec dd --mode conserve --fi 4.0 --c -100000000.0,-10]
  2.178e-13  F_inf 1.5 C [3000.0, 0.0]  eta* 1.1000625308564749  old 1.1000625308567145  [scan --prec dd --mode conserve --fi 1.5 --c -3000.0,-1000.0,]
  2.125e-13  F_inf 16.0 C [100000.0, 0.0]  eta* 15.947732200243433  old 15.947732200240043  [scan --prec dd --mode conserve --fi 16.0 --c -100000000.0,-1]
  2.065e-13  F_inf 1.5 C [3000.0, 0.0]  eta* 1.1000625308564973  old 1.1000625308567245  [scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,-2 -3000,-1000,-300,-]
  7.849e-14  F_inf 1.5 C [100.0, 0.0]  eta* 0.25907211152033527  old 0.25907211152041376  [scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,-2 -3000,-1000,-300,-]
