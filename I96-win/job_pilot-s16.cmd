@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONIOENCODING=utf-8
cd /d %~dp0..\..\negative-mass-i96
"%~dp0..\..\negative-mass-venv314\Scripts\python.exe" -u notes\warp\tanh_spectrum.py --part=vc,planted,tanh --sigmas=16 --ms=0.5 --p=16:320 --npan=320 --procs=1 --raw=%~dp0eig > "%~dp0pilot-s16.log" 2>&1
echo %ERRORLEVEL% > "%~dp0pilot-s16.log.exit"
