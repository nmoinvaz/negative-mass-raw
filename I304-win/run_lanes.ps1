# run_lanes.ps1 [-NLanes 3]: start the lanes of jobs.txt (throat_tail_b_jobs.py, one thread each, below-normal priority),
# wait for all of them, then write lanes_done. Never overwrites a log. Start and end go to queue.log.
param([int]$NLanes = 3)
$raw = Split-Path -Parent $MyInvocation.MyCommand.Path
$wt = "C:\Users\nathan\Source\negative-mass-i304\notes\wormhole_evolution"
$py = "C:\Users\nathan\Source\negative-mass-venv314\Scripts\python.exe"
New-Item -ItemType Directory -Force "$raw\logs" | Out-Null
$ps = @()
for ($l = 0; $l -lt $NLanes; $l++) {
  $log = "$raw\logs\lane$l.log"; $n = 1
  while (Test-Path $log) { $n++; $log = "$raw\logs\lane$l.$n.log" }
  $p = Start-Process -FilePath $py -ArgumentList @("$wt\throat_tail_b_jobs.py", "--raw=$raw", "--jobs=$raw\jobs.txt", "--lane=$l", "--nlanes=$NLanes") `
       -WorkingDirectory $wt -RedirectStandardOutput $log -RedirectStandardError "$log.err" -WindowStyle Hidden -PassThru
  $p.PriorityClass = "BelowNormal"
  $ps += $p
  "$(Get-Date -Format s) lane $l pid $($p.Id) -> $log" | Add-Content "$raw\queue.log"
}
$ps | Wait-Process
"$(Get-Date -Format s) all $NLanes lanes ended" | Add-Content "$raw\queue.log"
"done" | Set-Content "$raw\lanes_done"
