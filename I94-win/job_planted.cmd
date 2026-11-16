@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
cd /d C:\Users\nathan\Source\negative-mass-i94
C:\Users\nathan\Source\negative-mass-venv314\Scripts\python.exe -u notes\warp\tanh_spectrum_check.py --part=planted > C:\Users\nathan\Source\negative-mass-raw\I94-win\planted.log 2>&1
echo %ERRORLEVEL% > C:\Users\nathan\Source\negative-mass-raw\I94-win\planted.log.exit
