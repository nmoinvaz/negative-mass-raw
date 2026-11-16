@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
cd /d C:\Users\nathan\Source\negative-mass-i94
C:\Users\nathan\Source\negative-mass-venv314\Scripts\python.exe -u notes\warp\tanh_spectrum_check.py --part=solve --sigma=4 --disc=B --ms=10.5 --out=C:\Users\nathan\Source\negative-mass-raw\I94-win\eig > C:\Users\nathan\Source\negative-mass-raw\I94-win\pilot-s4B-m10.5.log 2>&1
echo %ERRORLEVEL% > C:\Users\nathan\Source\negative-mass-raw\I94-win\pilot-s4B-m10.5.log.exit
