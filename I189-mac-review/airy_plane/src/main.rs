//! ind189's harness: a k-plane of y' = J(x) y, J = Q (A + B x) Q^T for u'' = x u, v'' = 4 x v, carried from 0 to X by
//! multishoot's `plane::Plane::advance`; prints the basis and ln_vol as JSON.
//!
//!     airy_plane LANE K X [scaleonly]      LANE = f64 | dd | qd
use multidouble::dd::DD;
use multidouble::qd::QD;
use multishoot::plane::{JetSource, Jets, Plane, Real};
use multishoot::taylor::Plan;

trait Out: Real {
    fn s(self) -> String;
}
impl Out for f64 {
    fn s(self) -> String {
        format!("{:.17e}", self)
    }
}
impl Out for DD {
    fn s(self) -> String {
        QD::from_dd(self).to_sci(34)
    }
}
impl Out for QD {
    fn s(self) -> String {
        self.to_sci(66)
    }
}

fn r<T: Real>(a: i64, b: i64) -> T {
    T::from_f64(a as f64) / T::from_f64(b as f64)
}

/// Q as a dense row-major 4 x 4: G(2,3; 7/25,24/25) G(0,1; 8/17,15/17) G(1,3; 5/13,12/13) G(0,2; 3/5,4/5)
fn qmat<T: Real>() -> [[T; 4]; 4] {
    let mut q = [[T::zero(); 4]; 4];
    for (i, row) in q.iter_mut().enumerate() {
        row[i] = T::one();
    }
    // apply on the left in order: first G(0,2), then G(1,3), G(0,1), G(2,3)
    let gs: [(usize, usize, i64, i64, i64); 4] = [(0, 2, 3, 4, 5), (1, 3, 5, 12, 13), (0, 1, 8, 15, 17), (2, 3, 7, 24, 25)];
    for &(i, j, c, s, d) in &gs {
        let (cc, ss): (T, T) = (r(c, d), r(s, d));
        for col in 0..4 {
            let (a, b) = (q[i][col], q[j][col]);
            q[i][col] = cc * a - ss * b;
            q[j][col] = ss * a + cc * b;
        }
    }
    q
}

fn conj<T: Real>(q: &[[T; 4]; 4], m: &[[T; 4]; 4]) -> [[T; 4]; 4] {
    let mut t = [[T::zero(); 4]; 4];
    for i in 0..4 {
        for j in 0..4 {
            let mut acc = T::zero();
            for a in 0..4 {
                for b in 0..4 {
                    acc = acc + q[i][a] * m[a][b] * q[j][b];
                }
            }
            t[i][j] = acc;
        }
    }
    t
}

struct Airy<T: Real> {
    a: [[T; 4]; 4],
    b: [[T; 4]; 4],
}

impl<T: Real> JetSource<T> for Airy<T> {
    fn pattern(&self) -> Vec<(usize, usize)> {
        (0..4).flat_map(|i| (0..4).map(move |j| (i, j))).collect()
    }
    fn jets(&self, x0: f64, kj: usize, out: &mut Jets<T>) {
        let x = T::from_f64(x0);
        for e in out.ent.iter_mut() {
            for c in e.c.iter_mut().take(kj) {
                *c = T::zero();
            }
            e.c[0] = self.a[e.i][e.j] + self.b[e.i][e.j] * x;
            if kj >= 2 {
                e.c[1] = self.b[e.i][e.j];
                e.n = 2;
            } else {
                e.n = 1;
            }
        }
    }
}

fn run<T: Out>(k: usize, xend: f64, kt: usize, scaleonly: bool) {
    let q = qmat::<T>();
    let mut a = [[T::zero(); 4]; 4];
    let mut b = [[T::zero(); 4]; 4];
    a[0][1] = T::one();
    a[2][3] = T::one();
    b[1][0] = T::one();
    b[3][2] = T::from_f64(4.0);
    let src = Airy { a: conj(&q, &a), b: conj(&q, &b) };
    let bm: [[f64; 4]; 4] = [[1.0, 0.0, 0.5, 0.25], [0.5, 1.0, 0.0, -0.5], [0.25, -0.5, 1.0, 0.0], [0.0, 0.75, 0.5, 1.0]];
    let mut basis = vec![T::zero(); 4 * k];
    for c in 0..k {
        for i in 0..4 {
            let mut acc = T::zero();
            for m in 0..4 {
                acc = acc + q[i][m] * T::from_f64(bm[m][c]);
            }
            basis[c * 4 + i] = acc;
        }
    }
    let mut p = Plane::new(4, k, &basis);
    #[cfg(feature = "mutate")]
    if scaleonly {
        p.set_control(multishoot::control::PlaneControl::ScaleOnly);
    }
    #[cfg(not(feature = "mutate"))]
    assert!(!scaleonly, "scaleonly needs the mutate feature");
    let plan = Plan { kt, tol: T::EPS / 10.0, hmax: 0.5 };
    let st = p.advance(&src, 0.0, xend, &plan, kt);
    let cols: Vec<String> = p.columns().iter().map(|v| format!("\"{}\"", v.s())).collect();
    println!(
        "{{\"k\":{},\"X\":{},\"kt\":{},\"eps\":{:e},\"steps\":{},\"ln_vol\":\"{}\",\"ln_gram\":\"{}\",\"cols\":[{}]}}",
        k,
        xend,
        kt,
        T::EPS,
        st.steps,
        p.ln_vol().s(),
        p.ln_gram().s(),
        cols.join(",")
    );
}

fn main() {
    let a: Vec<String> = std::env::args().collect();
    let k: usize = a[2].parse().unwrap();
    let x: f64 = a[3].parse().unwrap();
    let so = a.get(4).map(|s| s == "scaleonly").unwrap_or(false);
    match a[1].as_str() {
        "f64" => run::<f64>(k, x, 24, so),
        "dd" => run::<DD>(k, x, 40, so),
        "qd" => run::<QD>(k, x, 70, so),
        l => panic!("lane {l}"),
    }
}
