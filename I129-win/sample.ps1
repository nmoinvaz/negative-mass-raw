# Samples the working set, peak working set and CPU time of the harm_circles.py processes every 60 s, with the free memory.
param([string]$Log)
while ($true) {
  $t = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
  $ps = Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -match 'harm_circles' }
  foreach ($p in $ps) {
    $q = Get-Process -Id $p.ProcessId -ErrorAction SilentlyContinue
    if ($q -and $q.WorkingSet64 -gt 30MB) {
      $a = ($p.CommandLine -replace '.*harm_circles.py','').Trim()
      "{0} pid={1} ws={2:N0}MB peak={3:N0}MB cpu={4:N0}s {5}" -f $t,$p.ProcessId,($q.WorkingSet64/1MB),($q.PeakWorkingSet64/1MB),$q.CPU,$a | Add-Content -Path $Log -Encoding utf8
    }
  }
  $os = Get-CimInstance Win32_OperatingSystem
  "{0} free={1:N1}GB of {2:N1}GB" -f $t,($os.FreePhysicalMemory/1MB),($os.TotalVisibleMemorySize/1MB) | Add-Content -Path $Log -Encoding utf8
  Start-Sleep -Seconds 60
}
