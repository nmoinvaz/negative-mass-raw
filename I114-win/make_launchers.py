"""Writes job_<job>.cmd and go_<job>.cmd for the jobs of jobs.txt (all of them, or only those named on the command line,
so a running job's launcher is never rewritten). Paths are relative to this folder (%~dp0), so no user name lands in the
public raw repository. job_<job>.cmd runs `convergence.py <args>` from phase2/nonradial of the i114 worktree with one
thread, NPROC=1, and writes the stdout to <job>.log (or the file named in jobs.txt), the stderr to <job>.stderr and the
exit code to <job>.log.exit. go_<job>.cmd starts it detached at below-normal priority."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
names = set(sys.argv[1:])
for line in open(os.path.join(HERE, "jobs.txt"), encoding="utf-8"):
    line = line.rstrip("\r\n")
    if not line.strip() or line.startswith("#"):
        continue
    job, sub, env, args, out = (line.split("|") + [""] * 5)[:5]
    if names and job not in names:
        continue
    lines = ["@echo off"]
    lines += [f"set {k}=1" for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")]
    lines += ["set PYTHONIOENCODING=utf-8", "set NPROC=1"]
    if sub:
        if sub != ".":
            lines.append(f'if not exist "%~dp0{sub}" mkdir "%~dp0{sub}"')
        lines.append(f"set PARTIAL_DIR=%~dp0{sub}")
    for kv in filter(None, env.split(";")):
        lines.append(f"set {kv}")
    lines.append("cd /d %~dp0..\\..\\negative-mass-i114\\phase2\\nonradial")
    stdout = out if out else f'"%~dp0{job}.log"'
    lines.append(f'"%~dp0..\\..\\negative-mass-venv314\\Scripts\\python.exe" -u convergence.py {args} > {stdout} '
                 f'2> "%~dp0{job}.stderr"')
    lines.append(f'echo %ERRORLEVEL% > "%~dp0{job}.log.exit"')
    with open(os.path.join(HERE, f"job_{job}.cmd"), "w", newline="\r\n") as f:
        f.write("\r\n".join(lines) + "\r\n")
    with open(os.path.join(HERE, f"go_{job}.cmd"), "w", newline="\r\n") as f:
        f.write(f'@echo off\r\nstart "i114-{job}" /BELOWNORMAL /MIN cmd /c "%~dp0job_{job}.cmd"\r\n')
    print("wrote", job)
