@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONIOENCODING=utf-8
cd /d %~dp0..\..\negative-mass-i129\phase2\nonradial
"%~dp0..\..\negative-mass-venv314\Scripts\python.exe" -u harm_circles.py --box=p7603_l2 --setting=S10 --raw=%~dp0. > "%~dp0S10-p7603_l2.log" 2>&1
echo %ERRORLEVEL% > "%~dp0S10-p7603_l2.log.exit"
