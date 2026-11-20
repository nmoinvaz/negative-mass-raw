@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
cd /d C:\Users\nathan\Source\negative-mass-i111
C:\Users\nathan\Source\negative-mass-venv314\Scripts\python.exe -u notes\warp\tanh_spectrum_check.py --part=solve --sigma=4 --disc=B --ms=8.5 --solver=arpack --floor=0.07 --fnth=4 --fh=0.4 --out=C:\Users\nathan\Source\negative-mass-raw\I111-win\eig > C:\Users\nathan\Source\negative-mass-raw\I111-win\pilot-s4B-m8.5.log 2>&1
echo %ERRORLEVEL% > C:\Users\nathan\Source\negative-mass-raw\I111-win\pilot-s4B-m8.5.log.exit
