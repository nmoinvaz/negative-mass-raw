//! ind190: three planted implicit equations through multishoot::implicit (criteria in ../README.md).
//!     cargo run --release -- [--mutate=wrong-root|cross-at|fold-at]
use multishoot::implicit::*;
use multishoot::multidouble::qd::QD;
use multishoot::DD;

trait L: Real {
    const NAME: &'static str;
    const KT: usize;
    const TOL: f64;
    const BAR: f64;
    fn exp_(self) -> Self;
    fn cos_(self) -> Self;
    fn sin_(self) -> Self;
    fn sqrt_(self) -> Self;
}
impl L for f64 {
    const NAME: &'static str = "f64";
    const KT: usize = 22;
    const TOL: f64 = 1e-14;
    const BAR: f64 = 1e-9;
    fn exp_(self) -> f64 { self.exp() }
    fn cos_(self) -> f64 { self.cos() }
    fn sin_(self) -> f64 { self.sin() }
    fn sqrt_(self) -> f64 { self.sqrt() }
}
macro_rules! lane {
    ($t:ty, $n:expr, $kt:expr, $tol:expr, $bar:expr) => {
        impl L for $t {
            const NAME: &'static str = $n;
            const KT: usize = $kt;
            const TOL: f64 = $tol;
            const BAR: f64 = $bar;
            fn exp_(self) -> $t { <$t>::exp(self) }
            fn cos_(self) -> $t { <$t>::cos(self) }
            fn sin_(self) -> $t { <$t>::sin(self) }
            fn sqrt_(self) -> $t { <$t>::sqrt(self) }
        }
    };
}
lane!(DD, "dd", 42, 1e-30, 1e-25);
lane!(QD, "qd", 80, 1e-62, 1e-56);

/// N = sum_g A_g(x) y^a y'^b y''^c with polynomial A_g
struct Eq {
    pat: Vec<Mono>,
    polys: Vec<Vec<f64>>,
}
impl<T: Scalar> Coefficients<T> for Eq {
    fn pattern(&self) -> Vec<Mono> {
        self.pat.clone()
    }
    fn jets(&self, x0: f64, _kt: usize, out: &mut Jets<T>) {
        for (g, p) in self.polys.iter().enumerate() {
            let poly: Vec<T> = p.iter().map(|&c| T::from_f64(c)).collect();
            taylor_shift(&poly, x0, &mut out.ent[g].c);
            out.ent[g].n = poly.len();
        }
    }
}
fn e1() -> Eq {
    Eq { pat: vec![(0, 0, 2), (0, 0, 0)], polys: vec![vec![1.0], vec![-4.0, 4.0]] }
}
fn e2() -> Eq {
    Eq { pat: vec![(0, 0, 2), (1, 0, 1), (2, 0, 0)], polys: vec![vec![1.0], vec![-1.0], vec![-2.0]] }
}
fn e3() -> Eq {
    Eq { pat: vec![(0, 0, 3), (0, 1, 2), (0, 2, 1), (0, 3, 0)], polys: vec![vec![1.0], vec![-2.0], vec![-1.0], vec![2.0]] }
}

fn rel<T: L>(y: T, ye: T) -> f64 {
    ((y - ye).to_f64() / ye.to_f64()).abs()
}
fn walk<T: L>(eq: &Eq, y0: [T; 3], mode: Branch, x1: f64, cps: &[f64]) -> WalkOut<T> {
    let mut o = WalkOpts::new(T::KT, T::TOL);
    o.plan.hmax = 0.3;
    o.branch = mode;
    let mut w = Walker::<T, _>::new(eq, 0.0, y0, o);
    w.run(x1, cps)
}
/// pi/2 in the lane: Newton on cos from the f64 value
fn half_pi<T: L>() -> T {
    let mut x = T::from_f64(std::f64::consts::FRAC_PI_2);
    for _ in 0..4 {
        x = x + x.cos_() / x.sin_();
    }
    x
}

fn lane_checks<T: L>(mutate: &str, k: &mut [bool; 3], log: &mut Vec<String>) {
    let one = T::one();
    let r2 = T::from_f64(2.0).sqrt_();
    // K1: closed forms at the end point
    let mut cases: Vec<(&str, Eq, [T; 3], Branch, f64, Box<dyn Fn(T) -> T>)> = vec![
        ("E2-P Project", e2(), [one, r2, T::from_f64(2.0)], Branch::Project, 2.0, Box::new(move |x: T| (r2 * x).exp_())),
        ("E2-P Conserve", e2(), [one, r2, T::from_f64(2.0)], Branch::Conserve, 2.0, Box::new(move |x: T| (r2 * x).exp_())),
        ("E2-C Project", e2(), [one, T::zero(), -one], Branch::Project, 3.0, Box::new(|x: T| x.cos_())),
        ("E3-T Project", e3(), [T::from_f64(0.5), one, T::from_f64(2.0)], Branch::Project, 2.0,
            Box::new(|x: T| (x.mulf(2.0)).exp_().mulf(0.5))),
    ];
    let m0 = if mutate == "wrong-root" { T::from_f64(2.0) } else { one };
    cases.push(("E3-M Project", e3(), [one, one, m0], Branch::Project, 2.0, Box::new(|x: T| x.exp_())));
    cases.push(("E3-M Conserve", e3(), [one, one, m0], Branch::Conserve, 2.0, Box::new(|x: T| x.exp_())));
    for (name, eq, y0, mode, x1, ex) in cases.iter() {
        let out = walk::<T>(eq, *y0, *mode, *x1, &[]);
        let e = rel(out.y[0], ex(T::from_f64(out.x)));
        let ok = out.stop == Stop::End && e <= T::BAR;
        k[0] &= ok;
        log.push(format!("[{}] K1 {name}: stop {:?} at x = {}, {} steps, rel err {:.2e} (bar {:.0e}){}",
            T::NAME, out.stop, out.x, out.steps, e, T::BAR, if ok { "" } else { "  <-- FAIL" }));
    }
    // K2: the crossing of E2-C
    let out = walk::<T>(&e2(), [one, T::zero(), -one], Branch::Project, 3.0, &[]);
    let mut xc = half_pi::<T>();
    if mutate == "cross-at" {
        xc = xc + T::from_f64(1e-3);
    }
    let ok2 = out.crossings.len() == 1 && out.crossings[0].located && (out.crossings[0].x - xc).to_f64().abs() <= T::BAR;
    k[1] &= ok2;
    log.push(format!("[{}] K2 E2-C: {} crossing(s){}{}", T::NAME, out.crossings.len(),
        out.crossings.iter().map(|c| format!(", x = {:?} located {} (|x - pi/2| = {:.2e})", c.x.to_f64(), c.located,
            (c.x - half_pi::<T>()).to_f64().abs())).collect::<String>(), if ok2 { "" } else { "  <-- FAIL" }));
    // K3: the fold of E1
    let out = walk::<T>(&e1(), [T::zero(), T::zero(), T::from_f64(2.0)], Branch::Project, 2.0, &[0.9]);
    let xf = if mutate == "fold-at" { 0.99 } else { 1.0 };
    let ex1 = |x: T| {
        let u = one - x;
        u * u * u.sqrt_() * T::from_f64(8.0) / T::from_f64(15.0) + x * T::from_f64(4.0) / T::from_f64(3.0)
            - T::from_f64(8.0) / T::from_f64(15.0)
    };
    let cp = out.cps.iter().find(|c| (c.0 - 0.9).abs() < 1e-12);
    let ecp = cp.map(|c| rel(c.1[0], ex1(T::from_f64(c.0)))).unwrap_or(f64::INFINITY);
    let gap = xf - out.x;
    let stop_ok = matches!(out.stop, Stop::Tiny | Stop::Pivot | Stop::ZeroPivot);
    let ok3 = stop_ok && gap > 0.0 && gap <= 1e-3 && ecp <= 1e3 * T::BAR;
    k[2] &= ok3;
    log.push(format!("[{}] K3 E1: stop {:?} at x = {} (fold - x = {:.2e}), {} steps; at x = 0.9 rel err {:.2e} (bar {:.0e}){}",
        T::NAME, out.stop, out.x, gap, out.steps, ecp, 1e3 * T::BAR, if ok3 { "" } else { "  <-- FAIL" }));
}

fn main() {
    let mutate = std::env::args().find_map(|a| a.strip_prefix("--mutate=").map(str::to_string)).unwrap_or_default();
    let mut k = [true; 3];
    let mut log = Vec::new();
    lane_checks::<f64>(&mutate, &mut k, &mut log);
    lane_checks::<DD>(&mutate, &mut k, &mut log);
    lane_checks::<QD>(&mutate, &mut k, &mut log);
    for l in &log {
        println!("{l}");
    }
    let names = ["K1", "K2", "K3"];
    for (i, ok) in k.iter().enumerate() {
        println!("[{}] {}", if *ok { "PASS" } else { "FAIL" }, names[i]);
    }
    let bad: Vec<_> = names.iter().zip(k.iter()).filter(|(_, ok)| !**ok).map(|(n, _)| *n).collect();
    println!("\n3 criteria, {} pass; failed: {:?}", 3 - bad.len(), bad);
    std::process::exit(if bad.is_empty() { 0 } else { 1 });
}
