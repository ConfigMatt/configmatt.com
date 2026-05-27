---
layout: post
title: "Managing Configuration Manager BITS jobs with Powershell"
date: 2017-06-29 22:52:00 +0000
author: Matt Atkinson
categories: ["ConfigMgr"]
tags:
  - "BITS"
  - "SCCM"
  - "Powershell"
---

I wanted to share some of the Powershell functions that I've created for managing the BITS jobs that are created when an SCCM client initiates a content download. I've added all of these to my Powershell profile so that I always have them loaded in my Powershell session. I should also mention that I don't consider myself a Powershell expert, so there are likely things being done in these functions which aren't considered best practice (using write-host for example) but they definitely get the job done.  
  
All of these functions leverage PsExec since the BITS Powershell cmdlets don't support remote computer usage. They each expect to find a copy of PsExec.exe at the root of the C drive so make sure you have a copy placed there, or modify the functions to fit your use case. They all use the mandatory parameter -computername, so make sure you specify that when using the function.  
  
First up is my function Get-BITSJobs, which simply gets a list of all of the SCCM BITS jobs on a remote computer and returns a list of them, including file count and size information:  
  

Function Get-BITSJobs { Param( [Parameter(Mandatory=$true)] [string]$computername )   
& 'C:\PsExec.exe' \\\$Computername -s bitsadmin.exe /list /allusers | Select-String -Pattern "CCMDTS Job"   
}   
Next is Set-BITSJobsForeground which will take all of the SCCM jobs on a remote computer and set them to foreground priority. This has often come in handy if a machine has been configure to throttle BITS download speeds, but for some reason I need that computer to finish it's downloads as fast as possible:  
  
Function Set-BITSJobsForeground { Param( [Parameter(Mandatory=$true)] [string]$computername )   
[string]$jobs = & 'C:\PsExec.exe' \\\$Computername -s bitsadmin.exe /list /allusers | Select-String -Pattern "CCMDTS Job"   
If($jobs -ne "") { $arrjobs = $jobs.Split("`{*`}") | select-String -Pattern "-" Foreach ($job in $arrjobs) { & 'C:\PsExec.exe' \\\$Computername -s bitsadmin.exe /setpriority "`{$job`}" foreground } } Else {Write-Host "No Jobs"} }   
Next is Set-BITSJobsComplete, this will mark all SCCM jobs as completed, including any that are in error status. It then will restart the SCCM client if you use the parameter -RestartSCCMService after which the client will restart the downloads where they left off. I have generally used this for when a machine has it's downloads stuck in an error state and I need to get the jobs to start again:   
Function Set-BITSJobsComplete { Param( [Parameter(Mandatory=$true)] [string]$computername, [switch]$RestartSCCMService )   
[string]$jobs = & 'C:\PsExec.exe' \\\$Computername -s bitsadmin.exe /list /allusers | Select-String -Pattern "CCMDTS Job"   
If($jobs -ne "") { $arrjobs = $jobs.Split("`{*`}") | select-String -Pattern "-" Foreach ($job in $arrjobs) { & 'C:\PsExec.exe' \\\$Computername -s bitsadmin.exe /complete "`{$job`}" }   
If ($RestartSCCMService) { get-service -ComputerName $computername -Name CcmExec | Restart-Service } } Else {Write-Host "No Jobs"} }   
Hopefully you will find these functions useful, I was using them often enough that it made it worth the effort to turn them in to functions. [Try adding them to your Powershell profile](<https://blogs.technet.microsoft.com/heyscriptingguy/2009/11/26/hey-scripting-guy-how-can-i-add-a-function-to-a-profile-in-windows-powershell/>) so that they will always be accessible to you whenever you have an open Powershell window.
