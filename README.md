# negative-mass-raw

Raw run output of [negative-mass](https://github.com/nmoinvaz/negative-mass): logs, per-point records (jsonl), states
(npz), checkpoints and attempts files, one folder per task and machine. The code repository keeps only what is derived
from them (tables, graphs, notes), naming the folder and commit where it uses them. [INDEX.md](INDEX.md) lists every
folder and what it holds.

## Layout

- One folder per task and machine: `I<issue>-<machine>/`, for example `I12-win2/`, where the issue is the task's issue
  in negative-mass. A task run on two machines has two folders.
- Every folder starts with a `README.md` whose first line is `# <folder>: <what it holds>`, followed by the machine,
  the checkout or worktree, and the issue's URL.

## Adding output

Clone this repository next to the code checkout, once:

    git clone git@github.com:nmoinvaz/negative-mass-raw.git ../negative-mass-raw

Point the run's output paths into its folder, and write the folder's `README.md` before the run. At each post and at
the end, from this repository's root:

    python3 make_index.py && git add <folder> INDEX.md && git commit -m "<folder>: ..." && git pull --no-rebase && git push

Add to your own folder only, never force-push, and keep each file under 90 MB. Only negative-mass's task output goes
here: nothing from another project, no credentials or personal files. `python3 make_index.py --check` exits 1 when
INDEX.md is stale or a folder's README.md is missing or malformed.
