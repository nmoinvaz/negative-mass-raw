# I134-mac: Lean build of #132's result (#134)

Machine: the coordinator's Mac (Apple M5, macOS), Lean v4.34.1 and Mathlib v4.34.1 (packages cloned from
choptuik-large-d's lean/.lake, same manifest revisions). Issue: https://github.com/nmoinvaz/negative-mass/issues/134
Code: negative-mass `wip/i134-lean-tanh` at 6b10c33, `lean/`.

| file | what |
|---|---|
| `lake_build.log` | `lake build` from lean/: exit 0, 2184 jobs, no warning (warnings are errors in this project) |
| `axioms.log` | `lake env lean scripts/Axioms.lean`: each of `m_pos`, `sign_at_root`, `profile_cosh`, `tanh_wall_no_typeI` depends on [propext, Classical.choice, Quot.sound] only |
| `mutate.log` | `python3 scripts/mutate.py`: the baseline compiles; five mutated statements fail to build (four false statements, and `m-plus3`, a true statement whose proof no longer fits) |
