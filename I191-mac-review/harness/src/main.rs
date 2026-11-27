//! ind191's harness: reads one decimal coefficient per line, rounds to the lane, runs `locate` with default options.
//!
//!     locate_harness LANE K FILE      LANE = f64 | dd | qd
use multisolver::multidouble::dd::DD;
use multisolver::multidouble::qd::QD;
use multisolver::locate::{locate, Kind, Model, Opts, Real};

fn run<T: Real>(c: Vec<T>) {
    match locate(&c, &Opts::default()) {
        None => println!("{{\"kind\":\"None\"}}"),
        Some(l) => {
            let k = match l.kind {
                Kind::Real => "Real",
                Kind::Pair => "Pair",
                Kind::Unresolved => "Unresolved",
            };
            let m = match l.model {
                Model::Ratio => "Ratio",
                Model::ThreeTerm => "ThreeTerm",
            };
            let s = &l.nearest;
            println!(
                "{{\"kind\":\"{k}\",\"model\":\"{m}\",\"re\":{:e},\"im\":{:e},\"alpha\":{:e},\"bar\":{:e},\"alpha_bar\":{:e},\"first\":{},\"degree\":{},\"rel_bar\":{:e}}}",
                s.re.to_f64(),
                s.im.to_f64(),
                s.alpha.to_f64(),
                s.bar,
                s.alpha_bar,
                l.first,
                l.degree,
                l.rel_bar
            );
        }
    }
}

fn main() {
    let a: Vec<String> = std::env::args().collect();
    let k: usize = a[2].parse().unwrap();
    let txt = std::fs::read_to_string(&a[3]).unwrap();
    let lines: Vec<&str> = txt.lines().take(k + 1).collect();
    match a[1].as_str() {
        "f64" => run(lines.iter().map(|s| s.parse::<f64>().unwrap()).collect()),
        "dd" => run(lines.iter().map(|s| QD::parse(s).unwrap().to_dd()).collect::<Vec<DD>>()),
        "qd" => run(lines.iter().map(|s| QD::parse(s).unwrap()).collect::<Vec<QD>>()),
        l => panic!("lane {l}"),
    }
}
