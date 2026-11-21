@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONIOENCODING=utf-8
cd /d %~dp0..\..\negative-mass-i127
"%~dp0..\..\negative-mass-venv314\Scripts\python.exe" -u notes\warp\tanh_spectrum_check.py --part=solve --sigma=2 --disc=B --ms=9.5 --solver=arpack --floor=0.025 --k0=512 --kmax=512 --fnth=4 --fh=0.4 --out=%~dp0eig > "%~dp0solve-s2-B-m9.5.log" 2>&1
echo %ERRORLEVEL% > "%~dp0solve-s2-B-m9.5.log.exit"
