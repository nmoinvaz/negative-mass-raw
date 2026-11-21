# Waits until queue.ps1 has logged the end of sectors-s8 ("finished sectors-s8" or "giving up"), then starts the queue for
# conv-s16-p320-n320 (step 4, attempt 1: sigma R = 16 sizes, P = N = 320). Later attempts are started by hand.
$raw = Split-Path -Parent $MyInvocation.MyCommand.Path
while (-not ((Test-Path "$raw\queue.log") -and (Select-String -Path "$raw\queue.log" -Pattern 'finished sectors-s8|sectors-s8 died \d+ times, giving up' -Quiet))) { Start-Sleep -Seconds 60 }
"$(Get-Date -Format s) sectors-s8 ended, starting the queue for conv-s16-p320-n320" | Add-Content "$raw\queue.log" -Encoding utf8
& powershell -NoProfile -ExecutionPolicy Bypass -File "$raw\queue.ps1" conv-s16-p320-n320
