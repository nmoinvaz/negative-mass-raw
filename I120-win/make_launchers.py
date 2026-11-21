"""Writes job_<job>.cmd and go_<job>.cmd for every line of jobs.txt, beside this file. Run with the venv python.
A line of jobs.txt is <job>|<arguments of tanh_spectrum_check.py>; <job> is also the log's name."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
for ln in open(os.path.join(HERE, 'jobs.txt'), encoding='utf-8'):
    if not ln.strip():
        continue
    job, args = ln.rstrip('\n').split('|', 1)
    job_cmd = (
        "@echo off\r\n"
        "set OMP_NUM_THREADS=1\r\n"
        "set OPENBLAS_NUM_THREADS=1\r\n"
        "set MKL_NUM_THREADS=1\r\n"
        "set PYTHONIOENCODING=utf-8\r\n"
        "cd /d %~dp0..\\..\\negative-mass-i120\r\n"
        f"\"%~dp0..\\..\\negative-mass-venv314\\Scripts\\python.exe\" -u notes\\warp\\tanh_spectrum_check.py {args} "
        f"> \"%~dp0{job}.log\" 2>&1\r\n"
        f"echo %ERRORLEVEL% > \"%~dp0{job}.log.exit\"\r\n")
    go_cmd = f"@echo off\r\nstart \"i120-{job}\" /BELOWNORMAL /MIN cmd /c \"%~dp0job_{job}.cmd\"\r\n"
    for name, txt in ((f"job_{job}.cmd", job_cmd), (f"go_{job}.cmd", go_cmd)):
        with open(os.path.join(HERE, name), 'w', newline='') as f:
            f.write(txt)
