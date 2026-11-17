@echo off
rem Usage: run_regen.cmd L GAMS. Re-prints the convergence table of a stage whose last evaluation was stopped at the cap:
rem convergence.py L with GAMS set to the gammas whose evaluations all finished, so it reads them from the partial file.
setlocal
set L=%1
set GAMS=%~2
set NPROC=1
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set PY=C:\Users\nathan\Source\negative-mass-venv314\Scripts\python.exe
set RAW=C:\Users\nathan\Source\negative-mass-raw\I4-win
cd /d C:\Users\nathan\Source\negative-mass-i4\phase2\nonradial
echo %date% %time% regen start GAMS=%GAMS% >> %RAW%\stage_l%L%.status
%PY% -u convergence.py %L% > convergence_l%L%_output.txt 2> %RAW%\convergence_l%L%_regen.stderr
echo %date% %time% regen exit %errorlevel% >> %RAW%\stage_l%L%.status
