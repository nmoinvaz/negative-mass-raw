# Waits for pilot-s16.log.exit, then starts queue.ps1 with the job sectors-s8 (one job, alone, restarted if it dies).
$raw = Split-Path -Parent $MyInvocation.MyCommand.Path
while (-not (Test-Path "$raw\pilot-s16.log.exit")) { Start-Sleep -Seconds 30 }
"$(Get-Date -Format s) pilot-s16 exited, starting the queue for sectors-s8" | Add-Content "$raw\queue.log" -Encoding utf8
& powershell -NoProfile -ExecutionPolicy Bypass -File "$raw\queue.ps1" sectors-s8
