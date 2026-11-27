Scratch experiment, nothing in the repository was edited. notes/wormhole_largeD/ was copied to a scratch directory twice (main at
1839211). In the second copy growth.csv's D = 4..11 rows were replaced by the crate's qd values (w2_output.txt) rounded half-even to
12 decimals, source "w2_crate qd (#195)" (growth_B_crate_rows.csv; the D >= 20 rows are main's, unchanged). paper_numbers.py was run
in both copies (python 3.14 venv, nice 10), both exit 0, "checks failed: 0".
diff_A_B.txt: only the eight D <= 11 lines of the first table differ, in the 10th decimal of W^2 a^2 and in the source column;
the 3-term difference, (data - 3 terms) s^2, the e-folding table (1/W to 4 decimals), the ST17 slopes and sigmas, the SH2002
comparison and every check are identical.
