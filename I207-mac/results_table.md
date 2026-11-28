| run | arm | what | rc | wall s | RSS MB | checks | failed | controls | gated log lines (raw) | (i) / (iii) / (ii) | dump records of another class or kind | largest eta* difference | against |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| run_06_on_ctl | on | `ctl`, 16 checks | 1 | 570 | 80 | 15 of 16 | ['regress167'] | - | 8 | 5 / 1 / 2 | 4 | 7.467e-12 | I190 `run_06_base_offgrid_ctl` |
| run_07_on_stage_a | on | full grid, stage a (15 checks) | 1 | 1861 | 106 | 10 of 15 | ['regress167', 'scan', 'spread', 'modes', 'bisect'] | - | 340 | 2 / 0 / 64 | 59 | 1.945e-11 | I183 `run_04a` |
| run_08_on_stage_b | on | full grid, stage b (`dd_qd`) | 1 | 1221 | 68 | 0 of 1 | ['dd_qd'] | - | 22 | 0 / 20 / 2 | 11 | 5.496e-15 | I183 `run_03b` |
| run_09_off_stage_a | off | full grid, stage a | 0 | 136 | 97 | 15 of 15 | [] | - | 0 | 0 / 0 / 0 | 0 | 1.332e-15 | I183 `run_04a` |
| run_10_off_stage_b | off | full grid, stage b | 0 | 131 | 72 | 1 of 1 | [] | - | 9 | 0 / 9 / 0 | 0 | 0.000e+00 | I183 `run_03b` |
| run_11_off_global | off | `conical_global.py` | 0 | 738 | 195 | 17 of 17 | [] | all fired on target only | 0 | 0 / 0 / 0 | - | - | I190 `run_11_base_global` |
| run_12_on_global | on | `conical_global.py` | 1 | 2470 | 190 | 16 of 17 | ['scan'] | all fired on target only | 104 | 0 / 0 / 50 | - | - | I190 `run_11_base_global` |
| run_13_off_loglog | off | `conical_loglog.py` | 0 | 520 | 104 | 20 of 20 | [] | all fired on target only | 0 | 0 / 0 / 0 | - | - | I190 `run_09_base_loglog` |
| run_14_on_loglog | on | `conical_loglog.py` | 1 | 1553 | 104 | 19 of 20 | ['basin'] | all fired on target only | 4 | 1 / 0 / 3 | - | - | I190 `run_09_base_loglog` |
| run_15_off_ctl | off | `ctl`, 16 checks | 0 | 77 | 78 | 16 of 16 | [] | - | 0 | 0 / 0 / 0 | 0 | 1.332e-15 | I190 `run_06_base_offgrid_ctl` |
| run_16_early_ctl | early | `ctl`, 16 checks | 1 | 89 | 79 | 14 of 16 | ['regress167', 'scan'] | - | 50 | 3 / 1 / 11 | 13 | 7.467e-12 | I190 `run_06_base_offgrid_ctl` |
| run_17_late_ctl | late | `ctl`, 16 checks | 0 | 85 | 79 | 16 of 16 | [] | - | 4 | 3 / 1 / 0 | 0 | 7.467e-12 | I190 `run_06_base_offgrid_ctl` |
| run_18_ungated_ctl | ungated | `ctl`, 16 checks | 1 | 2087 | 75 | 15 of 16 | ['regress167'] | - | 8 | 5 / 1 / 2 | 4 | 7.467e-12 | I190 `run_06_base_offgrid_ctl` |
| run_19_on_controls | on | `--controls-only locator-side,plant-locator,n-drift,recip-dd` | 1 | 3547 | 80 | - | - | 2 fired | - | - | - | - | I183 `ctl_run_03` |
