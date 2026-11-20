# Starts (2,B) then (2,A) as slots free, at most two solve jobs running, only if every finished job exited 0.
$raw = 'C:\Users\nathan\Source\negative-mass-raw\I111-win'
$logs = @{ s4B = 'solve-s4-B.log'; s4A = 'solve-s4-A.log'; s2B = 'solve-s2-B.log'; s2A = 'solve-s2-A.log' }
$started = New-Object System.Collections.Generic.List[string]
$started.Add('s4B'); $started.Add('s4A')
$pending = @('s2B', 's2A')
function Exit-Of($k) { $f = "$raw\$($logs[$k]).exit"; if (Test-Path $f) { return [int]((Get-Content $f -Raw).Trim()) } else { return $null } }
while ($pending.Count -gt 0) {
  $running = @($started | Where-Object { $null -eq (Exit-Of $_) })
  $failed = @($started | Where-Object { $e = Exit-Of $_; ($null -ne $e) -and ($e -ne 0) })
  if ($failed.Count -gt 0) { "$(Get-Date -Format s) stopping: $($failed -join ',') exited nonzero" | Add-Content "$raw\queue.log"; break }
  if ($running.Count -lt 2) {
    $next = $pending[0]; $pending = @($pending | Select-Object -Skip 1)
    & cmd.exe /c "$raw\go_$next.cmd"
    $started.Add($next)
    "$(Get-Date -Format s) started $next" | Add-Content "$raw\queue.log"
  }
  Start-Sleep -Seconds 20
}
"$(Get-Date -Format s) queue done" | Add-Content "$raw\queue.log"
