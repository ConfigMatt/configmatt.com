---
layout: post
title: "Cloud Management Gateway connection issues when using AzureAD authentication - StatusCode=401 StatusText=CMGConnector_Unauthorized"
date: 2019-12-06 01:36:00 +0000
author: Matt Atkinson
categories: ["ConfigMgr"]
---

Hi All,  
  
Just dropping a quick post regarding an issue we encountered recently when setting up a new Cloud Management Gateway and attempting to use only AzureAD based authentication.  
  
In our case we were using Intune to deploy the Configuration Manager client, and the CCMSetup service was getting installed but the CCMSetup.log was displaying some of the following errors when trying to perform the installation:  
RetrieveTokenFromStsServerImpl failed with error 0x87d0027e  
  
Failed to get CCM access token and client doesn't have PKI issued cert to use SSL. Error 0x80070002  
  
DownloadFileByWinHTTP failed with a non-recoverable failure, 0x87d00455  
  
[CCMHTTP] ERROR INFO: StatusCode=401 StatusText=CMGConnector_Unauthorized  
  
We were expecting to also find an CCM_STS.log file on the Managment Point, but it was not present at all. Digging in to the IIS traffic logs, we noticed that attempts to access the CCM_STS site were receiving a 302 response, indicating a redirect was occurring.  
  
This specific server we were using to hold the MP role also had the Application Catalog role installed (this was slated to be removed in the very near future). The Application Catalog role configured an IIS redirect on the default web site so that all requests to the server were getting redirected to the Application catalog. Simply disabling the redirect and restarting IIS was enough to get our client install working across the CMG using AAD authentication with no PKI required. I'd wager that this issue is extremely unlikely to affect another ConfigMgr environment as most folks have likely removed all of their application catalog roles by now, but I figured this was such an odd scenario that it would be worth a blog post in case it can help someone else out.  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjHwcpYQe2p1wb66aUjFjEFcCattZkNZWDyydT3yzGi8be-nwkOq7IMrdWEwj0aple_DtzHzQPWjLYI6IO-zX0K2QrbobdTnfyEY3zivzBOj1q2kOtDAp5mkAIB8AdgDR9Js9SPYMbTQsg/s1600/CMGConnectionPointError.PNG)](<https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjHwcpYQe2p1wb66aUjFjEFcCattZkNZWDyydT3yzGi8be-nwkOq7IMrdWEwj0aple_DtzHzQPWjLYI6IO-zX0K2QrbobdTnfyEY3zivzBOj1q2kOtDAp5mkAIB8AdgDR9Js9SPYMbTQsg/s1600/CMGConnectionPointError.PNG>)
