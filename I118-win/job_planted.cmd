@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
cd /d %~dp0..\..\negative-mass-i118
"%~dp0..\..\negative-mass-venv314\Scripts\python.exe" -u notes\warp\tanh_spectrum_check.py --part=planted --ms=9.5,10.5 --solver=arpack --floor=0.07 --fnth=4 --fh=0.4 > "%~dp0planted.log" 2>&1
echo %ERRORLEVEL% > "%~dp0planted.log.exit"
