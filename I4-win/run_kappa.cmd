@echo off
rem Usage: run_kappa.cmd L [L ...]. kappa_eff.py for each l, one after another (single process).
setlocal enabledelayedexpansion
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set PY=C:\Users\nathan\Source\negative-mass-venv314\Scripts\python.exe
set RAW=C:\Users\nathan\Source\negative-mass-raw\I4-win
cd /d C:\Users\nathan\Source\negative-mass-i4\phase2\nonradial
for %%L in (%*) do (
  echo %date% %time% kappa_eff %%L start >> %RAW%\stage_kappa.status
  %PY% -u kappa_eff.py %%L > kappa_eff_l%%L_output.txt 2> %RAW%\kappa_eff_l%%L.stderr
  echo %date% %time% kappa_eff %%L exit !errorlevel! >> %RAW%\stage_kappa.status
)
