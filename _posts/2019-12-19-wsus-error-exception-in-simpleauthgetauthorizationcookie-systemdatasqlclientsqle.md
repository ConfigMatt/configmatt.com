---
layout: post
title: "WSUS Error: Exception in SimpleAuth.GetAuthorizationCookie: System.Data.SqlClient.SqlException (0x80131904): DB has reached allowed max number of local computers"
date: 2019-12-19 00:32:00 +0000
author: Matt Atkinson
categories: ["ConfigMgr"]
---

So another fairly obscure issue occurred today that needs some better search results for the very few that would likely experience this issue.  
  
We were starting to see WSUS scan failures reports on some of our client devices when reviewing the built-in report Scan 1 - Last Scan States by Collection. In the report, the error displayed was:  
Same as SOAPCLIENT_SOAPFAULT - SOAP client failed because there was a SOAP fault for reasons of WU_E_PT_SOAP_* error codes.  
  
When we reviewed the SoftwareDistribution.log file on the SUP, we saw several instances of the error "w3wp.42 SimpleAuthImplementation.GetAuthorizationCookie EventId=400,Type=Error,Category=WsusService,Message=DB has reached allowed max number of local computers". We manage a large environment and are close to 100k clients in this ConfigMgr site which is the default number of devices that can be managed with a single WSUS server. Even though we have multiple SUP servers, they are all sharing a single database and all follow that same 100k total client limitation.  
  
Another cause of this issue was that we had fallen behind on our SUP maintenance that typically removes computers that haven't synced within 30 days, leading to a larger than normal accumulation of machines.  
  
We resolved the issue by immediately running our standard WSUS cleanup process (starting with the built in cleanup wizard, and finishing by declining superseded updates and defragmenting the database). We also have a plan to increase the number of devices that can be connected to WSUS to the maximum allowed when using Configuration Manager (150K) by executing the following Powershell code:  
  

[reflection.assembly]::LoadWithPartialName("Microsoft.UpdateServices.Administration") $config = (Get-WsusServer -Name WSUS.Server.Name -PortNumber 8530).GetConfiguration() $config.MaximumAllowedComputers = 150000 $config.Save()   
  
Hopefully this information will help anyone else that happens to run in to this limitation of WSUS, and most importantly, always run your WSUS maintenance :)
