@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONIOENCODING=utf-8
cd /d %~dp0..\..\negative-mass-i125
"%~dp0..\..\negative-mass-venv314\Scripts\python.exe" -u notes\warp\tanh_spectrum.py --part=vc,planted,tanh --procs=1 --sigmas=4 --ms=20.5 --raw=%~dp0eig > "%~dp0pilot-s4-m20.5.log" 2>&1
echo %ERRORLEVEL% > "%~dp0pilot-s4-m20.5.log.exit"
