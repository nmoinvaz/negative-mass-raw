# Runs one of #9's two job queues in sequence, each job appending its stdout and stderr to <job>.log beside this
# script. Logs each start and exit code in queue_<Q>.log. A crashed job is not retried, the queue goes on. Nothing here
# stops or kills a process.
#   queue.ps1 -Queue A            fd, complex, strong, then copies strongfield_eps+1.json
#   queue.ps1 -Queue B            pilot, then (only if the pilot passes) low_p16 ... low_m160
#   queue.ps1 -Queue B -From NAME resumes queue B at job NAME (after a held pilot)
param([Parameter(Mandatory)][ValidateSet('A', 'B')][string]$Queue, [string]$From = '')
$raw = $PSScriptRoot
$py = 'D:\negative-mass-venv314\Scripts\python.exe'
$env:OPENBLAS_NUM_THREADS = '1'; $env:OMP_NUM_THREADS = '1'; $env:MKL_NUM_THREADS = '1'
Set-Location 'D:\negative-mass\phase2\radial'
Set-Content -Path "$raw\queue_$Queue.pid" -Value $PID -Encoding ascii

function Log($m) { Add-Content -Path "$raw\queue_$Queue.log" -Value ("{0:yyyy-MM-dd HH:mm:ssZ} {1}" -f (Get-Date).ToUniversalTime(), $m) -Encoding ascii }

function Run($name, $pyArgs) {
    Log "start $name : python -X faulthandler -u $pyArgs"
    $sw = [Diagnostics.Stopwatch]::StartNew()
    $p = Start-Process -FilePath cmd -ArgumentList "/c $py -X faulthandler -u $pyArgs >> $raw\$name.log 2>&1" `
        -Wait -PassThru -NoNewWindow
    $sw.Stop()
    Log ("exit  $name : {0} (0x{1:X8}) after {2:N0} s" -f $p.ExitCode, [uint32]($p.ExitCode -band 0xFFFFFFFF), $sw.Elapsed.TotalSeconds)
    return @{ Code = $p.ExitCode; Secs = $sw.Elapsed.TotalSeconds }
}

$N = '0.3,1,3,6,9.2,15,25,35,40,42,42.6'
$jobs = if ($Queue -eq 'A') {
    @(
        @('fd', 'fd_check.py'),
        @('complex', 'complex_check.py'),
        @('strong', 'strongfield.py 1 0.280,0.279,0.278,0.277,0.276,0.275,0.274,0.273,0.272,0.271,0.270,0.269,0.268,0.267,0.266,0.265,0.264,0.263,0.262')
    )
} else {
    @(
        @('pilot', 'lowscan.py 1 42.6 160 160'),
        @('low_p16', "lowscan.py 1 $N 16 16"),
        @('low_p80', "lowscan.py 1 $N 80 80"),
        @('low_p160', "lowscan.py 1 $N 160 160"),
        @('low_m16', 'lowscan.py -1 0.3,1,12 16 16'),
        @('low_m80', 'lowscan.py -1 0.3,1,12 80 80'),
        @('low_m160', 'lowscan.py -1 0.3,1,12 160 160')
    )
}

Log "queue $Queue pid $PID, python $py, cwd $(Get-Location)"
$skipping = $From -ne ''
foreach ($j in $jobs) {
    if ($skipping) { if ($j[0] -eq $From) { $skipping = $false } else { Log "skip $($j[0])"; continue } }
    $r = Run $j[0] $j[1]
    if ($j[0] -eq 'pilot') {
        # The Mac's pilot row (I9-mac at ccde4b8) must be reproduced to the printed digits, within 30 min.
        $expected = "sigma2=['4.03972e-05', '1.80151e-03', '4.70273e-03']"
        $same = Select-String -Path "$raw\pilot.log" -SimpleMatch -Pattern $expected -Quiet
        if ($r.Code -ne 0 -or $r.Secs -gt 1800 -or -not $same) {
            Log ("HOLD queue B after the pilot: exit {0}, {1:N0} s (limit 1800), Mac's sigma2 row reproduced: {2}" -f $r.Code, $r.Secs, $same)
            exit 3
        }
        Log "pilot passed: exit 0, $([int]$r.Secs) s, row equals the Mac's"
    }
}
if ($Queue -eq 'A') {
    if (Test-Path -LiteralPath 'strongfield_eps+1.json') { Copy-Item -LiteralPath 'strongfield_eps+1.json' -Destination $raw; Log 'copied strongfield_eps+1.json' }
    else { Log 'no strongfield_eps+1.json to copy' }
}
Log "queue $Queue done"
