"""The one rerun of conv_085_l3 of issue 7: python -X faulthandler -u convergence.py 3 0.85, appending to conv_085_l3.log,
then the row comparison with the first run (compare_conv_rows.py). Runs after the two retries of retries.py."""
import os
import subprocess
import sys
import time

import retry_scan_085_l2 as S
import compare_conv_rows as C

RAW, NR, PY = S.RAW, S.NR, S.PY


def main():
    open(os.path.join(RAW, "retry3.pid"), "w").write(str(os.getpid()))
    env = dict(os.environ, PYTHONUNBUFFERED="1", OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1")
    env.pop("TAG", None)
    cmd = [PY, "-X", "faulthandler", "-u", "convergence.py", "3", "0.85"]
    t0 = time.time()
    S.say("conv_085_l3 retry start " + " ".join(cmd[1:]))
    with open(os.path.join(RAW, "conv_085_l3.log"), "ab") as log:
        log.write(f"=== {S.now()} conv_085_l3 retry: {' '.join(cmd[1:])}\n".encode())
        log.flush()
        rc = subprocess.run(cmd, cwd=NR, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
    S.say(f"conv_085_l3 retry exit {rc} after {time.time() - t0:.0f} s")
    rs = C.runs(open(os.path.join(RAW, "conv_085_l3.log"), encoding="utf-8", errors="replace").read())
    n, diff, extra = C.compare(rs[0], rs[-1])
    S.say(f"conv_085_l3 rows: compared {n}, {len(diff)} differ, {extra} only in the first run")


if __name__ == "__main__":
    main()
