# Development smoke test of ind194's star code: one canonical star near the crossing, timed (not a criterion run).
import sys, time
sys.argv = ["ind194.py", "--only=none"]
t0 = time.time()
exec(open("ind194.py").read().split("if OPT.scan:")[0])
for eps, P in ((1, 2.0504432387354122617e-04), (-1, 2.0728052897904927504e-04)):
    st = ground(P, eps, 1e-12)
    print(eps, {k: (f"{v:.15g}" if isinstance(v, float) else v) for k, v in st.items()}, f"{time.time() - t0:.1f} s", flush=True)
