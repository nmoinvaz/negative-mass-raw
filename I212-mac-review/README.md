# I212-mac-review: the coordinator's review of #212 (rerun, independent check ind212)

Machine: macOS (the coordinator's Mac, Apple M5, arm64), Python 3.14.7 (`/Users/nathan/Source/negative-mass/.venv`:
numpy, scipy, sympy, mpmath 1.3.0), nice 10, at most 2 processes. Issue:
https://github.com/nmoinvaz/negative-mass/issues/212. Under review: branch `wip/i212-black-universe` at 08a414d, raw
`I212-rpi5` at c50bd64. Written 2026-11-27 before the first run of `ind212.py` and before the rerun.

## Rerun

`rerun.sh`, from a detached worktree `~/Source/negative-mass-r212` at 08a414d, in `notes/black_universe`, in two chains
of one process each. It runs `stability.py check`, `planted`, `spectral` and `controls`, and `count c --res=R1|R2` for
every member of record. The expectation, written now: the same verdicts, counts and printed W as the Pi's, with digits
past the declared tolerances allowed to differ. scipy's integrators and BLAS are not bitwise portable between
aarch64 Linux and macOS.

## ind212: an independent eigenvalue count for the members without a throat

#212 counts by shooting with Brent refinement and checks by Chebyshev collocation. ind212 uses a third method:
- the Schrödinger form u_xx = (V̂ + W²)u of #212's note, §2, in the tortoise coordinate dx = dρ/A (b = 1);
- the background A(ρ) of its §1, with 3m = −2c/π;
- ρ(x) from dρ/dx = A, by scipy's DOP853 at rtol 1e-13;
- second-order finite differences on a uniform x grid with Dirichlet ends at x = ±X, X = 400;
- the lowest eigenvalue λ₀ of the symmetric tridiagonal matrix by `scipy.linalg.eigh_tridiagonal`, at h = 0.02 and
  0.01, then Richardson-extrapolated.

A growing mode is λ₀ < 0, with W = √(−λ₀).

It shares with #212 the background and V̂, which #212 checked against [BKZ12] (40) and (41) in sympy. It shares no
integrator, boundary treatment, root finder or spectral code. The u-form has the wall 2A²/ρ² at a throat, so ind212
covers only the members with no throat in the static region: c = −10, −3, −2, −1.5, −1.1, −1.01, −1.001, −1.0001
and −1.

## Criteria (each coded as worded; each can fail)

| id | criterion |
|---|---|
| K1 | For each of the nine members, ρ_h (the largest root of A) and κ = A′(ρ_h)/2, computed here from §1's A, equal #212's table to 1e-6 |
| K2 | At c = −10 … −1.0001, ind212 finds exactly one eigenvalue below −1e-6 at both grids (λ₀ < −1e-6 ≤ λ₁), and its extrapolated W agrees with #212's table to 1e-5 relative. At c = −1 it finds none (λ₀ ≥ −1e-6 at both grids) |
| K3 | ind212's W at c = −1.0001 equals κ there to within 1e-3 relative: the claim that W → κ as c → −1⁻ |

## Mutations (`--mutate=NAME`; each must make ind212 exit non-zero with exactly these criteria failing)

The targets are predicted from the code, not yet computed. A mutation that misses its targets is reported.

| mutation | change | targets |
|---|---|---|
| `wrong-V` | the term A²/R⁴ of V̂ doubled | K2, K3 |
| `wrong-m` | 3m = −2c/π replaced by −c/π, which breaks asymptotic flatness, moves ρ_h and κ | K1, K2, K3 |
| `short-X` | X = 20 (the bound state is cut) | K2 |

## Amendments

**A1, 2026-11-27, after run 1's mutations.** `wrong-m` crashed (`max()` of no roots): with the wrong mass, A has no
root on [−60, 60] at c = −10, and `horizon()` raised before any criterion was reported. A member with no horizon now
fails K1 and K2, where it used to stop the program. No bar, member, grid or tolerance changes. Run 2 reruns the base
case and the three mutations with A1.

## Runs (filled in as they are done)

| file | what |
|---|---|
