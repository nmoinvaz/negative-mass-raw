@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONIOENCODING=utf-8
set NPROC=1
if not exist "%~dp0regen5" mkdir "%~dp0regen5"
set PARTIAL_DIR=%~dp0regen5
set CAP_S=1
set GAMS=0.001,0.03,0.3,1,3,10,40,137,300,1000,6000
cd /d %~dp0..\..\negative-mass-i114\phase2\nonradial
"%~dp0..\..\negative-mass-venv314\Scripts\python.exe" -u convergence.py 5 > "%~dp0regen5.log" 2> "%~dp0regen5.stderr"
echo %ERRORLEVEL% > "%~dp0regen5.log.exit"
