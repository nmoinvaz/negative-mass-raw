@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONIOENCODING=utf-8
cd /d %~dp0..\..\negative-mass-i121\phase2\nonradial
"%~dp0..\..\negative-mass-venv314\Scripts\python.exe" -u zerilli_zeros.py -1 0.7603 2 0.02 0.1 1.84 --y0=1.68 --zfac=2 --plant=0.03,1.77 --cachedir=%~dp0cache > "%~dp0t2_z2.log" 2>&1
echo %ERRORLEVEL% > "%~dp0t2_z2.log.exit"
