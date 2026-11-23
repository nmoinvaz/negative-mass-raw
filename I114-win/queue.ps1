# Starts the listed jobs in order. One job at a time; a second only while choptuik-large-d's processes together use under
# 4 cores (CPU-seconds delta over 10 s, one reading per start, in cores.log). A job is done when <job>.log.exit exists;
# its exit code goes to queue.log and is a result, never a reason to restart or stop. Memory plays no part: nothing stops
# on it. A name with a leading '+' is a job already running: counted, not started. Our cores are the convergence.py
# processes and their descendants (the pool worker).
param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Jobs)
$raw = Split-Path -Parent $MyInvocation.MyCommand.Path
$re = 'p4_1025|hp1058|_hpkernel|venv-md510|choptuik'
$pending = New-Object System.Collections.Generic.List[string]
$started = New-Object System.Collections.Generic.List[string]
foreach ($j in $Jobs) { if ($j.StartsWith('+')) { $started.Add($j.Substring(1)) } else { $pending.Add($j) } }
function Log($m) { "$(Get-Date -Format s) $m" | Add-Content "$raw\queue.log" -Encoding utf8 }
function Exit-Of($j) { $f = "$raw\$j.log.exit"; if ((Test-Path $f) -and (Get-Item $f).Length -gt 0) { return [int]((Get-Content $f -Raw).Trim()) } else { return $null } }
function Snap {
  $h = @{}
  foreach ($p in Get-CimInstance Win32_Process) {
    $h[[int]$p.ProcessId] = @{ cpu = ([double]$p.KernelModeTime + [double]$p.UserModeTime) / 1e7; cmd = [string]$p.CommandLine
                               name = $p.Name; ppid = [int]$p.ParentProcessId; ws = [double]$p.WorkingSetSize }
  }
  $h
}
function Ours($h, $k) {
  $c = $k
  for ($d = 0; $d -lt 8 -and $h.ContainsKey($c); $d++) {
    if ($h[$c].cmd -match 'convergence\.py') { return $true }
    $c = $h[$c].ppid
  }
  return $false
}
function Choptuik-Cores {
  $a = Snap; Start-Sleep -Seconds 10; $b = Snap
  $ch = 0.0; $ours = 0.0; $other = 0.0; $ws = 0.0
  foreach ($k in $b.Keys) {
    $d = $b[$k].cpu - $(if ($a.ContainsKey($k)) { $a[$k].cpu } else { 0.0 })
    if (Ours $b $k) { $ws += $b[$k].ws }
    if ($d -le 0) { continue }
    if (Ours $b $k) { $ours += $d }
    elseif ($b[$k].cmd -match $re -or $b[$k].name -match 'rustc|cargo|link') { $ch += $d }
    elseif ($b[$k].name -ne 'System Idle Process') { $other += $d }
  }
  $free = (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB
  "{0} choptuik_cores={1:N2} ours_cores={2:N2} other_cores={3:N2} ours_ws_mib={4:N0} free_gib={5:N1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), ($ch / 10), ($ours / 10), ($other / 10), ($ws / 1MB), $free | Add-Content "$raw\cores.log" -Encoding utf8
  return ($ch / 10)
}
Log "queue start (pid $PID): $($Jobs -join ' ')"
while ($pending.Count -gt 0 -or $started.Count -gt 0) {
  foreach ($j in @($started)) {
    $e = Exit-Of $j
    if ($null -ne $e) { $started.Remove($j) | Out-Null; Log "finished $j exit $e" }
  }
  $running = $started.Count
  if ($pending.Count -gt 0) {
    $go = $false
    if ($running -eq 0) { $go = $true }
    elseif ($running -lt 2) {
      $c = Choptuik-Cores
      if ($c -lt 4.0) { $go = $true } else { Log "waiting: choptuik-large-d uses $([math]::Round($c, 2)) cores" }
    }
    if ($go) {
      $next = $pending[0]; $pending.RemoveAt(0)
      & cmd.exe /c "$raw\go_$next.cmd"
      $started.Add($next)
      Log "started $next"
    }
  }
  Start-Sleep -Seconds 20
}
Log "queue done"
