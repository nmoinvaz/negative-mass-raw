@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
cd /d C:\Users\nathan\Source\negative-mass-i111
C:\Users\nathan\Source\negative-mass-venv314\Scripts\python.exe -u notes\warp\tanh_spectrum_check.py --part=solve --sigma=2 --disc=A --ms=0.5 --solver=arpack --out=C:\Users\nathan\Source\negative-mass-raw\I111-win\base > C:\Users\nathan\Source\negative-mass-raw\I111-win\base-s2A.log 2>&1
echo %ERRORLEVEL% > C:\Users\nathan\Source\negative-mass-raw\I111-win\base-s2A.log.exit
