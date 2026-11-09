@echo off
rem Starts #9's two job queues (A, B) and one cpu/memory reporter for each, all detached, at Normal priority.
rem Resume a held queue B at a job: launch.cmd B low_p16
cd /d "%~dp0"
if "%1"=="B" goto onlyb
start "I9 queue A" /min powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0queue.ps1" -Queue A
start "I9 memwatch A" /min powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0memwatch.ps1" -Log "%~dp0memwatch_A.log" -PidFile "%~dp0queue_A.pid"
:onlyb
if exist queue_B.pid del queue_B.pid
if "%2"=="" (
  start "I9 queue B" /min powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0queue.ps1" -Queue B
) else (
  start "I9 queue B" /min powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0queue.ps1" -Queue B -From %2
)
start "I9 memwatch B" /min powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0memwatch.ps1" -Log "%~dp0memwatch_B.log" -PidFile "%~dp0queue_B.pid"
