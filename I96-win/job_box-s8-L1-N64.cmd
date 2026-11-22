@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONIOENCODING=utf-8
cd /d %~dp0..\..\negative-mass-i96
"%~dp0..\..\negative-mass-venv314\Scripts\python.exe" -u notes\warp\frank_loss.py --part=krylov --sigmas=8 --Ns=64 --L=1 --vs=0.5 > "%~dp0box-s8-L1-N64.log" 2>&1
echo %ERRORLEVEL% > "%~dp0box-s8-L1-N64.log.exit"
