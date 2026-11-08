"""The last three runs of issue 7, one at a time, each with -X faulthandler, each continuing after a crash of the one
before (the coordinator lifted the stop rule for this list only):

1. scan_085_l2: retry_scan_085_l2.main() (TAG=_n100, pool of 2), then its comparison with the serial diagnostic.
2. conv_085_l3: retry_conv_085_l3.main() (convergence.py 3 0.85), then the row comparison with the first run.
3. conv_085_l2: retries.conv() (convergence.py 2 0.85) a third time.

Nothing else is run afterwards. Exit codes and comparisons go to retry.log.
"""
import os
import traceback

import retries as R
import retry_conv_085_l3 as T
import retry_scan_085_l2 as S


def attempt(label, fn):
    try:
        fn()
    except Exception:
        S.say(f"{label}: the driver raised, continuing\n" + traceback.format_exc())


def main():
    open(os.path.join(S.RAW, "retry2.pid"), "w").write(str(os.getpid()))
    S.say("retries2 start: scan_085_l2, conv_085_l3, conv_085_l2")
    attempt("scan_085_l2", S.main)
    attempt("conv_085_l3", T.main)
    attempt("conv_085_l2", R.conv)
    S.say("retries2 finished, nothing more is run")


if __name__ == "__main__":
    main()
