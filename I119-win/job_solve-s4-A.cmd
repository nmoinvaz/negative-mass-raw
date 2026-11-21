@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONIOENCODING=utf-8
cd /d %~dp0..\..\negative-mass-i119
"%~dp0..\..\negative-mass-venv314\Scripts\python.exe" -u notes\warp\tanh_spectrum_check.py --part=solve --sigma=4 --disc=A --ms=4.5,5.5,6.5,7.5,8.5,9.5,10.5 --solver=arpack --floor=0.04 --fnth=4 --fh=0.4 --out=%~dp0eig > "%~dp0solve-s4-A.log" 2>&1
echo %ERRORLEVEL% > "%~dp0solve-s4-A.log.exit"
