# status.ps1 for run 2 of l = 6 (amendment 1 of README.md): elapsed wall time since the last `start` record of the l = 6
# partial file, the worker's cpu seconds and their ratio, the state of the scheduled tasks, the gaps over 150 s in
# memory-sampler-run2.log (a suspended laptop leaves gaps and a ratio below 1), the last sample and the queue.log tail.
# Reports only.
$raw = Split-Path -Parent $MyInvocation.MyCommand.Path
$now = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
$job = 'run_l6_run2'
$part = "$raw\convergence_l6_w0.7603.partial.csv"
$lines = Get-Content $part
$st = $lines | Where-Object { $_ -match '^\{"start"' } | Select-Object -Last 1
$o = $st | ConvertFrom-Json
$ex = if ((Test-Path "$raw\$job.log.exit") -and (Get-Item "$raw\$job.log.exit").Length -gt 0) { (Get-Content "$raw\$job.log.exit" -Raw).Trim() } else { 'running' }
$wall = $now - $o.time
$p = Get-Process -Id $o.pid -ErrorAction SilentlyContinue
$cpu = if ($p) { $p.CPU } else { $null }
$ratio = if ($cpu) { '{0:N3}' -f ($cpu / $wall) } else { 'n/a' }
"{0}: worker pid {1} ({2}), exit {3}, wall {4:N0} s ({5:N2} h), cpu {6:N0} s, cpu/wall {7}" -f $job, $o.pid, $(if ($p) { 'alive' } else { 'not running' }), $ex, $wall, ($wall / 3600), $cpu, $ratio
"partial file: {0} results, {1} start, {2} done, {3} capped, {4} died records" -f @($lines | Where-Object { $_ -match '^\[' }).Count, @($lines | Where-Object { $_ -match '^\{"start"' }).Count, @($lines | Where-Object { $_ -match '^\{"done"' }).Count, @($lines | Where-Object { $_ -match '^\{"capped"' }).Count, @($lines | Where-Object { $_ -match '^\{"died"' }).Count
foreach ($t in 'nm-i114-l6-run2', 'nm-i114-keepawake-run2', 'nm-i114-sampler-run2') {
  $x = Get-ScheduledTask -TaskName $t -ErrorAction SilentlyContinue
  "task {0}: {1}" -f $t, $(if ($x) { $x.State } else { 'absent' })
}
$prev = $null; $gaps = @()
foreach ($line in Get-Content "$raw\memory-sampler-run2.log" | Where-Object { $_ -match 'free=' }) {
  $t = [datetime]::ParseExact($line.Substring(0, 19), 'yyyy-MM-dd HH:mm:ss', $null)
  if ($prev -and ($t - $prev).TotalSeconds -gt 150) { $gaps += ("{0} -> {1} ({2:N0} s)" -f $prev.ToString('MM-dd HH:mm:ss'), $t.ToString('HH:mm:ss'), ($t - $prev).TotalSeconds) }
  $prev = $t
}
"sampler gaps over 150 s: " + $(if ($gaps) { $gaps -join '; ' } else { 'none' })
"last sample: " + (Get-Content "$raw\memory-sampler-run2.log" -Tail 1)
"queue.log tail: " + ((Get-Content "$raw\queue.log" -Tail 2) -join ' | ')
