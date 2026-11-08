@echo off
rem Starts the I7 job queue and its memory reporter, both detached, at Normal priority.
cd /d "%~dp0"
if exist queue.pid del queue.pid
start "I7 queue" /min "C:\Users\nathan\Source\negative-mass-venv\Scripts\python.exe" -u "%~dp0queue.py"
start "I7 memwatch" /min powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0memwatch.ps1" -Log "%~dp0memwatch.log"
