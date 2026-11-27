| script | arm | exit | checks | controls | wall (s) | max rss (MB) | load at start |
|---|---|---|---|---|---|---|---|
| conical_global.py (checks and controls) | base | 0 | 17 passed, 0 failed | all fired on target only | 1814 | 181 | 1.08 1.06 1.07 |
| conical_global.py (checks and controls) | on | 0 | 17 passed, 0 failed | all fired on target only | 1856 | 181 | 1.01 1.04 1.07 |
| conical_loglog.py (checks and controls) | base | 0 | 20 passed, 0 failed | all fired on target only | 1534 | 98 | 1.09 1.08 1.12 |
| conical_loglog.py (checks and controls) | on | 0 | 20 passed, 0 failed | all fired on target only | 1201 | 98 | 1.09 1.12 1.14 |
| conical_offgrid.py --grid=ctl --no-controls | base | 0 | 16 passed, 0 failed | - | 680 | 99 | 0.95 1.54 1.28 |
| conical_offgrid.py --grid=ctl --no-controls | off | 0 | 16 passed, 0 failed | - | 317 | 72 | 1.03 1.03 1.03 |
| conical_offgrid.py --grid=ctl --no-controls | on | 0 | 16 passed, 0 failed | - | 162 | 72 | 1.03 1.05 1.08 |
| conical_offgrid.py --grid=ctl --no-controls | on (rebased head) | 0 | 16 passed, 0 failed | - | 162 | 72 | 1.69 1.69 1.37 |
| conical_offgrid.py --grid=ctl --controls-only n-drift,recip-dd | base | 0 | - | all fired on target only | 1370 | 72 | 1.04 1.07 1.12 |
| conical_offgrid.py --grid=ctl --controls-only n-drift,recip-dd | on | 0 | - | all fired on target only | 626 | 72 | 1.17 1.10 1.08 |
