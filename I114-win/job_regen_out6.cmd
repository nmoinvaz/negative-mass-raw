@echo off
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONIOENCODING=utf-8
set NPROC=1
set PARTIAL_DIR=%~dp0.
set CAP_S=432000
set GAMS=0.001,0.03,0.3,1,3,10,40,137,300,1000,12000
cd /d %~dp0..\..\negative-mass-i114\phase2\nonradial
"%~dp0..\..\negative-mass-venv314\Scripts\python.exe" -u convergence.py 6 > convergence_l6_output.txt 2> "%~dp0regen_out6.stderr"
echo %ERRORLEVEL% > "%~dp0regen_out6.log.exit"
