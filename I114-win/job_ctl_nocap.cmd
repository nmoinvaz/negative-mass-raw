@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONIOENCODING=utf-8
set NPROC=1
if not exist "%~dp0ctl_nocap" mkdir "%~dp0ctl_nocap"
set PARTIAL_DIR=%~dp0ctl_nocap
set CAP_S=4
set GAMS=0.001,40
cd /d %~dp0..\..\negative-mass-i114\phase2\nonradial
"%~dp0..\..\negative-mass-venv314\Scripts\python.exe" -u convergence.py 2 --mutate=nocap > "%~dp0ctl_nocap.log" 2> "%~dp0ctl_nocap.stderr"
echo %ERRORLEVEL% > "%~dp0ctl_nocap.log.exit"
