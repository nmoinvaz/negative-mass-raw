# Holds SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED) until the queue's powershell process exits, then
# releases it (ES_CONTINUOUS alone). No power setting or plan is changed. The request lasts as long as this thread
# lives, so the loop below stays on the main thread. Start and end go to queue.log.
param([int]$QueuePid)
$raw = Split-Path -Parent $MyInvocation.MyCommand.Path
function Log($m) {
  for ($i = 0; $i -lt 5; $i++) {
    try { "$(Get-Date -Format s) $m" | Add-Content "$raw\queue.log" -Encoding utf8 -ErrorAction Stop; break } catch { Start-Sleep -Milliseconds 300 }
  }
}
Add-Type -Namespace Win32 -Name Power -MemberDefinition '[DllImport("kernel32.dll")] public static extern uint SetThreadExecutionState(uint f);'
$ES_CONTINUOUS = [uint32]2147483648
$ES_SYSTEM_REQUIRED = [uint32]1
$prev = [Win32.Power]::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM_REQUIRED)
if ($prev -eq 0) { Log "keep-awake: SetThreadExecutionState failed"; exit 1 }
Log "keep-awake start (pid $PID, waits for queue pid $QueuePid, previous state 0x$($prev.ToString('X')))"
while (Get-Process -Id $QueuePid -ErrorAction SilentlyContinue) { Start-Sleep -Seconds 30 }
[void][Win32.Power]::SetThreadExecutionState($ES_CONTINUOUS)
Log "keep-awake end (queue pid $QueuePid gone)"
