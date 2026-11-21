@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONIOENCODING=utf-8
cd /d %~dp0..\..\negative-mass-i120
"%~dp0..\..\negative-mass-venv314\Scripts\python.exe" -u notes\warp\tanh_spectrum_check.py --part=solve --sigma=2 --disc=A --ms=11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5 --solver=arpack --out=%~dp0eig > "%~dp0solve-s2-A.log" 2>&1
echo %ERRORLEVEL% > "%~dp0solve-s2-A.log.exit"
