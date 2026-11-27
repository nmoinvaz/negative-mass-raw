//! Design probe of #188: the cost of a complex multiply-add pair (re, im) against a real one, in f64, dd and qd.
//! The kernel is the Taylor recursion's inner loop, s += c[m] * y[k - m] over 30 terms, repeated.
use multidouble::dd::DD;
use multidouble::qd::QD;
use std::ops::{Add, Mul, Sub};
use std::hint::black_box;
use std::time::Instant;

#[derive(Clone, Copy, Debug)]
struct C<T> {
    re: T,
    im: T,
}
impl<T: Copy + Add<Output = T>> Add for C<T> {
    type Output = C<T>;
    fn add(self, o: C<T>) -> C<T> {
        C { re: self.re + o.re, im: self.im + o.im }
    }
}
impl<T: Copy + Add<Output = T> + Sub<Output = T> + Mul<Output = T>> Mul for C<T> {
    type Output = C<T>;
    fn mul(self, o: C<T>) -> C<T> {
        C { re: self.re * o.re - self.im * o.im, im: self.re * o.im + self.im * o.re }
    }
}

trait L: Copy + Add<Output = Self> + Sub<Output = Self> + Mul<Output = Self> {
    fn f(x: f64) -> Self;
    fn z() -> Self;
    fn h(self) -> f64;
}
impl L for f64 {
    fn f(x: f64) -> f64 { x }
    fn z() -> f64 { 0.0 }
    fn h(self) -> f64 { self }
}
impl L for DD {
    fn f(x: f64) -> DD { DD::from_f64(x) }
    fn z() -> DD { DD::ZERO }
    fn h(self) -> f64 { self.to_f64() }
}
impl L for QD {
    fn f(x: f64) -> QD { QD::from_f64(x) }
    fn z() -> QD { QD::ZERO }
    fn h(self) -> f64 { self.to_f64() }
}

fn real<T: L>(reps: usize) -> (f64, f64) {
    let a: Vec<T> = (0..30).map(|i| T::f(0.5 + 0.01 * i as f64)).collect();
    let b: Vec<T> = (0..30).map(|i| T::f(0.7 - 0.013 * i as f64)).collect();
    let t = Instant::now();
    let mut acc = T::z();
    for r in 0..reps {
        let mut s = T::z();
        for m in 0..30 {
            s = s + black_box(a[m]) * black_box(b[29 - m]);
        }
        acc = acc + s * T::f(1e-3 * (r % 7) as f64);
    }
    (t.elapsed().as_secs_f64(), acc.h())
}

fn cplx<T: L>(reps: usize) -> (f64, f64) {
    let a: Vec<C<T>> = (0..30).map(|i| C { re: T::f(0.5 + 0.01 * i as f64), im: T::f(0.1 - 0.003 * i as f64) }).collect();
    let b: Vec<C<T>> = (0..30).map(|i| C { re: T::f(0.7 - 0.013 * i as f64), im: T::f(0.2 + 0.002 * i as f64) }).collect();
    let t = Instant::now();
    let mut acc = C { re: T::z(), im: T::z() };
    for r in 0..reps {
        let mut s = C { re: T::z(), im: T::z() };
        for m in 0..30 {
            s = s + black_box(a[m]) * black_box(b[29 - m]);
        }
        let k = C { re: T::f(1e-3 * (r % 7) as f64), im: T::f(1e-4) };
        acc = acc + s * k;
    }
    (t.elapsed().as_secs_f64(), acc.re.h() + acc.im.h())
}

fn main() {
    for (name, reps) in [("f64", 4_000_000usize), ("dd", 400_000), ("qd", 60_000)] {
        for rep in 0..2 {
            let (tr, tc) = match name {
                "f64" => (real::<f64>(reps), cplx::<f64>(reps)),
                "dd" => (real::<DD>(reps), cplx::<DD>(reps)),
                _ => (real::<QD>(reps), cplx::<QD>(reps)),
            };
            println!("{name} rep{rep}: real {:.1} ns/term, complex {:.1} ns/term, ratio {:.2}  (sinks {:.3e} {:.3e})", tr.0 / (reps * 30) as f64 * 1e9, tc.0 / (reps * 30) as f64 * 1e9, tc.0 / tr.0, tr.1, tc.1);
        }
    }
}
