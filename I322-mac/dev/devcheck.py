import sys
mut = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != "none" else None
sys.argv = ["remainder.py", "check", "--only=P1,P2,P3,D1,D2,D4", "--cache=/private/tmp/claude-501/-Users-nathan-Source-negative-mass-i322/07a7c86f-beae-4b72-bf6b-2793fd26190f/scratchpad/cache"] + ([f"--mutate={mut}"] if mut else [])
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i322/notes/black_universe")
import numpy as np
import remainder as rm
rm.horizon_series = lambda ro: (np.arange(20, 100), np.linspace(8, 24, 80), np.linspace(1, 2, 80))
sys.exit(rm.run_checks())
