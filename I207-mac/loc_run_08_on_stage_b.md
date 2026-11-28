records with a `loc` key: 960

1. totals (records; records with calls of locate; with an Unresolved step; with a pair step; with no result at a step; SINGULAR records whose stop step differs from the old rule's; SINGULAR records the old rule would not have stopped by then)

| file kind | class | records | with calls | Unresolved | pair | nothing | stop step differs | old rule no stop |
|---|---|---|---|---|---|---|---|---|
| offgrid | FLOOR | 233 | 0 | 0 | 0 | 0 | 0 | 0 |
| offgrid | SINGULAR | 721 | 721 | 40 | 47 | 0 | 5 | 15 |
| offgrid | TINYSTEP | 6 | 6 | 0 | 6 | 0 | 0 | 0 |

2. records where locate said Unresolved or gave nothing at a gated step: 40 records

| file command (start) | F_inf | C | class | kind | base class:kind | steps | calls | real | Unresolved | nothing | pair | old real | locate not real while old real | stop step | old stop step | eta* | old eta* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| scan --prec dd --mode conserve --fi 12.0 | 12 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 900 | 107 | 76 | 4 | 0 | 27 | 76 | 0 | 900 | 900 | 11.80758764 | 11.80758764 |
| scan --prec dd --mode conserve --fi 12.0 | 12 | 100000 | SINGULAR | F->0 | SINGULAR:a3->0 | 2059 | 1184 | 86 | 11 | 0 | 68 | 118 | 32 | 2059 | 366 | 11.82837564 | 11.94329521 |
| scan --prec dd --mode conserve --fi 6.0  | 6 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 2375 | 1367 | 77 | 11 | 0 | 70 | 111 | 34 | 2375 | 2375 | 5.676108256 | 5.676108256 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1134 | 126 | 75 | 10 | 0 | 37 | 75 | 0 | 1134 | 1134 | 4.60350778 | 4.60350778 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 3974 | 2919 | 86 | 11 | 0 | 72 | 124 | 38 | 3974 | 369 | 4.621440417 | 4.887360434 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 913 | 137 | 75 | 11 | 0 | 43 | 79 | 4 | 913 | 913 | 23.89303019 | 23.89303019 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 300000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1682 | 903 | 86 | 11 | 0 | 70 | 120 | 34 | 1682 | 362 | 23.90645139 | 23.96419759 |
| scan --prec dd --mode conserve --fi 8.0  | 8 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 1320 | 375 | 76 | 12 | 0 | 54 | 93 | 17 | 1320 | 1320 | 7.74378012 | 7.74378012 |
| scan --prec dd --mode conserve --fi 3.0  | 3 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 2941 | 1744 | 75 | 11 | 0 | 68 | 108 | 33 | 2941 | 2941 | 2.408310586 | 2.408310586 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 855 | 129 | 75 | 12 | 0 | 39 | 75 | 0 | 855 | 855 | 31.91172367 | 31.91172367 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 300000 | SINGULAR | F->0 | SINGULAR:F->0 | 1180 | 438 | 80 | 10 | 0 | 66 | 108 | 28 | 1180 | 1180 | 31.92248282 | 31.92248282 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1236 | 410 | 76 | 11 | 0 | 61 | 100 | 24 | 1236 | 1236 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -300000 | SINGULAR | F->0 | SINGULAR:F->0 | 830 | 154 | 76 | 12 | 0 | 48 | 83 | 7 | 830 | 830 | 63.94674087 | 63.94674087 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -100000 | SINGULAR | F->0 | SINGULAR:F->0 | 895 | 218 | 76 | 11 | 0 | 58 | 95 | 19 | 895 | 895 | 63.9497507 | 63.9497507 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -30000 | SINGULAR | F->0 | SINGULAR:F->0 | 921 | 244 | 76 | 12 | 0 | 61 | 98 | 22 | 921 | 921 | 63.95060498 | 63.95060498 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -10000 | SINGULAR | F->0 | SINGULAR:F->0 | 927 | 251 | 75 | 12 | 0 | 62 | 98 | 23 | 927 | 927 | 63.95083414 | 63.95083414 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -3000 | SINGULAR | F->0 | SINGULAR:F->0 | 930 | 253 | 75 | 11 | 0 | 63 | 99 | 24 | 930 | 930 | 63.95091289 | 63.95091289 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95093525 | 63.95093525 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -300 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094307 | 63.95094307 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -100 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.9509453 | 63.9509453 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -30 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094608 | 63.95094608 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -10 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.9509463 | 63.9509463 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -3 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.95094638 | 63.95094638 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -1 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 258 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.9509464 | 63.9509464 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 0 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 256 | 75 | 10 | 0 | 63 | 99 | 24 | 932 | 932 | 63.95094641 | 63.95094641 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 1 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.95094642 | 63.95094642 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 3 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.95094645 | 63.95094645 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094652 | 63.95094652 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 30 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094675 | 63.95094675 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 100 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094753 | 63.95094753 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 300 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094976 | 63.95094976 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 255 | 75 | 10 | 0 | 63 | 99 | 24 | 932 | 932 | 63.95095756 | 63.95095756 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 257 | 76 | 11 | 0 | 63 | 100 | 24 | 933 | 933 | 63.9509798 | 63.9509798 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 936 | 258 | 76 | 11 | 0 | 63 | 100 | 24 | 936 | 936 | 63.95105719 | 63.95105719 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 943 | 266 | 77 | 11 | 0 | 63 | 101 | 24 | 943 | 943 | 63.95127439 | 63.95127439 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 994 | 294 | 77 | 10 | 0 | 65 | 104 | 27 | 994 | 994 | 63.9519919 | 63.9519919 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 300000 | SINGULAR | F->0 | SINGULAR:F->0 | 1081 | 381 | 85 | 10 | 0 | 64 | 111 | 26 | 1081 | 1081 | 63.95373817 | 63.95373817 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 1000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1483 | 782 | 99 | 11 | 0 | 67 | 130 | 31 | 1483 | 379 | 63.95771562 | 63.97939557 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1563 | 458 | 75 | 10 | 0 | 52 | 90 | 15 | 1563 | 1563 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode conserve --fi 128. | 128 | -3000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1317 | 666 | 106 | 32 | 0 | 73 | 135 | 29 | 1317 | 374 | 127.9742308 | 127.9850717 |

3. records where locate read a pair at a gated step: 53 records

| file command (start) | F_inf | C | class | kind | base class:kind | steps | calls | real | Unresolved | nothing | pair | old real | locate not real while old real | stop step | old stop step | eta* | old eta* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| scan --prec dd --mode conserve --fi 2.0  | 2 | 10000 | TINYSTEP |  | SINGULAR:a3->0 | 415 | 74 | 19 | 0 | 0 | 55 | 54 | 35 | 415 | 378 | - | 1.723881779 |
| scan --prec dd --mode conserve --fi 12.0 | 12 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 900 | 107 | 76 | 4 | 0 | 27 | 76 | 0 | 900 | 900 | 11.80758764 | 11.80758764 |
| scan --prec dd --mode conserve --fi 12.0 | 12 | 100000 | SINGULAR | F->0 | SINGULAR:a3->0 | 2059 | 1184 | 86 | 11 | 0 | 68 | 118 | 32 | 2059 | 366 | 11.82837564 | 11.94329521 |
| scan --prec qd --mode conserve --fi 1.5  | 1.5 | 10000 | TINYSTEP |  | SINGULAR:a3->0 | 432 | 87 | 27 | 0 | 0 | 60 | 69 | 42 | 432 | 391 | - | 1.111951034 |
| scan --prec qd --mode conserve --fi 1.5  | 1.5 | 30000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 392 | 43 | 40 | 0 | 0 | 3 | 43 | 3 | 392 | 392 | 1.115792337 | 1.115792337 |
| scan --prec dd --mode conserve --fi 6.0  | 6 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 937 | 98 | 75 | 0 | 0 | 23 | 75 | 0 | 937 | 937 | 5.654148443 | 5.654148443 |
| scan --prec dd --mode conserve --fi 6.0  | 6 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 2375 | 1367 | 77 | 11 | 0 | 70 | 111 | 34 | 2375 | 2375 | 5.676108256 | 5.676108256 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1134 | 126 | 75 | 10 | 0 | 37 | 75 | 0 | 1134 | 1134 | 4.60350778 | 4.60350778 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 3974 | 2919 | 86 | 11 | 0 | 72 | 124 | 38 | 3974 | 369 | 4.621440417 | 4.887360434 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 913 | 137 | 75 | 11 | 0 | 43 | 79 | 4 | 913 | 913 | 23.89303019 | 23.89303019 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 300000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1682 | 903 | 86 | 11 | 0 | 70 | 120 | 34 | 1682 | 362 | 23.90645139 | 23.96419759 |
| scan --prec dd --mode conserve --fi 8.0  | 8 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 1320 | 375 | 76 | 12 | 0 | 54 | 93 | 17 | 1320 | 1320 | 7.74378012 | 7.74378012 |
| scan --prec dd --mode conserve --fi 8.0  | 8 | 100000 | TINYSTEP |  | SINGULAR:a3->0 | 404 | 73 | 35 | 0 | 0 | 38 | 67 | 32 | 404 | 368 | - | 7.928774963 |
| scan --prec dd --mode conserve --fi -2.0 | -2 | -10000 | TINYSTEP |  | SINGULAR:a3->0 | 415 | 74 | 19 | 0 | 0 | 55 | 54 | 35 | 415 | 378 | - | 1.723881779 |
| scan --prec dd --mode conserve --fi 0.15 | 0.15 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 606 | 130 | 71 | 0 | 0 | 59 | 81 | 10 | 606 | 606 | 1.655110783e-06 | 1.655110783e-06 |
| scan --prec dd --mode conserve --fi 3.0  | 3 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 2941 | 1744 | 75 | 11 | 0 | 68 | 108 | 33 | 2941 | 2941 | 2.408310586 | 2.408310586 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 855 | 129 | 75 | 12 | 0 | 39 | 75 | 0 | 855 | 855 | 31.91172367 | 31.91172367 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 300000 | SINGULAR | F->0 | SINGULAR:F->0 | 1180 | 438 | 80 | 10 | 0 | 66 | 108 | 28 | 1180 | 1180 | 31.92248282 | 31.92248282 |
| scan --prec qd --mode conserve --fi 0.02 | 0.02 | 1 | SINGULAR | F->0 | SINGULAR:F->0 | 682 | 174 | 65 | 0 | 0 | 109 | 85 | 20 | 682 | 682 | 1.126952069e-06 | 1.126952069e-06 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1236 | 410 | 76 | 11 | 0 | 61 | 100 | 24 | 1236 | 1236 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -300000 | SINGULAR | F->0 | SINGULAR:F->0 | 830 | 154 | 76 | 12 | 0 | 48 | 83 | 7 | 830 | 830 | 63.94674087 | 63.94674087 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -100000 | SINGULAR | F->0 | SINGULAR:F->0 | 895 | 218 | 76 | 11 | 0 | 58 | 95 | 19 | 895 | 895 | 63.9497507 | 63.9497507 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -30000 | SINGULAR | F->0 | SINGULAR:F->0 | 921 | 244 | 76 | 12 | 0 | 61 | 98 | 22 | 921 | 921 | 63.95060498 | 63.95060498 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -10000 | SINGULAR | F->0 | SINGULAR:F->0 | 927 | 251 | 75 | 12 | 0 | 62 | 98 | 23 | 927 | 927 | 63.95083414 | 63.95083414 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -3000 | SINGULAR | F->0 | SINGULAR:F->0 | 930 | 253 | 75 | 11 | 0 | 63 | 99 | 24 | 930 | 930 | 63.95091289 | 63.95091289 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95093525 | 63.95093525 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -300 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094307 | 63.95094307 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -100 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.9509453 | 63.9509453 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -30 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094608 | 63.95094608 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -10 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.9509463 | 63.9509463 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -3 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.95094638 | 63.95094638 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -1 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 258 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.9509464 | 63.9509464 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 0 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 256 | 75 | 10 | 0 | 63 | 99 | 24 | 932 | 932 | 63.95094641 | 63.95094641 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 1 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.95094642 | 63.95094642 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 3 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.95094645 | 63.95094645 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094652 | 63.95094652 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 30 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094675 | 63.95094675 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 100 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094753 | 63.95094753 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 300 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094976 | 63.95094976 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 255 | 75 | 10 | 0 | 63 | 99 | 24 | 932 | 932 | 63.95095756 | 63.95095756 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 257 | 76 | 11 | 0 | 63 | 100 | 24 | 933 | 933 | 63.9509798 | 63.9509798 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 936 | 258 | 76 | 11 | 0 | 63 | 100 | 24 | 936 | 936 | 63.95105719 | 63.95105719 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 943 | 266 | 77 | 11 | 0 | 63 | 101 | 24 | 943 | 943 | 63.95127439 | 63.95127439 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 994 | 294 | 77 | 10 | 0 | 65 | 104 | 27 | 994 | 994 | 63.9519919 | 63.9519919 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 300000 | SINGULAR | F->0 | SINGULAR:F->0 | 1081 | 381 | 85 | 10 | 0 | 64 | 111 | 26 | 1081 | 1081 | 63.95373817 | 63.95373817 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 1000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1483 | 782 | 99 | 11 | 0 | 67 | 130 | 31 | 1483 | 379 | 63.95771562 | 63.97939557 |
| scan --prec qd --mode conserve --fi 0.15 | 0.15 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 643 | 149 | 65 | 0 | 0 | 84 | 73 | 8 | 643 | 643 | 1.655110783e-06 | 1.655110783e-06 |
| scan --prec dd --mode conserve --fi 0.02 | 0.02 | 1 | SINGULAR | F->0 | SINGULAR:F->0 | 632 | 147 | 71 | 0 | 0 | 76 | 89 | 18 | 632 | 632 | 1.126952069e-06 | 1.126952069e-06 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1563 | 458 | 75 | 10 | 0 | 52 | 90 | 15 | 1563 | 1563 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 30000 | TINYSTEP |  | SINGULAR:a3->0 | 408 | 73 | 29 | 0 | 0 | 44 | 62 | 33 | 408 | 372 | - | 3.864651293 |
| scan --prec dd --mode conserve --fi 128. | 128 | -3000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1317 | 666 | 106 | 32 | 0 | 73 | 135 | 29 | 1317 | 374 | 127.9742308 | 127.9850717 |
| scan --prec dd --mode conserve --fi 128. | 128 | -1000000 | TINYSTEP |  | SINGULAR:a3->0 | 414 | 79 | 39 | 0 | 0 | 40 | 69 | 30 | 414 | 375 | - | 127.9866166 |
| scan --prec dd --mode conserve --fi 128. | 128 | 100000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 376 | 40 | 39 | 0 | 0 | 1 | 40 | 1 | 376 | 376 | 127.9872713 | 127.9872713 |

4. records whose stop is not the old rule's: 11 records

| file command (start) | F_inf | C | class | kind | base class:kind | steps | calls | real | Unresolved | nothing | pair | old real | locate not real while old real | stop step | old stop step | eta* | old eta* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| scan --prec dd --mode conserve --fi 2.0  | 2 | 10000 | TINYSTEP |  | SINGULAR:a3->0 | 415 | 74 | 19 | 0 | 0 | 55 | 54 | 35 | 415 | 378 | - | 1.723881779 |
| scan --prec dd --mode conserve --fi 12.0 | 12 | 100000 | SINGULAR | F->0 | SINGULAR:a3->0 | 2059 | 1184 | 86 | 11 | 0 | 68 | 118 | 32 | 2059 | 366 | 11.82837564 | 11.94329521 |
| scan --prec qd --mode conserve --fi 1.5  | 1.5 | 10000 | TINYSTEP |  | SINGULAR:a3->0 | 432 | 87 | 27 | 0 | 0 | 60 | 69 | 42 | 432 | 391 | - | 1.111951034 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 3974 | 2919 | 86 | 11 | 0 | 72 | 124 | 38 | 3974 | 369 | 4.621440417 | 4.887360434 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 300000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1682 | 903 | 86 | 11 | 0 | 70 | 120 | 34 | 1682 | 362 | 23.90645139 | 23.96419759 |
| scan --prec dd --mode conserve --fi 8.0  | 8 | 100000 | TINYSTEP |  | SINGULAR:a3->0 | 404 | 73 | 35 | 0 | 0 | 38 | 67 | 32 | 404 | 368 | - | 7.928774963 |
| scan --prec dd --mode conserve --fi -2.0 | -2 | -10000 | TINYSTEP |  | SINGULAR:a3->0 | 415 | 74 | 19 | 0 | 0 | 55 | 54 | 35 | 415 | 378 | - | 1.723881779 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 1000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1483 | 782 | 99 | 11 | 0 | 67 | 130 | 31 | 1483 | 379 | 63.95771562 | 63.97939557 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 30000 | TINYSTEP |  | SINGULAR:a3->0 | 408 | 73 | 29 | 0 | 0 | 44 | 62 | 33 | 408 | 372 | - | 3.864651293 |
| scan --prec dd --mode conserve --fi 128. | 128 | -3000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1317 | 666 | 106 | 32 | 0 | 73 | 135 | 29 | 1317 | 374 | 127.9742308 | 127.9850717 |
| scan --prec dd --mode conserve --fi 128. | 128 | -1000000 | TINYSTEP |  | SINGULAR:a3->0 | 414 | 79 | 39 | 0 | 0 | 40 | 69 | 30 | 414 | 375 | - | 127.9866166 |

5. eta* against the old rule's eta* on the same steps: 706 SINGULAR records with both; largest |difference| / max(1, eta*) 5.754e-02; above 1e-12: 5; above 1e-10: 5

  5.754e-02  F_inf 5.0 C [30000.0, 0.0]  eta* 4.6214404173726855  old 4.887360434025165  [scan --prec dd --mode conserve --fi 5.0 --c -100000000.0,-30]
  9.716e-03  F_inf 12.0 C [100000.0, 0.0]  eta* 11.828375635408252  old 11.94329521159453  [scan --prec dd --mode conserve --fi 12.0 --c -100000000.0,-3]
  2.416e-03  F_inf 24.0 C [300000.0, 0.0]  eta* 23.90645139482445  old 23.96419759302467  [scan --prec dd --mode conserve --fi 24.0 --c -100000000.0,-3]
  3.390e-04  F_inf 64.0 C [1000000.0, 0.0]  eta* 63.95771561796049  old 63.9793955680057  [scan --prec dd --mode conserve --fi 64.0 --c -100000000.0,-3]
  8.471e-05  F_inf 128.0 C [-3000000.0, 0.0]  eta* 127.97423084838282  old 127.98507168821324  [scan --prec dd --mode conserve --fi 128.0 --c -100000000.0,-]
  5.496e-15  F_inf 12.0 C [100000000.0, 0.0]  eta* 11.958225026476656  old 11.95822502647659  [scan --prec dd --mode conserve --fi 12.0 --c -100000000.0,-3]
  5.991e-16  F_inf 1.5 C [10000.0, 0.0]  eta* 1.111951033628728  old 1.1119510336287286  [scan --prec dd --mode conserve --fi 1.5 --c -100000000.0,-30]
  3.626e-16  F_inf 5.0 C [10000000.0, 0.0]  eta* 4.898914584932958  old 4.898914584932956  [scan --prec dd --mode conserve --fi 5.0 --c -100000000.0,-30]
