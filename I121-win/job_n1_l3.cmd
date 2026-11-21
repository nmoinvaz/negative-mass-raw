@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONIOENCODING=utf-8
cd /d %~dp0..\..\negative-mass-i121\phase2\nonradial
"%~dp0..\..\negative-mass-venv314\Scripts\python.exe" -u zerilli_zeros.py -1 0.7603 3 0.0001 0.1 0.23 --plant=0.0005,0.12 --cachedir=%~dp0cache > "%~dp0n1_l3.log" 2>&1
echo %ERRORLEVEL% > "%~dp0n1_l3.log.exit"
