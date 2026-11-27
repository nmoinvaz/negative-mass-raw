//! D1 of I192-mac: for planted coefficient sets c_0 .. c_29 about u = 0 (all in f64), the width at which the
//! tail test (|c_k| h^k <= tail * sum_j |c_j| h^j for the last `last` orders) passes, and multisolver 0.3.0's
//! `locate` with default options: kind, |s|, bar, exponent, and the time of one call. The truth is printed beside.
use multisolver::locate::{locate, Kind, Opts};
use std::time::Instant;

const NB: usize = 30;

fn ok(c: &[f64], h: f64, tail: f64, last: usize) -> bool {
    let mut sum = 0.0;
    let mut hk = 1.0;
    let mut worst = 0.0f64;
    for (k, x) in c.iter().enumerate() {
        let t = x.abs() * hk;
        sum += t;
        if k + last >= c.len() {
            worst = worst.max(t);
        }
        hk *= h;
    }
    sum == 0.0 || worst <= tail * sum
}

/// the largest h up to `cap` at which the tail test passes (bisection, 100 steps)
fn width(c: &[f64], cap: f64, tail: f64, last: usize) -> f64 {
    if ok(c, cap, tail, last) {
        return cap;
    }
    let (mut lo, mut hi) = (0.0, cap);
    for _ in 0..100 {
        let mid = 0.5 * (lo + hi);
        if ok(c, mid, tail, last) {
            lo = mid;
        } else {
            hi = mid;
        }
    }
    lo
}

struct Set {
    name: &'static str,
    truth: &'static str,
    radius: f64,
    c: Vec<f64>,
}

fn binom_half(k: usize) -> f64 {
    // (-1)^k binom(1/2, k): c_k of (1 - u)^(1/2)
    let mut b = 1.0;
    for j in 0..k {
        b *= (0.5 - j as f64) / (j as f64 + 1.0);
    }
    if k % 2 == 1 { -b } else { b }
}

fn sets() -> Vec<Set> {
    let mut v = vec![];
    let n = NB;
    v.push(Set { name: "S1 1/(1-u)", truth: "s=1 alpha=-1", radius: 1.0, c: vec![1.0; n] });
    v.push(Set { name: "S2 1/(1-u)^2", truth: "s=1 alpha=-2", radius: 1.0, c: (0..n).map(|k| (k + 1) as f64).collect() });
    v.push(Set {
        name: "S3 1/(1-u)^3",
        truth: "s=1 alpha=-3",
        radius: 1.0,
        c: (0..n).map(|k| ((k + 1) * (k + 2)) as f64 / 2.0).collect(),
    });
    v.push(Set { name: "S4 (1-u)^(1/2)", truth: "s=1 alpha=0.5", radius: 1.0, c: (0..n).map(binom_half).collect() });
    for (name, th) in [("S5 pair at angle 0.6", 0.6f64), ("S6 pair at angle 0.05", 0.05f64)] {
        v.push(Set {
            name,
            truth: if th > 0.5 { "s=e^(0.6i) alpha=-1" } else { "s=e^(0.05i) alpha=-1" },
            radius: 1.0,
            c: (0..n).map(|k| ((k + 1) as f64 * th).sin() / th.sin()).collect(),
        });
    }
    let mut f = 1.0;
    let e1: Vec<f64> = (0..n).map(|k| { if k > 0 { f /= k as f64; } f }).collect();
    v.push(Set { name: "S7 e^u", truth: "entire", radius: f64::INFINITY, c: e1 });
    let mut f = 1.0;
    let e10: Vec<f64> = (0..n).map(|k| { if k > 0 { f *= 10.0 / k as f64; } f }).collect();
    v.push(Set { name: "S7b e^(10u)", truth: "entire", radius: f64::INFINITY, c: e10 });
    v.push(Set { name: "S8 1/(1-u^3)", truth: "s=1 (and e^(+-2 pi i/3)) alpha=-1", radius: 1.0, c: (0..n).map(|k| if k % 3 == 0 { 1.0 } else { 0.0 }).collect() });
    v.push(Set { name: "S9 1/(1-u^2)", truth: "s=+-1 alpha=-1", radius: 1.0, c: (0..n).map(|k| if k % 2 == 0 { 1.0 } else { 0.0 }).collect() });
    v.push(Set {
        name: "S10 1/(1-u) + 1/(1+u/1.2)",
        truth: "s=1 alpha=-1, then s=-1.2",
        radius: 1.0,
        c: (0..n).map(|k| 1.0 + (-1.0f64 / 1.2).powi(k as i32)).collect(),
    });
    let x0 = 1e-3f64;
    v.push(Set {
        name: "S11 1/x^2 about x0=1e-3",
        truth: "s=-1e-3 alpha=-2",
        radius: x0,
        c: (0..n).map(|k| (if k % 2 == 0 { 1.0 } else { -1.0 }) * (k + 1) as f64 * x0.powi(-(k as i32) - 2)).collect(),
    });
    v
}

fn main() {
    println!("# D1: tail width (nb {NB}, tail 1e-25, search cap 100 radii or 100) and locate (default Opts), f64");
    println!("{:<28}{:>13}{:>13}{:>13}  {}", "set", "W(last 2)", "W(last 2)/R", "W(last 4)/R", "locate: kind |s| bar alpha alpha_bar  [model first degree]  time/call  | truth");
    for s in sets() {
        let cap = if s.radius.is_finite() { 100.0 * s.radius } else { 100.0 };
        let w2 = width(&s.c, cap, 1e-25, 2);
        let w4 = width(&s.c, cap, 1e-25, 4);
        let t0 = Instant::now();
        let reps = 200;
        let mut loc = None;
        for _ in 0..reps {
            loc = locate(&s.c, &Opts::default());
        }
        let dt = t0.elapsed().as_secs_f64() / reps as f64;
        let t1 = Instant::now();
        let mut sink = 0.0;
        for _ in 0..reps {
            sink += width(&s.c, cap, 1e-25, 2);
        }
        let dw = t1.elapsed().as_secs_f64() / reps as f64;
        let ratio = |w: f64| if s.radius.is_finite() { format!("{:.4}", w / s.radius) } else { "-".to_string() };
        let lt = match &loc {
            None => "None".to_string(),
            Some(l) => {
                let k = match l.kind {
                    Kind::Real => "Real",
                    Kind::Pair => "Pair",
                    Kind::Unresolved => "Unresolved",
                };
                format!(
                    "{k} |s|={:.6e} bar={:.2e} re={:.6e} im={:.6e} alpha={:.4} abar={:.2e} [{:?} {} {}]",
                    l.nearest.radius(), l.nearest.bar, l.nearest.re, l.nearest.im, l.nearest.alpha, l.nearest.alpha_bar, l.model, l.first, l.degree
                )
            }
        };
        println!("{:<28}{:>13.5e}{:>13}{:>13}  {} t_locate={:.1}us t_width={:.1}us | {}{}", s.name, w2, ratio(w2), ratio(w4), lt, dt * 1e6, dw * 1e6, s.truth, if sink < 0.0 { "!" } else { "" });
    }
}
