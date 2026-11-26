//! Probe of #184: does `Relaxed` form any square at the orders the walker uses, and does it pay at octo-double?
//! A product of two series of n = kt + 2 coefficients is formed online (order k is read after steps 0..k-1), once with
//! `Relaxed::sum` and once with `cs_range`; squares formed, bitwise equality of the two, and the time of each.
use multidouble::dd::DD;
use multidouble::dual::Lane;
use multidouble::field::{cs_range, Fl};
use multidouble::native::{DV, OV, QV};
use multidouble::series::Relaxed;
use std::time::Instant;

struct Rng(u64);
impl Rng {
    fn next(&mut self) -> f64 {
        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        ((self.0 >> 11) as f64 / (1u64 << 53) as f64) * 2.0 - 1.0
    }
}

fn series<T: Lane>(n: usize, r: &mut Rng) -> Vec<Fl<T, 1>> {
    (0..n)
        .map(|i| {
            let s = (-0.3 * i as f64).exp2();
            Fl::<T, 1>::splat(DD::new(r.next() * s, r.next() * s * 1e-17))
        })
        .collect()
}

fn probe<T: Lane>(name: &str, kt: usize) {
    let n = kt + 2;
    let mut r = Rng(7);
    let (x, y) = (series::<T>(n, &mut r), series::<T>(n, &mut r));
    let reps = 20;
    // relaxed
    let t0 = Instant::now();
    let mut rel_out = Vec::new();
    let mut squares = 0;
    for _ in 0..reps {
        let mut p = Relaxed::<T, 1>::new(n);
        rel_out.clear();
        for k in 0..n {
            rel_out.push(p.sum(&x, &y, k, 0, k));
            p.step(&x, &y, k);
        }
        squares = p.squares;
    }
    let t_rel = t0.elapsed().as_secs_f64() / reps as f64;
    let t0 = Instant::now();
    let mut cs_out = Vec::new();
    for _ in 0..reps {
        cs_out.clear();
        for k in 0..n {
            cs_out.push(cs_range(&x, &y, k, 0, k));
        }
    }
    let t_cs = t0.elapsed().as_secs_f64() / reps as f64;
    let same = rel_out.iter().zip(&cs_out).all(|(a, b)| {
        let (a, b) = (a.0[0], b.0[0]);
        format!("{a:?}") == format!("{b:?}")
    });
    println!(
        "{name} order {kt}: BLOCK_MIN {}, squares formed {squares}, online product bitwise cs_range: {same}, Relaxed {:.3} ms, cs_range {:.3} ms",
        T::BLOCK_MIN,
        t_rel * 1e3,
        t_cs * 1e3
    );
}

fn main() {
    probe::<DV>("DV", 30);
    probe::<QV>("QV", 60);
    probe::<OV>("OV", 120);
    probe::<OV>("OV", 240);
    probe::<QV>("QV", 240);
}
