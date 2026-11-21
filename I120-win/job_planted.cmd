@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONIOENCODING=utf-8
cd /d %~dp0..\..\negative-mass-i120
"%~dp0..\..\negative-mass-venv314\Scripts\python.exe" -u notes\warp\tanh_spectrum_check.py --part=planted --ms=11.5,20.5 --solver=arpack > "%~dp0planted.log" 2>&1
echo %ERRORLEVEL% > "%~dp0planted.log.exit"
