@echo off
rem Usage: run_scan.cmd L GMAX NPROC. The scan step of a stage only, stopping at a failure or at a sign change of D.
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

echo %date% %time% scan start NPROC=%NPROC% >> %ST%
%PY% -u scan_growing.py -1 0.7603 %L% 100 0.001 %GMAX% >> %RAW%\scan_l%L%.log 2>&1
set RC=%errorlevel%
echo %date% %time% scan exit %RC% >> %ST%
if not "%RC%"=="0" exit /b 1
findstr /C:"sign change in [" %RAW%\scan_l%L%.log >nul
if not errorlevel 1 (
  echo %date% %time% STOP sign change of D in the scan >> %ST%
  exit /b 3
)
echo %date% %time% scan done >> %ST%
exit /b 0
