# I192-mac design: `multishoot::table`, Taylor tables of coefficient functions along a path

Status: **design for review** (stage 1). No library code is written. Everything below that is a number came from a prototype outside the library: `proto_table.py` (the rule
in 90-digit decimal arithmetic, planted problems, controls, a plane stepper) and `exp_locate/` (Rust, multisolver 0.3.0). The criteria were committed before the first run
(README, raw 4ccb6cf1); amendment A1 records what changed after it. Raw folder: `negative-mass-raw/I192-mac`.

## Answer

- **The rule is #186's tail test, generalized.** `multisolver::locate` does not replace it (section 3): it is 20 times slower, it has no answer for an entire function whose
  truncated series still needs a finite width, and it is `Unresolved` on the one planted series where the tail test is blind. The table stores series and cuts each step
  at `fraction` of the width at which the stored series have converged to `tail`. The library knows nothing of J, stars or polar.
- **Planted problems pass the bars written beforehand** with 20 to 700 times to spare (the tightest is a conjugate pair ahead, 1/21 to 1/39 of the bar). Each control fires
  on its target except one, which was a no-op and is replaced (section 7).
- **One result to decide on** (section 4): the plane stepper through the table passes at the default `fraction` 0.3 in f64, dd and qd, but its steps reach past the table's
  converged width in dd (6 of 90 steps, up to 1.03 w) and qd (22 of 95, up to 1.13 w); fraction 0.7 fails the bar in dd. The coupling is real; a hard limit needs a change to
  `plane::JetSource` (an option, not in this PR unless you want it).
- **Estimate** revised: 7 to 10 h (stage 1 took about 1 h; stage 2 about 3 to 4 h; stage 3 about 3 to 5 h, mostly the two builds' 13-minute check runs and the repin comparison).

## 1. API

```text
 the caller's functions        multishoot::table                     the consumers
┌─────────────────────┐     ┌────────────────────────┐     ┌──────────────────────────────┐
│ impl SeriesSource<T>│────▶│ Table::<T>::build      │────▶│ Table::shifted(x0, f, kj, ..)│
│  series(x0, dir, nb)│     │  one series per step,  │     │ TableJets: plane::JetSource  │
│  -> valid_to        │     │  cut by its own width  │     │ the crate's own JetSource    │
└─────────────────────┘     └────────────────────────┘     │  (J0 + s² J1, then shift)    │
                                                           └──────────────────────────────┘
```

```rust
/// What the caller supplies: the Taylor series of its F functions about any point of the path.
pub trait SeriesSource<T: Real> {
    fn functions(&self) -> usize;
    /// Coefficients 0..nb of every function about x0, `out[f * nb + k]`, for a path running in direction `dir` (+1 or -1);
    /// at a boundary of the source's own pieces, the piece that starts at x0 in that direction. Returns the farthest point,
    /// in that direction, up to which these series hold (the end of the piece), or +-infinity.
    fn series(&self, x0: f64, dir: f64, nb: usize, out: &mut [T]) -> f64;
}

pub struct Opts { pub nb: usize, pub tail: f64, pub last: usize, pub fraction: f64, pub hmax: f64, pub atol: f64, pub max_steps: usize,
                  #[cfg(feature = "mutate")] pub control: TableControl }
impl Opts { pub fn new(nb: usize, tail: f64) -> Opts }          // last 2, fraction 0.3, hmax inf, atol 0, max_steps 1_000_000

pub enum Error { NotFinite { x: f64, f: usize, k: usize }, Stall { x: f64 }, TooManySteps { x: f64 } }

pub struct Table<T: Real> { /* dir, nb, start[], end[], width[], c[(step * F + f) * nb + k] */ }
impl<T: Real> Table<T> {
    pub fn build<S: SeriesSource<T>>(src: &S, xa: f64, xb: f64, opts: &Opts) -> Result<Table<T>, Error>;   // xb < xa runs backward
    pub fn steps(&self) -> usize;  pub fn functions(&self) -> usize;  pub fn nb(&self) -> usize;
    pub fn bounds(&self, i: usize) -> (f64, f64);           // the step's start (the series' centre) and end, in path order
    pub fn width(&self, i: usize) -> f64;                   // the converged width found at the start (at most limit / fraction)
    pub fn find(&self, x: f64) -> Option<usize>;            // the step holding x; a boundary belongs to the step that starts there
    pub fn series(&self, i: usize, f: usize) -> &[T];       // stored coefficients about the step's start
    pub fn shifted(&self, x0: f64, f: usize, kj: usize, out: &mut [T]);   // jets of f about x0 (kj <= nb), delta = x0 - start exact in T
    pub fn headroom(&self, x0: f64) -> f64;                 // width(i) - |x0 - start(i)|: how far a step from x0 stays inside the width
    pub fn map<U: Real>(&self, conv: impl Fn(T) -> U) -> Table<U>;         // a table built in dd, used in f64 (U::from_dd)
}
pub fn shift<T: Real>(c: &mut [T], delta: T, kj: usize);    // the polynomial's first kj coefficients about its start + delta
pub struct TableJets<'a, T: Real> { pub table: &'a Table<T>, pub pattern: Vec<(usize, usize)> }   // function e <-> pattern entry e
impl<T: Real> plane::JetSource<T> for TableJets<'_, T> { .. }
```

- **Scalar.** `plane::Real` (f64, DD, QD, OD): the table is generic over it and holds coefficients in the lane. Building in DD and `map`-ping to f64 is #186's `to_lane`.
- **A crate with a parameter** (J0 + s² J1 in #186) stores two functions per entry and combines them before `shift`, as `JTable::jets` does now; `shift` is public for that.
- **`valid_to`** is what lets a source with its own pieces (the star's Taylor steps) say where its series stop holding; a step never ends past it. A source without pieces returns infinity.
- **Errors, not panics.** `Stall`: a step that does not move x (a singularity on the path: PG stalls at x = 4.999999999999993 in f64, 4.999999999999989 in dd and 4.999999999999988 in qd, after 574, 855 and 972 steps); `NotFinite`: a coefficient
  that is NaN or infinite, naming the function and order; `TooManySteps`. #186's `h < 1e-14 b => step = the star step` is **not** carried over: it hides a stall by jumping to the piece end.
- Files of the PR: `src/table.rs` (new), `src/lib.rs` (module and docs), `src/control.rs` (`TableControl`), `tests/table.rs`, `README.md` (a section). No other module changes.

## 2. The rule

For the series `c_0 .. c_(nb-1)` of every function about the step start b, `t_k(h) = |c_k| h^k` and `S(h) = sum_k t_k(h)`. The **width** `w` is the largest `h <= cap` with
`t_k(h) <= tail * S(h) + atol` for k = nb - last .. nb - 1, for **every** function. The step is `min(fraction * w, limit)`, with `limit = min(|valid_to - b|, |xb - b|, hmax)` and
`cap = limit / fraction`, so a series that converges past `limit` ends the step at `limit`. Breakpoints are f64.

| parameter | meaning | #186's value | default |
|---|---|---|---|
| `nb` | coefficients stored per function | 30 | none (the caller's) |
| `tail` | the last orders' share of the sum | 1e-25 | none |
| `last` | how many trailing orders are tested | 2 | 2 |
| `fraction` | the step's share of the width (headroom for a consumer's step) | 0.3 | 0.3 |
| `hmax`, `atol` | longest step; an absolute floor under the test (a function that is zero up to noise) | none, none | inf, 0 |

- **Monotone, so bisection.** Each `t_k / S` is nondecreasing in h wherever k exceeds the weighted mean order, so the test passes on an interval [0, w]; the library bisects on h:
  it halves down from `cap` until the test passes, then bisects between that h and 2h (53 steps), so the resolution is relative to w, not to `cap`. (The prototype bisects on [0, cap] in 110 steps: the
  same function found differently, which C3 checks through the breakpoints.)
- **Scaled, IEEE only.** Each term is formed from (mantissa, power of two) pairs aligned to the largest, so `|c_k| h^k` never leaves f64's range; no libm, so the breakpoints are
  the same bits on every backend. PS shows why: with `1/(1 + 1e5 x)` in qd (c_58 = 1e290), the plain f64 test underflows `h^58`, sees zero last terms and gives the whole path as one step (E = 1.0).
- **`last` is a blind spot, not a bug to hide.** A series whose last `last` coefficients vanish by symmetry (PE: `1/(1-x^3)` about 0, c_28 = c_29 = 0) passes the test at any h: the first step runs to `hmax`, past
  the pole. With `last` 3 it is correct (63 steps in dd). The default stays 2 to reproduce #186; a source with a symmetry of period p needs `last` >= p + 1.
- **Cost.** One source evaluation per step (the step end is the next start) plus 110 evaluations of the test, nb F terms each: 5 µs per function at nb 30, against 110 µs for `locate`.

## 3. A tail test or `locate`

D1 (`dev_02`): f64, nb 30, tail 1e-25. W is the tail test's width, R the radius; `locate` with its default options.

| series | W/R, last 2 | W/R, last 4 | `locate` | its bar |
|---|---|---|---|---|
| 1/(1-u) | 0.129 | 0.110 | Real, \|s\| = 1 | 1.8e-15 |
| 1/(1-u)^2, ^3 | 0.114, 0.104 | 0.097, 0.088 | Real, 1 | 1.8e-15 |
| (1-u)^(1/2) | 0.160 | 0.139 | Real, 1 | 1.8e-15 |
| pair at angle 0.6, 0.05 | 0.126, 0.116 | 0.111, 0.098 | Pair, 1 | 6.8e-15, 1.6e-10 |
| 1/(1-u^2) | 0.128 | 0.109 | Real, 1 | 1.5e-11 |
| 1/(1-u) + 1/(1+u/1.2) | 0.131 | 0.112 | Real, 1 | 1.8e-15 |
| 1/x^2 about 1e-3 (coefficients to 1e90) | 0.114 | 0.097 | Real, 1e-3 | 3.0e-18 |
| e^u, e^(10u) (entire) | W = 1.53, 0.153 | | **Unresolved** | |
| 1/(1-u^3) (period 3) | **W = cap** (blind) | 0.119 | **Unresolved** | |

`locate` is accurate where it resolves (its estimator-range bar is 1e-15 to 1e-10 of |s|), but **a table needs the width at which the truncated stored series converged, not the radius**:
for e^u the radius is infinite and the width is 1.53, so a tail test is needed whatever `locate` says. It costs about 110 µs against 5 µs. And it does not see the one planted case where
the tail test is blind (1/(1-u^3): `Unresolved`), so it is no guard (the decision rule written before the run: a guard only if it resolves that series). The width over the radius lies in
[0.104, 0.160] for every resolved series, a spread of 1.5.
**Use of `locate`:** none in the rule. As an independent check it is cheap and optional (criterion C6: width / \|s\| of PA's `1/x` and PC in [0.09, 0.17], dd). Say if you want it; it adds a test
dependence on `multisolver::locate` and its failure mode (confidently wrong near the noise floor) to a test.

## 4. The consumer's reach (PH): the one open design point

The table promises the stored series are converged to `tail` out to the width w from the step start. A consumer's step from x0 inside a table step reaches
`|x0 - start| + h <= fraction * w + h`. With `fraction` 0.3 that is within w only while the consumer's own step h is at most 0.7 w. The planner's step is set by the plane's tolerance, not by the table, so
they are coupled: PH is `y' = (M/x) y` (a pole behind the path, exact solution), `Plane::advance` at its default plan (tol 100 eps, kt = optimal, kj = kt), table of `1/x` with `nb = kt + 12`, `tail = eps_lane`.

| lane | kt | table steps | plane steps | plane error (bar) | ln_vol error (bar) | max (shift + step) / w | steps past w |
|---|---|---|---|---|---|---|---|
| f64 | 22 | 116 | 86 | 3e-67 (1.1e-12) | 1.6e-14 (1.1e-11) | 0.92 | 0 |
| dd | 42 | 150 | 90 | 6e-66 (1.2e-28) | 1.6e-30 (1.2e-27) | 1.03 | 6 |
| qd | 80 | 186 | 95 | 1.5e-66 (1.5e-60) | 2.0e-62 (1.5e-59) | 1.13 | 22 |

(Decimal arithmetic: the errors are truncation only; the lanes' roundoff is added in the library test.) Fraction at dd: 0.2 passes (0 past w, 222 table steps), 0.3 passes, 0.5 passes (25 past, up to
1.25 w, 92 table steps), **0.7 fails** the log-volume bar (1.0e-26 against 1.2e-27, 57 past, 1.44 w), **1.0 fails** (1.0e-23, 1.61 w). So 0.3 passes here with a factor 1e3 to spare in dd (and passes #186's T3), and the coupling is a property to document: **a table's `fraction` has to leave room
for the consumer's longest step**, `fraction <= 1 - h_consumer / w`; for this plane at tol 100 eps the sweep passes up to 0.5 and fails at 0.7. The default stays 0.3, reported with this table.

**Option L (not in this PR unless you say so).** `JetSource::limit(&self, x0, dir) -> f64` with a default of infinity, and `Plane::advance` caps each step at it; `TableJets::limit` returns the headroom.
The reach is then at most w by construction and `fraction` only has to keep the cap positive. It changes `plane.rs` (a backward-compatible default method, a control `NoLimit`, a test), which #189's merged
code owns. Without it the crate has no way to cap a plane step, and relies on `fraction`.

## 5. Lanes

f64, DD, QD and OD through `plane::Real`; no other trait is needed. Planted lanes and parameters (nb, tail): f64 (20, 1e-13), dd (30, 1e-25), qd (60, 1e-55), and od (100, 1e-115) as one smoke case
(PC; PA at 1e-3 would put c_99 at 1e305, the edge of f64's range). The table's own arithmetic is the lane's plus f64 IEEE operations; the step points and coefficients are digested (FNV over every part) in
the tests and compared bitwise on the default build (aarch64 NEON on this Mac) and `--features portable`; `+avx2,+fma` cannot run here and is not run.

## 6. Planted problems and criteria

The functions are rational: coefficients about any point by recurrence, references in closed form, in the lane; none shares code with the table. Prototype step counts in the table (these become C3):

| case | functions, path | f64 | dd | qd |
|---|---|---|---|---|
| **PA** poles behind, source pieces of length 6 | 1/x², 1/x, 1/(30-x); [1e-3, 25] | 221 | 315 | 344 |
| **PB** a piece boundary the series cannot cross | 1/(30-x) + 3 (x-5)₊²; [0, 20], `valid_to` 5 | 14 | 23 | 29 |
| **PC** a conjugate pair ahead | 1/((x-12)² + 0.04); [10, 14] | 106 | 157 | 178 |
| **PD** no singularity, width set by nb | (1 + x/4)^40; [0, 3] | 37 | 31 | 1 (degree 40 < nb: exact) |
| **PE** the blind spot | 1/(1-x³); [0, 0.9], hmax 0.5 | n/a | `last` 2: 42 (fails), `last` 3: 63 | 48 (fails), 70 |
| **PF** backward | PA's, [25, 1e-3] | 213 | 306 | 334 |
| **PG** a singularity on the path | 1/(x-5); [0, 10] | Stall 574 steps | Stall 855 | Stall 972 |
| **PP** a polynomial from a non-dyadic start | 1 + 2x + 3x² - x⁴; [0.1, 3] | 1 | 1 | 1 |
| **PS** scale | 1/(1 + 1e5 x); [0, 1], qd only | | | 346 |
| **PH** plane through the table | section 4 | 116 | 150 | 186 |

- **C1, the jets.** For every step, function, x0 = start + t (len) and h = u max(0, min(0.7 w, valid_to - x0)) (t, u in 0, 1/4, 1/2, 3/4, 1): `|sum jets_k h^k - f(x0 + h)| / sum |jets_k| h^k <= 10 tail`.
  Prototype maxima against the bar: PA 4.6e-15/1e-12, 1.9e-27/1e-24, 1.4e-57/1e-54; PB 1.5e-14, 3.8e-27, 2.0e-57; PC 4.6e-14, 2.6e-26, 2.8e-56; PD 3.4e-16, 6.1e-29; PF 3.6e-15, 1.6e-27, 1.3e-57;
  PP, PD qd at the decimal floor; PS qd 1.2e-57 (bar 1e-54); PE with `last` 3: 2.1e-28 (dd), 1.5e-58 (qd). PE with `last` 2 fails (infinite: the reach crosses the pole), as recorded.
- **C2, the structure.** Contiguous bitwise, first start xa and last end xb bitwise, direction, no step past `valid_to`, `len <= fraction w (1 + 1e-12)`, and `len >= fraction w (1 - 1e-6)` unless cut. The test recomputes w from the stored series with the nominal tail by its own bisection.
- **C3, an independent step list.** Count and breakpoints (every 20th, within 1e-9 relative) from `proto_table.py` for PA, PB, PC, PD, PF, PS, PH; shares the rule's definition, not the code.
- **C4, PH.** As in section 4, with the bars as #189's (1e4 eps, 1e4 eps max(1, ref)).
- **C5, errors.** PG: `Err(Stall)` with x within 1e-9 of 5, from below; the pole moved to 15 gives Ok (19, 28, 32 steps). A NaN at function 2, order 7 gives `NotFinite { f: 2, k: 7 }`.
- **C6 (optional).** Width / `locate`'s \|s\| in [0.09, 0.17].

## 7. Controls and their computed effects

Library controls (`mutate`, `TableControl`, set on `Opts` for the build ones and on the table for lookup ones); effect = the largest C1 E (bar 10 tail) and C2's `len / (0.3 w)` (must be <= 1), prototype, dd unless stated.

| control | what it breaks | computed effect | declared target |
|---|---|---|---|
| `Wide` | step = `limit` (to `valid_to` or `hmax`), the width ignored: #186's `wide_table` | PA E 8e88 (C2 1.7e5); PB 6.4e-9 (C2 12); PC 1.0 (C2 53); PD f64 0.37, dd 7.8e-5; PF E inf | C1, C2 in PA, PB, PC, PF, PD (f64, dd); **silent** on PD qd, PP (their width is the cap), and in PH it runs away (3000 plane steps, stopped), so PH does not run it |
| `FractionOne` | fraction 1 | PA E 1.6e-20 (f64 1.9e-10, qd 9.6e-44); PB 2.8e-20; PC 2.0e-19; PD dd 1.0e-22; C2 3.33; PH dd ln_vol 1.0e-23 (bar 1.2e-27), qd 1.1e-45 (1.5e-59) | C1, C2, PH in dd and qd; **PH f64 silent** (1.6e-12 against 1.1e-11) |
| `LooseTail` | tail 1e-5 | PA 6.8e-6 f64, 1.1e-5 dd, 4.7e-5 qd; PB 2e-4 to 7e-4; PC 2e-5 to 1e-4; PD 5e-7; PH dd 1.0e-24 (bar 1.2e-27), qd 5.9e-38 (1.5e-59) | C1 in every case with a finite width; C2 only if it recomputes with the nominal tail; PH dd, qd; **PH f64 silent** (3.2e-14) |
| `IgnoreValidTo` | steps cross `valid_to` | PB E 126 (f64), 9.5 (dd), 27 (qd); C2: 1 step crosses 5; PA and PF: 4 steps cross 6, 12, 18, 24 and C1 is silent (analytic across) | PB: C1 and C2; PA, PF: C2 only |
| `NoShift` | the lookup does not shift | PA 0.06 to 0.09; PB 67 to 384; PC 0.08 to 0.16; PD f64 0.85, dd 1.1 (qd 5e9); PP 39 | C1 everywhere |
| `ShiftF64` | the shift's delta formed in f64 | **PA, PB, PC, PD, PF: silent in every lane** (Sterbenz: the f64 difference of nearby f64 numbers is exact). PP: 4.6e-16 against 1e-24 (dd) and 1e-54 (qd) | **PP in dd and qd only**; silent in f64 by design. A no-op control would have passed unnoticed (#187 had two) |
| `Unscaled` | the plain f64 tail test | PS qd: one step [0, 1], E 1.0 (bar 1e-54) | C1 on PS |

In the test, wrong inputs: `ref_scale` (the reference times 1 + 1e-4: E 1e-4 everywhere), `pole_off_path` (C5's).

## 8. What is reused, and what is not

| from | what | use |
|---|---|---|
| multishoot `plane` | `Real`, `JetSource`, `Jets`, `Entry`; `Plane::advance` | the scalar and the consumer interface; PH runs through them. `TableJets` is a `JetSource` |
| multishoot `taylor` | `Plan`, `step_from_norms`, `kth_root` | not used: the planner's step is a closed form for absolute `e_k h^k <= tol`; the table's test is relative to a sum that depends on h, hence a bisection. The planner's *idea* (last two orders) is the rule's |
| multishoot `implicit::taylor_shift` | shifts a polynomial about 0 by an f64 | not used: the shift must be the exact difference of two f64 in the lane (a dd lane needs it for steps longer than the start; PP), so `table::shift` is written in the lane's type, as the crate's own |
| multishoot `interp`, `jet` | trigonometric interpolation; series in a parameter of the residual | read; no overlap |
| multisolver `locate` | the nearest singularity | section 3: not in the rule; optional in a test |
| multidouble | `DD`, `QD`, `OD` | through `Real` |

## 9. Found while designing (reported, not fixed in the crate)

1. #186's `build_table` has `x1 = if ... || h < 1e-14 * b { st.x1 }`: a step too small to be real jumps to the end of the star step, which hides a singularity at b. The library returns `Stall`.
2. #186's `width_of` forms `|c_k| h^k` in plain f64 (fine at nb 30, x >= 1e-3, wrong at nb 60 with c_58 = 1e290: PS). The library scales.
3. The two-term tail test is blind to a period-3 symmetry (PE); a documented limit with `last`.
4. A **fraction** that is right for one consumer is wrong for a looser one (section 4); #186's 0.3 holds for the plane at tol 100 eps and fails at 0.7.
5. `ShiftF64` was a no-op on four planted cases (section 7).
6. (known, not mine) `plane.rs`'s doc says classical Gram-Schmidt; its loop is modified, twice.

## 10. Stages

- **Stage 2** (after approval): `src/table.rs`, `TableControl`, `tests/table.rs` (the criteria in the test's doc comment first, then the prototype's numbers as constants for C3, then the controls run once each to see them fire),
  README section; `cargo fmt`, `cargo clippy --all-targets --features mutate -- -D warnings` and with `portable,mutate`, tests on the default build and `--features portable`, digest compared bitwise; `+avx2,+fma` not run. PR with `gh pr create`, link on the issue, not merged.
- **Stage 3** (only on your word, after #188's crate work is merged): repin the crate to multishoot main (multidouble 6.1.0), flag off, compare every check of `taylor_polar.py` and #189's plane rows bitwise against the old pin and report any difference; then the J table behind a cargo feature, with `last` 2, tail 1e-25, nb 30, fraction 0.3 (so the step list should equal #186's apart from the removed `1e-14 b` jump), both builds' checks passing, `wide_table` still firing; a section `## #192: J's table from multishoot` in `taylor_polar.md`.

## 11. Decisions requested

1. **Approve the API and the rule** (sections 1 and 2), or name what to change.
2. **Option L** (section 4): leave `plane` as it is (the PR stays one module; `fraction` documented as a consumer-coupled parameter), or add `JetSource::limit` to this PR, or file it as its own task.
3. **`last` default 2** (reproduces #186; PE's blind spot documented) or 4 (robust to period 3, steps about 11 % shorter at the same `tail`).
4. **C6** (`locate` as an independent check in a test): include or drop.
5. **Controls:** `ShiftF64` declared on PP in dd and qd only; `Wide` not run through the plane in PH. Confirm.
