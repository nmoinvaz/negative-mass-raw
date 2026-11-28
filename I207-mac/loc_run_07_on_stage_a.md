records with a `loc` key: 5132

1. totals (records; records with calls of locate; with an Unresolved step; with a pair step; with no result at a step; SINGULAR records whose stop step differs from the old rule's; SINGULAR records the old rule would not have stopped by then)

| file kind | class | records | with calls | Unresolved | pair | nothing | stop step differs | old rule no stop |
|---|---|---|---|---|---|---|---|---|
| conical | FLOOR | 15 | 15 | 0 | 0 | 0 | 0 | 0 |
| conical | NONFINITE | 2 | 2 | 0 | 2 | 0 | 0 | 0 |
| conical | SINGULAR | 170 | 170 | 9 | 14 | 0 | 0 | 0 |
| offgrid | FLOOR | 1096 | 203 | 0 | 0 | 0 | 0 | 0 |
| offgrid | NOSTART | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
| offgrid | SINGULAR | 3818 | 3818 | 231 | 277 | 0 | 32 | 102 |
| offgrid | TINYSTEP | 25 | 25 | 0 | 25 | 0 | 0 | 0 |

2. records where locate said Unresolved or gave nothing at a gated step: 240 records

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
| scan --prec dd --mode conserve --fi 16.0 | 16 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 520 | 125 | 76 | 8 | 0 | 41 | 76 | 0 | 520 | 520 | 15.79501095 | 15.79501095 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 595 | 173 | 80 | 15 | 0 | 61 | 93 | 13 | 595 | 595 | 15.81421368 | 15.81421368 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 682 | 258 | 105 | 16 | 0 | 69 | 130 | 25 | 682 | 284 | 15.83865707 | 15.92525529 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 699 | 166 | 72 | 14 | 0 | 59 | 89 | 17 | 699 | 699 | 1.162043429 | 1.162043429 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 3000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1275 | 737 | 109 | 14 | 0 | 71 | 142 | 33 | 1275 | 285 | 1.201426408 | 1.708539646 |
| scan --prec dd --mode project --fi 4.0 - | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1738 | 582 | 75 | 10 | 0 | 52 | 90 | 15 | 1738 | 1738 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode conserve --fi 12.0 | 12 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 900 | 107 | 76 | 4 | 0 | 27 | 76 | 0 | 900 | 900 | 11.80758764 | 11.80758764 |
| scan --prec dd --mode conserve --fi 12.0 | 12 | 100000 | SINGULAR | F->0 | SINGULAR:a3->0 | 2059 | 1184 | 86 | 11 | 0 | 68 | 118 | 32 | 2059 | 366 | 11.82837564 | 11.94329521 |
| scan --prec dd --mode project --fi 24.0  | 24 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 935 | 149 | 76 | 11 | 0 | 43 | 80 | 4 | 935 | 935 | 23.89303019 | 23.89303019 |
| scan --prec dd --mode project --fi 24.0  | 24 | 300000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1891 | 1103 | 87 | 11 | 0 | 70 | 121 | 34 | 1891 | 362 | 23.90645139 | 23.96419759 |
| scan --prec dd --mode conserve --fi -3.0 | -3 | -10000 | SINGULAR | F->0 | SINGULAR:F->0 | 2941 | 1744 | 75 | 11 | 0 | 68 | 108 | 33 | 2941 | 2941 | 2.408310586 | 2.408310586 |
| scan --prec dd --mode conserve --fi 6.0  | 6 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 2375 | 1367 | 77 | 11 | 0 | 70 | 111 | 34 | 2375 | 2375 | 5.676108256 | 5.676108256 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -300000 | SINGULAR | F->0 | SINGULAR:F->0 | 853 | 153 | 76 | 12 | 0 | 48 | 83 | 7 | 853 | 853 | 63.94674087 | 63.94674087 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -100000 | SINGULAR | F->0 | SINGULAR:F->0 | 919 | 220 | 76 | 11 | 0 | 58 | 95 | 19 | 919 | 919 | 63.9497507 | 63.9497507 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -30000 | SINGULAR | F->0 | SINGULAR:F->0 | 944 | 244 | 76 | 12 | 0 | 61 | 98 | 22 | 944 | 944 | 63.95060498 | 63.95060498 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -10000 | SINGULAR | F->0 | SINGULAR:F->0 | 950 | 251 | 75 | 12 | 0 | 62 | 98 | 23 | 950 | 950 | 63.95083414 | 63.95083414 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -3000 | SINGULAR | F->0 | SINGULAR:F->0 | 953 | 255 | 76 | 11 | 0 | 63 | 100 | 24 | 953 | 953 | 63.95091289 | 63.95091289 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 956 | 257 | 76 | 10 | 0 | 63 | 100 | 24 | 956 | 956 | 63.95093525 | 63.95093525 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -300 | SINGULAR | F->0 | SINGULAR:F->0 | 955 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 955 | 955 | 63.95094307 | 63.95094307 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -100 | SINGULAR | F->0 | SINGULAR:F->0 | 955 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 955 | 955 | 63.9509453 | 63.9509453 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -30 | SINGULAR | F->0 | SINGULAR:F->0 | 956 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 956 | 956 | 63.95094608 | 63.95094608 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -10 | SINGULAR | F->0 | SINGULAR:F->0 | 955 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 955 | 955 | 63.9509463 | 63.9509463 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -3 | SINGULAR | F->0 | SINGULAR:F->0 | 955 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 955 | 955 | 63.95094638 | 63.95094638 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -1 | SINGULAR | F->0 | SINGULAR:F->0 | 956 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 956 | 956 | 63.9509464 | 63.9509464 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 0 | SINGULAR | F->0 | SINGULAR:F->0 | 955 | 254 | 75 | 10 | 0 | 63 | 99 | 24 | 955 | 955 | 63.95094641 | 63.95094641 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 1 | SINGULAR | F->0 | SINGULAR:F->0 | 956 | 257 | 76 | 10 | 0 | 63 | 100 | 24 | 956 | 956 | 63.95094642 | 63.95094642 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 3 | SINGULAR | F->0 | SINGULAR:F->0 | 955 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 955 | 955 | 63.95094645 | 63.95094645 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 955 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 955 | 955 | 63.95094652 | 63.95094652 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 30 | SINGULAR | F->0 | SINGULAR:F->0 | 956 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 956 | 956 | 63.95094675 | 63.95094675 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 100 | SINGULAR | F->0 | SINGULAR:F->0 | 956 | 257 | 76 | 10 | 0 | 63 | 100 | 24 | 956 | 956 | 63.95094753 | 63.95094753 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 300 | SINGULAR | F->0 | SINGULAR:F->0 | 955 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 955 | 955 | 63.95094976 | 63.95094976 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 956 | 257 | 76 | 10 | 0 | 63 | 100 | 24 | 956 | 956 | 63.95095756 | 63.95095756 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 956 | 255 | 75 | 11 | 0 | 63 | 99 | 24 | 956 | 956 | 63.9509798 | 63.9509798 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 959 | 261 | 76 | 11 | 0 | 63 | 100 | 24 | 959 | 959 | 63.95105719 | 63.95105719 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 966 | 267 | 77 | 11 | 0 | 63 | 101 | 24 | 966 | 966 | 63.95127439 | 63.95127439 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1017 | 294 | 77 | 10 | 0 | 65 | 104 | 27 | 1017 | 1017 | 63.9519919 | 63.9519919 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 300000 | SINGULAR | F->0 | SINGULAR:F->0 | 1103 | 380 | 85 | 10 | 0 | 64 | 111 | 26 | 1103 | 1103 | 63.95373817 | 63.95373817 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 1000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1508 | 783 | 99 | 11 | 0 | 67 | 130 | 31 | 1508 | 402 | 63.95771562 | 63.97939557 |
| scan --prec dd --mode conserve --fi 6.0  | 6 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 598 | 143 | 75 | 15 | 0 | 52 | 80 | 5 | 598 | 598 | 5.603075027 | 5.603075027 |
| scan --prec dd --mode conserve --fi 6.0  | 6 | 10000 | SINGULAR | F->0 | SINGULAR:a3->0 | 811 | 349 | 111 | 17 | 0 | 68 | 138 | 27 | 811 | 268 | 5.654148443 | 5.879711063 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1158 | 126 | 75 | 10 | 0 | 37 | 75 | 0 | 1158 | 1158 | 4.60350778 | 4.60350778 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 4000 | 2925 | 86 | 11 | 0 | 72 | 124 | 38 | 4000 | 392 | 4.621440417 | 4.887360434 |
| scan --prec dd --mode project --fi 12.0  | 12 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 918 | 107 | 76 | 4 | 0 | 27 | 76 | 0 | 918 | 918 | 11.80758764 | 11.80758764 |
| scan --prec dd --mode project --fi 12.0  | 12 | 100000 | SINGULAR | F->0 | SINGULAR:a3->0 | 2377 | 1482 | 86 | 11 | 0 | 68 | 118 | 32 | 2377 | 366 | 11.82837564 | 11.94329521 |
| scan --prec dd --mode project --fi 3.0 - | 3 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 3532 | 2273 | 75 | 11 | 0 | 68 | 108 | 33 | 3532 | 3532 | 2.408310586 | 2.408310586 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 878 | 130 | 76 | 12 | 0 | 39 | 76 | 0 | 878 | 878 | 31.91172367 | 31.91172367 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 300000 | SINGULAR | F->0 | SINGULAR:F->0 | 1205 | 440 | 80 | 10 | 0 | 66 | 108 | 28 | 1205 | 1205 | 31.92248282 | 31.92248282 |
| scan --prec dd --mode conserve --fi -5.0 | -5 | -10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1134 | 126 | 75 | 10 | 0 | 37 | 75 | 0 | 1134 | 1134 | 4.60350778 | 4.60350778 |
| scan --prec dd --mode conserve --fi -5.0 | -5 | -30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 3974 | 2919 | 86 | 11 | 0 | 72 | 124 | 38 | 3974 | 369 | 4.621440417 | 4.887360434 |
| scan --prec dd --mode project --fi 6.0 - | 6 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 2787 | 1739 | 79 | 11 | 0 | 68 | 111 | 32 | 2787 | 2787 | 5.676108256 | 5.676108256 |
| scan --prec dd --mode project --fi 128.0 | 128 | -3000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1426 | 774 | 106 | 22 | 0 | 85 | 135 | 29 | 1426 | 374 | 127.9742308 | 127.9850717 |
| scan --prec dd --mode conserve --fi 1.5  | 1.5 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 747 | 207 | 72 | 14 | 0 | 68 | 99 | 27 | 747 | 747 | 0.5442949715 | 0.5442949715 |
| scan --prec dd --mode conserve --fi 12.0 | 12 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 923 | 107 | 76 | 4 | 0 | 27 | 76 | 0 | 923 | 923 | 11.80758764 | 11.80758764 |
| scan --prec dd --mode conserve --fi 12.0 | 12 | 100000 | SINGULAR | F->0 | SINGULAR:a3->0 | 2082 | 1184 | 85 | 11 | 0 | 68 | 117 | 32 | 2082 | 389 | 11.82837564 | 11.94329521 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1134 | 126 | 75 | 10 | 0 | 37 | 75 | 0 | 1134 | 1134 | 4.60350778 | 4.60350778 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 3974 | 2919 | 86 | 11 | 0 | 72 | 124 | 38 | 3974 | 369 | 4.621440417 | 4.887360434 |
| scan --prec dd --mode conserve --fi 128. | 128 | -3000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1338 | 666 | 106 | 31 | 0 | 76 | 135 | 29 | 1338 | 397 | 127.9742308 | 127.9850717 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 913 | 137 | 75 | 11 | 0 | 43 | 79 | 4 | 913 | 913 | 23.89303019 | 23.89303019 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 300000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1682 | 903 | 86 | 11 | 0 | 70 | 120 | 34 | 1682 | 362 | 23.90645139 | 23.96419759 |
| scan --prec dd --mode conserve --fi 0.75 | 0.75 | 300 | SINGULAR | other | SINGULAR:other | 313 | 23 | 22 | 1 | 0 | 0 | 18 | 0 | 313 | 313 | 1.157378105e-06 | 1.157378098e-06 |
| scan --prec dd --mode conserve --fi 8.0  | 8 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 1320 | 375 | 76 | 12 | 0 | 54 | 93 | 17 | 1320 | 1320 | 7.74378012 | 7.74378012 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 710 | 184 | 74 | 15 | 0 | 65 | 97 | 23 | 710 | 710 | 3.490621782 | 3.490621782 |
| scan --prec dd --mode conserve --fi -16. | -16 | -100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1236 | 410 | 76 | 11 | 0 | 61 | 100 | 24 | 1236 | 1236 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi 3.0  | 3 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 2941 | 1744 | 75 | 11 | 0 | 68 | 108 | 33 | 2941 | 2941 | 2.408310586 | 2.408310586 |
| scan --prec dd --mode conserve --fi 3.0  | 3 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 2958 | 1736 | 75 | 11 | 0 | 68 | 108 | 33 | 2958 | 2958 | 2.408310586 | 2.408310586 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | -30000 | SINGULAR | F->0 | SINGULAR:F->0 | 583 | 204 | 94 | 14 | 0 | 62 | 107 | 13 | 583 | 583 | 31.8886427 | 31.8886427 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | -10000 | SINGULAR | F->0 | SINGULAR:F->0 | 608 | 228 | 100 | 19 | 0 | 61 | 119 | 19 | 608 | 608 | 31.89479941 | 31.89479941 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | -3000 | SINGULAR | F->0 | SINGULAR:F->0 | 616 | 236 | 104 | 18 | 0 | 62 | 123 | 19 | 616 | 616 | 31.89657033 | 31.89657033 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 618 | 238 | 105 | 16 | 0 | 63 | 124 | 19 | 618 | 618 | 31.89704716 | 31.89704716 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | -300 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 239 | 105 | 19 | 0 | 61 | 124 | 19 | 619 | 619 | 31.89721119 | 31.89721119 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | -100 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 238 | 104 | 19 | 0 | 62 | 123 | 19 | 619 | 619 | 31.89725779 | 31.89725779 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | -30 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 238 | 104 | 19 | 0 | 62 | 123 | 19 | 619 | 619 | 31.89727408 | 31.89727408 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | -10 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 238 | 104 | 19 | 0 | 62 | 123 | 19 | 619 | 619 | 31.89727873 | 31.89727873 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | -3 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 238 | 104 | 19 | 0 | 62 | 123 | 19 | 619 | 619 | 31.89728035 | 31.89728035 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | -1 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 238 | 104 | 19 | 0 | 62 | 123 | 19 | 619 | 619 | 31.89728082 | 31.89728082 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 0 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 238 | 104 | 19 | 0 | 62 | 123 | 19 | 619 | 619 | 31.89728105 | 31.89728105 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 1 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 238 | 104 | 19 | 0 | 62 | 123 | 19 | 619 | 619 | 31.89728128 | 31.89728128 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 3 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 238 | 104 | 19 | 0 | 62 | 123 | 19 | 619 | 619 | 31.89728175 | 31.89728175 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 238 | 104 | 19 | 0 | 62 | 123 | 19 | 619 | 619 | 31.89728337 | 31.89728337 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 30 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 239 | 104 | 19 | 0 | 62 | 123 | 19 | 619 | 619 | 31.89728802 | 31.89728802 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 100 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 239 | 104 | 19 | 0 | 62 | 123 | 19 | 619 | 619 | 31.89730428 | 31.89730428 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 300 | SINGULAR | F->0 | SINGULAR:F->0 | 620 | 240 | 105 | 19 | 0 | 62 | 124 | 19 | 620 | 620 | 31.89735064 | 31.89735064 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 620 | 240 | 106 | 17 | 0 | 62 | 125 | 19 | 620 | 620 | 31.897512 | 31.897512 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 3000 | SINGULAR | F->0 | SINGULAR:a3->0 | 622 | 242 | 106 | 18 | 0 | 62 | 126 | 20 | 622 | 280 | 31.89796534 | 31.94134069 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 10000 | SINGULAR | F->0 | SINGULAR:a3->0 | 630 | 249 | 108 | 17 | 0 | 64 | 128 | 20 | 630 | 279 | 31.89946777 | 31.94284122 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 650 | 268 | 113 | 18 | 0 | 65 | 136 | 23 | 650 | 279 | 31.90315561 | 31.94652425 |
| scan --prec dd --mode conserve --fi -64. | -64 | 300000 | SINGULAR | F->0 | SINGULAR:F->0 | 830 | 154 | 76 | 12 | 0 | 48 | 83 | 7 | 830 | 830 | 63.94674087 | 63.94674087 |
| scan --prec dd --mode conserve --fi -64. | -64 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 895 | 218 | 76 | 11 | 0 | 58 | 95 | 19 | 895 | 895 | 63.9497507 | 63.9497507 |
| scan --prec dd --mode conserve --fi -64. | -64 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 921 | 244 | 76 | 12 | 0 | 61 | 98 | 22 | 921 | 921 | 63.95060498 | 63.95060498 |
| scan --prec dd --mode conserve --fi -64. | -64 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 927 | 251 | 75 | 12 | 0 | 62 | 98 | 23 | 927 | 927 | 63.95083414 | 63.95083414 |
| scan --prec dd --mode conserve --fi -64. | -64 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 930 | 253 | 75 | 11 | 0 | 63 | 99 | 24 | 930 | 930 | 63.95091289 | 63.95091289 |
| scan --prec dd --mode conserve --fi -64. | -64 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95093525 | 63.95093525 |
| scan --prec dd --mode conserve --fi -64. | -64 | 300 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094307 | 63.95094307 |
| scan --prec dd --mode conserve --fi -64. | -64 | 100 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.9509453 | 63.9509453 |
| scan --prec dd --mode conserve --fi -64. | -64 | 30 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094608 | 63.95094608 |
| scan --prec dd --mode conserve --fi -64. | -64 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.9509463 | 63.9509463 |
| scan --prec dd --mode conserve --fi -64. | -64 | 3 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.95094638 | 63.95094638 |
| scan --prec dd --mode conserve --fi -64. | -64 | 1 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 258 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.9509464 | 63.9509464 |
| scan --prec dd --mode conserve --fi -64. | -64 | 0 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 256 | 75 | 10 | 0 | 63 | 99 | 24 | 932 | 932 | 63.95094641 | 63.95094641 |
| scan --prec dd --mode conserve --fi -64. | -64 | -1 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.95094642 | 63.95094642 |
| scan --prec dd --mode conserve --fi -64. | -64 | -3 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.95094645 | 63.95094645 |
| scan --prec dd --mode conserve --fi -64. | -64 | -10 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094652 | 63.95094652 |
| scan --prec dd --mode conserve --fi -64. | -64 | -30 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094675 | 63.95094675 |
| scan --prec dd --mode conserve --fi -64. | -64 | -100 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094753 | 63.95094753 |
| scan --prec dd --mode conserve --fi -64. | -64 | -300 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094976 | 63.95094976 |
| scan --prec dd --mode conserve --fi -64. | -64 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 255 | 75 | 10 | 0 | 63 | 99 | 24 | 932 | 932 | 63.95095756 | 63.95095756 |
| scan --prec dd --mode conserve --fi -64. | -64 | -3000 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 257 | 76 | 11 | 0 | 63 | 100 | 24 | 933 | 933 | 63.9509798 | 63.9509798 |
| scan --prec dd --mode conserve --fi -64. | -64 | -10000 | SINGULAR | F->0 | SINGULAR:F->0 | 936 | 258 | 76 | 11 | 0 | 63 | 100 | 24 | 936 | 936 | 63.95105719 | 63.95105719 |
| scan --prec dd --mode conserve --fi -64. | -64 | -30000 | SINGULAR | F->0 | SINGULAR:F->0 | 943 | 266 | 77 | 11 | 0 | 63 | 101 | 24 | 943 | 943 | 63.95127439 | 63.95127439 |
| scan --prec dd --mode conserve --fi -64. | -64 | -100000 | SINGULAR | F->0 | SINGULAR:F->0 | 994 | 294 | 77 | 10 | 0 | 65 | 104 | 27 | 994 | 994 | 63.9519919 | 63.9519919 |
| scan --prec dd --mode conserve --fi -64. | -64 | -300000 | SINGULAR | F->0 | SINGULAR:F->0 | 1081 | 381 | 85 | 10 | 0 | 64 | 111 | 26 | 1081 | 1081 | 63.95373817 | 63.95373817 |
| scan --prec dd --mode conserve --fi -64. | -64 | -1000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1483 | 782 | 99 | 11 | 0 | 67 | 130 | 31 | 1483 | 379 | 63.95771562 | 63.97939557 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 636 | 168 | 75 | 19 | 0 | 60 | 93 | 18 | 636 | 636 | 4.55827794 | 4.55827794 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 855 | 129 | 75 | 12 | 0 | 39 | 75 | 0 | 855 | 855 | 31.91172367 | 31.91172367 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 300000 | SINGULAR | F->0 | SINGULAR:F->0 | 1180 | 438 | 80 | 10 | 0 | 66 | 108 | 28 | 1180 | 1180 | 31.92248282 | 31.92248282 |
| scan --prec dd --mode conserve --fi -8.0 | -8 | -30000 | SINGULAR | F->0 | SINGULAR:F->0 | 1320 | 375 | 76 | 12 | 0 | 54 | 93 | 17 | 1320 | 1320 | 7.74378012 | 7.74378012 |
| scan --prec dd --mode conserve --fi 8.0  | 8 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 545 | 110 | 76 | 2 | 0 | 32 | 76 | 0 | 545 | 545 | 7.66136651 | 7.66136651 |
| scan --prec dd --mode conserve --fi 8.0  | 8 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 678 | 235 | 95 | 18 | 0 | 67 | 120 | 25 | 678 | 678 | 7.715408871 | 7.715408871 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1236 | 410 | 76 | 11 | 0 | 61 | 100 | 24 | 1236 | 1236 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1588 | 457 | 75 | 10 | 0 | 52 | 90 | 15 | 1588 | 1588 | 3.527557745 | 3.527557745 |
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
| scan --prec dd --mode conserve --fi 3.0  | 3 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 626 | 105 | 74 | 3 | 0 | 28 | 74 | 0 | 626 | 626 | 2.321748788 | 2.321748788 |
| scan --prec dd --mode conserve --fi 3.0  | 3 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 840 | 309 | 91 | 18 | 0 | 69 | 119 | 28 | 840 | 840 | 2.381267496 | 2.381267496 |
| scan --prec dd --mode conserve --fi -12. | -12 | -30000 | SINGULAR | F->0 | SINGULAR:F->0 | 900 | 107 | 76 | 4 | 0 | 27 | 76 | 0 | 900 | 900 | 11.80758764 | 11.80758764 |
| scan --prec dd --mode conserve --fi -12. | -12 | -100000 | SINGULAR | F->0 | SINGULAR:a3->0 | 2059 | 1184 | 86 | 11 | 0 | 68 | 118 | 32 | 2059 | 366 | 11.82837564 | 11.94329521 |
| scan --prec dd --mode project --fi 16.0  | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1327 | 485 | 76 | 11 | 0 | 61 | 100 | 24 | 1327 | 1327 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi -2.0 | -2 | -3000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1275 | 737 | 109 | 14 | 0 | 71 | 142 | 33 | 1275 | 285 | 1.201426408 | 1.708539646 |
| scan --prec dd --mode conserve --fi -2.0 | -2 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 699 | 166 | 72 | 14 | 0 | 59 | 89 | 17 | 699 | 699 | 1.162043429 | 1.162043429 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | -10000 | SINGULAR | F->0 | SINGULAR:F->0 | 544 | 149 | 76 | 16 | 0 | 55 | 82 | 6 | 544 | 544 | 23.84994339 | 23.84994339 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | -3000 | SINGULAR | F->0 | SINGULAR:F->0 | 569 | 173 | 82 | 19 | 0 | 56 | 93 | 11 | 569 | 569 | 23.85729041 | 23.85729041 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 575 | 179 | 86 | 17 | 0 | 57 | 96 | 10 | 575 | 575 | 23.85907098 | 23.85907098 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | -300 | SINGULAR | F->0 | SINGULAR:F->0 | 577 | 180 | 85 | 17 | 0 | 58 | 96 | 11 | 577 | 577 | 23.85966658 | 23.85966658 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | -100 | SINGULAR | F->0 | SINGULAR:F->0 | 578 | 182 | 86 | 17 | 0 | 58 | 98 | 12 | 578 | 578 | 23.85983425 | 23.85983425 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | -30 | SINGULAR | F->0 | SINGULAR:F->0 | 578 | 182 | 86 | 17 | 0 | 58 | 98 | 12 | 578 | 578 | 23.85989268 | 23.85989268 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | -10 | SINGULAR | F->0 | SINGULAR:F->0 | 578 | 182 | 86 | 17 | 0 | 58 | 98 | 12 | 578 | 578 | 23.85990935 | 23.85990935 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | -3 | SINGULAR | F->0 | SINGULAR:F->0 | 578 | 182 | 86 | 17 | 0 | 58 | 98 | 12 | 578 | 578 | 23.85991518 | 23.85991518 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | -1 | SINGULAR | F->0 | SINGULAR:F->0 | 578 | 182 | 86 | 17 | 0 | 58 | 98 | 12 | 578 | 578 | 23.85991685 | 23.85991685 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 0 | SINGULAR | F->0 | SINGULAR:F->0 | 578 | 182 | 86 | 17 | 0 | 58 | 98 | 12 | 578 | 578 | 23.85991768 | 23.85991768 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 1 | SINGULAR | F->0 | SINGULAR:F->0 | 578 | 182 | 86 | 17 | 0 | 58 | 98 | 12 | 578 | 578 | 23.85991852 | 23.85991852 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 3 | SINGULAR | F->0 | SINGULAR:F->0 | 578 | 182 | 86 | 17 | 0 | 58 | 98 | 12 | 578 | 578 | 23.85992018 | 23.85992018 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 578 | 182 | 86 | 17 | 0 | 58 | 98 | 12 | 578 | 578 | 23.85992601 | 23.85992601 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 30 | SINGULAR | F->0 | SINGULAR:F->0 | 578 | 182 | 86 | 17 | 0 | 58 | 98 | 12 | 578 | 578 | 23.85994266 | 23.85994266 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 100 | SINGULAR | F->0 | SINGULAR:F->0 | 578 | 182 | 86 | 17 | 0 | 58 | 98 | 12 | 578 | 578 | 23.86000084 | 23.86000084 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 300 | SINGULAR | F->0 | SINGULAR:F->0 | 579 | 183 | 87 | 17 | 0 | 58 | 98 | 11 | 579 | 579 | 23.86016636 | 23.86016636 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 581 | 184 | 86 | 17 | 0 | 59 | 98 | 12 | 581 | 581 | 23.86073735 | 23.86073735 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 585 | 188 | 87 | 15 | 0 | 60 | 100 | 13 | 585 | 585 | 23.86230099 | 23.86230099 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 603 | 206 | 93 | 19 | 0 | 59 | 109 | 16 | 603 | 603 | 23.867097 | 23.867097 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 642 | 244 | 105 | 18 | 0 | 64 | 126 | 21 | 642 | 281 | 23.87689777 | 23.93471435 |
| scan --prec dd --mode project --fi 64.0  | 64 | -300000 | SINGULAR | F->0 | SINGULAR:F->0 | 841 | 163 | 76 | 12 | 0 | 51 | 83 | 7 | 841 | 841 | 63.94674087 | 63.94674087 |
| scan --prec dd --mode project --fi 64.0  | 64 | -100000 | SINGULAR | F->0 | SINGULAR:F->0 | 918 | 237 | 76 | 11 | 0 | 59 | 95 | 19 | 918 | 918 | 63.9497507 | 63.9497507 |
| scan --prec dd --mode project --fi 64.0  | 64 | -30000 | SINGULAR | F->0 | SINGULAR:F->0 | 948 | 268 | 76 | 12 | 0 | 63 | 98 | 22 | 948 | 948 | 63.95060498 | 63.95060498 |
| scan --prec dd --mode project --fi 64.0  | 64 | -10000 | SINGULAR | F->0 | SINGULAR:F->0 | 957 | 277 | 76 | 12 | 0 | 64 | 99 | 23 | 957 | 957 | 63.95083414 | 63.95083414 |
| scan --prec dd --mode project --fi 64.0  | 64 | -3000 | SINGULAR | F->0 | SINGULAR:F->0 | 959 | 279 | 76 | 11 | 0 | 64 | 100 | 24 | 959 | 959 | 63.95091289 | 63.95091289 |
| scan --prec dd --mode project --fi 64.0  | 64 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 960 | 281 | 76 | 10 | 0 | 63 | 100 | 24 | 960 | 960 | 63.95093525 | 63.95093525 |
| scan --prec dd --mode project --fi 64.0  | 64 | -300 | SINGULAR | F->0 | SINGULAR:F->0 | 960 | 279 | 76 | 10 | 0 | 63 | 100 | 24 | 960 | 960 | 63.95094307 | 63.95094307 |
| scan --prec dd --mode project --fi 64.0  | 64 | -100 | SINGULAR | F->0 | SINGULAR:F->0 | 960 | 279 | 76 | 10 | 0 | 63 | 100 | 24 | 960 | 960 | 63.9509453 | 63.9509453 |
| scan --prec dd --mode project --fi 64.0  | 64 | -30 | SINGULAR | F->0 | SINGULAR:F->0 | 961 | 281 | 76 | 10 | 0 | 65 | 100 | 24 | 961 | 961 | 63.95094608 | 63.95094608 |
| scan --prec dd --mode project --fi 64.0  | 64 | -10 | SINGULAR | F->0 | SINGULAR:F->0 | 960 | 281 | 75 | 10 | 0 | 63 | 99 | 24 | 960 | 960 | 63.9509463 | 63.9509463 |
| scan --prec dd --mode project --fi 64.0  | 64 | -3 | SINGULAR | F->0 | SINGULAR:F->0 | 961 | 281 | 76 | 10 | 0 | 63 | 100 | 24 | 961 | 961 | 63.95094638 | 63.95094638 |
| scan --prec dd --mode project --fi 64.0  | 64 | -1 | SINGULAR | F->0 | SINGULAR:F->0 | 962 | 283 | 76 | 10 | 0 | 63 | 100 | 24 | 962 | 962 | 63.9509464 | 63.9509464 |
| scan --prec dd --mode project --fi 64.0  | 64 | 0 | SINGULAR | F->0 | SINGULAR:F->0 | 960 | 279 | 75 | 10 | 0 | 63 | 99 | 24 | 960 | 960 | 63.95094641 | 63.95094641 |
| scan --prec dd --mode project --fi 64.0  | 64 | 1 | SINGULAR | F->0 | SINGULAR:F->0 | 960 | 278 | 75 | 10 | 0 | 65 | 99 | 24 | 960 | 960 | 63.95094642 | 63.95094642 |
| scan --prec dd --mode project --fi 64.0  | 64 | 3 | SINGULAR | F->0 | SINGULAR:F->0 | 962 | 281 | 76 | 10 | 0 | 63 | 100 | 24 | 962 | 962 | 63.95094645 | 63.95094645 |
| scan --prec dd --mode project --fi 64.0  | 64 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 961 | 280 | 76 | 10 | 0 | 64 | 100 | 24 | 961 | 961 | 63.95094652 | 63.95094652 |
| scan --prec dd --mode project --fi 64.0  | 64 | 30 | SINGULAR | F->0 | SINGULAR:F->0 | 961 | 280 | 76 | 10 | 0 | 63 | 100 | 24 | 961 | 961 | 63.95094675 | 63.95094675 |
| scan --prec dd --mode project --fi 64.0  | 64 | 100 | SINGULAR | F->0 | SINGULAR:F->0 | 961 | 280 | 76 | 10 | 0 | 63 | 100 | 24 | 961 | 961 | 63.95094753 | 63.95094753 |
| scan --prec dd --mode project --fi 64.0  | 64 | 300 | SINGULAR | F->0 | SINGULAR:F->0 | 961 | 281 | 76 | 10 | 0 | 63 | 100 | 24 | 961 | 961 | 63.95094976 | 63.95094976 |
| scan --prec dd --mode project --fi 64.0  | 64 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 960 | 281 | 76 | 10 | 0 | 63 | 100 | 24 | 960 | 960 | 63.95095756 | 63.95095756 |
| scan --prec dd --mode project --fi 64.0  | 64 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 962 | 282 | 76 | 11 | 0 | 64 | 100 | 24 | 962 | 962 | 63.9509798 | 63.9509798 |
| scan --prec dd --mode project --fi 64.0  | 64 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 965 | 284 | 75 | 11 | 0 | 63 | 99 | 24 | 965 | 965 | 63.95105719 | 63.95105719 |
| scan --prec dd --mode project --fi 64.0  | 64 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 975 | 295 | 77 | 11 | 0 | 65 | 101 | 24 | 975 | 975 | 63.95127439 | 63.95127439 |
| scan --prec dd --mode project --fi 64.0  | 64 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1029 | 325 | 77 | 10 | 0 | 68 | 104 | 27 | 1029 | 1029 | 63.9519919 | 63.9519919 |
| scan --prec dd --mode project --fi 64.0  | 64 | 300000 | SINGULAR | F->0 | SINGULAR:F->0 | 1136 | 432 | 86 | 10 | 0 | 65 | 112 | 26 | 1136 | 1136 | 63.95373817 | 63.95373817 |
| scan --prec dd --mode project --fi 64.0  | 64 | 1000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1637 | 930 | 98 | 11 | 0 | 67 | 129 | 31 | 1637 | 379 | 63.95771562 | 63.97939557 |
| scan --prec dd --mode project --fi 8.0 - | 8 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 1430 | 459 | 76 | 12 | 0 | 54 | 93 | 17 | 1430 | 1430 | 7.74378012 | 7.74378012 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1134 | 126 | 75 | 10 | 0 | 37 | 75 | 0 | 1134 | 1134 | 4.60350778 | 4.60350778 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 13335.21432 | SINGULAR | F->0 | SINGULAR:F->0 | 1405 | 350 | 75 | 10 | 0 | 50 | 88 | 13 | 1405 | 1405 | 4.609750889 | 4.609750889 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 17782.7941 | SINGULAR | F->0 | SINGULAR:F->0 | 1880 | 830 | 75 | 10 | 0 | 62 | 101 | 26 | 1880 | 1880 | 4.614769523 | 4.614769523 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 23713.73706 | SINGULAR | F->0 | SINGULAR:F->0 | 2751 | 1696 | 80 | 10 | 0 | 69 | 113 | 33 | 2751 | 2751 | 4.618780509 | 4.618780509 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 31622.7766 | SINGULAR | F->0 | SINGULAR:a3->0 | 4344 | 3291 | 89 | 11 | 0 | 71 | 126 | 37 | 4344 | 369 | 4.621970366 | 4.887866457 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 42169.65034 | SINGULAR | F->0 | SINGULAR:F->0 | 861 | 103 | 75 | 1 | 0 | 27 | 75 | 0 | 861 | 861 | 15.84596646 | 15.84596646 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 56234.13252 | SINGULAR | F->0 | SINGULAR:F->0 | 934 | 129 | 76 | 11 | 0 | 38 | 76 | 0 | 934 | 934 | 15.85164729 | 15.85164729 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 74989.42093 | SINGULAR | F->0 | SINGULAR:F->0 | 1045 | 216 | 76 | 10 | 0 | 50 | 88 | 12 | 1045 | 1045 | 15.85675999 | 15.85675999 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1236 | 410 | 76 | 11 | 0 | 61 | 100 | 24 | 1236 | 1236 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 133352.1432 | SINGULAR | F->0 | SINGULAR:F->0 | 1562 | 736 | 79 | 11 | 0 | 69 | 111 | 32 | 1562 | 1562 | 15.86512546 | 15.86512546 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 177827.941 | SINGULAR | F->0 | SINGULAR:a3->0 | 2136 | 1308 | 91 | 11 | 0 | 68 | 124 | 33 | 2136 | 363 | 15.86840232 | 15.95484213 |
| scan --prec dd --mode conserve --fi -4.0 | -4 | -10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1563 | 458 | 75 | 10 | 0 | 52 | 90 | 15 | 1563 | 1563 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode conserve --fi -128 | -128 | 3000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1317 | 666 | 106 | 32 | 0 | 73 | 135 | 29 | 1317 | 374 | 127.9742308 | 127.9850717 |
| scan --prec dd --mode project --fi 32.0  | 32 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 868 | 130 | 76 | 12 | 0 | 39 | 76 | 0 | 868 | 868 | 31.91172367 | 31.91172367 |
| scan --prec dd --mode project --fi 32.0  | 32 | 300000 | SINGULAR | F->0 | SINGULAR:F->0 | 1259 | 509 | 80 | 10 | 0 | 66 | 108 | 28 | 1259 | 1259 | 31.92248282 | 31.92248282 |
| scan --prec dd --mode conserve --fi -32. | -32 | -100000 | SINGULAR | F->0 | SINGULAR:F->0 | 855 | 129 | 75 | 12 | 0 | 39 | 75 | 0 | 855 | 855 | 31.91172367 | 31.91172367 |
| scan --prec dd --mode conserve --fi -32. | -32 | -300000 | SINGULAR | F->0 | SINGULAR:F->0 | 1180 | 438 | 80 | 10 | 0 | 66 | 108 | 28 | 1180 | 1180 | 31.92248282 | 31.92248282 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1259 | 409 | 76 | 11 | 0 | 61 | 100 | 24 | 1259 | 1259 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi 8.0  | 8 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 1342 | 374 | 75 | 12 | 0 | 54 | 92 | 17 | 1342 | 1342 | 7.74378012 | 7.74378012 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1563 | 458 | 75 | 10 | 0 | 52 | 90 | 15 | 1563 | 1563 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode conserve --fi 6.0  | 6 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 2397 | 1364 | 78 | 11 | 0 | 69 | 111 | 33 | 2397 | 2397 | 5.676108256 | 5.676108256 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 935 | 139 | 76 | 11 | 0 | 43 | 80 | 4 | 935 | 935 | 23.89303019 | 23.89303019 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 300000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1707 | 908 | 87 | 11 | 0 | 70 | 121 | 34 | 1707 | 384 | 23.90645139 | 23.96419759 |
| scan --prec dd --mode project --fi 5.0 - | 5 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1198 | 126 | 75 | 10 | 0 | 37 | 75 | 0 | 1198 | 1198 | 4.60350778 | 4.60350778 |
| scan --prec dd --mode project --fi 5.0 - | 5 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 4916 | 3818 | 86 | 11 | 0 | 72 | 124 | 38 | 4916 | 369 | 4.621440417 | 4.887360434 |
| scan --prec dd --mode conserve --fi 12.0 | 12 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 598 | 182 | 82 | 20 | 0 | 59 | 99 | 17 | 598 | 598 | 11.77626991 | 11.77626991 |
| scan --prec dd --mode conserve --fi 12.0 | 12 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 773 | 330 | 116 | 19 | 0 | 67 | 143 | 27 | 773 | 287 | 11.80758764 | 11.9227013 |
| scan --prec dd --mode conserve --fi -6.0 | -6 | -30000 | SINGULAR | F->0 | SINGULAR:F->0 | 2375 | 1367 | 77 | 11 | 0 | 70 | 111 | 34 | 2375 | 2375 | 5.676108256 | 5.676108256 |
| scan --prec dd --mode conserve --fi -24. | -24 | -100000 | SINGULAR | F->0 | SINGULAR:F->0 | 913 | 137 | 75 | 11 | 0 | 43 | 79 | 4 | 913 | 913 | 23.89303019 | 23.89303019 |
| scan --prec dd --mode conserve --fi -24. | -24 | -300000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1682 | 903 | 86 | 11 | 0 | 70 | 120 | 34 | 1682 | 362 | 23.90645139 | 23.96419759 |
| scan --prec dd --mode conserve --fi 128. | 128 | -3000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1317 | 666 | 106 | 32 | 0 | 73 | 135 | 29 | 1317 | 374 | 127.9742308 | 127.9850717 |

3. records where locate read a pair at a gated step: 318 records

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
| scan --prec dd --mode conserve --fi 16.0 | 16 | -300 | SINGULAR | F->0 | SINGULAR:F->0 | 483 | 85 | 76 | 0 | 0 | 9 | 76 | 0 | 483 | 483 | 15.78033551 | 15.78033551 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | -100 | SINGULAR | F->0 | SINGULAR:F->0 | 485 | 90 | 75 | 0 | 0 | 15 | 75 | 0 | 485 | 485 | 15.78139717 | 15.78139717 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | -30 | SINGULAR | F->0 | SINGULAR:F->0 | 486 | 91 | 76 | 0 | 0 | 15 | 76 | 0 | 486 | 486 | 15.7817624 | 15.7817624 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | -10 | SINGULAR | F->0 | SINGULAR:F->0 | 486 | 90 | 75 | 0 | 0 | 15 | 75 | 0 | 486 | 486 | 15.78186616 | 15.78186616 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | -3 | SINGULAR | F->0 | SINGULAR:F->0 | 486 | 90 | 75 | 0 | 0 | 15 | 75 | 0 | 486 | 486 | 15.78190242 | 15.78190242 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | -1 | SINGULAR | F->0 | SINGULAR:F->0 | 486 | 91 | 75 | 0 | 0 | 16 | 75 | 0 | 486 | 486 | 15.78191277 | 15.78191277 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 0 | SINGULAR | F->0 | SINGULAR:F->0 | 486 | 91 | 75 | 0 | 0 | 16 | 75 | 0 | 486 | 486 | 15.78191794 | 15.78191794 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 1 | SINGULAR | F->0 | SINGULAR:F->0 | 486 | 91 | 75 | 0 | 0 | 16 | 75 | 0 | 486 | 486 | 15.78192312 | 15.78192312 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 3 | SINGULAR | F->0 | SINGULAR:F->0 | 486 | 91 | 75 | 0 | 0 | 16 | 75 | 0 | 486 | 486 | 15.78193347 | 15.78193347 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 487 | 93 | 76 | 0 | 0 | 17 | 76 | 0 | 487 | 487 | 15.78196966 | 15.78196966 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 30 | SINGULAR | F->0 | SINGULAR:F->0 | 487 | 93 | 76 | 0 | 0 | 17 | 76 | 0 | 487 | 487 | 15.7820729 | 15.7820729 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100 | SINGULAR | F->0 | SINGULAR:F->0 | 488 | 94 | 76 | 0 | 0 | 18 | 76 | 0 | 488 | 488 | 15.7824322 | 15.7824322 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 300 | SINGULAR | F->0 | SINGULAR:F->0 | 490 | 96 | 76 | 0 | 0 | 20 | 76 | 0 | 490 | 490 | 15.78344167 | 15.78344167 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 498 | 104 | 75 | 0 | 0 | 29 | 75 | 0 | 498 | 498 | 15.78678799 | 15.78678799 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 520 | 125 | 76 | 8 | 0 | 41 | 76 | 0 | 520 | 520 | 15.79501095 | 15.79501095 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 595 | 173 | 80 | 15 | 0 | 61 | 93 | 13 | 595 | 595 | 15.81421368 | 15.81421368 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 682 | 258 | 105 | 16 | 0 | 69 | 130 | 25 | 682 | 284 | 15.83865707 | 15.92525529 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 699 | 166 | 72 | 14 | 0 | 59 | 89 | 17 | 699 | 699 | 1.162043429 | 1.162043429 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 3000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1275 | 737 | 109 | 14 | 0 | 71 | 142 | 33 | 1275 | 285 | 1.201426408 | 1.708539646 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 10000 | TINYSTEP |  | SINGULAR:a3->0 | 415 | 74 | 19 | 0 | 0 | 55 | 54 | 35 | 415 | 378 | - | 1.723881779 |
| scan --prec dd --mode project --fi 4.0 - | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1738 | 582 | 75 | 10 | 0 | 52 | 90 | 15 | 1738 | 1738 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode project --fi 4.0 - | 4 | 30000 | TINYSTEP |  | SINGULAR:a3->0 | 408 | 73 | 28 | 0 | 0 | 45 | 62 | 34 | 408 | 372 | - | 3.864651293 |
| scan --prec dd --mode project --fi 0.15  | 0.15 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 606 | 130 | 71 | 0 | 0 | 59 | 81 | 10 | 606 | 606 | 1.655110783e-06 | 1.655110783e-06 |
| scan --prec dd --mode conserve --fi 12.0 | 12 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 900 | 107 | 76 | 4 | 0 | 27 | 76 | 0 | 900 | 900 | 11.80758764 | 11.80758764 |
| scan --prec dd --mode conserve --fi 12.0 | 12 | 100000 | SINGULAR | F->0 | SINGULAR:a3->0 | 2059 | 1184 | 86 | 11 | 0 | 68 | 118 | 32 | 2059 | 366 | 11.82837564 | 11.94329521 |
| scan --prec dd --mode project --fi 24.0  | 24 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 935 | 149 | 76 | 11 | 0 | 43 | 80 | 4 | 935 | 935 | 23.89303019 | 23.89303019 |
| scan --prec dd --mode project --fi 24.0  | 24 | 300000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1891 | 1103 | 87 | 11 | 0 | 70 | 121 | 34 | 1891 | 362 | 23.90645139 | 23.96419759 |
| scan --prec dd --mode conserve --fi -3.0 | -3 | -10000 | SINGULAR | F->0 | SINGULAR:F->0 | 2941 | 1744 | 75 | 11 | 0 | 68 | 108 | 33 | 2941 | 2941 | 2.408310586 | 2.408310586 |
| scan --prec dd --mode conserve --fi 6.0  | 6 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 937 | 98 | 75 | 0 | 0 | 23 | 75 | 0 | 937 | 937 | 5.654148443 | 5.654148443 |
| scan --prec dd --mode conserve --fi 6.0  | 6 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 2375 | 1367 | 77 | 11 | 0 | 70 | 111 | 34 | 2375 | 2375 | 5.676108256 | 5.676108256 |
| scan --prec dd --mode project --fi 0.02  | 0.02 | 1 | SINGULAR | F->0 | SINGULAR:F->0 | 632 | 147 | 71 | 0 | 0 | 76 | 89 | 18 | 632 | 632 | 1.126952069e-06 | 1.126952069e-06 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -300000 | SINGULAR | F->0 | SINGULAR:F->0 | 853 | 153 | 76 | 12 | 0 | 48 | 83 | 7 | 853 | 853 | 63.94674087 | 63.94674087 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -100000 | SINGULAR | F->0 | SINGULAR:F->0 | 919 | 220 | 76 | 11 | 0 | 58 | 95 | 19 | 919 | 919 | 63.9497507 | 63.9497507 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -30000 | SINGULAR | F->0 | SINGULAR:F->0 | 944 | 244 | 76 | 12 | 0 | 61 | 98 | 22 | 944 | 944 | 63.95060498 | 63.95060498 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -10000 | SINGULAR | F->0 | SINGULAR:F->0 | 950 | 251 | 75 | 12 | 0 | 62 | 98 | 23 | 950 | 950 | 63.95083414 | 63.95083414 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -3000 | SINGULAR | F->0 | SINGULAR:F->0 | 953 | 255 | 76 | 11 | 0 | 63 | 100 | 24 | 953 | 953 | 63.95091289 | 63.95091289 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 956 | 257 | 76 | 10 | 0 | 63 | 100 | 24 | 956 | 956 | 63.95093525 | 63.95093525 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -300 | SINGULAR | F->0 | SINGULAR:F->0 | 955 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 955 | 955 | 63.95094307 | 63.95094307 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -100 | SINGULAR | F->0 | SINGULAR:F->0 | 955 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 955 | 955 | 63.9509453 | 63.9509453 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -30 | SINGULAR | F->0 | SINGULAR:F->0 | 956 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 956 | 956 | 63.95094608 | 63.95094608 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -10 | SINGULAR | F->0 | SINGULAR:F->0 | 955 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 955 | 955 | 63.9509463 | 63.9509463 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -3 | SINGULAR | F->0 | SINGULAR:F->0 | 955 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 955 | 955 | 63.95094638 | 63.95094638 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | -1 | SINGULAR | F->0 | SINGULAR:F->0 | 956 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 956 | 956 | 63.9509464 | 63.9509464 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 0 | SINGULAR | F->0 | SINGULAR:F->0 | 955 | 254 | 75 | 10 | 0 | 63 | 99 | 24 | 955 | 955 | 63.95094641 | 63.95094641 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 1 | SINGULAR | F->0 | SINGULAR:F->0 | 956 | 257 | 76 | 10 | 0 | 63 | 100 | 24 | 956 | 956 | 63.95094642 | 63.95094642 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 3 | SINGULAR | F->0 | SINGULAR:F->0 | 955 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 955 | 955 | 63.95094645 | 63.95094645 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 955 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 955 | 955 | 63.95094652 | 63.95094652 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 30 | SINGULAR | F->0 | SINGULAR:F->0 | 956 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 956 | 956 | 63.95094675 | 63.95094675 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 100 | SINGULAR | F->0 | SINGULAR:F->0 | 956 | 257 | 76 | 10 | 0 | 63 | 100 | 24 | 956 | 956 | 63.95094753 | 63.95094753 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 300 | SINGULAR | F->0 | SINGULAR:F->0 | 955 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 955 | 955 | 63.95094976 | 63.95094976 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 956 | 257 | 76 | 10 | 0 | 63 | 100 | 24 | 956 | 956 | 63.95095756 | 63.95095756 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 956 | 255 | 75 | 11 | 0 | 63 | 99 | 24 | 956 | 956 | 63.9509798 | 63.9509798 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 959 | 261 | 76 | 11 | 0 | 63 | 100 | 24 | 959 | 959 | 63.95105719 | 63.95105719 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 966 | 267 | 77 | 11 | 0 | 63 | 101 | 24 | 966 | 966 | 63.95127439 | 63.95127439 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1017 | 294 | 77 | 10 | 0 | 65 | 104 | 27 | 1017 | 1017 | 63.9519919 | 63.9519919 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 300000 | SINGULAR | F->0 | SINGULAR:F->0 | 1103 | 380 | 85 | 10 | 0 | 64 | 111 | 26 | 1103 | 1103 | 63.95373817 | 63.95373817 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 1000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1508 | 783 | 99 | 11 | 0 | 67 | 130 | 31 | 1508 | 402 | 63.95771562 | 63.97939557 |
| scan --prec dd --mode conserve --fi -2.0 | -2 | -10000 | TINYSTEP |  | SINGULAR:a3->0 | 438 | 74 | 20 | 0 | 0 | 54 | 54 | 34 | 438 | 401 | - | 1.723881779 |
| scan --prec dd --mode conserve --fi 6.0  | 6 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 598 | 143 | 75 | 15 | 0 | 52 | 80 | 5 | 598 | 598 | 5.603075027 | 5.603075027 |
| scan --prec dd --mode conserve --fi 6.0  | 6 | 10000 | SINGULAR | F->0 | SINGULAR:a3->0 | 811 | 349 | 111 | 17 | 0 | 68 | 138 | 27 | 811 | 268 | 5.654148443 | 5.879711063 |
| scan --prec dd --mode conserve --fi 0.03 | 0.03 | 1 | SINGULAR | F->0 | SINGULAR:F->0 | 479 | 157 | 72 | 0 | 0 | 79 | 91 | 19 | 479 | 479 | 0.000113626682 | 0.0001136266821 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1158 | 126 | 75 | 10 | 0 | 37 | 75 | 0 | 1158 | 1158 | 4.60350778 | 4.60350778 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 4000 | 2925 | 86 | 11 | 0 | 72 | 124 | 38 | 4000 | 392 | 4.621440417 | 4.887360434 |
| scan --prec dd --mode project --fi 12.0  | 12 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 918 | 107 | 76 | 4 | 0 | 27 | 76 | 0 | 918 | 918 | 11.80758764 | 11.80758764 |
| scan --prec dd --mode project --fi 12.0  | 12 | 100000 | SINGULAR | F->0 | SINGULAR:a3->0 | 2377 | 1482 | 86 | 11 | 0 | 68 | 118 | 32 | 2377 | 366 | 11.82837564 | 11.94329521 |
| scan --prec dd --mode project --fi 3.0 - | 3 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 3532 | 2273 | 75 | 11 | 0 | 68 | 108 | 33 | 3532 | 3532 | 2.408310586 | 2.408310586 |
| scan --prec dd --mode conserve --fi 0.02 | 0.02 | 1 | SINGULAR | F->0 | SINGULAR:F->0 | 655 | 147 | 71 | 0 | 0 | 76 | 89 | 18 | 655 | 655 | 1.126952069e-06 | 1.126952069e-06 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 878 | 130 | 76 | 12 | 0 | 39 | 76 | 0 | 878 | 878 | 31.91172367 | 31.91172367 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 300000 | SINGULAR | F->0 | SINGULAR:F->0 | 1205 | 440 | 80 | 10 | 0 | 66 | 108 | 28 | 1205 | 1205 | 31.92248282 | 31.92248282 |
| scan --prec dd --mode conserve --fi -5.0 | -5 | -10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1134 | 126 | 75 | 10 | 0 | 37 | 75 | 0 | 1134 | 1134 | 4.60350778 | 4.60350778 |
| scan --prec dd --mode conserve --fi -5.0 | -5 | -30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 3974 | 2919 | 86 | 11 | 0 | 72 | 124 | 38 | 3974 | 369 | 4.621440417 | 4.887360434 |
| scan --prec dd --mode project --fi 6.0 - | 6 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 964 | 98 | 75 | 0 | 0 | 23 | 75 | 0 | 964 | 964 | 5.654148443 | 5.654148443 |
| scan --prec dd --mode project --fi 6.0 - | 6 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 2787 | 1739 | 79 | 11 | 0 | 68 | 111 | 32 | 2787 | 2787 | 5.676108256 | 5.676108256 |
| scan --prec dd --mode project --fi 128.0 | 128 | -3000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1426 | 774 | 106 | 22 | 0 | 85 | 135 | 29 | 1426 | 374 | 127.9742308 | 127.9850717 |
| scan --prec dd --mode project --fi 128.0 | 128 | -1000000 | TINYSTEP |  | SINGULAR:a3->0 | 414 | 79 | 40 | 0 | 0 | 39 | 69 | 29 | 414 | 375 | - | 127.9866166 |
| scan --prec dd --mode project --fi 128.0 | 128 | 100000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 376 | 40 | 39 | 0 | 0 | 1 | 40 | 1 | 376 | 376 | 127.9872713 | 127.9872713 |
| scan --prec dd --mode conserve --fi -0.1 | -0.15 | -10 | SINGULAR | F->0 | SINGULAR:F->0 | 606 | 130 | 71 | 0 | 0 | 59 | 81 | 10 | 606 | 606 | 1.655110783e-06 | 1.655110783e-06 |
| scan --prec dd --mode conserve --fi 1.5  | 1.5 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 747 | 207 | 72 | 14 | 0 | 68 | 99 | 27 | 747 | 747 | 0.5442949715 | 0.5442949715 |
| scan --prec dd --mode conserve --fi 12.0 | 12 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 923 | 107 | 76 | 4 | 0 | 27 | 76 | 0 | 923 | 923 | 11.80758764 | 11.80758764 |
| scan --prec dd --mode conserve --fi 12.0 | 12 | 100000 | SINGULAR | F->0 | SINGULAR:a3->0 | 2082 | 1184 | 85 | 11 | 0 | 68 | 117 | 32 | 2082 | 389 | 11.82837564 | 11.94329521 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1134 | 126 | 75 | 10 | 0 | 37 | 75 | 0 | 1134 | 1134 | 4.60350778 | 4.60350778 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 3974 | 2919 | 86 | 11 | 0 | 72 | 124 | 38 | 3974 | 369 | 4.621440417 | 4.887360434 |
| scan --prec dd --mode conserve --fi 128. | 128 | -3000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1338 | 666 | 106 | 31 | 0 | 76 | 135 | 29 | 1338 | 397 | 127.9742308 | 127.9850717 |
| scan --prec dd --mode conserve --fi 128. | 128 | -1000000 | TINYSTEP |  | SINGULAR:a3->0 | 437 | 79 | 40 | 0 | 0 | 39 | 69 | 29 | 437 | 398 | - | 127.9866166 |
| scan --prec dd --mode conserve --fi 128. | 128 | -300000 | TINYSTEP |  | SINGULAR:a3->0 | 437 | 78 | 43 | 0 | 0 | 35 | 72 | 29 | 437 | 399 | - | 127.9870458 |
| scan --prec dd --mode conserve --fi 128. | 128 | 100000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 398 | 40 | 39 | 0 | 0 | 1 | 40 | 1 | 398 | 398 | 127.9872713 | 127.9872713 |
| scan --prec dd --mode project --fi -2.0  | -2 | -10000 | TINYSTEP |  | SINGULAR:a3->0 | 415 | 74 | 19 | 0 | 0 | 55 | 54 | 35 | 415 | 378 | - | 1.723881779 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 913 | 137 | 75 | 11 | 0 | 43 | 79 | 4 | 913 | 913 | 23.89303019 | 23.89303019 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 300000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1682 | 903 | 86 | 11 | 0 | 70 | 120 | 34 | 1682 | 362 | 23.90645139 | 23.96419759 |
| scan --prec dd --mode conserve --fi 0.75 | 0.75 | 100 | SINGULAR | F->0 | SINGULAR:F->0 | 453 | 114 | 71 | 0 | 0 | 43 | 71 | 0 | 453 | 453 | 0.0004081235124 | 0.0004081235124 |
| scan --prec dd --mode conserve --fi 0.2  | 0.2 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 458 | 160 | 73 | 0 | 0 | 83 | 92 | 19 | 458 | 458 | 7.499522165e-05 | 7.499522172e-05 |
| scan --prec dd --mode conserve --fi 8.0  | 8 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 1320 | 375 | 76 | 12 | 0 | 54 | 93 | 17 | 1320 | 1320 | 7.74378012 | 7.74378012 |
| scan --prec dd --mode conserve --fi 8.0  | 8 | 100000 | TINYSTEP |  | SINGULAR:a3->0 | 404 | 73 | 35 | 0 | 0 | 38 | 67 | 32 | 404 | 368 | - | 7.928774963 |
| scan --prec dd --mode conserve --fi -2.0 | -2 | -10000 | TINYSTEP |  | SINGULAR:a3->0 | 415 | 74 | 19 | 0 | 0 | 55 | 54 | 35 | 415 | 378 | - | 1.723881779 |
| scan --prec dd --mode conserve --fi 1.0  | 1 | 1778.27941 | SINGULAR | F->0 | SINGULAR:F->0 | 605 | 86 | 71 | 0 | 0 | 15 | 71 | 0 | 605 | 605 | 1.016442601e-05 | 1.016442601e-05 |
| scan --prec dd --mode conserve --fi 1.0  | 1 | 2371.373706 | SINGULAR | F->0 | SINGULAR:F->0 | 634 | 107 | 71 | 0 | 0 | 36 | 71 | 0 | 634 | 634 | 4.753463496e-06 | 4.753463496e-06 |
| scan --prec dd --mode conserve --fi 1.0  | 1 | 3162.27766 | SINGULAR | F->0 | SINGULAR:F->0 | 639 | 127 | 71 | 0 | 0 | 56 | 78 | 7 | 639 | 639 | 2.214734957e-06 | 2.214734957e-06 |
| scan --prec dd --mode conserve --fi 1.0  | 1 | 4216.965034 | SINGULAR | F->0 | SINGULAR:F->0 | 641 | 145 | 71 | 0 | 0 | 74 | 87 | 16 | 641 | 641 | 1.028812223e-06 | 1.028812223e-06 |
| scan --prec dd --mode conserve --fi -1.0 | -1 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 474 | 179 | 81 | 0 | 0 | 83 | 101 | 20 | 474 | 474 | 4.578491649e-05 | 4.578491656e-05 |
| scan --prec dd --mode conserve --fi -1.0 | -1 | -300 | SINGULAR | F->0 | SINGULAR:F->0 | 444 | 94 | 71 | 0 | 0 | 23 | 71 | 0 | 444 | 444 | 0.0009548066174 | 0.0009548066175 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 710 | 184 | 74 | 15 | 0 | 65 | 97 | 23 | 710 | 710 | 3.490621782 | 3.490621782 |
| scan --prec dd --mode conserve --fi -16. | -16 | -100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1236 | 410 | 76 | 11 | 0 | 61 | 100 | 24 | 1236 | 1236 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi 0.15 | 0.15 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 606 | 130 | 71 | 0 | 0 | 59 | 81 | 10 | 606 | 606 | 1.655110783e-06 | 1.655110783e-06 |
| scan --prec dd --mode conserve --fi 0.1  | 0.1 | 5.623413252 | SINGULAR | F->0 | SINGULAR:F->0 | 609 | 119 | 71 | 0 | 0 | 48 | 75 | 4 | 609 | 609 | 2.860275801e-06 | 2.860275801e-06 |
| scan --prec dd --mode conserve --fi 3.0  | 3 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 2941 | 1744 | 75 | 11 | 0 | 68 | 108 | 33 | 2941 | 2941 | 2.408310586 | 2.408310586 |
| scan --prec dd --mode conserve --fi 3.0  | 3 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 2958 | 1736 | 75 | 11 | 0 | 68 | 108 | 33 | 2958 | 2958 | 2.408310586 | 2.408310586 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | -30000 | SINGULAR | F->0 | SINGULAR:F->0 | 583 | 204 | 94 | 14 | 0 | 62 | 107 | 13 | 583 | 583 | 31.8886427 | 31.8886427 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | -10000 | SINGULAR | F->0 | SINGULAR:F->0 | 608 | 228 | 100 | 19 | 0 | 61 | 119 | 19 | 608 | 608 | 31.89479941 | 31.89479941 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | -3000 | SINGULAR | F->0 | SINGULAR:F->0 | 616 | 236 | 104 | 18 | 0 | 62 | 123 | 19 | 616 | 616 | 31.89657033 | 31.89657033 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 618 | 238 | 105 | 16 | 0 | 63 | 124 | 19 | 618 | 618 | 31.89704716 | 31.89704716 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | -300 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 239 | 105 | 19 | 0 | 61 | 124 | 19 | 619 | 619 | 31.89721119 | 31.89721119 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | -100 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 238 | 104 | 19 | 0 | 62 | 123 | 19 | 619 | 619 | 31.89725779 | 31.89725779 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | -30 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 238 | 104 | 19 | 0 | 62 | 123 | 19 | 619 | 619 | 31.89727408 | 31.89727408 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | -10 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 238 | 104 | 19 | 0 | 62 | 123 | 19 | 619 | 619 | 31.89727873 | 31.89727873 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | -3 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 238 | 104 | 19 | 0 | 62 | 123 | 19 | 619 | 619 | 31.89728035 | 31.89728035 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | -1 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 238 | 104 | 19 | 0 | 62 | 123 | 19 | 619 | 619 | 31.89728082 | 31.89728082 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 0 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 238 | 104 | 19 | 0 | 62 | 123 | 19 | 619 | 619 | 31.89728105 | 31.89728105 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 1 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 238 | 104 | 19 | 0 | 62 | 123 | 19 | 619 | 619 | 31.89728128 | 31.89728128 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 3 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 238 | 104 | 19 | 0 | 62 | 123 | 19 | 619 | 619 | 31.89728175 | 31.89728175 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 238 | 104 | 19 | 0 | 62 | 123 | 19 | 619 | 619 | 31.89728337 | 31.89728337 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 30 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 239 | 104 | 19 | 0 | 62 | 123 | 19 | 619 | 619 | 31.89728802 | 31.89728802 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 100 | SINGULAR | F->0 | SINGULAR:F->0 | 619 | 239 | 104 | 19 | 0 | 62 | 123 | 19 | 619 | 619 | 31.89730428 | 31.89730428 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 300 | SINGULAR | F->0 | SINGULAR:F->0 | 620 | 240 | 105 | 19 | 0 | 62 | 124 | 19 | 620 | 620 | 31.89735064 | 31.89735064 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 620 | 240 | 106 | 17 | 0 | 62 | 125 | 19 | 620 | 620 | 31.897512 | 31.897512 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 3000 | SINGULAR | F->0 | SINGULAR:a3->0 | 622 | 242 | 106 | 18 | 0 | 62 | 126 | 20 | 622 | 280 | 31.89796534 | 31.94134069 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 10000 | SINGULAR | F->0 | SINGULAR:a3->0 | 630 | 249 | 108 | 17 | 0 | 64 | 128 | 20 | 630 | 279 | 31.89946777 | 31.94284122 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 650 | 268 | 113 | 18 | 0 | 65 | 136 | 23 | 650 | 279 | 31.90315561 | 31.94652425 |
| scan --prec dd --mode conserve --fi -64. | -64 | 300000 | SINGULAR | F->0 | SINGULAR:F->0 | 830 | 154 | 76 | 12 | 0 | 48 | 83 | 7 | 830 | 830 | 63.94674087 | 63.94674087 |
| scan --prec dd --mode conserve --fi -64. | -64 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 895 | 218 | 76 | 11 | 0 | 58 | 95 | 19 | 895 | 895 | 63.9497507 | 63.9497507 |
| scan --prec dd --mode conserve --fi -64. | -64 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 921 | 244 | 76 | 12 | 0 | 61 | 98 | 22 | 921 | 921 | 63.95060498 | 63.95060498 |
| scan --prec dd --mode conserve --fi -64. | -64 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 927 | 251 | 75 | 12 | 0 | 62 | 98 | 23 | 927 | 927 | 63.95083414 | 63.95083414 |
| scan --prec dd --mode conserve --fi -64. | -64 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 930 | 253 | 75 | 11 | 0 | 63 | 99 | 24 | 930 | 930 | 63.95091289 | 63.95091289 |
| scan --prec dd --mode conserve --fi -64. | -64 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95093525 | 63.95093525 |
| scan --prec dd --mode conserve --fi -64. | -64 | 300 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094307 | 63.95094307 |
| scan --prec dd --mode conserve --fi -64. | -64 | 100 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.9509453 | 63.9509453 |
| scan --prec dd --mode conserve --fi -64. | -64 | 30 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094608 | 63.95094608 |
| scan --prec dd --mode conserve --fi -64. | -64 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.9509463 | 63.9509463 |
| scan --prec dd --mode conserve --fi -64. | -64 | 3 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.95094638 | 63.95094638 |
| scan --prec dd --mode conserve --fi -64. | -64 | 1 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 258 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.9509464 | 63.9509464 |
| scan --prec dd --mode conserve --fi -64. | -64 | 0 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 256 | 75 | 10 | 0 | 63 | 99 | 24 | 932 | 932 | 63.95094641 | 63.95094641 |
| scan --prec dd --mode conserve --fi -64. | -64 | -1 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.95094642 | 63.95094642 |
| scan --prec dd --mode conserve --fi -64. | -64 | -3 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 933 | 933 | 63.95094645 | 63.95094645 |
| scan --prec dd --mode conserve --fi -64. | -64 | -10 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094652 | 63.95094652 |
| scan --prec dd --mode conserve --fi -64. | -64 | -30 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094675 | 63.95094675 |
| scan --prec dd --mode conserve --fi -64. | -64 | -100 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 255 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094753 | 63.95094753 |
| scan --prec dd --mode conserve --fi -64. | -64 | -300 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 256 | 76 | 10 | 0 | 63 | 100 | 24 | 932 | 932 | 63.95094976 | 63.95094976 |
| scan --prec dd --mode conserve --fi -64. | -64 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 932 | 255 | 75 | 10 | 0 | 63 | 99 | 24 | 932 | 932 | 63.95095756 | 63.95095756 |
| scan --prec dd --mode conserve --fi -64. | -64 | -3000 | SINGULAR | F->0 | SINGULAR:F->0 | 933 | 257 | 76 | 11 | 0 | 63 | 100 | 24 | 933 | 933 | 63.9509798 | 63.9509798 |
| scan --prec dd --mode conserve --fi -64. | -64 | -10000 | SINGULAR | F->0 | SINGULAR:F->0 | 936 | 258 | 76 | 11 | 0 | 63 | 100 | 24 | 936 | 936 | 63.95105719 | 63.95105719 |
| scan --prec dd --mode conserve --fi -64. | -64 | -30000 | SINGULAR | F->0 | SINGULAR:F->0 | 943 | 266 | 77 | 11 | 0 | 63 | 101 | 24 | 943 | 943 | 63.95127439 | 63.95127439 |
| scan --prec dd --mode conserve --fi -64. | -64 | -100000 | SINGULAR | F->0 | SINGULAR:F->0 | 994 | 294 | 77 | 10 | 0 | 65 | 104 | 27 | 994 | 994 | 63.9519919 | 63.9519919 |
| scan --prec dd --mode conserve --fi -64. | -64 | -300000 | SINGULAR | F->0 | SINGULAR:F->0 | 1081 | 381 | 85 | 10 | 0 | 64 | 111 | 26 | 1081 | 1081 | 63.95373817 | 63.95373817 |
| scan --prec dd --mode conserve --fi -64. | -64 | -1000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1483 | 782 | 99 | 11 | 0 | 67 | 130 | 31 | 1483 | 379 | 63.95771562 | 63.97939557 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 636 | 168 | 75 | 19 | 0 | 60 | 93 | 18 | 636 | 636 | 4.55827794 | 4.55827794 |
| scan --prec dd --mode conserve --fi 1.0  | 1 | 300 | SINGULAR | F->0 | SINGULAR:F->0 | 444 | 94 | 71 | 0 | 0 | 23 | 71 | 0 | 444 | 444 | 0.0009548066174 | 0.0009548066175 |
| scan --prec dd --mode conserve --fi 1.0  | 1 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 474 | 179 | 81 | 0 | 0 | 83 | 101 | 20 | 474 | 474 | 4.578491649e-05 | 4.578491656e-05 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 855 | 129 | 75 | 12 | 0 | 39 | 75 | 0 | 855 | 855 | 31.91172367 | 31.91172367 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 300000 | SINGULAR | F->0 | SINGULAR:F->0 | 1180 | 438 | 80 | 10 | 0 | 66 | 108 | 28 | 1180 | 1180 | 31.92248282 | 31.92248282 |
| scan --prec dd --mode conserve --fi -8.0 | -8 | -30000 | SINGULAR | F->0 | SINGULAR:F->0 | 1320 | 375 | 76 | 12 | 0 | 54 | 93 | 17 | 1320 | 1320 | 7.74378012 | 7.74378012 |
| scan --prec dd --mode conserve --fi -8.0 | -8 | -100000 | TINYSTEP |  | SINGULAR:a3->0 | 404 | 73 | 35 | 0 | 0 | 38 | 67 | 32 | 404 | 368 | - | 7.928774963 |
| scan --prec dd --mode conserve --fi 8.0  | 8 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 545 | 110 | 76 | 2 | 0 | 32 | 76 | 0 | 545 | 545 | 7.66136651 | 7.66136651 |
| scan --prec dd --mode conserve --fi 8.0  | 8 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 678 | 235 | 95 | 18 | 0 | 67 | 120 | 25 | 678 | 678 | 7.715408871 | 7.715408871 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1236 | 410 | 76 | 11 | 0 | 61 | 100 | 24 | 1236 | 1236 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1588 | 457 | 75 | 10 | 0 | 52 | 90 | 15 | 1588 | 1588 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 30000 | TINYSTEP |  | SINGULAR:a3->0 | 431 | 73 | 28 | 0 | 0 | 45 | 62 | 34 | 431 | 395 | - | 3.864651293 |
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
| scan --prec dd --mode conserve --fi 3.0  | 3 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 626 | 105 | 74 | 3 | 0 | 28 | 74 | 0 | 626 | 626 | 2.321748788 | 2.321748788 |
| scan --prec dd --mode conserve --fi 3.0  | 3 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 840 | 309 | 91 | 18 | 0 | 69 | 119 | 28 | 840 | 840 | 2.381267496 | 2.381267496 |
| scan --prec dd --mode conserve --fi -12. | -12 | -30000 | SINGULAR | F->0 | SINGULAR:F->0 | 900 | 107 | 76 | 4 | 0 | 27 | 76 | 0 | 900 | 900 | 11.80758764 | 11.80758764 |
| scan --prec dd --mode conserve --fi -12. | -12 | -100000 | SINGULAR | F->0 | SINGULAR:a3->0 | 2059 | 1184 | 86 | 11 | 0 | 68 | 118 | 32 | 2059 | 366 | 11.82837564 | 11.94329521 |
| scan --prec dd --mode project --fi 16.0  | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1327 | 485 | 76 | 11 | 0 | 61 | 100 | 24 | 1327 | 1327 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode project --fi 16.0  | 16 | 300000 | TINYSTEP |  | SINGULAR:a3->0 | 401 | 74 | 33 | 0 | 0 | 41 | 67 | 34 | 401 | 364 | - | 15.95942409 |
| scan --prec dd --mode conserve --fi -2.0 | -2 | -3000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1275 | 737 | 109 | 14 | 0 | 71 | 142 | 33 | 1275 | 285 | 1.201426408 | 1.708539646 |
| scan --prec dd --mode conserve --fi -2.0 | -2 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 699 | 166 | 72 | 14 | 0 | 59 | 89 | 17 | 699 | 699 | 1.162043429 | 1.162043429 |
| scan --prec dd --mode conserve --fi 0.1  | 0.1 | 3 | SINGULAR | F->0 | SINGULAR:F->0 | 444 | 96 | 70 | 0 | 0 | 26 | 70 | 0 | 444 | 444 | 0.0007367239632 | 0.0007367239633 |
| scan --prec dd --mode conserve --fi -2.0 | -2 | -10000 | TINYSTEP |  | SINGULAR:a3->0 | 415 | 74 | 19 | 0 | 0 | 55 | 54 | 35 | 415 | 378 | - | 1.723881779 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | -10000 | SINGULAR | F->0 | SINGULAR:F->0 | 544 | 149 | 76 | 16 | 0 | 55 | 82 | 6 | 544 | 544 | 23.84994339 | 23.84994339 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | -3000 | SINGULAR | F->0 | SINGULAR:F->0 | 569 | 173 | 82 | 19 | 0 | 56 | 93 | 11 | 569 | 569 | 23.85729041 | 23.85729041 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 575 | 179 | 86 | 17 | 0 | 57 | 96 | 10 | 575 | 575 | 23.85907098 | 23.85907098 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | -300 | SINGULAR | F->0 | SINGULAR:F->0 | 577 | 180 | 85 | 17 | 0 | 58 | 96 | 11 | 577 | 577 | 23.85966658 | 23.85966658 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | -100 | SINGULAR | F->0 | SINGULAR:F->0 | 578 | 182 | 86 | 17 | 0 | 58 | 98 | 12 | 578 | 578 | 23.85983425 | 23.85983425 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | -30 | SINGULAR | F->0 | SINGULAR:F->0 | 578 | 182 | 86 | 17 | 0 | 58 | 98 | 12 | 578 | 578 | 23.85989268 | 23.85989268 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | -10 | SINGULAR | F->0 | SINGULAR:F->0 | 578 | 182 | 86 | 17 | 0 | 58 | 98 | 12 | 578 | 578 | 23.85990935 | 23.85990935 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | -3 | SINGULAR | F->0 | SINGULAR:F->0 | 578 | 182 | 86 | 17 | 0 | 58 | 98 | 12 | 578 | 578 | 23.85991518 | 23.85991518 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | -1 | SINGULAR | F->0 | SINGULAR:F->0 | 578 | 182 | 86 | 17 | 0 | 58 | 98 | 12 | 578 | 578 | 23.85991685 | 23.85991685 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 0 | SINGULAR | F->0 | SINGULAR:F->0 | 578 | 182 | 86 | 17 | 0 | 58 | 98 | 12 | 578 | 578 | 23.85991768 | 23.85991768 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 1 | SINGULAR | F->0 | SINGULAR:F->0 | 578 | 182 | 86 | 17 | 0 | 58 | 98 | 12 | 578 | 578 | 23.85991852 | 23.85991852 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 3 | SINGULAR | F->0 | SINGULAR:F->0 | 578 | 182 | 86 | 17 | 0 | 58 | 98 | 12 | 578 | 578 | 23.85992018 | 23.85992018 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 578 | 182 | 86 | 17 | 0 | 58 | 98 | 12 | 578 | 578 | 23.85992601 | 23.85992601 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 30 | SINGULAR | F->0 | SINGULAR:F->0 | 578 | 182 | 86 | 17 | 0 | 58 | 98 | 12 | 578 | 578 | 23.85994266 | 23.85994266 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 100 | SINGULAR | F->0 | SINGULAR:F->0 | 578 | 182 | 86 | 17 | 0 | 58 | 98 | 12 | 578 | 578 | 23.86000084 | 23.86000084 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 300 | SINGULAR | F->0 | SINGULAR:F->0 | 579 | 183 | 87 | 17 | 0 | 58 | 98 | 11 | 579 | 579 | 23.86016636 | 23.86016636 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 581 | 184 | 86 | 17 | 0 | 59 | 98 | 12 | 581 | 581 | 23.86073735 | 23.86073735 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 585 | 188 | 87 | 15 | 0 | 60 | 100 | 13 | 585 | 585 | 23.86230099 | 23.86230099 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 603 | 206 | 93 | 19 | 0 | 59 | 109 | 16 | 603 | 603 | 23.867097 | 23.867097 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 642 | 244 | 105 | 18 | 0 | 64 | 126 | 21 | 642 | 281 | 23.87689777 | 23.93471435 |
| scan --prec dd --mode project --fi 64.0  | 64 | -300000 | SINGULAR | F->0 | SINGULAR:F->0 | 841 | 163 | 76 | 12 | 0 | 51 | 83 | 7 | 841 | 841 | 63.94674087 | 63.94674087 |
| scan --prec dd --mode project --fi 64.0  | 64 | -100000 | SINGULAR | F->0 | SINGULAR:F->0 | 918 | 237 | 76 | 11 | 0 | 59 | 95 | 19 | 918 | 918 | 63.9497507 | 63.9497507 |
| scan --prec dd --mode project --fi 64.0  | 64 | -30000 | SINGULAR | F->0 | SINGULAR:F->0 | 948 | 268 | 76 | 12 | 0 | 63 | 98 | 22 | 948 | 948 | 63.95060498 | 63.95060498 |
| scan --prec dd --mode project --fi 64.0  | 64 | -10000 | SINGULAR | F->0 | SINGULAR:F->0 | 957 | 277 | 76 | 12 | 0 | 64 | 99 | 23 | 957 | 957 | 63.95083414 | 63.95083414 |
| scan --prec dd --mode project --fi 64.0  | 64 | -3000 | SINGULAR | F->0 | SINGULAR:F->0 | 959 | 279 | 76 | 11 | 0 | 64 | 100 | 24 | 959 | 959 | 63.95091289 | 63.95091289 |
| scan --prec dd --mode project --fi 64.0  | 64 | -1000 | SINGULAR | F->0 | SINGULAR:F->0 | 960 | 281 | 76 | 10 | 0 | 63 | 100 | 24 | 960 | 960 | 63.95093525 | 63.95093525 |
| scan --prec dd --mode project --fi 64.0  | 64 | -300 | SINGULAR | F->0 | SINGULAR:F->0 | 960 | 279 | 76 | 10 | 0 | 63 | 100 | 24 | 960 | 960 | 63.95094307 | 63.95094307 |
| scan --prec dd --mode project --fi 64.0  | 64 | -100 | SINGULAR | F->0 | SINGULAR:F->0 | 960 | 279 | 76 | 10 | 0 | 63 | 100 | 24 | 960 | 960 | 63.9509453 | 63.9509453 |
| scan --prec dd --mode project --fi 64.0  | 64 | -30 | SINGULAR | F->0 | SINGULAR:F->0 | 961 | 281 | 76 | 10 | 0 | 65 | 100 | 24 | 961 | 961 | 63.95094608 | 63.95094608 |
| scan --prec dd --mode project --fi 64.0  | 64 | -10 | SINGULAR | F->0 | SINGULAR:F->0 | 960 | 281 | 75 | 10 | 0 | 63 | 99 | 24 | 960 | 960 | 63.9509463 | 63.9509463 |
| scan --prec dd --mode project --fi 64.0  | 64 | -3 | SINGULAR | F->0 | SINGULAR:F->0 | 961 | 281 | 76 | 10 | 0 | 63 | 100 | 24 | 961 | 961 | 63.95094638 | 63.95094638 |
| scan --prec dd --mode project --fi 64.0  | 64 | -1 | SINGULAR | F->0 | SINGULAR:F->0 | 962 | 283 | 76 | 10 | 0 | 63 | 100 | 24 | 962 | 962 | 63.9509464 | 63.9509464 |
| scan --prec dd --mode project --fi 64.0  | 64 | 0 | SINGULAR | F->0 | SINGULAR:F->0 | 960 | 279 | 75 | 10 | 0 | 63 | 99 | 24 | 960 | 960 | 63.95094641 | 63.95094641 |
| scan --prec dd --mode project --fi 64.0  | 64 | 1 | SINGULAR | F->0 | SINGULAR:F->0 | 960 | 278 | 75 | 10 | 0 | 65 | 99 | 24 | 960 | 960 | 63.95094642 | 63.95094642 |
| scan --prec dd --mode project --fi 64.0  | 64 | 3 | SINGULAR | F->0 | SINGULAR:F->0 | 962 | 281 | 76 | 10 | 0 | 63 | 100 | 24 | 962 | 962 | 63.95094645 | 63.95094645 |
| scan --prec dd --mode project --fi 64.0  | 64 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 961 | 280 | 76 | 10 | 0 | 64 | 100 | 24 | 961 | 961 | 63.95094652 | 63.95094652 |
| scan --prec dd --mode project --fi 64.0  | 64 | 30 | SINGULAR | F->0 | SINGULAR:F->0 | 961 | 280 | 76 | 10 | 0 | 63 | 100 | 24 | 961 | 961 | 63.95094675 | 63.95094675 |
| scan --prec dd --mode project --fi 64.0  | 64 | 100 | SINGULAR | F->0 | SINGULAR:F->0 | 961 | 280 | 76 | 10 | 0 | 63 | 100 | 24 | 961 | 961 | 63.95094753 | 63.95094753 |
| scan --prec dd --mode project --fi 64.0  | 64 | 300 | SINGULAR | F->0 | SINGULAR:F->0 | 961 | 281 | 76 | 10 | 0 | 63 | 100 | 24 | 961 | 961 | 63.95094976 | 63.95094976 |
| scan --prec dd --mode project --fi 64.0  | 64 | 1000 | SINGULAR | F->0 | SINGULAR:F->0 | 960 | 281 | 76 | 10 | 0 | 63 | 100 | 24 | 960 | 960 | 63.95095756 | 63.95095756 |
| scan --prec dd --mode project --fi 64.0  | 64 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 962 | 282 | 76 | 11 | 0 | 64 | 100 | 24 | 962 | 962 | 63.9509798 | 63.9509798 |
| scan --prec dd --mode project --fi 64.0  | 64 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 965 | 284 | 75 | 11 | 0 | 63 | 99 | 24 | 965 | 965 | 63.95105719 | 63.95105719 |
| scan --prec dd --mode project --fi 64.0  | 64 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 975 | 295 | 77 | 11 | 0 | 65 | 101 | 24 | 975 | 975 | 63.95127439 | 63.95127439 |
| scan --prec dd --mode project --fi 64.0  | 64 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1029 | 325 | 77 | 10 | 0 | 68 | 104 | 27 | 1029 | 1029 | 63.9519919 | 63.9519919 |
| scan --prec dd --mode project --fi 64.0  | 64 | 300000 | SINGULAR | F->0 | SINGULAR:F->0 | 1136 | 432 | 86 | 10 | 0 | 65 | 112 | 26 | 1136 | 1136 | 63.95373817 | 63.95373817 |
| scan --prec dd --mode project --fi 64.0  | 64 | 1000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1637 | 930 | 98 | 11 | 0 | 67 | 129 | 31 | 1637 | 379 | 63.95771562 | 63.97939557 |
| scan --prec dd --mode project --fi 8.0 - | 8 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 1430 | 459 | 76 | 12 | 0 | 54 | 93 | 17 | 1430 | 1430 | 7.74378012 | 7.74378012 |
| scan --prec dd --mode project --fi 8.0 - | 8 | 100000 | TINYSTEP |  | SINGULAR:a3->0 | 404 | 73 | 34 | 0 | 0 | 39 | 67 | 33 | 404 | 368 | - | 7.928774963 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 7498.942093 | SINGULAR | F->0 | SINGULAR:F->0 | 956 | 97 | 75 | 0 | 0 | 22 | 75 | 0 | 956 | 956 | 4.595794203 | 4.595794203 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1134 | 126 | 75 | 10 | 0 | 37 | 75 | 0 | 1134 | 1134 | 4.60350778 | 4.60350778 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 13335.21432 | SINGULAR | F->0 | SINGULAR:F->0 | 1405 | 350 | 75 | 10 | 0 | 50 | 88 | 13 | 1405 | 1405 | 4.609750889 | 4.609750889 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 17782.7941 | SINGULAR | F->0 | SINGULAR:F->0 | 1880 | 830 | 75 | 10 | 0 | 62 | 101 | 26 | 1880 | 1880 | 4.614769523 | 4.614769523 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 23713.73706 | SINGULAR | F->0 | SINGULAR:F->0 | 2751 | 1696 | 80 | 10 | 0 | 69 | 113 | 33 | 2751 | 2751 | 4.618780509 | 4.618780509 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 31622.7766 | SINGULAR | F->0 | SINGULAR:a3->0 | 4344 | 3291 | 89 | 11 | 0 | 71 | 126 | 37 | 4344 | 369 | 4.621970366 | 4.887866457 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 42169.65034 | TINYSTEP |  | SINGULAR:a3->0 | 407 | 74 | 29 | 0 | 0 | 45 | 63 | 34 | 407 | 370 | - | 4.890278599 |
| scan --prec dd --mode conserve --fi -0.0 | -0.02 | -1 | SINGULAR | F->0 | SINGULAR:F->0 | 632 | 147 | 71 | 0 | 0 | 76 | 89 | 18 | 632 | 632 | 1.126952069e-06 | 1.126952069e-06 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 42169.65034 | SINGULAR | F->0 | SINGULAR:F->0 | 861 | 103 | 75 | 1 | 0 | 27 | 75 | 0 | 861 | 861 | 15.84596646 | 15.84596646 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 56234.13252 | SINGULAR | F->0 | SINGULAR:F->0 | 934 | 129 | 76 | 11 | 0 | 38 | 76 | 0 | 934 | 934 | 15.85164729 | 15.85164729 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 74989.42093 | SINGULAR | F->0 | SINGULAR:F->0 | 1045 | 216 | 76 | 10 | 0 | 50 | 88 | 12 | 1045 | 1045 | 15.85675999 | 15.85675999 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1236 | 410 | 76 | 11 | 0 | 61 | 100 | 24 | 1236 | 1236 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 133352.1432 | SINGULAR | F->0 | SINGULAR:F->0 | 1562 | 736 | 79 | 11 | 0 | 69 | 111 | 32 | 1562 | 1562 | 15.86512546 | 15.86512546 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 177827.941 | SINGULAR | F->0 | SINGULAR:a3->0 | 2136 | 1308 | 91 | 11 | 0 | 68 | 124 | 33 | 2136 | 363 | 15.86840232 | 15.95484213 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 237137.3706 | TINYSTEP |  | SINGULAR:a3->0 | 401 | 76 | 23 | 0 | 0 | 53 | 59 | 36 | 401 | 363 | - | 15.95756102 |
| scan --prec dd --mode conserve --fi -4.0 | -4 | -10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1563 | 458 | 75 | 10 | 0 | 52 | 90 | 15 | 1563 | 1563 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode conserve --fi -4.0 | -4 | -30000 | TINYSTEP |  | SINGULAR:a3->0 | 408 | 73 | 29 | 0 | 0 | 44 | 62 | 33 | 408 | 372 | - | 3.864651293 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 10000 | TINYSTEP |  | SINGULAR:a3->0 | 438 | 74 | 20 | 0 | 0 | 54 | 54 | 34 | 438 | 401 | - | 1.723881779 |
| scan --prec dd --mode conserve --fi -128 | -128 | 3000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1317 | 666 | 106 | 32 | 0 | 73 | 135 | 29 | 1317 | 374 | 127.9742308 | 127.9850717 |
| scan --prec dd --mode conserve --fi -128 | -128 | 1000000 | TINYSTEP |  | SINGULAR:a3->0 | 414 | 79 | 39 | 0 | 0 | 40 | 69 | 30 | 414 | 375 | - | 127.9866166 |
| scan --prec dd --mode conserve --fi -128 | -128 | -100000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 376 | 40 | 39 | 0 | 0 | 1 | 40 | 1 | 376 | 376 | 127.9872713 | 127.9872713 |
| scan --prec dd --mode conserve --fi 0.02 | 0.02 | 1 | SINGULAR | F->0 | SINGULAR:F->0 | 632 | 147 | 71 | 0 | 0 | 76 | 89 | 18 | 632 | 632 | 1.126952069e-06 | 1.126952069e-06 |
| scan --prec dd --mode project --fi 32.0  | 32 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 868 | 130 | 76 | 12 | 0 | 39 | 76 | 0 | 868 | 868 | 31.91172367 | 31.91172367 |
| scan --prec dd --mode project --fi 32.0  | 32 | 300000 | SINGULAR | F->0 | SINGULAR:F->0 | 1259 | 509 | 80 | 10 | 0 | 66 | 108 | 28 | 1259 | 1259 | 31.92248282 | 31.92248282 |
| scan --prec dd --mode conserve --fi -32. | -32 | -100000 | SINGULAR | F->0 | SINGULAR:F->0 | 855 | 129 | 75 | 12 | 0 | 39 | 75 | 0 | 855 | 855 | 31.91172367 | 31.91172367 |
| scan --prec dd --mode conserve --fi -32. | -32 | -300000 | SINGULAR | F->0 | SINGULAR:F->0 | 1180 | 438 | 80 | 10 | 0 | 66 | 108 | 28 | 1180 | 1180 | 31.92248282 | 31.92248282 |
| scan --prec dd --mode conserve --fi 0.15 | 0.15 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 629 | 130 | 71 | 0 | 0 | 59 | 81 | 10 | 629 | 629 | 1.655110783e-06 | 1.655110783e-06 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 1259 | 409 | 76 | 11 | 0 | 61 | 100 | 24 | 1259 | 1259 | 15.86125434 | 15.86125434 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 300000 | TINYSTEP |  | SINGULAR:a3->0 | 424 | 74 | 34 | 0 | 0 | 40 | 67 | 33 | 424 | 387 | - | 15.95942409 |
| scan --prec dd --mode conserve --fi 8.0  | 8 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 1342 | 374 | 75 | 12 | 0 | 54 | 92 | 17 | 1342 | 1342 | 7.74378012 | 7.74378012 |
| scan --prec dd --mode conserve --fi 8.0  | 8 | 100000 | TINYSTEP |  | SINGULAR:a3->0 | 427 | 73 | 33 | 0 | 0 | 40 | 67 | 34 | 427 | 391 | - | 7.928774963 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1563 | 458 | 75 | 10 | 0 | 52 | 90 | 15 | 1563 | 1563 | 3.527557745 | 3.527557745 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 30000 | TINYSTEP |  | SINGULAR:a3->0 | 408 | 73 | 29 | 0 | 0 | 44 | 62 | 33 | 408 | 372 | - | 3.864651293 |
| scan --prec dd --mode conserve --fi 6.0  | 6 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 959 | 98 | 75 | 0 | 0 | 23 | 75 | 0 | 959 | 959 | 5.654148443 | 5.654148443 |
| scan --prec dd --mode conserve --fi 6.0  | 6 | 30000 | SINGULAR | F->0 | SINGULAR:F->0 | 2397 | 1364 | 78 | 11 | 0 | 69 | 111 | 33 | 2397 | 2397 | 5.676108256 | 5.676108256 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 100000 | SINGULAR | F->0 | SINGULAR:F->0 | 935 | 139 | 76 | 11 | 0 | 43 | 80 | 4 | 935 | 935 | 23.89303019 | 23.89303019 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 300000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1707 | 908 | 87 | 11 | 0 | 70 | 121 | 34 | 1707 | 384 | 23.90645139 | 23.96419759 |
| scan --prec dd --mode conserve --fi 0.25 | 0.25 | 10 | SINGULAR | F->0 | SINGULAR:F->0 | 433 | 95 | 71 | 0 | 0 | 24 | 71 | 0 | 433 | 433 | 0.0007153455038 | 0.0007153455038 |
| scan --prec dd --mode project --fi 5.0 - | 5 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 1198 | 126 | 75 | 10 | 0 | 37 | 75 | 0 | 1198 | 1198 | 4.60350778 | 4.60350778 |
| scan --prec dd --mode project --fi 5.0 - | 5 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 4916 | 3818 | 86 | 11 | 0 | 72 | 124 | 38 | 4916 | 369 | 4.621440417 | 4.887360434 |
| scan --prec dd --mode conserve --fi 12.0 | 12 | 3000 | SINGULAR | F->0 | SINGULAR:F->0 | 509 | 99 | 76 | 0 | 0 | 23 | 76 | 0 | 509 | 509 | 11.73902016 | 11.73902016 |
| scan --prec dd --mode conserve --fi 12.0 | 12 | 10000 | SINGULAR | F->0 | SINGULAR:F->0 | 598 | 182 | 82 | 20 | 0 | 59 | 99 | 17 | 598 | 598 | 11.77626991 | 11.77626991 |
| scan --prec dd --mode conserve --fi 12.0 | 12 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 773 | 330 | 116 | 19 | 0 | 67 | 143 | 27 | 773 | 287 | 11.80758764 | 11.9227013 |
| scan --prec dd --mode conserve --fi -6.0 | -6 | -10000 | SINGULAR | F->0 | SINGULAR:F->0 | 937 | 98 | 75 | 0 | 0 | 23 | 75 | 0 | 937 | 937 | 5.654148443 | 5.654148443 |
| scan --prec dd --mode conserve --fi -6.0 | -6 | -30000 | SINGULAR | F->0 | SINGULAR:F->0 | 2375 | 1367 | 77 | 11 | 0 | 70 | 111 | 34 | 2375 | 2375 | 5.676108256 | 5.676108256 |
| scan --prec dd --mode conserve --fi -24. | -24 | -100000 | SINGULAR | F->0 | SINGULAR:F->0 | 913 | 137 | 75 | 11 | 0 | 43 | 79 | 4 | 913 | 913 | 23.89303019 | 23.89303019 |
| scan --prec dd --mode conserve --fi -24. | -24 | -300000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1682 | 903 | 86 | 11 | 0 | 70 | 120 | 34 | 1682 | 362 | 23.90645139 | 23.96419759 |
| scan --prec dd --mode conserve --fi 0.07 | 0.07 | 3 | SINGULAR | F->0 | SINGULAR:fold | 480 | 188 | 84 | 0 | 0 | 86 | 106 | 22 | 480 | 282 | 2.420504793e-05 | 4.785330889e-05 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 10000 | TINYSTEP |  | SINGULAR:a3->0 | 415 | 74 | 19 | 0 | 0 | 55 | 54 | 35 | 415 | 378 | - | 1.723881779 |
| scan --prec dd --mode conserve --fi 128. | 128 | -3000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1317 | 666 | 106 | 32 | 0 | 73 | 135 | 29 | 1317 | 374 | 127.9742308 | 127.9850717 |
| scan --prec dd --mode conserve --fi 128. | 128 | -1000000 | TINYSTEP |  | SINGULAR:a3->0 | 414 | 79 | 39 | 0 | 0 | 40 | 69 | 30 | 414 | 375 | - | 127.9866166 |
| scan --prec dd --mode conserve --fi 128. | 128 | 100000 | SINGULAR | a3->0 | SINGULAR:a3->0 | 376 | 40 | 39 | 0 | 0 | 1 | 40 | 1 | 376 | 376 | 127.9872713 | 127.9872713 |
| scan --prec dd --mode project --fi 2.0 - | 2 | 10000 | TINYSTEP |  | SINGULAR:a3->0 | 415 | 74 | 19 | 0 | 0 | 55 | 54 | 35 | 415 | 378 | - | 1.723881779 |

4. records whose stop is not the old rule's: 59 records

| file command (start) | F_inf | C | class | kind | base class:kind | steps | calls | real | Unresolved | nothing | pair | old real | locate not real while old real | stop step | old stop step | eta* | old eta* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | 2 | 3000 | NONFINITE |  | SINGULAR:a3->0 | 378 | 103 | 54 | 0 | 0 | 49 | 98 | 44 | 317 | 272 | - | 1.708539646 |
| scan 0.25,0.5,0.75,1,1.5,2,3,4,-0.5,-1,- | -2 | -3000 | NONFINITE |  | SINGULAR:a3->0 | 378 | 103 | 54 | 0 | 0 | 49 | 98 | 44 | 317 | 272 | - | 1.708539646 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 682 | 258 | 105 | 16 | 0 | 69 | 130 | 25 | 682 | 284 | 15.83865707 | 15.92525529 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 3000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1275 | 737 | 109 | 14 | 0 | 71 | 142 | 33 | 1275 | 285 | 1.201426408 | 1.708539646 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 10000 | TINYSTEP |  | SINGULAR:a3->0 | 415 | 74 | 19 | 0 | 0 | 55 | 54 | 35 | 415 | 378 | - | 1.723881779 |
| scan --prec dd --mode project --fi 4.0 - | 4 | 30000 | TINYSTEP |  | SINGULAR:a3->0 | 408 | 73 | 28 | 0 | 0 | 45 | 62 | 34 | 408 | 372 | - | 3.864651293 |
| scan --prec dd --mode conserve --fi 12.0 | 12 | 100000 | SINGULAR | F->0 | SINGULAR:a3->0 | 2059 | 1184 | 86 | 11 | 0 | 68 | 118 | 32 | 2059 | 366 | 11.82837564 | 11.94329521 |
| scan --prec dd --mode project --fi 24.0  | 24 | 300000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1891 | 1103 | 87 | 11 | 0 | 70 | 121 | 34 | 1891 | 362 | 23.90645139 | 23.96419759 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 1000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1508 | 783 | 99 | 11 | 0 | 67 | 130 | 31 | 1508 | 402 | 63.95771562 | 63.97939557 |
| scan --prec dd --mode conserve --fi -2.0 | -2 | -10000 | TINYSTEP |  | SINGULAR:a3->0 | 438 | 74 | 20 | 0 | 0 | 54 | 54 | 34 | 438 | 401 | - | 1.723881779 |
| scan --prec dd --mode conserve --fi 6.0  | 6 | 10000 | SINGULAR | F->0 | SINGULAR:a3->0 | 811 | 349 | 111 | 17 | 0 | 68 | 138 | 27 | 811 | 268 | 5.654148443 | 5.879711063 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 4000 | 2925 | 86 | 11 | 0 | 72 | 124 | 38 | 4000 | 392 | 4.621440417 | 4.887360434 |
| scan --prec dd --mode project --fi 12.0  | 12 | 100000 | SINGULAR | F->0 | SINGULAR:a3->0 | 2377 | 1482 | 86 | 11 | 0 | 68 | 118 | 32 | 2377 | 366 | 11.82837564 | 11.94329521 |
| scan --prec dd --mode conserve --fi -5.0 | -5 | -30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 3974 | 2919 | 86 | 11 | 0 | 72 | 124 | 38 | 3974 | 369 | 4.621440417 | 4.887360434 |
| scan --prec dd --mode project --fi 128.0 | 128 | -3000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1426 | 774 | 106 | 22 | 0 | 85 | 135 | 29 | 1426 | 374 | 127.9742308 | 127.9850717 |
| scan --prec dd --mode project --fi 128.0 | 128 | -1000000 | TINYSTEP |  | SINGULAR:a3->0 | 414 | 79 | 40 | 0 | 0 | 39 | 69 | 29 | 414 | 375 | - | 127.9866166 |
| scan --prec dd --mode conserve --fi 12.0 | 12 | 100000 | SINGULAR | F->0 | SINGULAR:a3->0 | 2082 | 1184 | 85 | 11 | 0 | 68 | 117 | 32 | 2082 | 389 | 11.82837564 | 11.94329521 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 3974 | 2919 | 86 | 11 | 0 | 72 | 124 | 38 | 3974 | 369 | 4.621440417 | 4.887360434 |
| scan --prec dd --mode conserve --fi 128. | 128 | -3000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1338 | 666 | 106 | 31 | 0 | 76 | 135 | 29 | 1338 | 397 | 127.9742308 | 127.9850717 |
| scan --prec dd --mode conserve --fi 128. | 128 | -1000000 | TINYSTEP |  | SINGULAR:a3->0 | 437 | 79 | 40 | 0 | 0 | 39 | 69 | 29 | 437 | 398 | - | 127.9866166 |
| scan --prec dd --mode conserve --fi 128. | 128 | -300000 | TINYSTEP |  | SINGULAR:a3->0 | 437 | 78 | 43 | 0 | 0 | 35 | 72 | 29 | 437 | 399 | - | 127.9870458 |
| scan --prec dd --mode project --fi -2.0  | -2 | -10000 | TINYSTEP |  | SINGULAR:a3->0 | 415 | 74 | 19 | 0 | 0 | 55 | 54 | 35 | 415 | 378 | - | 1.723881779 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 300000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1682 | 903 | 86 | 11 | 0 | 70 | 120 | 34 | 1682 | 362 | 23.90645139 | 23.96419759 |
| scan --prec dd --mode conserve --fi 8.0  | 8 | 100000 | TINYSTEP |  | SINGULAR:a3->0 | 404 | 73 | 35 | 0 | 0 | 38 | 67 | 32 | 404 | 368 | - | 7.928774963 |
| scan --prec dd --mode conserve --fi -2.0 | -2 | -10000 | TINYSTEP |  | SINGULAR:a3->0 | 415 | 74 | 19 | 0 | 0 | 55 | 54 | 35 | 415 | 378 | - | 1.723881779 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 3000 | SINGULAR | F->0 | SINGULAR:a3->0 | 622 | 242 | 106 | 18 | 0 | 62 | 126 | 20 | 622 | 280 | 31.89796534 | 31.94134069 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 10000 | SINGULAR | F->0 | SINGULAR:a3->0 | 630 | 249 | 108 | 17 | 0 | 64 | 128 | 20 | 630 | 279 | 31.89946777 | 31.94284122 |
| scan --prec dd --mode conserve --fi 32.0 | 32 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 650 | 268 | 113 | 18 | 0 | 65 | 136 | 23 | 650 | 279 | 31.90315561 | 31.94652425 |
| scan --prec dd --mode conserve --fi -64. | -64 | -1000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1483 | 782 | 99 | 11 | 0 | 67 | 130 | 31 | 1483 | 379 | 63.95771562 | 63.97939557 |
| scan --prec dd --mode conserve --fi -8.0 | -8 | -100000 | TINYSTEP |  | SINGULAR:a3->0 | 404 | 73 | 35 | 0 | 0 | 38 | 67 | 32 | 404 | 368 | - | 7.928774963 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 30000 | TINYSTEP |  | SINGULAR:a3->0 | 431 | 73 | 28 | 0 | 0 | 45 | 62 | 34 | 431 | 395 | - | 3.864651293 |
| scan --prec dd --mode conserve --fi 64.0 | 64 | 1000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1483 | 782 | 99 | 11 | 0 | 67 | 130 | 31 | 1483 | 379 | 63.95771562 | 63.97939557 |
| scan --prec dd --mode conserve --fi -12. | -12 | -100000 | SINGULAR | F->0 | SINGULAR:a3->0 | 2059 | 1184 | 86 | 11 | 0 | 68 | 118 | 32 | 2059 | 366 | 11.82837564 | 11.94329521 |
| scan --prec dd --mode project --fi 16.0  | 16 | 300000 | TINYSTEP |  | SINGULAR:a3->0 | 401 | 74 | 33 | 0 | 0 | 41 | 67 | 34 | 401 | 364 | - | 15.95942409 |
| scan --prec dd --mode conserve --fi -2.0 | -2 | -3000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1275 | 737 | 109 | 14 | 0 | 71 | 142 | 33 | 1275 | 285 | 1.201426408 | 1.708539646 |
| scan --prec dd --mode conserve --fi -2.0 | -2 | -10000 | TINYSTEP |  | SINGULAR:a3->0 | 415 | 74 | 19 | 0 | 0 | 55 | 54 | 35 | 415 | 378 | - | 1.723881779 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 642 | 244 | 105 | 18 | 0 | 64 | 126 | 21 | 642 | 281 | 23.87689777 | 23.93471435 |
| scan --prec dd --mode project --fi 64.0  | 64 | 1000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1637 | 930 | 98 | 11 | 0 | 67 | 129 | 31 | 1637 | 379 | 63.95771562 | 63.97939557 |
| scan --prec dd --mode project --fi 8.0 - | 8 | 100000 | TINYSTEP |  | SINGULAR:a3->0 | 404 | 73 | 34 | 0 | 0 | 39 | 67 | 33 | 404 | 368 | - | 7.928774963 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 31622.7766 | SINGULAR | F->0 | SINGULAR:a3->0 | 4344 | 3291 | 89 | 11 | 0 | 71 | 126 | 37 | 4344 | 369 | 4.621970366 | 4.887866457 |
| scan --prec dd --mode conserve --fi 5.0  | 5 | 42169.65034 | TINYSTEP |  | SINGULAR:a3->0 | 407 | 74 | 29 | 0 | 0 | 45 | 63 | 34 | 407 | 370 | - | 4.890278599 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 177827.941 | SINGULAR | F->0 | SINGULAR:a3->0 | 2136 | 1308 | 91 | 11 | 0 | 68 | 124 | 33 | 2136 | 363 | 15.86840232 | 15.95484213 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 237137.3706 | TINYSTEP |  | SINGULAR:a3->0 | 401 | 76 | 23 | 0 | 0 | 53 | 59 | 36 | 401 | 363 | - | 15.95756102 |
| scan --prec dd --mode conserve --fi -4.0 | -4 | -30000 | TINYSTEP |  | SINGULAR:a3->0 | 408 | 73 | 29 | 0 | 0 | 44 | 62 | 33 | 408 | 372 | - | 3.864651293 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 10000 | TINYSTEP |  | SINGULAR:a3->0 | 438 | 74 | 20 | 0 | 0 | 54 | 54 | 34 | 438 | 401 | - | 1.723881779 |
| scan --prec dd --mode conserve --fi -128 | -128 | 3000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1317 | 666 | 106 | 32 | 0 | 73 | 135 | 29 | 1317 | 374 | 127.9742308 | 127.9850717 |
| scan --prec dd --mode conserve --fi -128 | -128 | 1000000 | TINYSTEP |  | SINGULAR:a3->0 | 414 | 79 | 39 | 0 | 0 | 40 | 69 | 30 | 414 | 375 | - | 127.9866166 |
| scan --prec dd --mode conserve --fi 16.0 | 16 | 300000 | TINYSTEP |  | SINGULAR:a3->0 | 424 | 74 | 34 | 0 | 0 | 40 | 67 | 33 | 424 | 387 | - | 15.95942409 |
| scan --prec dd --mode conserve --fi 8.0  | 8 | 100000 | TINYSTEP |  | SINGULAR:a3->0 | 427 | 73 | 33 | 0 | 0 | 40 | 67 | 34 | 427 | 391 | - | 7.928774963 |
| scan --prec dd --mode conserve --fi 4.0  | 4 | 30000 | TINYSTEP |  | SINGULAR:a3->0 | 408 | 73 | 29 | 0 | 0 | 44 | 62 | 33 | 408 | 372 | - | 3.864651293 |
| scan --prec dd --mode conserve --fi 24.0 | 24 | 300000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1707 | 908 | 87 | 11 | 0 | 70 | 121 | 34 | 1707 | 384 | 23.90645139 | 23.96419759 |
| scan --prec dd --mode project --fi 5.0 - | 5 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 4916 | 3818 | 86 | 11 | 0 | 72 | 124 | 38 | 4916 | 369 | 4.621440417 | 4.887360434 |
| scan --prec dd --mode conserve --fi 12.0 | 12 | 30000 | SINGULAR | F->0 | SINGULAR:a3->0 | 773 | 330 | 116 | 19 | 0 | 67 | 143 | 27 | 773 | 287 | 11.80758764 | 11.9227013 |
| scan --prec dd --mode conserve --fi -24. | -24 | -300000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1682 | 903 | 86 | 11 | 0 | 70 | 120 | 34 | 1682 | 362 | 23.90645139 | 23.96419759 |
| scan --prec dd --mode conserve --fi 0.07 | 0.07 | 3 | SINGULAR | F->0 | SINGULAR:fold | 480 | 188 | 84 | 0 | 0 | 86 | 106 | 22 | 480 | 282 | 2.420504793e-05 | 4.785330889e-05 |
| scan --prec dd --mode conserve --fi 2.0  | 2 | 10000 | TINYSTEP |  | SINGULAR:a3->0 | 415 | 74 | 19 | 0 | 0 | 55 | 54 | 35 | 415 | 378 | - | 1.723881779 |
| scan --prec dd --mode conserve --fi 128. | 128 | -3000000 | SINGULAR | F->0 | SINGULAR:a3->0 | 1317 | 666 | 106 | 32 | 0 | 73 | 135 | 29 | 1317 | 374 | 127.9742308 | 127.9850717 |
| scan --prec dd --mode conserve --fi 128. | 128 | -1000000 | TINYSTEP |  | SINGULAR:a3->0 | 414 | 79 | 39 | 0 | 0 | 40 | 69 | 30 | 414 | 375 | - | 127.9866166 |
| scan --prec dd --mode project --fi 2.0 - | 2 | 10000 | TINYSTEP |  | SINGULAR:a3->0 | 415 | 74 | 19 | 0 | 0 | 55 | 54 | 35 | 415 | 378 | - | 1.723881779 |

5. eta* against the old rule's eta* on the same steps: 3886 SINGULAR records with both; largest |difference| / max(1, eta*) 4.221e-01; above 1e-12: 77; above 1e-10: 32

  4.221e-01  F_inf 2.0 C [3000.0, 0.0]  eta* 1.2014264075106749  old 1.7085396460352056  [scan --prec dd --mode conserve --fi 2.0 --c -3000.0,-1000.0,]
  4.221e-01  F_inf -2.0 C [-3000.0, 0.0]  eta* 1.2014264075106749  old 1.7085396460352056  [scan --prec dd --mode conserve --fi -2.0 --c -3000.0,-1000.0]
  5.754e-02  F_inf 5.0 C [30000.0, 0.0]  eta* 4.6214404173726855  old 4.887360434025165  [scan --prec dd --mode conserve --fi 5.0 --c -100000000.0,-30]
  5.754e-02  F_inf -5.0 C [-30000.0, 0.0]  eta* 4.6214404173726855  old 4.887360434025165  [scan --prec dd --mode conserve --fi -5.0 --c 100000000.0,300]
  5.754e-02  F_inf 5.0 C [30000.0, 0.0]  eta* 4.6214404173726855  old 4.887360434025165  [scan --prec dd --mode conserve --fi 5.0 --c -100000000.0,-30]
  5.754e-02  F_inf 5.0 C [30000.0, 0.0]  eta* 4.6214404173726855  old 4.887360434025165  [scan --prec dd --mode project --fi 5.0 --c -100000000.0,-300]
  5.753e-02  F_inf 5.0 C [31622.776601683792, 0.0]  eta* 4.621970365691967  old 4.887866456982279  [scan --prec dd --mode conserve --fi 5.0 --c -100000000.0,-74]
  3.989e-02  F_inf 6.0 C [10000.0, 0.0]  eta* 5.654148443377775  old 5.879711062825615  [scan --prec dd --mode conserve --fi 6.0 --c -100000000.0,-30]
