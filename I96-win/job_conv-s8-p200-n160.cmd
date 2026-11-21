@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONIOENCODING=utf-8
cd /d %~dp0..\..\negative-mass-i96
"%~dp0..\..\negative-mass-venv314\Scripts\python.exe" -u notes\warp\tanh_spectrum.py --part=conv --sigmas=8 --p=8:200 --npan=160 --convtol=1e-8 --procs=1 > "%~dp0conv-s8-p200-n160.log" 2>&1
echo %ERRORLEVEL% > "%~dp0conv-s8-p200-n160.log.exit"
