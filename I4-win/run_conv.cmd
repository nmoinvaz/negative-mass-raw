@echo off
rem Usage: run_conv.cmd L GMAX NPROC. The convergence and kappa_eff steps of a stage, stopping at a failure or at a convergence
rem variant whose sign of D differs.
setlocal
set L=%1
set GMAX=%2
set NPROC=%3
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set PY=C:\Users\nathan\Source\negative-mass-venv314\Scripts\python.exe
set RAW=C:\Users\nathan\Source\negative-mass-raw\I4-win
set ST=%RAW%\stage_l%L%.status
cd /d C:\Users\nathan\Source\negative-mass-i4\phase2\nonradial

set GAMS=0.001,0.03,0.3,1,3,10,40,137,300,1000,%GMAX%
echo %date% %time% convergence start NPROC=%NPROC% >> %ST%
%PY% -u convergence.py %L% > convergence_l%L%_output.txt 2> %RAW%\convergence_l%L%.stderr
set RC=%errorlevel%
echo %date% %time% convergence exit %RC% >> %ST%
if not "%RC%"=="0" exit /b 1
%PY% -c "import re,sys; sys.exit(4 if any(re.search(r'signs=\[[^\]]*,', x) for x in open(sys.argv[1])) else 0)" convergence_l%L%_output.txt
if errorlevel 1 (
  echo %date% %time% STOP a convergence variant flips the sign of D >> %ST%
  exit /b 4
)

echo %date% %time% kappa_eff start >> %ST%
%PY% -u kappa_eff.py %L% > kappa_eff_l%L%_output.txt 2> %RAW%\kappa_eff_l%L%.stderr
set RC=%errorlevel%
echo %date% %time% kappa_eff exit %RC% >> %ST%
if not "%RC%"=="0" exit /b 1
echo %date% %time% stage done >> %ST%
exit /b 0
