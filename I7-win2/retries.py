"""The two retries of issue 7, one after the other so #7 stays at 2 processes, both with -X faulthandler.

1. conv_085_l2:  python -X faulthandler -u convergence.py 2 0.85, appending to conv_085_l2.log.
2. scan_085_l2:  retry_scan_085_l2.py (TAG=_n100, pool of 2, -X faulthandler), then its comparison with the diagnostic.

If the first crashes again nothing more is run: the traceback is in conv_085_l2.log and the coordinator decides.
"""
import os
import subprocess
import time

import retry_scan_085_l2 as S

RAW = S.RAW
NR = S.NR
PY = S.PY


def conv():
    env = dict(os.environ, PYTHONUNBUFFERED="1", OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1")
    env.pop("TAG", None)
    cmd = [PY, "-X", "faulthandler", "-u", "convergence.py", "2", "0.85"]
    t0 = time.time()
    S.say("conv_085_l2 retry start " + " ".join(cmd[1:]))
    with open(os.path.join(RAW, "conv_085_l2.log"), "ab") as log:
        log.write(f"=== {S.now()} conv_085_l2 retry: {' '.join(cmd[1:])}\n".encode())
        log.flush()
        rc = subprocess.run(cmd, cwd=NR, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
    S.say(f"conv_085_l2 retry exit {rc} after {time.time() - t0:.0f} s")
    return rc


def main():
    open(os.path.join(RAW, "retry.pid"), "w").write(str(os.getpid()))
    if conv() != 0:
        S.say("conv_085_l2 failed again, nothing more is run, waiting for the coordinator")
        return
    S.main()


if __name__ == "__main__":
    main()
