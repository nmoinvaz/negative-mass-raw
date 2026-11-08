# Reports the cpu and memory of the I55 queue's process tree, one line per interval. It only reports, it never
# stops or kills a process.  Usage: powershell -File memwatch.ps1 -Log memwatch.log
param([string]$Log = "$PSScriptRoot\memwatch.log", [int]$Interval = 60, [string]$PidFile = "$PSScriptRoot\queue.pid")
$pidFile = $PidFile
for ($i = 0; $i -lt 60 -and -not (Test-Path $pidFile); $i++) { Start-Sleep 2 }
if (-not (Test-Path $pidFile)) { exit 1 }
$root = [int](Get-Content $pidFile)
$maxWs = 0.0; $maxPriv = 0.0; $last = @{}; $lastT = Get-Date
while ($true) {
    if (-not (Get-Process -Id $root -ErrorAction SilentlyContinue)) { break }
    $all = Get-CimInstance Win32_Process | Select-Object ProcessId, ParentProcessId, CommandLine
    $ids = @($root); $grew = $true
    while ($grew) {
        $kids = @($all | Where-Object { $ids -contains $_.ParentProcessId -and $ids -notcontains $_.ProcessId } |
            ForEach-Object { $_.ProcessId })
        $grew = $kids.Count -gt 0; $ids += $kids
    }
    $ps = @(Get-Process -Id $ids -ErrorAction SilentlyContinue)
    $ws = ($ps | Measure-Object WorkingSet64 -Sum).Sum / 1MB
    $priv = ($ps | Measure-Object PrivateMemorySize64 -Sum).Sum / 1MB
    $peak = ($ps | Measure-Object PeakWorkingSet64 -Sum).Sum / 1MB
    if ($ws -gt $maxWs) { $maxWs = $ws }; if ($priv -gt $maxPriv) { $maxPriv = $priv }
    $now = Get-Date; $dt = ($now - $lastT).TotalSeconds; $d = 0.0; $cur = @{}
    foreach ($p in $ps) { $cur[$p.Id] = $p.CPU; if ($last.ContainsKey($p.Id)) { $d += $p.CPU - $last[$p.Id] } }
    $cores = if ($dt -gt 0) { $d / $dt } else { 0 }
    $last = $cur; $lastT = $now
    $job = ($all | Where-Object { $_.ParentProcessId -eq $root } | Select-Object -First 1).CommandLine
    if ($job) { $job = ($job -replace '^.*? -u ', '') }
    $free = (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB
    $line = "{0:yyyy-MM-dd HH:mm:ssZ} procs={1} ws={2:N0}MB priv={3:N0}MB sumpeakws={4:N0}MB maxws={5:N0}MB maxpriv={6:N0}MB cores={7:N2} sysfree={8:N1}GB job={9}" -f `
        $now.ToUniversalTime(), $ps.Count, $ws, $priv, $peak, $maxWs, $maxPriv, $cores, $free, $job
    Add-Content -Path $Log -Value $line -Encoding ascii
    Start-Sleep $Interval
}
Add-Content -Path $Log -Value ("{0:yyyy-MM-dd HH:mm:ssZ} queue exited" -f (Get-Date).ToUniversalTime()) -Encoding ascii
