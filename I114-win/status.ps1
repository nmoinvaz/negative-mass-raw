# Prints, for each run of run_l5 / run_l6 that has no exit file, the elapsed wall time since its start record, the
# worker's cpu seconds and their ratio, then the gaps over 150 s in memory-sampler.log (a suspended laptop leaves gaps and
# a ratio below 1), the last core reading and the free memory. Reports only.
$raw = Split-Path -Parent $MyInvocation.MyCommand.Path
$now = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
foreach ($r in @(@('run_l5', 5), @('run_l6', 6))) {
  $job = $r[0]; $l = $r[1]
  $part = "$raw\convergence_l${l}_w0.7603.partial.csv"
  $st = Get-Content $part | Where-Object { $_ -match '^\{"start"' } | Select-Object -Last 1
  if (-not $st) { "$job : no start record"; continue }
  $o = $st | ConvertFrom-Json
  $ex = if (Test-Path "$raw\$job.log.exit") { (Get-Content "$raw\$job.log.exit" -Raw).Trim() } else { 'running' }
  $wall = $now - $o.time
  $p = Get-Process -Id $o.pid -ErrorAction SilentlyContinue
  $cpu = if ($p) { $p.CPU } else { $null }
  $ratio = if ($cpu) { '{0:N3}' -f ($cpu / $wall) } else { 'n/a' }
  "{0}: worker pid {1}, exit {2}, wall {3:N0} s ({4:N2} h), cpu {5:N0} s, cpu/wall {6}, results in partial file {7}" -f $job, $o.pid, $ex, $wall, ($wall / 3600), $cpu, $ratio, ((Get-Content $part | Where-Object { $_ -match '^\[' }).Count)
}
$prev = $null; $gaps = @()
foreach ($line in Get-Content "$raw\memory-sampler.log" | Where-Object { $_ -match 'free=' }) {
  $t = [datetime]::ParseExact($line.Substring(0, 19), 'yyyy-MM-dd HH:mm:ss', $null)
  if ($prev -and ($t - $prev).TotalSeconds -gt 150) { $gaps += ("{0} -> {1} ({2:N0} s)" -f $prev.ToString('MM-dd HH:mm:ss'), $t.ToString('HH:mm:ss'), ($t - $prev).TotalSeconds) }
  $prev = $t
}
"sampler gaps over 150 s: " + $(if ($gaps) { $gaps -join '; ' } else { 'none' })
"last sample: " + (Get-Content "$raw\memory-sampler.log" -Tail 1)
"last core reading: " + (Get-Content "$raw\cores.log" -Tail 1)
"queue.log tail: " + ((Get-Content "$raw\queue.log" -Tail 2) -join ' | ')
