@echo off
rem Usage: run_stage.cmd L GMAX. Steps run one after another and the chain stops at the first failure, at a sign change of D
rem in the scan, or at a convergence variant whose sign differs (the coordinator's stop conditions).
setlocal
set L=%1
set GMAX=%2
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set NPROC=4
set PY=C:\Users\nathan\Source\negative-mass-venv314\Scripts\python.exe
set RAW=C:\Users\nathan\Source\negative-mass-raw\I4-win
set ST=%RAW%\stage_l%L%.status
cd /d C:\Users\nathan\Source\negative-mass-i4\phase2\nonradial

echo %date% %time% scan start >> %ST%
%PY% -u scan_growing.py -1 0.7603 %L% 100 0.001 %GMAX% >> %RAW%\scan_l%L%.log 2>&1
set RC=%errorlevel%
echo %date% %time% scan exit %RC% >> %ST%
if not "%RC%"=="0" exit /b 1
findstr /C:"sign change in [" %RAW%\scan_l%L%.log >nul
if not errorlevel 1 (
  echo %date% %time% STOP sign change of D in the scan >> %ST%
  exit /b 3
)

set GAMS=0.001,0.03,0.3,1,3,10,40,137,300,1000,%GMAX%
echo %date% %time% convergence start >> %ST%
%PY% -u convergence.py %L% > convergence_l%L%_output.txt 2>&1
set RC=%errorlevel%
echo %date% %time% convergence exit %RC% >> %ST%
if not "%RC%"=="0" exit /b 1
%PY% -c "import re,sys; sys.exit(4 if any(re.search(r'signs=\[[^\]]*,', x) for x in open(sys.argv[1])) else 0)" convergence_l%L%_output.txt
if errorlevel 1 (
  echo %date% %time% STOP a convergence variant flips the sign of D >> %ST%
  exit /b 4
)

echo %date% %time% kappa_eff start >> %ST%
%PY% -u kappa_eff.py %L% > kappa_eff_l%L%_output.txt 2>&1
set RC=%errorlevel%
echo %date% %time% kappa_eff exit %RC% >> %ST%
if not "%RC%"=="0" exit /b 1
echo %date% %time% stage done >> %ST%
exit /b 0
