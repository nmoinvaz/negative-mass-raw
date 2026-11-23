# Samples the working set, peak working set and CPU time of the convergence.py processes every $Every s, the pool worker
# (a descendant of a process whose command line names the script) included, and the free memory. Reports only.
param([string]$Log, [int]$Every = 60)
while ($true) {
  $t = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
  $all = Get-CimInstance Win32_Process -Filter "Name='python.exe'"
  $byId = @{}
  foreach ($p in $all) { $byId[[int]$p.ProcessId] = $p }
  foreach ($p in $all) {
    $a = $null; $c = $p
    for ($d = 0; $d -lt 8 -and $c; $d++) {
      if ([string]$c.CommandLine -match 'convergence\.py') {
        $a = ([string]$c.CommandLine -replace '.*convergence\.py', '').Trim()
        break
      }
      $c = $byId[[int]$c.ParentProcessId]
    }
    if ($null -eq $a) { continue }
    $q = Get-Process -Id $p.ProcessId -ErrorAction SilentlyContinue
    if ($q -and $q.WorkingSet64 -gt 30MB) {
      "{0} pid={1} ws={2:N0}MB peak={3:N0}MB cpu={4:N0}s args={5}" -f $t, $p.ProcessId, ($q.WorkingSet64 / 1MB), ($q.PeakWorkingSet64 / 1MB), $q.CPU, $a | Add-Content -Path $Log -Encoding utf8
    }
  }
  $os = Get-CimInstance Win32_OperatingSystem
  "{0} free={1:N1}GB of {2:N1}GB" -f $t, ($os.FreePhysicalMemory / 1MB), ($os.TotalVisibleMemorySize / 1MB) | Add-Content -Path $Log -Encoding utf8
  Start-Sleep -Seconds $Every
}
