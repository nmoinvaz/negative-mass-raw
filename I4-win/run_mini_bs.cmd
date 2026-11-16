@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
cd /d C:\Users\nathan\Source\negative-mass-i4\phase2\nonradial
C:\Users\nathan\Source\negative-mass-venv314\Scripts\python.exe -u mini_bs.py > C:\Users\nathan\Source\negative-mass-raw\I4-win\mini_bs.log 2>&1
echo mini_bs exit %errorlevel% >> C:\Users\nathan\Source\negative-mass-raw\I4-win\mini_bs.log
