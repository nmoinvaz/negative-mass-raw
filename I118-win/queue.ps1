# Starts (4,B), (4,A), (2,B), (2,A) one at a time. A second solve starts only while choptuik-large-d's processes together
# use under 4 cores (CPU-seconds delta over 10 s). Stops if a finished job exited nonzero. Memory plays no part.
$raw = Split-Path -Parent $MyInvocation.MyCommand.Path
$logs = [ordered]@{ s4B = 'solve-s4-B.log'; s4A = 'solve-s4-A.log'; s2B = 'solve-s2-B.log'; s2A = 'solve-s2-A.log' }
$started = New-Object System.Collections.Generic.List[string]
$pending = @($logs.Keys)
$re = 'p4_1025|hp1058|_hpkernel|venv-md510|choptuik'
function Exit-Of($k) { $f = "$raw\$($logs[$k]).exit"; if (Test-Path $f) { return [int]((Get-Content $f -Raw).Trim()) } else { return $null } }
function Snap {
  $h = @{}
  foreach ($p in Get-CimInstance Win32_Process) {
    $h[[int]$p.ProcessId] = @{ cpu = ([double]$p.KernelModeTime + [double]$p.UserModeTime) / 1e7; cmd = [string]$p.CommandLine; name = $p.Name }
  }
  $h
}
function Choptuik-Cores {
  $a = Snap; Start-Sleep -Seconds 10; $b = Snap
  $ch = 0.0; $ours = 0.0; $other = 0.0
  foreach ($k in $b.Keys) {
    $d = $b[$k].cpu - $(if ($a.ContainsKey($k)) { $a[$k].cpu } else { 0.0 })
    if ($d -le 0) { continue }
    if ($b[$k].cmd -match 'tanh_spectrum_check') { $ours += $d }
    elseif ($b[$k].cmd -match $re -or $b[$k].name -match 'rustc|cargo|link') { $ch += $d }
    elseif ($b[$k].name -ne 'System Idle Process') { $other += $d }
  }
  "{0} choptuik_cores={1:N2} ours_cores={2:N2} other_cores={3:N2}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), ($ch / 10), ($ours / 10), ($other / 10) | Add-Content "$raw\cores.log" -Encoding utf8
  return ($ch / 10)
}
while ($pending.Count -gt 0) {
  $running = @($started | Where-Object { $null -eq (Exit-Of $_) })
  $failed = @($started | Where-Object { $e = Exit-Of $_; ($null -ne $e) -and ($e -ne 0) })
  if ($failed.Count -gt 0) { "$(Get-Date -Format s) stopping: $($failed -join ',') exited nonzero" | Add-Content "$raw\queue.log" -Encoding utf8; break }
  $go = $false
  if ($running.Count -eq 0) { $go = $true }
  elseif ($running.Count -lt 2) {
    $c = Choptuik-Cores
    if ($c -lt 4.0) { $go = $true } else { "$(Get-Date -Format s) waiting: choptuik-large-d uses $([math]::Round($c,2)) cores" | Add-Content "$raw\queue.log" -Encoding utf8 }
  }
  if ($go) {
    $next = $pending[0]; $pending = @($pending | Select-Object -Skip 1)
    & cmd.exe /c "$raw\go_$next.cmd"
    $started.Add($next)
    "$(Get-Date -Format s) started $next" | Add-Content "$raw\queue.log" -Encoding utf8
  }
  Start-Sleep -Seconds 30
}
"$(Get-Date -Format s) queue done" | Add-Content "$raw\queue.log" -Encoding utf8
