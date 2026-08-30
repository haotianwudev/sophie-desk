<#
Registers the supervisor as a Windows Scheduled Task: starts at logon, restarts
on failure, runs the persistent --loop (default tick every 30 min).

Run once, manually, from an elevated or normal PowerShell prompt:
    .\supervisor\register-task.ps1

Re-running it is safe -- it replaces the existing task definition.
#>

$ErrorActionPreference = "Stop"

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

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger `
    -Settings $settings -Description "Sophie desk supervisor -- probe loop, status commit, never a judgement call" `
    -Force | Out-Null

Write-Host "Registered '$taskName'. It starts at your next logon."
Write-Host "To start it right now without logging off: Start-ScheduledTask -TaskName '$taskName'"
Write-Host "To check on it: Get-ScheduledTask -TaskName '$taskName' | Get-ScheduledTaskInfo"
