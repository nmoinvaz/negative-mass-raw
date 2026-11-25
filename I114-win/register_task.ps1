# Registers a trigger-less scheduled task that runs one command as the current user. Start it with `schtasks /run /tn
# <name>`; it then runs under the Schedule service (svchost), not under the starting terminal, and survives the session
# that started it. Settings differ from `schtasks /create` defaults: no 72 h execution limit (the l = 6 run needs about
# 89 h), no stop or refusal on battery, one instance at a time. No trigger, so it never fires by itself.
param(
  [Parameter(Mandatory)][string]$Name,
  [Parameter(Mandatory)][string]$Execute,
  [string]$Argument = '',
  [ValidateSet('S4U', 'Interactive')][string]$Logon = 'Interactive'
)
$ErrorActionPreference = 'Stop'
$me = "$env:USERDOMAIN\$env:USERNAME"
$a = if ($Argument) { New-ScheduledTaskAction -Execute $Execute -Argument $Argument } else { New-ScheduledTaskAction -Execute $Execute }
$s = New-ScheduledTaskSettingsSet -ExecutionTimeLimit ([TimeSpan]::Zero) -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -MultipleInstances IgnoreNew
$p = New-ScheduledTaskPrincipal -UserId $me -LogonType $Logon -RunLevel Limited
Register-ScheduledTask -TaskName $Name -Action $a -Settings $s -Principal $p -Force | Out-Null
$t = Get-ScheduledTask -TaskName $Name
"{0}: registered, logon {1}, priority {2}, time limit {3}, multiple {4}, battery stop {5}, triggers {6}" -f $Name, $t.Principal.LogonType, $t.Settings.Priority, $t.Settings.ExecutionTimeLimit, $t.Settings.MultipleInstances, $t.Settings.StopIfGoingOnBatteries, @($t.Triggers).Count
