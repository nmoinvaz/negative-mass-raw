records with a `loc` key: 615

1. totals (records; records with calls of locate; with an Unresolved step; with a pair step; with no result at a step; SINGULAR records whose stop step differs from the old rule's; SINGULAR records the old rule would not have stopped by then)

| file kind | class | records | with calls | Unresolved | pair | nothing | stop step differs | old rule no stop |
|---|---|---|---|---|---|---|---|---|
| conical | FLOOR | 15 | 15 | 0 | 0 | 0 | 0 | 0 |
| conical | NONFINITE | 3 | 3 | 3 | 0 | 0 | 0 | 0 |
| conical | SINGULAR | 169 | 169 | 17 | 0 | 0 | 3 | 0 |
| offgrid | FLOOR | 77 | 23 | 1 | 0 | 0 | 0 | 0 |
| offgrid | SINGULAR | 344 | 344 | 37 | 0 | 0 | 13 | 0 |
| offgrid | TINYSTEP | 7 | 7 | 7 | 0 | 0 | 0 | 0 |

2. records where locate said Unresolved or gave nothing at a gated step: 65 records

| file command (start) | F_inf | C | class | kind | base class:kind | steps | calls | real | Unresolved | nothing | pair | old real | locate not real while old real | stop step | old stop step | eta* | old eta* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 0.25 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 599 | 213 | 171 | 42 | 0 | 0 | 171 | 0 | 462 | 462 | 0.0007153455038 | 0.0007153455038 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 0.5 | 30 | SINGULAR | F->0 | SINGULAR:F->0 | 599 | 194 | 176 | 18 | 0 | 0 | 176 | 0 | 462 | 462 | 0.001124585934 | 0.001124585934 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 0.75 | 100 | SINGULAR | F->0 | SINGULAR:F->0 | 704 | 268 | 185 | 83 | 0 | 0 | 189 | 4 | 508 | 508 | 0.0004081235124 | 0.0004081235124 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 0.75 | 300 | NONFINITE |  | SINGULAR:other | 498 | 128 | 35 | 93 | 0 | 0 | 115 | 82 | 212 | 166 | - | 1.157378097e-06 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 1 | 300 | SINGULAR | F->0 | SINGULAR:F->0 | 692 | 236 | 187 | 49 | 0 | 0 | 187 | 0 | 495 | 495 | 0.0009548066174 | 0.0009548066175 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 1 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 796 | 422 | 199 | 223 | 0 | 0 | 266 | 67 | 499 | 499 | 4.578491649e-05 | 4.578491656e-05 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 1 | 3000 | NONFINITE |  | SINGULAR:other | 727 | 118 | 0 | 118 | 0 | 0 | 105 | 105 | 204 | 152 | - | 3.649447461e-06 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 1.5 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 991 | 353 | 181 | 172 | 0 | 0 | 218 | 37 | 930 | 930 | 0.5442949715 | 0.5442949715 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 1.5 | 3000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 364 | 88 | 5 | 83 | 0 | 0 | 88 | 83 | 303 | 272 | 1.100062531 | 1.100062531 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 2 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 953 | 315 | 194 | 121 | 0 | 0 | 217 | 23 | 892 | 892 | 1.162043429 | 1.162043429 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 2 | 3000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 355 | 80 | 5 | 75 | 0 | 0 | 80 | 75 | 294 | 272 | 1.708539646 | 1.708539646 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 3 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 894 | 257 | 216 | 41 | 0 | 0 | 216 | 0 | 833 | 833 | 2.321748788 | 2.321748788 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 3 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 1172 | 524 | 221 | 303 | 0 | 0 | 279 | 58 | 1111 | 1111 | 2.381267496 | 2.381267496 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 4 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 1020 | 373 | 229 | 144 | 0 | 0 | 261 | 32 | 959 | 959 | 3.490621782 | 3.490621782 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | -0.5 | -30 | SINGULAR | F->0 | SINGULAR:F->0 | 599 | 194 | 176 | 18 | 0 | 0 | 176 | 0 | 462 | 462 | 0.001124585934 | 0.001124585934 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | -1 | -3000 | NONFINITE |  | SINGULAR:other | 727 | 118 | 0 | 118 | 0 | 0 | 105 | 105 | 204 | 152 | - | 3.649447461e-06 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | -1 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 796 | 422 | 199 | 223 | 0 | 0 | 266 | 67 | 499 | 499 | 4.578491649e-05 | 4.578491656e-05 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | -1 | -300 | SINGULAR | F->0 | SINGULAR:F->0 | 692 | 236 | 187 | 49 | 0 | 0 | 187 | 0 | 495 | 495 | 0.0009548066174 | 0.0009548066175 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | -2 | -3000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 355 | 80 | 5 | 75 | 0 | 0 | 80 | 75 | 294 | 272 | 1.708539646 | 1.708539646 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | -2 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 953 | 315 | 194 | 121 | 0 | 0 | 217 | 23 | 892 | 892 | 1.162043429 | 1.162043429 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 699 | 166 | 72 | 94 | 0 | 0 | 89 | 17 | 699 | 699 | 1.162043429 | 1.162043429 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 3000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 302 | 58 | 5 | 53 | 0 | 0 | 58 | 53 | 302 | 285 | 1.708539646 | 1.708539646 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 0 | SINGULAR | F->0 | SINGULAR:F->0 | 486 | 91 | 75 | 16 | 0 | 0 | 75 | 0 | 486 | 486 | 15.78191794 | 15.78191794 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 595 | 173 | 75 | 86 | 0 | 0 | 93 | 18 | 595 | 595 | 15.81421368 | 15.81421368 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 336 | 90 | 5 | 85 | 0 | 0 | 83 | 78 | 336 | 288 | 15.9477322 | 15.9477322 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 1000000 | TINYSTEP |  | SINGULAR:a3->0 | 447 | 57 | 0 | 57 | 0 | 0 | 57 | 57 | 447 | 417 | - | 1.73192683 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1259 | 409 | 86 | 323 | 0 | 0 | 100 | 14 | 1259 | 1259 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000000 | TINYSTEP |  | SINGULAR:a3->0 | 513 | 89 | 64 | 25 | 0 | 0 | 83 | 19 | 513 | 499 | - | 15.96866047 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1236 | 410 | 86 | 324 | 0 | 0 | 100 | 14 | 1236 | 1236 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000000 | TINYSTEP |  | SINGULAR:a3->0 | 491 | 89 | 64 | 25 | 0 | 0 | 83 | 19 | 491 | 477 | - | 15.96866047 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 1000000 | TINYSTEP |  | SINGULAR:a3->0 | 462 | 52 | 0 | 52 | 0 | 0 | 50 | 50 | 462 | 435 | - | 1.73192683 |
| scan --prec dd --mode conserve --fi 1.5  | 1.5 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 747 | 207 | 72 | 135 | 0 | 0 | 99 | 27 | 747 | 747 | 0.5442949715 | 0.5442949715 |
| scan --prec dd --mode conserve --fi 1.5  | 1.5 | 3000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 311 | 64 | 5 | 59 | 0 | 0 | 64 | 59 | 311 | 287 | 1.100062531 | 1.100062531 |
| scan --prec qd --mode conserve --fi 4.0  | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1115 | 203 | 77 | 126 | 0 | 0 | 77 | 0 | 1115 | 1115 | 3.527557745 | 3.527557745 |
| scan --prec qd --mode conserve --fi 4.0  | 4 | 100000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 411 | 77 | 7 | 70 | 0 | 0 | 77 | 70 | 411 | 378 | 3.870076593 | 3.870076593 |
| scan --prec dd --mode conserve --fi -16. | -16 | -100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1236 | 410 | 86 | 324 | 0 | 0 | 100 | 14 | 1236 | 1236 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi -16. | -16 | -100000000 | TINYSTEP |  | SINGULAR:a3->0 | 491 | 89 | 64 | 25 | 0 | 0 | 83 | 19 | 491 | 477 | - | 15.96866047 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1563 | 458 | 86 | 372 | 0 | 0 | 90 | 4 | 1563 | 1563 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 100000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 407 | 64 | 5 | 59 | 0 | 0 | 64 | 59 | 407 | 376 | 3.870076593 | 3.870076593 |
| scan --prec dd --mode conserve --fi 0.75 | 0.75 | 100 | SINGULAR | F->0 | SINGULAR:F->0 | 453 | 114 | 71 | 43 | 0 | 0 | 71 | 0 | 453 | 453 | 0.0004081235124 | 0.0004081235124 |
| scan --prec dd --mode conserve --fi 0.75 | 0.75 | 300 | FLOOR | log | SINGULAR:other | 457 | 166 | 5 | 161 | 0 | 0 | 59 | 55 | 457 | 313 | - | 1.157378098e-06 |
| scan --prec dd --mode conserve --fi -1.0 | -1 | -3000 | SINGULAR | F->0 | SINGULAR:other | 518 | 211 | 58 | 153 | 0 | 0 | 110 | 53 | 518 | 330 | 2.547628971e-06 | 3.649447456e-06 |
| scan --prec dd --mode conserve --fi -1.0 | -1 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 474 | 179 | 71 | 108 | 0 | 0 | 101 | 30 | 474 | 474 | 4.578491649e-05 | 4.578491656e-05 |
| scan --prec dd --mode conserve --fi -1.0 | -1 | -300 | SINGULAR | F->0 | SINGULAR:F->0 | 444 | 94 | 71 | 23 | 0 | 0 | 71 | 0 | 444 | 444 | 0.0009548066174 | 0.0009548066175 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 710 | 184 | 74 | 110 | 0 | 0 | 97 | 23 | 710 | 710 | 3.490621782 | 3.490621782 |
| scan --prec dd --mode conserve --fi 1.0  | 1 | 300 | SINGULAR | F->0 | SINGULAR:F->0 | 444 | 94 | 71 | 23 | 0 | 0 | 71 | 0 | 444 | 444 | 0.0009548066174 | 0.0009548066175 |
| scan --prec dd --mode conserve --fi 1.0  | 1 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 474 | 179 | 71 | 108 | 0 | 0 | 101 | 30 | 474 | 474 | 4.578491649e-05 | 4.578491656e-05 |
| scan --prec dd --mode conserve --fi 1.0  | 1 | 3000 | SINGULAR | F->0 | SINGULAR:other | 518 | 211 | 58 | 153 | 0 | 0 | 110 | 53 | 518 | 330 | 2.547628971e-06 | 3.649447456e-06 |
| scan --prec dd --mode conserve --fi 3.0  | 3 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 626 | 105 | 74 | 31 | 0 | 0 | 74 | 0 | 626 | 626 | 2.321748788 | 2.321748788 |
| scan --prec dd --mode conserve --fi 3.0  | 3 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 840 | 309 | 77 | 232 | 0 | 0 | 119 | 42 | 840 | 840 | 2.381267496 | 2.381267496 |
| scan --prec dd --mode conserve --fi -2.0 | -2 | -3000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 302 | 58 | 5 | 53 | 0 | 0 | 58 | 53 | 302 | 285 | 1.708539646 | 1.708539646 |
| scan --prec dd --mode conserve --fi -2.0 | -2 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 699 | 166 | 72 | 94 | 0 | 0 | 89 | 17 | 699 | 699 | 1.162043429 | 1.162043429 |
| scan --prec dd --mode project --fi 16.0  | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1327 | 485 | 86 | 399 | 0 | 0 | 100 | 14 | 1327 | 1327 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode project --fi 16.0  | 16 | 100000000 | TINYSTEP |  | SINGULAR:a3->0 | 491 | 89 | 64 | 25 | 0 | 0 | 83 | 19 | 491 | 477 | - | 15.96866047 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 10000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 332 | 75 | 5 | 70 | 0 | 0 | 75 | 70 | 332 | 297 | 3.851819411 | 3.851819411 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 100000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 407 | 144 | 40 | 104 | 0 | 0 | 135 | 96 | 407 | 314 | 3.870076593 | 3.870076593 |
| scan --prec dd --mode project --fi 4.0 - | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1738 | 582 | 86 | 496 | 0 | 0 | 90 | 4 | 1738 | 1738 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode project --fi 4.0 - | 4 | 100000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 407 | 64 | 5 | 59 | 0 | 0 | 64 | 59 | 407 | 376 | 3.870076593 | 3.870076593 |
| scan --prec dd --mode conserve --fi 0.25 | 0.25 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 433 | 95 | 71 | 24 | 0 | 0 | 71 | 0 | 433 | 433 | 0.0007153455038 | 0.0007153455038 |
| scan --prec qd --mode conserve --fi 16.0 | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 966 | 230 | 81 | 149 | 0 | 0 | 88 | 7 | 966 | 966 | 15.86125434 | 15.86125434 |
| scan --prec qd --mode conserve --fi 16.0 | 16 | 100000000 | TINYSTEP |  | SINGULAR:a3->0 | 467 | 95 | 54 | 41 | 0 | 0 | 82 | 30 | 467 | 442 | - | 15.96866047 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1588 | 457 | 86 | 371 | 0 | 0 | 90 | 4 | 1588 | 1588 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 100000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 430 | 64 | 5 | 59 | 0 | 0 | 64 | 59 | 430 | 399 | 3.870076593 | 3.870076593 |
| scan --prec dd --mode conserve --fi -4.0 | -4 | -10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1563 | 458 | 86 | 372 | 0 | 0 | 90 | 4 | 1563 | 1563 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode conserve --fi -4.0 | -4 | -100000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 407 | 64 | 5 | 59 | 0 | 0 | 64 | 59 | 407 | 376 | 3.870076593 | 3.870076593 |

3. records where locate read a pair at a gated step: 0 records


4. records whose stop is not the old rule's: 27 records

| file command (start) | F_inf | C | class | kind | base class:kind | steps | calls | real | Unresolved | nothing | pair | old real | locate not real while old real | stop step | old stop step | eta* | old eta* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 0.75 | 300 | NONFINITE |  | SINGULAR:other | 498 | 128 | 35 | 93 | 0 | 0 | 115 | 82 | 212 | 166 | - | 1.157378097e-06 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 1 | 3000 | NONFINITE |  | SINGULAR:other | 727 | 118 | 0 | 118 | 0 | 0 | 105 | 105 | 204 | 152 | - | 3.649447461e-06 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 1.5 | 3000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 364 | 88 | 5 | 83 | 0 | 0 | 88 | 83 | 303 | 272 | 1.100062531 | 1.100062531 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 2 | 3000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 355 | 80 | 5 | 75 | 0 | 0 | 80 | 75 | 294 | 272 | 1.708539646 | 1.708539646 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | -1 | -3000 | NONFINITE |  | SINGULAR:other | 727 | 118 | 0 | 118 | 0 | 0 | 105 | 105 | 204 | 152 | - | 3.649447461e-06 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | -2 | -3000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 355 | 80 | 5 | 75 | 0 | 0 | 80 | 75 | 294 | 272 | 1.708539646 | 1.708539646 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 3000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 302 | 58 | 5 | 53 | 0 | 0 | 58 | 53 | 302 | 285 | 1.708539646 | 1.708539646 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 336 | 90 | 5 | 85 | 0 | 0 | 83 | 78 | 336 | 288 | 15.9477322 | 15.9477322 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 1000000 | TINYSTEP |  | SINGULAR:a3->0 | 447 | 57 | 0 | 57 | 0 | 0 | 57 | 57 | 447 | 417 | - | 1.73192683 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000000 | TINYSTEP |  | SINGULAR:a3->0 | 513 | 89 | 64 | 25 | 0 | 0 | 83 | 19 | 513 | 499 | - | 15.96866047 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000000 | TINYSTEP |  | SINGULAR:a3->0 | 491 | 89 | 64 | 25 | 0 | 0 | 83 | 19 | 491 | 477 | - | 15.96866047 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 1000000 | TINYSTEP |  | SINGULAR:a3->0 | 462 | 52 | 0 | 52 | 0 | 0 | 50 | 50 | 462 | 435 | - | 1.73192683 |
| scan --prec dd --mode conserve --fi 1.5  | 1.5 | 3000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 311 | 64 | 5 | 59 | 0 | 0 | 64 | 59 | 311 | 287 | 1.100062531 | 1.100062531 |
| scan --prec qd --mode conserve --fi 4.0  | 4 | 100000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 411 | 77 | 7 | 70 | 0 | 0 | 77 | 70 | 411 | 378 | 3.870076593 | 3.870076593 |
| scan --prec dd --mode conserve --fi -16. | -16 | -100000000 | TINYSTEP |  | SINGULAR:a3->0 | 491 | 89 | 64 | 25 | 0 | 0 | 83 | 19 | 491 | 477 | - | 15.96866047 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 100000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 407 | 64 | 5 | 59 | 0 | 0 | 64 | 59 | 407 | 376 | 3.870076593 | 3.870076593 |
| scan --prec dd --mode conserve --fi 0.75 | 0.75 | 300 | FLOOR | log | SINGULAR:other | 457 | 166 | 5 | 161 | 0 | 0 | 59 | 55 | 457 | 313 | - | 1.157378098e-06 |
| scan --prec dd --mode conserve --fi -1.0 | -1 | -3000 | SINGULAR | F->0 | SINGULAR:other | 518 | 211 | 58 | 153 | 0 | 0 | 110 | 53 | 518 | 330 | 2.547628971e-06 | 3.649447456e-06 |
| scan --prec dd --mode conserve --fi 1.0  | 1 | 3000 | SINGULAR | F->0 | SINGULAR:other | 518 | 211 | 58 | 153 | 0 | 0 | 110 | 53 | 518 | 330 | 2.547628971e-06 | 3.649447456e-06 |
| scan --prec dd --mode conserve --fi -2.0 | -2 | -3000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 302 | 58 | 5 | 53 | 0 | 0 | 58 | 53 | 302 | 285 | 1.708539646 | 1.708539646 |
| scan --prec dd --mode project --fi 16.0  | 16 | 100000000 | TINYSTEP |  | SINGULAR:a3->0 | 491 | 89 | 64 | 25 | 0 | 0 | 83 | 19 | 491 | 477 | - | 15.96866047 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 10000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 332 | 75 | 5 | 70 | 0 | 0 | 75 | 70 | 332 | 297 | 3.851819411 | 3.851819411 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 100000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 407 | 144 | 40 | 104 | 0 | 0 | 135 | 96 | 407 | 314 | 3.870076593 | 3.870076593 |
| scan --prec dd --mode project --fi 4.0 - | 4 | 100000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 407 | 64 | 5 | 59 | 0 | 0 | 64 | 59 | 407 | 376 | 3.870076593 | 3.870076593 |
| scan --prec qd --mode conserve --fi 16.0 | 16 | 100000000 | TINYSTEP |  | SINGULAR:a3->0 | 467 | 95 | 54 | 41 | 0 | 0 | 82 | 30 | 467 | 442 | - | 15.96866047 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 100000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 430 | 64 | 5 | 59 | 0 | 0 | 64 | 59 | 430 | 399 | 3.870076593 | 3.870076593 |
| scan --prec dd --mode conserve --fi -4.0 | -4 | -100000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 407 | 64 | 5 | 59 | 0 | 0 | 64 | 59 | 407 | 376 | 3.870076593 | 3.870076593 |

5. eta* against the old rule's eta* on the same steps: 513 SINGULAR records with both; largest |difference| / max(1, eta*) 1.102e-06; above 1e-12: 6; above 1e-10: 2

  1.102e-06  F_inf -1.0 C [-3000.0, 0.0]  eta* 2.5476289711206824e-06  old 3.6494474562655617e-06  [scan --prec dd --mode conserve --fi -1.0 --c -3000.0,-1000.0]
  1.102e-06  F_inf 1.0 C [3000.0, 0.0]  eta* 2.5476289711206824e-06  old 3.6494474562655617e-06  [scan --prec dd --mode conserve --fi 1.0 --c -3000.0,-1000.0,]
  3.136e-12  F_inf 4.0 C [100000.0, 0.0]  eta* 3.8700765928292324  old 3.870076592817097  [scan --prec dd --mode conserve --fi 4.0 --c -100000000.0,-10]
  2.464e-12  F_inf 1.5 C [3000.0, 0.0]  eta* 1.100062530859435  old 1.1000625308567245  [scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,-2 -3000,-1000,-300,-]
  2.364e-12  F_inf 2.0 C [3000.0, 0.0]  eta* 1.7085396460394195  old 1.708539646035381  [scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,-2 -3000,-1000,-300,-]
  2.364e-12  F_inf -2.0 C [-3000.0, 0.0]  eta* 1.7085396460394195  old 1.708539646035381  [scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,-2 -3000,-1000,-300,-]
  9.400e-13  F_inf 1.5 C [3000.0, 0.0]  eta* 1.1000625308577485  old 1.1000625308567145  [scan --prec dd --mode conserve --fi 1.5 --c -3000.0,-1000.0,]
  5.830e-13  F_inf 2.0 C [3000.0, 0.0]  eta* 1.7085396460362017  old 1.7085396460352056  [scan --prec dd --mode conserve --fi 2.0 --c -3000.0,-1000.0,]
