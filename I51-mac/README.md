# I51-mac: the coordinator's review of #51's reading gaps and rerun searches for the novelty check

Machine: macOS (the coordinator's Mac, arm64), Python 3.14, at nice 10 with at most 2 processes.
Issue: https://github.com/nmoinvaz/negative-mass/issues/51. Reviewed raw `I51-rpi5` at baa0650 (no repository branch).

## Independent check `ind51.py` (criteria written before its first run)

ind51 shares no code with `rerun_queries.py`, `make_quotes.py` or `make_queries_md.py`. It fetches its sources itself
(GET only, a generic client name) and reads them with its own patterns. For DG08 it reads the copies in `I149-rpi5`,
whose sha256 the coordinator's `I149-mac/ind149.py` verified against fresh fetches. Shared with #51: the list of sources
and the findings tested.

| id | criterion | kind |
|---|---|---|
| K1 | arXiv lists 2608.24577 with a v2 dated 26 Oct 2026; its v1 TeX contains "0.63" and "0.995"; its v2 TeX contains neither, and contains "no sign of instability" | text |
| K2 | the abstract of Paranjape's "Puzzles with Negative Mass" (INSPIRE or Springer) contains "dynamically stable configuration" and not the word "possible" | text |
| K3 | the arXiv abstract of 1204.1269 contains "Havas and Goldberg" and "equivalent" | text |
| K4 | arXiv:2611.14482 (abstract or e-print) contains "nonradial perturbations" with "forthcoming", and "stable only for" | text |
| K5 | DG08 (`I149-rpi5/dg08_v1..v3`): v2 and v3 contain "We will set" next to the 1/ψ definition and "missing in the spectrum"; v1 contains "We will set" and not "missing in the spectrum" | text |
| K6 | the Price 1993 DOI (10.1119/1.17293) does not give the article text here: an HTTP error, or a page without the article body | observation turned criterion |

Mutations, each must exit 1 with its target failing: `v2num` (0.995 required in v2; K1), `possible` ("possible" required
in Paranjape's abstract; K2), `havas` ("Havas and Goldberg 1963" required; K3), `laguna` ("radial perturbations of
singustars in a forthcoming" with "radial" alone, so "nonradial" must not match; K4).

## Results
