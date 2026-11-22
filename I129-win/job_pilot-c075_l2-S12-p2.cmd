@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONIOENCODING=utf-8
cd /d %~dp0..\..\negative-mass-i129\phase2\nonradial
"%~dp0..\..\negative-mass-venv314\Scripts\python.exe" -u harm_circles.py --box=c075_l2 --setting=S12 --points=2 --raw=%~dp0. > "%~dp0pilot-c075_l2-S12-p2.log" 2>&1
echo %ERRORLEVEL% > "%~dp0pilot-c075_l2-S12-p2.log.exit"
