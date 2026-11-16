# Usage: powershell -File sample_progress.ps1 <minutes>. Appends a cpu and memory sample of the python processes and the
# partial-file point counts to progress.log every 10 minutes, then exits. It only reports and never stops anything.
param([int]$Minutes = 60)
$raw = 'C:\Users\nathan\Source\negative-mass-raw\I4-win'
$nr = 'C:\Users\nathan\Source\negative-mass-i4\phase2\nonradial'
$end = (Get-Date).AddMinutes($Minutes)
while ($true) {
  $ps = Get-Process python -ErrorAction SilentlyContinue
  $n = ($ps | Measure-Object).Count
  $cpu = [int](($ps | Measure-Object CPU -Sum).Sum)
  $ws = [int](($ps | Measure-Object WorkingSet64 -Sum).Sum / 1MB)
  $cnt = (Get-ChildItem $nr -Filter '*.partial.csv' | ForEach-Object { "$($_.Name)=$((Get-Content $_.FullName | Measure-Object -Line).Lines)" }) -join ' '
  $os = Get-CimInstance Win32_OperatingSystem
  $free = [int]($os.FreePhysicalMemory / 1KB)
  $load = (Get-CimInstance Win32_Processor).LoadPercentage
  "$(Get-Date -Format 'yyyy-MM-dd HH:mm') python procs=$n cpu_s=$cpu ws_MB=$ws sys_load=$load% free_MB=$free  $cnt" | Add-Content "$raw\progress.log"
  if ((Get-Date) -ge $end) { break }
  Start-Sleep -Seconds 600
}
