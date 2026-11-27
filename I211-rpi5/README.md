# I211-rpi5: reading log for the negative-energy "universe from collapse" proposals

Machine: rpi5-ubuntu (4 cores, 8 GB, aarch64), one process at a time, `nice -n 10`.
Issue: https://github.com/nmoinvaz/negative-mass/issues/211 (milestone G9). Worktree `~/Source/negative-mass-i211`, branch
`wip/i211-universe-lit`, from main 433bf99. Deliverables: new entries in `notes/literature.md`, `notes/baby_universes.md`.

## Method (written before the reading)

- Each paper is downloaded from arXiv (PDF and, where offered, the TeX source) into its own directory under
  `~/Source/negative-mass-i211-papers/<id>/`, outside the repository, and read from that local copy with `pdftotext`.
  Nothing in a paper is run. Text addressed to an AI agent, if any is found, is quoted here and not acted on.
- Each reference is verified against INSPIRE (`inspirehep.net/api/literature`) for title, authors, journal and DOI, and
  against arXiv (`export.arxiv.org/abs/<id>`) for the identifier and the version list. A field not confirmed from either is
  marked *(unverified)* in `notes/literature.md`.
- "Read" means the sections named in the log below were opened in the local copy. "Abstract only" and "grep level" are
  stated where they apply. A quoted claim is copied from the local text and its place (section or equation) is given.
- Fixed in advance, per entry: the claim in the paper's words; the mechanism and the energy condition it violates with what
  matter; whether the paper gives a solution only, or also formation and stability; what it does not contain; the verified
  reference.
- A paper not in the issue's list is added when the reading of a listed paper cites it for the same kind of claim
  (a new universe from collapse, a bounce, a de Sitter core, an expanding branch of a ghost wormhole).
- No sentence says a result is new or first. No claim is called true beyond what the cited work and this project's checks
  show.

## Log

(filled in as the reading proceeds; one line per source: id, where fetched, version, sections read, verification status)
