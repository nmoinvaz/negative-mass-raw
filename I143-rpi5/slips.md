# I143-rpi5: slips (mine), none changed a criterion

1. Two processes at once, about 6 minutes: I started a development run of the even-parity section while the step 2 unit (`nm-i143-step2`) was still
   running. The rule is one process. The development run was killed by PID and restarted after step 2 had finished.
2. `pgrep -f "dev.py --part=even"` matched my own shell command line and killed the shell (exit 144). Known from #102; the rule is `ps` and the exact PID.
3. `flow_sub` built jets to order 4 for every function although the equations need order 2. The even-parity run sat in E.2 for more than 7 minutes
   with no output (stdout was piped into `tail`). Fixed by building only the orders that occur; E.2 then takes 5 s. No check changed.
4. A first draft of A.1 contained placeholder lines (`dep_L = ... if False else None`). Rewritten before any run of the even section.
5. The step 2 log (`step2_odd.log`) was produced by the script before the even section was appended; the committed file (734d5a3) already contains the
   unfinished even section. `--part=odd` ends before it, so the output is the same.
6. The check "no second derivative in δG_rr" (part of E.2) was first written with K_2 and H_2 in its allowed set, so it could not fail. When I tightened it, it failed
   because `Grr` was an uncancelled sum whose second-derivative coefficients cancel only after `cancel`. The criterion is unchanged; the code now cancels first and the check passes.
7. The final controls were first run with a `master_reduce` that used expression-tree `cancel`; the `mv_coef` control ran 282 s once and more than 27 minutes the next time (hash-seed dependent).
   I stopped it, replaced the arithmetic by the rational function field Q(r, M, s, L), and restarted the final run and the controls (README, "Final run, first attempt stopped").
8. A second restart of the final run (after 3 minutes) for the tightened E.2 check and for printing the factors μ of E.4; nothing was run with the earlier script past that point.
9. The third attempt at the final run sat for more than 10 minutes in `sp.factor` of the nine printed radial equations (display only; the same line took seconds in the earlier run, so the time depends on
   the hash seed). I stopped it and replaced `sp.factor` by `sp.factor_terms` in that print. No check changed.
