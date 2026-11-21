@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONIOENCODING=utf-8
cd /d %~dp0..\..\negative-mass-i120
"%~dp0..\..\negative-mass-venv314\Scripts\python.exe" -u notes\warp\tanh_spectrum_check.py --part=solve --sigma=4 --disc=B --ms=20.5 --solver=arpack --out=%~dp0eig > "%~dp0pilot-s4-B-m20.5.log" 2>&1
echo %ERRORLEVEL% > "%~dp0pilot-s4-B-m20.5.log.exit"
