@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
cd /d C:\Users\nathan\Source\negative-mass-i111
C:\Users\nathan\Source\negative-mass-venv314\Scripts\python.exe -u notes\warp\tanh_spectrum_check.py --part=planted --ms=0.5 --solver=arpack --floor=0.07 --fnth=4 --fh=0.4 --mutate=kterm > C:\Users\nathan\Source\negative-mass-raw\I111-win\control-kterm.log 2>&1
echo %ERRORLEVEL% > C:\Users\nathan\Source\negative-mass-raw\I111-win\control-kterm.log.exit
