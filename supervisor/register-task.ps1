<#
Registers the supervisor as a Windows Scheduled Task: starts at logon, restarts
on failure, runs the persistent --loop (default tick every 30 min).

Requires an ELEVATED PowerShell (Run as Administrator) -- registering an AtLogOn
task with these settings needs admin rights. Run once:
    .\supervisor\register-task.ps1

Re-running it is safe -- it replaces the existing task definition.
#>

$ErrorActionPreference = "Stop"

$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    throw "Not running elevated. Right-click PowerShell -> Run as Administrator, then re-run this script from the sophie-desk root."
}

$vault   = Split-Path -Parent $PSScriptRoot
$python  = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $python) { $python = (Get-Command py -ErrorAction SilentlyContinue).Source }
if (-not $python) { throw "No python or py on PATH -- install Python or fix PATH first." }

$taskName = "sophie-desk-supervisor"
$scriptPath = Join-Path $vault "supervisor\run.py"

$action  = New-ScheduledTaskAction -Execute $python -Argument "`"$scriptPath`" --loop" -WorkingDirectory $vault
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet `
    -RestartCount 5 -RestartInterval (New-TimeSpan -Minutes 1) `
    -ExecutionTimeLimit (New-TimeSpan -Days 0) `
    -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

try {
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger `
        -Settings $settings -Description "Sophie desk supervisor -- probe loop, status commit, never a judgement call" `
        -Force -ErrorAction Stop | Out-Null
} catch {
    throw "Register-ScheduledTask failed: $($_.Exception.Message)"
}

# Never trust the cmdlet's own reported success -- verify the task actually exists
# before saying so. (This check is here because a real run hit exactly this: a
# printed 'Access is denied' followed by the old version of this script still
# claiming success, because nothing after Register-ScheduledTask ever checked.)
$confirmed = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if (-not $confirmed) {
    throw "Register-ScheduledTask returned without error, but the task does not exist afterward. Something silently failed -- check manually with: Get-ScheduledTask -TaskName '$taskName'"
}

Write-Host "Confirmed: '$taskName' exists (state: $($confirmed.State)). It starts at your next logon."
Write-Host "To start it right now without logging off: Start-ScheduledTask -TaskName '$taskName'"
Write-Host "To check on it: Get-ScheduledTask -TaskName '$taskName' | Get-ScheduledTaskInfo"
