@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONIOENCODING=utf-8
cd /d %~dp0..\..\negative-mass-i121\phase2\nonradial
"%~dp0..\..\negative-mass-venv314\Scripts\python.exe" -u zerilli_zeros.py -1 0.7603 2 0.1 2.0 2.5 --plant=0.3,1.76 --cachedir=%~dp0cache > "%~dp0p7603_l2.log" 2>&1
echo %ERRORLEVEL% > "%~dp0p7603_l2.log.exit"
