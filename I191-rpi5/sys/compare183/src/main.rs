//! compare183 (#191): the new locator on the series that #183's walk read at its last step.
//!
//! Input (stdin, one point per line): id x_last l F_hi F_lo F1_hi F1_lo F2_hi F2_lo, the state of #183's last step in
//! double-double and the step variable's scale l (a power of two). The series of the three fields (F, F', F'') about
//! x_last in s = (x - x_last)/l is formed by #183's `hp::taylor_p` in double-double to order kt (default 30, as #183's
//! double-double walks), and the locator runs on each field. Output: one JSON line per (point, field).
//! Nothing of #183's crate is changed.
use conical_global::hp::{recips, taylor_p, HpCfg, PolyQ};
use conical_global::model::Mutation;
use multishoot::lane::BaseLane;
use multishoot::multidouble::precision::{Double, Precision};
use multishoot::multidouble::simd::Native;
use multishoot::{Fl, DD};
use multisolver_new::locate::{locate, Kind, Model, Opts};
use std::io::BufRead;

type P = Double;
type V = <P as Precision<Native>>::V;

fn kind(k: Kind) -> &'static str {
    match k {
        Kind::Real => "real",
        Kind::Pair => "pair",
        Kind::Unresolved => "unresolved",
    }
}

fn main() {
    let kt: usize = std::env::args().nth(1).map(|s| s.parse().unwrap()).unwrap_or(30);
    let poly = PolyQ::conical(&Mutation::default());
    let cfg = HpCfg::new(kt, 1e-12);
    let ik = recips::<P>(kt, false);
    for line in std::io::stdin().lock().lines() {
        let line = line.unwrap();
        let t: Vec<&str> = line.split_whitespace().collect();
        if t.len() != 9 {
            continue;
        }
        let id = t[0];
        let v: Vec<f64> = t[1..].iter().map(|s| s.parse().unwrap()).collect();
        let (x, l) = (v[0], v[1]);
        let ik_l: Vec<V> = ik.iter().map(|w| w.mulf(l)).collect();
        let mut c: [Vec<Fl<V, 1>>; 3] = std::array::from_fn(|_| vec![Fl::<V, 1>::zero(); kt + 2]);
        for f in 0..3 {
            c[f][0] = Fl([P::splat(DD { hi: v[2 + 2 * f], lo: v[3 + 2 * f] })]);
        }
        taylor_p::<P>(&poly, x, l, &mut c, &ik_l, &cfg);
        for f in 0..3 {
            let coef: Vec<DD> = (0..=kt).map(|k| P::field_get(&c[f][k], 0)).collect();
            if std::env::var("COMPARE183_DUMP").is_ok() {
                for (k, v) in coef.iter().enumerate() {
                    eprintln!("coef {id} {f} {k} {:e} {:e}", v.hi, v.lo);
                }
            }
            match locate::<DD>(&coef, &Opts::default()) {
                None => println!("{{\"id\": \"{id}\", \"field\": {f}, \"kind\": \"none\"}}"),
                Some(loc) => {
                    let n = &loc.nearest;
                    let far = loc.farther.map_or("null".to_string(), |s| {
                        format!(
                            "{{\"re\": [{:e}, {:e}], \"alpha\": {:e}, \"bar\": {:e}, \"alpha_bar\": {:e}}}",
                            s.re.hi, s.re.lo, s.alpha.to_f64(), s.bar, s.alpha_bar
                        )
                    });
                    println!(
                        "{{\"id\": \"{id}\", \"field\": {f}, \"kind\": \"{}\", \"model\": \"{}\", \"first\": {}, \"degree\": {}, \"l\": {:e}, \"x\": {:e}, \"re\": [{:e}, {:e}], \"im\": [{:e}, {:e}], \"alpha\": [{:e}, {:e}], \"bar\": {:e}, \"alpha_bar\": {:e}, \"rel_bar\": {:e}, \"skew\": {:e}, \"farther\": {}}}",
                        kind(loc.kind),
                        if loc.model == Model::Ratio { "ratio" } else { "three-term" },
                        loc.first,
                        loc.degree,
                        l,
                        x,
                        n.re.hi, n.re.lo, n.im.hi, n.im.lo, n.alpha.hi, n.alpha.lo, n.bar, n.alpha_bar, loc.rel_bar, loc.skew, far
                    );
                }
            }
        }
    }
}
