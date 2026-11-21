@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONIOENCODING=utf-8
cd /d %~dp0..\..\negative-mass-i121\phase2\nonradial
"%~dp0..\..\negative-mass-venv314\Scripts\python.exe" -u zerilli_zeros.py -1 0.70 3 0.1 2.0 2.5 --plant=0.3,1.76 --cachedir=%~dp0cache > "%~dp0p070_l3.log" 2>&1
echo %ERRORLEVEL% > "%~dp0p070_l3.log.exit"
