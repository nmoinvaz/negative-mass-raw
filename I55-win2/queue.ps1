# Runs #55's two jobs in sequence, each appending to <job>.log beside this script, then copies the scan's CSV.
# Logs each start and exit code in queue.log. A crashed job is not retried, the queue goes on. Nothing here
# stops or kills a process.
$raw = $PSScriptRoot
$py = 'D:\negative-mass-venv\Scripts\python.exe'
$env:OPENBLAS_NUM_THREADS = '1'; $env:OMP_NUM_THREADS = '1'; $env:MKL_NUM_THREADS = '1'
Set-Location 'D:\negative-mass\phase2\nonradial'
Set-Content -Path "$raw\queue.pid" -Value $PID -Encoding ascii

function Log($m) { Add-Content -Path "$raw\queue.log" -Value ("{0:yyyy-MM-dd HH:mm:ssZ} {1}" -f (Get-Date).ToUniversalTime(), $m) -Encoding ascii }

function Run($name, $pyArgs) {
    Log "start $name : python -X faulthandler -u $pyArgs"
    $p = Start-Process -FilePath cmd -ArgumentList "/c $py -X faulthandler -u $pyArgs >> $raw\$name.log 2>&1" `
        -Wait -PassThru -NoNewWindow
    Log ("exit  $name : {0} (0x{1:X8})" -f $p.ExitCode, [uint32]($p.ExitCode -band 0xFFFFFFFF))
}

Log "queue pid $PID, python $py, cwd $(Get-Location)"
Run 'conv_085_l3' 'convergence.py 3 0.85'
$env:TAG = '_n100'
Run 'scan_085_l2' 'scan_growing.py -1 0.85 2 100 1e-3 300'
Remove-Item Env:\TAG
$csv = 'scan_eps-1_w0.85_l2_n100.csv'
if (Test-Path $csv) { Copy-Item $csv "$raw\$csv"; Log "copied $csv" } else { Log "no $csv to copy" }
Log "queue done"
