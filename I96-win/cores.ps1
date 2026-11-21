# One reading of choptuik-large-d's cores (CPU-seconds delta over 10 s of processes matching the regex below), written to
# cores.log with our cores, other cores, our working set and free GiB. Same definition as queue.ps1's gate.
$raw = Split-Path -Parent $MyInvocation.MyCommand.Path
$re = 'p4_1025|hp1058|_hpkernel|venv-md510|choptuik'
function Snap {
  $h = @{}
  foreach ($p in Get-CimInstance Win32_Process) {
    $h[[int]$p.ProcessId] = @{ cpu = ([double]$p.KernelModeTime + [double]$p.UserModeTime) / 1e7; cmd = [string]$p.CommandLine; name = $p.Name; ppid = [int]$p.ParentProcessId }
  }
  $h
}
function Is-Ours($h, $id) {
  for ($d = 0; $d -lt 8 -and $h.ContainsKey($id); $d++) {
    if ($h[$id].cmd -match '(tanh_spectrum|frank_loss)\.py') { return $true }
    $id = $h[$id].ppid
  }
  return $false
}
function Choptuik-Cores {
  $a = Snap; Start-Sleep -Seconds 10; $b = Snap
  $ch = 0.0; $ours = 0.0; $other = 0.0; $ws = 0.0
  foreach ($k in $b.Keys) {
    $d = $b[$k].cpu - $(if ($a.ContainsKey($k)) { $a[$k].cpu } else { 0.0 })
    if ($d -le 0) { continue }
    if (Is-Ours $b $k) { $ours += $d }
    elseif ($b[$k].cmd -match $re -or $b[$k].name -match 'rustc|cargo|link') { $ch += $d }
    elseif ($b[$k].name -ne 'System Idle Process') { $other += $d }
  }
  foreach ($k in $b.Keys) { if ($b[$k].name -eq 'python.exe' -and (Is-Ours $b $k)) { $ws += [double](Get-Process -Id $k -ErrorAction SilentlyContinue).WorkingSet64 } }
  $free = (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB
  "{0} choptuik_cores={1:N2} ours_cores={2:N2} other_cores={3:N2} ours_ws_mib={4:N0} free_gib={5:N1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), ($ch / 10), ($ours / 10), ($other / 10), ($ws / 1MB), $free | Add-Content "$raw\cores.log" -Encoding utf8
  return ($ch / 10)
}

$c = Choptuik-Cores
Get-Content "$raw\cores.log" -Tail 1
