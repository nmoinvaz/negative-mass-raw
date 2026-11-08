@echo off
rem Starts the I55 job queue and its cpu/memory reporter, both detached, at Normal priority.
cd /d "%~dp0"
if exist queue.pid del queue.pid
start "I55 queue" /min powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0queue.ps1"
start "I55 memwatch" /min powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0memwatch.ps1" -Log "%~dp0memwatch.log"
