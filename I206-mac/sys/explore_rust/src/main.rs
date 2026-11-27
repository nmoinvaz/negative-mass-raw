//! I206-mac: the locator of multisolver, as shipped, on the series the Python exploration (explore3.py) dumped: the same
//! 90 cases x 3 lanes of I191's design exploration. Per series and per grid of first orders (the default, and the #191
//! grid 0.2 ... 0.6 K) it prints the kind, the chosen cell, the error of s and of alpha and their bars, and at the end the
//! counts the README's criterion 2 reports: resolved cells, the bar of s covering the error of s, the bar of alpha
//! covering the error of alpha, the kind right; and the control, the same bars multiplied by 1e-3.
//!
//!     explore_rust <series.txt>... 
//!
//! Not the gate of criterion 2 (that is the Python instrument's, which has no floor on the bar and fewer rows per fit);
//! the port's own figures.
use multisolver::locate::{locate, Kind, Opts, Real};
use multisolver::multidouble::{dd::DD, qd::QD};

fn from_parts<T: Real>(s: &str) -> T {
    s.split(',').fold(T::from_f64(0.0), |a, p| a + T::from_f64(p.parse::<f64>().expect("part")))
}

#[derive(Default, Clone)]
struct Tally {
    series: usize,
    none: usize,
    resolved: usize,
    cov_s: usize,
    cov_a: usize,
    kind_right: usize,
    cov_s_shrunk: usize,
    misses: Vec<String>,
}

struct Out {
    kind: Kind,
    model: String,
    first: usize,
    degree: usize,
    err_s: f64,
    bar_s: f64,
    err_a: f64,
    bar_a: f64,
}

fn run<T: Real>(c: &[T], truth: &(T, T, T), opts: &Opts) -> Option<Out> {
    let loc = locate(c, opts)?;
    let n = &loc.nearest;
    let rad = (truth.0.to_f64()).hypot(truth.1.to_f64());
    let err_s = (n.re - truth.0).to_f64().hypot((n.im - truth.1).to_f64()) / rad;
    Some(Out {
        kind: loc.kind,
        model: format!("{:?}", loc.model),
        first: loc.first,
        degree: loc.degree,
        err_s,
        bar_s: n.bar / rad,
        err_a: (n.alpha - truth.2).to_f64().abs(),
        bar_a: n.alpha_bar,
    })
}

fn grid_old() -> Opts {
    Opts {
        starts: vec![0.2, 0.3, 0.4, 0.5, 0.6],
        ..Opts::default()
    }
}

fn tally(t: &mut Tally, label: &str, id: &str, want_pair: bool, o: Option<Out>) {
    t.series += 1;
    let Some(o) = o else {
        t.none += 1;
        println!("{id} {label}: none");
        return;
    };
    let resolved = o.kind != Kind::Unresolved;
    println!(
        "{id} {label}: {:?} {} first {} deg {} | s: err {:.1e} bar {:.1e} | alpha: err {:.1e} bar {:.1e}{}",
        o.kind,
        o.model,
        o.first,
        o.degree,
        o.err_s,
        o.bar_s,
        o.err_a,
        o.bar_a,
        if resolved && (o.err_s > o.bar_s || o.err_a > o.bar_a) { "  MISS" } else { "" }
    );
    if resolved {
        t.resolved += 1;
        if o.err_s <= o.bar_s {
            t.cov_s += 1;
        } else {
            t.misses.push(id.to_string());
        }
        if o.err_a <= o.bar_a {
            t.cov_a += 1;
        }
        if (o.kind == Kind::Pair) == want_pair {
            t.kind_right += 1;
        }
        if o.err_s <= 1e-3 * o.bar_s {
            t.cov_s_shrunk += 1;
        }
    }
}

fn series<T: Real>(tok: &[&str], id: &str, want_pair: bool, new: &mut Tally, old: &mut Tally) {
    let truth = (from_parts::<T>(tok[5]), from_parts::<T>(tok[6]), from_parts::<T>(tok[7]));
    let c: Vec<T> = tok[8..].iter().map(|s| from_parts::<T>(s)).collect();
    tally(new, "new", id, want_pair, run(&c, &truth, &Opts::default()));
    tally(old, "old", id, want_pair, run(&c, &truth, &grid_old()));
}

fn main() {
    println!("default starts: {:?}", Opts::default().starts);
    let (mut new, mut old) = (Tally::default(), Tally::default());
    let mut lanes: std::collections::BTreeMap<String, (Tally, Tally)> = Default::default();
    for path in std::env::args().skip(1) {
        let text = std::fs::read_to_string(&path).expect("read series");
        for (ln, line) in text.lines().enumerate() {
            let tok: Vec<&str> = line.split(' ').collect();
            let (lane, kind) = (tok[1], tok[2]);
            let k: usize = tok[4].parse().unwrap();
            assert_eq!(tok.len(), 8 + k + 1, "{path}:{ln}");
            let id = format!("{path}:{} {lane}", tok[0]);
            let e = lanes.entry(lane.to_string()).or_default();
            let (mut n, mut o) = (Tally::default(), Tally::default());
            match lane {
                "f64" => series::<f64>(&tok, &id, kind == "pair", &mut n, &mut o),
                "dd" => series::<DD>(&tok, &id, kind == "pair", &mut n, &mut o),
                "qd" => series::<QD>(&tok, &id, kind == "pair", &mut n, &mut o),
                _ => panic!("lane {lane}"),
            }
            for (a, b) in [(&mut new, &n), (&mut old, &o), (&mut e.0, &n), (&mut e.1, &o)] {
                a.series += b.series;
                a.none += b.none;
                a.resolved += b.resolved;
                a.cov_s += b.cov_s;
                a.cov_a += b.cov_a;
                a.kind_right += b.kind_right;
                a.cov_s_shrunk += b.cov_s_shrunk;
                a.misses.extend(b.misses.iter().cloned());
            }
        }
    }
    let show = |name: &str, t: &Tally| {
        println!(
            "SUMMARY {name}: series {} none {} resolved {} sigma covered {} (misses {}) alpha covered {} kind right {} | control (bars x 1e-3): sigma covered {}",
            t.series,
            t.none,
            t.resolved,
            t.cov_s,
            t.resolved - t.cov_s,
            t.cov_a,
            t.kind_right,
            t.cov_s_shrunk
        );
        println!("SUMMARY {name}: misses {:?}", t.misses);
    };
    show("all, default grid (0.2 ... 0.8 K)", &new);
    show("all, #191 grid (0.2 ... 0.6 K)", &old);
    for (lane, (n, o)) in &lanes {
        show(&format!("{lane}, default grid"), n);
        show(&format!("{lane}, #191 grid"), o);
    }
}
