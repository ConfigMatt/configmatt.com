---
layout: post
title: "High CPU utilization by CCMExec after upgrading to SCCM Build 1810"
date: 2019-02-13 21:27:00 +0000
author: Matt Atkinson
categories: ["ConfigMgr"]
---

Hi All!

  
Encountered another issue today that I felt was worth a blog post since it happened after upgrading to build 1810 and there were very few Google hits on the error message.   
We were alerted to an issue on a handful of workstation where the CCMExec and WMI services were consuming 100% of the CPU.   
Taking a brief look at the client logs, I noticed that the M365AHandler.log was constantly rolling over nearly every single second. The log was showing error messages like the following: Running: "C:\Windows\system32\CompatTelRunner.exe" -m:appraiser.dll -f:DoScheduledTelemetryRun ent Executing command line: Run Appraiser CreateProcess failed. Code(0x80070002) Command line execution failed (80070002) CommandLine.Execute() failed. CM365ASystemTask:RunAppraiser() failed. 0x80070002.   
A quick search for C:\Windows\system32\CompatTelRunner.exe found that the file did not exist.   
The solution for us was to install [KB2952664](<https://support.microsoft.com/en-us/help/2952664/compatibility-update-for-keeping-windows-up-to-date-in-windows-7>). This update was previously deployed in our environment, but it appears these systems experiencing the issue were not targeted with it. Installing the update caused the CompatTelRunner.exe file to be created and the SCCM component was able to run it successfully.
